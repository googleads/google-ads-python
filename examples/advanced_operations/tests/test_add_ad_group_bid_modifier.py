# Copyright 2020 Google LLC
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
"""Tests for add_ad_group_bid_modifier.py."""

from unittest import mock
from unittest import TestCase

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
# Attempt to import DeviceEnum from the versioned enum path
from google.ads.googleads.v20.enums import DeviceEnum

from examples.advanced_operations.add_ad_group_bid_modifier import main


_CUSTOMER_ID = "1234567890"
_AD_GROUP_ID = "9876543210"
_BID_MODIFIER_VALUE = 1.5
# Using the known value for DeviceEnum.MOBILE (which is 3) directly
# to avoid issues with enum access at module load time.
# DeviceEnum.MOBILE.value is 3.
_MODIFIER_RESOURCE_NAME = (
    f"customers/{_CUSTOMER_ID}/adGroupBidModifiers/"
    f"{_AD_GROUP_ID}~3"
)


@mock.patch("examples.advanced_operations.add_ad_group_bid_modifier.GoogleAdsClient.load_from_storage")
class AddAdGroupBidModifierTest(TestCase):
    def setUp(self):
        self.client_mock = mock.MagicMock(spec=GoogleAdsClient)
        self.ad_group_service_mock = self.client_mock.get_service("AdGroupService")
        self.ad_group_bm_service_mock = self.client_mock.get_service("AdGroupBidModifierService")

        # Mock the ad group path
        self.ad_group_service_mock.ad_group_path.return_value = (
            f"customers/{_CUSTOMER_ID}/adGroups/{_AD_GROUP_ID}"
        )

        # Mock the response from mutate_ad_group_bid_modifiers
        mock_result = mock.Mock()
        mock_result.resource_name = _MODIFIER_RESOURCE_NAME
        self.ad_group_bm_service_mock.mutate_ad_group_bid_modifiers.return_value.results = [
            mock_result
        ]

        # Mock enums
        self.client_mock.enums = mock.MagicMock() # Ensure enums attribute exists
        # Create a mock for the DeviceEnum type itself
        mock_device_enum = mock.MagicMock()
        # Set the MOBILE attribute on this mock to return the integer value 3
        mock_device_enum.MOBILE = 3
        self.client_mock.enums.DeviceEnum = mock_device_enum


    def test_main_success(self, mock_load_client):
        mock_load_client.return_value = self.client_mock

        main(self.client_mock, _CUSTOMER_ID, _AD_GROUP_ID, _BID_MODIFIER_VALUE)

        self.ad_group_service_mock.ad_group_path.assert_called_once_with(
            _CUSTOMER_ID, _AD_GROUP_ID
        )

        # Check that mutate_ad_group_bid_modifiers was called
        self.ad_group_bm_service_mock.mutate_ad_group_bid_modifiers.assert_called_once()

        # Get the actual operation passed to the mock
        call_args = self.ad_group_bm_service_mock.mutate_ad_group_bid_modifiers.call_args
        operation = call_args[1]["operations"][0].create # Accessing create from AdGroupBidModifierOperation

        self.assertEqual(
            operation.ad_group,
            f"customers/{_CUSTOMER_ID}/adGroups/{_AD_GROUP_ID}",
        )
        self.assertEqual(operation.bid_modifier, _BID_MODIFIER_VALUE)
        # Assert against the integer value since DeviceEnum.MOBILE might be problematic
        self.assertEqual(operation.device.type_, 3)


    def test_main_google_ads_exception(self, mock_load_client):
        mock_load_client.return_value = self.client_mock

        # Configure the service mock to raise GoogleAdsException
        self.ad_group_bm_service_mock.mutate_ad_group_bid_modifiers.side_effect = GoogleAdsException(
            error=mock.Mock(),
            failure=mock.Mock(errors=[mock.Mock(message="Test Error")]),
            request_id="test_request_id",
            call=mock.Mock() # Added missing call argument
        )

        with self.assertRaises(GoogleAdsException):
            main(self.client_mock, _CUSTOMER_ID, _AD_GROUP_ID, _BID_MODIFIER_VALUE)

if __name__ == "__main__":
    TestCase.main()
