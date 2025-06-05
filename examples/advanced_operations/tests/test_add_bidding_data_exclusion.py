# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for add_bidding_data_exclusion.py."""

from unittest import mock
from unittest import TestCase

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v20.enums import (
    SeasonalityEventScopeEnum,
    AdvertisingChannelTypeEnum,
)

from examples.advanced_operations.add_bidding_data_exclusion import main

_CUSTOMER_ID = "1234567890"
_START_DATE_TIME = "2024-01-01 00:00:00"
_END_DATE_TIME = "2024-01-15 23:59:59"
_EXCLUSION_RESOURCE_NAME = f"customers/{_CUSTOMER_ID}/biddingDataExclusions/1"


@mock.patch("examples.advanced_operations.add_bidding_data_exclusion.GoogleAdsClient.load_from_storage")
class AddBiddingDataExclusionTest(TestCase):
    def setUp(self):
        self.client_mock = mock.MagicMock(spec=GoogleAdsClient)
        self.bidding_data_exclusion_service_mock = self.client_mock.get_service(
            "BiddingDataExclusionService"
        )

        # Mock enums
        self.client_mock.enums = mock.MagicMock()

        mock_seasonality_event_scope_enum = mock.MagicMock()
        mock_seasonality_event_scope_enum.CHANNEL = 4 # SeasonalityEventScopeEnum.CHANNEL.value
        self.client_mock.enums.SeasonalityEventScopeEnum = mock_seasonality_event_scope_enum

        mock_advertising_channel_type_enum = mock.MagicMock()
        mock_advertising_channel_type_enum.SEARCH = 2 # AdvertisingChannelTypeEnum.SEARCH.value
        self.client_mock.enums.AdvertisingChannelTypeEnum = mock_advertising_channel_type_enum

        # Mock response
        self.bidding_data_exclusion_service_mock.mutate_bidding_data_exclusions.return_value.results = [
            mock.Mock(resource_name=_EXCLUSION_RESOURCE_NAME)
        ]

        # Mock type for operation
        self.mock_operation = mock.MagicMock()
        self.mock_bidding_data_exclusion = mock.MagicMock()
        self.mock_operation.create = self.mock_bidding_data_exclusion
        # Initialize list attributes
        self.mock_bidding_data_exclusion.advertising_channel_types = []
        self.mock_bidding_data_exclusion.campaigns = []

        self.client_mock.get_type.return_value = self.mock_operation


    def test_main_success(self, mock_load_client):
        mock_load_client.return_value = self.client_mock

        main(self.client_mock, _CUSTOMER_ID, _START_DATE_TIME, _END_DATE_TIME)

        self.bidding_data_exclusion_service_mock.mutate_bidding_data_exclusions.assert_called_once_with(
            customer_id=_CUSTOMER_ID, operations=[self.mock_operation]
        )

        # Assertions on the bidding_data_exclusion object
        self.assertIsNotNone(self.mock_bidding_data_exclusion.name)
        self.assertTrue(self.mock_bidding_data_exclusion.name.startswith("Data exclusion #"))
        self.assertEqual(self.mock_bidding_data_exclusion.scope, 4) # SeasonalityEventScopeEnum.CHANNEL.value
        self.assertIn(2, self.mock_bidding_data_exclusion.advertising_channel_types) # AdvertisingChannelTypeEnum.SEARCH.value
        self.assertEqual(self.mock_bidding_data_exclusion.start_date_time, _START_DATE_TIME)
        self.assertEqual(self.mock_bidding_data_exclusion.end_date_time, _END_DATE_TIME)


    def test_main_google_ads_exception(self, mock_load_client):
        mock_load_client.return_value = self.client_mock
        self.bidding_data_exclusion_service_mock.mutate_bidding_data_exclusions.side_effect = GoogleAdsException(
            error=mock.Mock(),
            failure=mock.Mock(errors=[mock.Mock(message="Test Error")]),
            request_id="test_request_id",
            call=mock.Mock()
        )

        with self.assertRaises(GoogleAdsException):
            main(self.client_mock, _CUSTOMER_ID, _START_DATE_TIME, _END_DATE_TIME)

if __name__ == "__main__":
    TestCase.main()
