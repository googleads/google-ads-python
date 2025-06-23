# Copyright 2025 Google LLC
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
import unittest
from unittest.mock import MagicMock, patch

import examples.assets.add_call as add_call


class TestAddCall(unittest.TestCase):
    @patch("examples.assets.add_call.GoogleAdsClient")
    def test_add_call_asset(self, mock_google_ads_client_constructor):
        mock_client_instance = mock_google_ads_client_constructor.return_value
        mock_asset_service = MagicMock()
        mock_google_ads_service = MagicMock()

        def get_service_side_effect(service_name):
            if service_name == "AssetService":
                return mock_asset_service
            elif service_name == "GoogleAdsService":
                return mock_google_ads_service
            return MagicMock()

        mock_client_instance.get_service.side_effect = get_service_side_effect
        mock_asset_operation = MagicMock(spec=["create"])
        mock_call_asset = mock_asset_operation.create.call_asset
        mock_ad_schedule_targets_list = MagicMock(spec=["append"])
        mock_call_asset.ad_schedule_targets = mock_ad_schedule_targets_list
        mock_ad_schedule_info = MagicMock()

        def get_type_side_effect(type_name):
            if type_name == "AssetOperation":
                return mock_asset_operation
            elif type_name == "AdScheduleInfo":
                return mock_ad_schedule_info
            return MagicMock()

        mock_client_instance.get_type.side_effect = get_type_side_effect
        mock_client_instance.enums.DayOfWeekEnum.MONDAY = "MONDAY_ENUM"
        mock_client_instance.enums.MinuteOfHourEnum.ZERO = "ZERO_ENUM"
        mock_client_instance.enums.CallConversionReportingStateEnum.USE_RESOURCE_LEVEL_CALL_CONVERSION_ACTION = (
            "REPORTING_STATE_ENUM"
        )
        customer_id = "1234567890"
        phone_number = "(800) 555-0100"
        phone_country = "US"
        conversion_action_id = "987654321"
        mock_asset_service.mutate_assets.return_value.results = [
            MagicMock(resource_name="asset_resource_name")
        ]
        mock_google_ads_service.conversion_action_path.return_value = (
            "conversion_action_path"
        )
        returned_resource_name = add_call.add_call_asset(
            mock_client_instance,
            customer_id,
            phone_number,
            phone_country,
            conversion_action_id,
        )
        self.assertEqual(returned_resource_name, "asset_resource_name")
        mock_client_instance.get_service.assert_any_call("AssetService")
        mock_client_instance.get_service.assert_any_call("GoogleAdsService")
        mock_client_instance.get_type.assert_any_call("AssetOperation")
        mock_client_instance.get_type.assert_any_call("AdScheduleInfo")
        self.assertEqual(mock_call_asset.country_code, phone_country)
        self.assertEqual(mock_call_asset.phone_number, phone_number)
        self.assertEqual(
            mock_call_asset.call_conversion_action, "conversion_action_path"
        )
        self.assertEqual(
            mock_call_asset.call_conversion_reporting_state,
            "REPORTING_STATE_ENUM",
        )
        mock_ad_schedule_targets_list.append.assert_called_once_with(
            mock_ad_schedule_info
        )
        self.assertEqual(mock_ad_schedule_info.day_of_week, "MONDAY_ENUM")
        self.assertEqual(mock_ad_schedule_info.start_hour, 9)
        self.assertEqual(mock_ad_schedule_info.end_hour, 17)
        self.assertEqual(mock_ad_schedule_info.start_minute, "ZERO_ENUM")
        self.assertEqual(mock_ad_schedule_info.end_minute, "ZERO_ENUM")
        mock_asset_service.mutate_assets.assert_called_once_with(
            customer_id=customer_id, operations=[mock_asset_operation]
        )
        self.assertIs(mock_asset_operation.create.call_asset, mock_call_asset)

    @patch("examples.assets.add_call.GoogleAdsClient")
    def test_link_asset_to_account(self, mock_google_ads_client_constructor):
        mock_client_instance = mock_google_ads_client_constructor.return_value
        mock_customer_asset_service = MagicMock()
        mock_client_instance.get_service.return_value = (
            mock_customer_asset_service
        )
        mock_customer_asset_operation = MagicMock(spec=["create"])
        mock_client_instance.get_type.return_value = (
            mock_customer_asset_operation
        )
        mock_customer_asset = mock_customer_asset_operation.create
        mock_client_instance.enums.AssetFieldTypeEnum.CALL = "CALL_ENUM"
        customer_id = "1234567890"
        asset_resource_name = "asset_resource_name"
        mock_customer_asset_service.mutate_customer_assets.return_value.results = [
            MagicMock(resource_name="customer_asset_resource_name")
        ]
        add_call.link_asset_to_account(
            mock_client_instance, customer_id, asset_resource_name
        )
        mock_client_instance.get_service.assert_called_once_with(
            "CustomerAssetService"
        )
        mock_client_instance.get_type.assert_called_once_with(
            "CustomerAssetOperation"
        )
        self.assertEqual(mock_customer_asset.asset, asset_resource_name)
        self.assertEqual(mock_customer_asset.field_type, "CALL_ENUM")
        mock_customer_asset_service.mutate_customer_assets.assert_called_once_with(
            customer_id=customer_id, operations=[mock_customer_asset_operation]
        )

    # This test directly invokes the 'main' function from add_call.py,
    # ensuring its internal logic (calls to add_call_asset and link_asset_to_account) is tested.
    # It relies on those functions being correctly patched if they interact with external services.
    @patch(
        "examples.assets.add_call.link_asset_to_account"
    )  # Mock the function that links asset to account
    @patch(
        "examples.assets.add_call.add_call_asset"
    )  # Mock the function that creates the asset
    def test_main_function_logic(
        self, mock_add_call_asset, mock_link_asset_to_account
    ):
        mock_client_instance = MagicMock()  # Mock the GoogleAdsClient instance
        mock_add_call_asset.return_value = (
            "test_asset_resource_name"  # Mock return value for asset creation
        )

        # Define test parameters
        customer_id = "cust123"
        phone_number = "123-456-7890"
        phone_country = "CA"
        conversion_action_id = "conv123"

        # Call the main function from the add_call module
        add_call.main(
            mock_client_instance,
            customer_id,
            phone_number,
            phone_country,
            conversion_action_id,
        )

        # Assert that add_call_asset was called correctly
        mock_add_call_asset.assert_called_once_with(
            mock_client_instance,
            customer_id,
            phone_number,
            phone_country,
            conversion_action_id,
        )
        # Assert that link_asset_to_account was called correctly with the mocked asset name
        mock_link_asset_to_account.assert_called_once_with(
            mock_client_instance, customer_id, "test_asset_resource_name"
        )
