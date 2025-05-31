import unittest
from unittest.mock import patch, MagicMock, call

from examples.basic_operations import update_responsive_search_ad

class TestUpdateResponsiveSearchAd(unittest.TestCase):

    @patch("examples.basic_operations.update_responsive_search_ad.argparse.ArgumentParser")
    @patch("examples.basic_operations.update_responsive_search_ad.GoogleAdsClient.load_from_storage")
    def test_main(self, mock_load_from_storage, mock_argument_parser):
        # Mock the GoogleAdsClient
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client

        # Mock the AdService
        mock_ad_service = MagicMock()
        mock_google_ads_client.get_service.return_value = mock_ad_service

        # Mock command line arguments
        mock_args = MagicMock()
        mock_args.customer_id = "1234567890"
        mock_args.ad_id = "ADID1" # This example updates an existing Ad ID
        mock_argument_parser.return_value.parse_args.return_value = mock_args

        ad_resource_name = f"customers/{mock_args.customer_id}/ads/{mock_args.ad_id}"

        # Mock the response for AdService.mutate_ads
        mock_mutate_response = MagicMock()
        mock_mutate_result = MagicMock()
        mock_mutate_result.resource_name = ad_resource_name
        mock_mutate_response.results = [mock_mutate_result]
        mock_ad_service.mutate_ads.return_value = mock_mutate_response

        # Call the main function of the example script
        with patch("builtins.print") as mock_print,              patch("google.ads.googleads.client.GoogleAdsClient.get_type") as mock_get_type_on_instance,              patch("google.protobuf.field_mask_pb2.FieldMask") as mock_field_mask:

            # Mocking get_type on the instance of the client used in main
            mock_ad_type_instance = MagicMock() # This will be the Ad object
            mock_ad_type_instance.resource_name = ad_resource_name
            # Initialize some mock RSA data that the example will update
            mock_ad_type_instance.responsive_search_ad.headlines = [MagicMock(), MagicMock()] # Example has 2 existing
            mock_ad_type_instance.responsive_search_ad.descriptions = [MagicMock()] # Example has 1 existing

            mock_ad_operation_type_instance = MagicMock() # This is for AdOperation

            def get_type_instance_side_effect(type_name):
                if type_name == "Ad":
                    return mock_ad_type_instance
                elif type_name == "AdOperation":
                    return mock_ad_operation_type_instance
                elif type_name == "AdTextAsset": # For creating new headlines/descriptions
                    return MagicMock()
                raise ValueError(f"Unexpected type for instance: {type_name}")
            mock_get_type_on_instance.side_effect = get_type_instance_side_effect

            update_responsive_search_ad.main(mock_google_ads_client, mock_args.customer_id, mock_args.ad_id)

        # Assertions
        mock_load_from_storage.assert_called_once_with(version="v19")
        mock_google_ads_client.get_service.assert_called_once_with("AdService")

        mock_get_type_on_instance.assert_any_call("AdOperation")
        mock_get_type_on_instance.assert_any_call("Ad")
        mock_get_type_on_instance.assert_any_call("AdTextAsset") # Called multiple times

        self.assertEqual(mock_ad_service.mutate_ads.call_count, 1)
        args_mutate, kwargs_mutate = mock_ad_service.mutate_ads.call_args

        self.assertEqual(kwargs_mutate['customer_id'], mock_args.customer_id)

        operation = kwargs_mutate['operations'][0]
        # Check the update field of the operation
        self.assertEqual(operation.update.resource_name, ad_resource_name)

        # Check updated headlines and descriptions (example adds one new headline and one new description)
        self.assertEqual(len(operation.update.responsive_search_ad.headlines), 3) # 2 existing + 1 new
        self.assertTrue(operation.update.responsive_search_ad.headlines[-1].text.startswith("Cruise to Mars #"))
        self.assertEqual(operation.update.responsive_search_ad.headlines[-1].pinned_field, mock_google_ads_client.enums.ServedAssetFieldTypeEnum.HEADLINE_1)

        self.assertEqual(len(operation.update.responsive_search_ad.descriptions), 2) # 1 existing + 1 new
        self.assertTrue(operation.update.responsive_search_ad.descriptions[-1].text.startswith("Best Space Cruise Line #"))
        self.assertEqual(operation.update.responsive_search_ad.descriptions[-1].pinned_field, mock_google_ads_client.enums.ServedAssetFieldTypeEnum.DESCRIPTION_1)

        # Check that FieldMask was called correctly
        # Paths should include "responsive_search_ad.headlines" and "responsive_search_ad.descriptions"
        # The exact paths depend on how the FieldMaskUtil is used or FieldMask is constructed in the script
        updated_paths = mock_field_mask.call_args[1]['paths'] # Get 'paths' from kwargs
        self.assertIn("responsive_search_ad.headlines", updated_paths)
        self.assertIn("responsive_search_ad.descriptions", updated_paths)
        self.assertEqual(operation.update_mask, mock_field_mask.return_value)

        # Verify print output
        expected_print_call = call(
            f"Responsive search ad with resource name '{ad_resource_name}' was updated."
        )
        mock_print.assert_has_calls([expected_print_call])

if __name__ == "__main__":
    unittest.main()
