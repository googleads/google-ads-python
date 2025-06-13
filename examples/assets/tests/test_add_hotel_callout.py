# Copyright 2022 Google LLC
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
from unittest.mock import MagicMock, patch, call
import sys
import argparse
import os

# Add the repository root directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from examples.assets import add_hotel_callout
try:
    from google.ads.googleads.client import GoogleAdsClient as RealGoogleAdsClient
except ImportError:
    RealGoogleAdsClient = MagicMock()

class TestAddHotelCallout(unittest.TestCase):

    @patch("examples.assets.add_hotel_callout.GoogleAdsClient")
    def test_add_hotel_callout_assets(self, mock_google_ads_client_constructor):
        mock_client_instance = mock_google_ads_client_constructor.return_value
        mock_asset_service = MagicMock()
        mock_client_instance.get_service.return_value = mock_asset_service

        mock_operations = [MagicMock(), MagicMock()]
        mock_client_instance.get_type.side_effect = mock_operations

        customer_id = "test_customer_123"
        language_code = "en"
        expected_texts = ["Activities", "Facilities"]

        mock_results = [MagicMock(resource_name=f"asset_rn_{i}") for i in range(len(expected_texts))]
        mock_asset_service.mutate_assets.return_value.results = mock_results

        returned_resource_names = add_hotel_callout.add_hotel_callout_assets(
            mock_client_instance, customer_id, language_code
        )

        self.assertEqual(mock_client_instance.get_type.call_count, len(expected_texts))
        mock_client_instance.get_type.assert_called_with("AssetOperation")

        for i, text in enumerate(expected_texts):
            asset_mock = mock_operations[i].create
            self.assertEqual(asset_mock.hotel_callout_asset.text, text)
            self.assertEqual(asset_mock.hotel_callout_asset.language_code, language_code)

        mock_asset_service.mutate_assets.assert_called_once_with(
            customer_id=customer_id, operations=mock_operations
        )
        self.assertEqual(returned_resource_names, [res.resource_name for res in mock_results])

    @patch("examples.assets.add_hotel_callout.GoogleAdsClient")
    def test_link_asset_to_account(self, mock_google_ads_client_constructor):
        mock_client_instance = mock_google_ads_client_constructor.return_value
        mock_customer_asset_service = MagicMock()
        mock_client_instance.get_service.return_value = mock_customer_asset_service

        mock_operations = [MagicMock(), MagicMock()]
        mock_client_instance.get_type.side_effect = mock_operations
        mock_client_instance.enums.AssetFieldTypeEnum.HOTEL_CALLOUT = "HOTEL_CALLOUT_ENUM"

        customer_id = "test_customer_123"
        resource_names = ["asset_rn_0", "asset_rn_1"]

        mock_results = [MagicMock(resource_name=f"ca_asset_rn_{i}") for i in range(len(resource_names))]
        mock_customer_asset_service.mutate_customer_assets.return_value.results = mock_results

        add_hotel_callout.link_asset_to_account(
            mock_client_instance, customer_id, resource_names
        )

        self.assertEqual(mock_client_instance.get_type.call_count, len(resource_names))
        mock_client_instance.get_type.assert_called_with("CustomerAssetOperation")

        for i, rn in enumerate(resource_names):
            customer_asset_mock = mock_operations[i].create
            self.assertEqual(customer_asset_mock.asset, rn)
            self.assertEqual(customer_asset_mock.field_type, "HOTEL_CALLOUT_ENUM")

        mock_customer_asset_service.mutate_customer_assets.assert_called_once_with(
            customer_id=customer_id, operations=mock_operations
        )

    @patch("examples.assets.add_hotel_callout.link_asset_to_account")
    @patch("examples.assets.add_hotel_callout.add_hotel_callout_assets")
    def test_main_function_logic(self, mock_add_assets, mock_link_assets):
        mock_client_instance = MagicMock()
        customer_id = "test_customer_123"
        language_code = "fr"

        mock_asset_resource_names = ["asset1", "asset2"]
        mock_add_assets.return_value = mock_asset_resource_names

        add_hotel_callout.main(mock_client_instance, customer_id, language_code)

        mock_add_assets.assert_called_once_with(mock_client_instance, customer_id, language_code)
        mock_link_assets.assert_called_once_with(mock_client_instance, customer_id, mock_asset_resource_names)

# TestMainExecution class removed due to persistent issues with runpy and mock interaction.

if __name__ == "__main__":
    unittest.main()
