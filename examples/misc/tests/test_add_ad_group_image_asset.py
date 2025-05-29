import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root directory to sys.path to allow robust import of the script under test.
# This assumes the test file is located at 'examples/misc/tests/test_add_ad_group_image_asset.py'
# and the script to test is at 'examples/misc/add_ad_group_image_asset.py'.
# The project root would then be '../..' from this file's directory.
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from examples.misc import add_ad_group_image_asset

class TestAddAdGroupImageAsset(unittest.TestCase):

    @patch('examples.misc.add_ad_group_image_asset.GoogleAdsClient.load_from_storage')
    def test_main_function(self, mock_load_from_storage):
        # Mock the GoogleAdsClient instance
        mock_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_ads_client

        # Mock the AdGroupAssetService
        mock_ad_group_asset_service = mock_ads_client.get_service.return_value

        # Define test parameters and expected values
        customer_id = "1234567890"
        ad_group_id = "111222333"
        asset_id = "987654321"
        
        expected_asset_resource_name = f"customers/{customer_id}/assets/{asset_id}"
        expected_ad_group_resource_name = f"customers/{customer_id}/adGroups/{ad_group_id}"
        mock_created_resource_name = f"customers/{customer_id}/adGroupAssets/{ad_group_id}~{asset_id}"

        # Configure mock path helper methods
        mock_ad_group_asset_service.asset_path.return_value = expected_asset_resource_name
        mock_ad_group_asset_service.ad_group_path.return_value = expected_ad_group_resource_name

        # Configure mock for client.get_type("AdGroupAssetOperation")
        # This mock will be used by the script to create the operation object
        mock_operation = MagicMock()
        mock_ads_client.get_type.return_value = mock_operation
        
        # Configure mock for AssetFieldTypeEnum
        # The script accesses client.enums.AssetFieldTypeEnum.AD_IMAGE
        mock_ads_client.enums.AssetFieldTypeEnum.AD_IMAGE = "AD_IMAGE_ENUM_VALUE_FOR_TEST"

        # Configure mock for the mutate_ad_group_assets method response
        mock_mutate_response = MagicMock()
        mock_mutate_response.results = [MagicMock(resource_name=mock_created_resource_name)]
        mock_ad_group_asset_service.mutate_ad_group_assets.return_value = mock_mutate_response

        # Call the main function of the script, capturing print output
        with patch('builtins.print') as mock_print:
            add_ad_group_image_asset.main(
                mock_ads_client,
                customer_id,
                ad_group_id,
                asset_id
            )

        # --- Assertions ---

        # Verify GoogleAdsClient.load_from_storage was called (implicitly by @patch)
        mock_load_from_storage.assert_called_once() # Path is checked by the patch decorator

        # Verify AdGroupAssetService was fetched
        mock_ads_client.get_service.assert_called_once_with("AdGroupAssetService")

        # Verify path helper methods were called with correct parameters
        mock_ad_group_asset_service.asset_path.assert_called_once_with(customer_id, asset_id)
        mock_ad_group_asset_service.ad_group_path.assert_called_once_with(customer_id, ad_group_id)
        
        # Verify client.get_type("AdGroupAssetOperation") was called
        mock_ads_client.get_type.assert_called_once_with("AdGroupAssetOperation")

        # Verify the mutate_ad_group_assets call
        # The script constructs an operation and passes it.
        # We need to check the arguments of this call.
        
        # Expected operation built by the script:
        # ad_group_asset_operation = client.get_type("AdGroupAssetOperation") (this is our mock_operation)
        # ad_group_asset_set = ad_group_asset_operation.create
        # ad_group_asset_set.asset = expected_asset_resource_name
        # ad_group_asset_set.field_type = client.enums.AssetFieldTypeEnum.AD_IMAGE
        # ad_group_asset_set.ad_group = expected_ad_group_resource_name
        
        # Check that the 'create' attribute of our mock_operation was configured as expected
        self.assertEqual(mock_operation.create.asset, expected_asset_resource_name)
        self.assertEqual(mock_operation.create.ad_group, expected_ad_group_resource_name)
        self.assertEqual(mock_operation.create.field_type, mock_ads_client.enums.AssetFieldTypeEnum.AD_IMAGE)

        # Now, check if mutate_ad_group_assets was called with this 'mock_operation'
        mock_ad_group_asset_service.mutate_ad_group_assets.assert_called_once_with(
            customer_id=customer_id,
            operations=[mock_operation] # The script passes the operation it built
        )

        # Verify the printed output
        expected_print_message = (
            f"Created ad group asset with resource name: '{mock_created_resource_name}'"
        )
        # The script loops through results, so check if any call matches.
        mock_print.assert_any_call(expected_print_message)

if __name__ == "__main__":
    unittest.main()
