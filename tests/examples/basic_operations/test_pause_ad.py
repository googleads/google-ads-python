import unittest
from unittest.mock import patch, MagicMock, call

from examples.basic_operations import pause_ad

class TestPauseAd(unittest.TestCase):

    @patch("examples.basic_operations.pause_ad.argparse.ArgumentParser")
    @patch("examples.basic_operations.pause_ad.GoogleAdsClient.load_from_storage")
    def test_main(self, mock_load_from_storage, mock_argument_parser):
        # Mock the GoogleAdsClient
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client

        # Mock the AdGroupAdService
        mock_ad_group_ad_service = MagicMock()

        # The script only uses AdGroupAdService
        mock_google_ads_client.get_service.return_value = mock_ad_group_ad_service

        # Mock enums - AdGroupAdStatusEnum.PAUSED will be a MagicMock itself.
        # No need to assign it a string value, we will check if the attribute was set to this specific mock.
        # mock_google_ads_client.enums.AdGroupAdStatusEnum.PAUSED = "PAUSED_ENUM_VAL"
        # mock_google_ads_client.enums.AdGroupAdStatusEnum.ENABLED = "ENABLED_ENUM_VAL"

        # Store the mock enum object for assertion
        # Corrected based on script usage: AdGroupStatusEnum, not AdGroupAdStatusEnum
        expected_paused_status_enum = mock_google_ads_client.enums.AdGroupStatusEnum.PAUSED


        # Mock command line arguments
        mock_args = MagicMock()
        mock_args.customer_id = "1234567890"
        mock_args.ad_group_id = "ADGROUPID_01"
        mock_args.ad_id = "ADID_01"
        mock_argument_parser.return_value.parse_args.return_value = mock_args

        # Define the expected resource name
        expected_resource_name = f"customers/{mock_args.customer_id}/adGroupAds/{mock_args.ad_group_id}~{mock_args.ad_id}"

        # Mock ad_group_ad_service.ad_group_ad_path to return the expected resource name
        mock_ad_group_ad_service.ad_group_ad_path.return_value = expected_resource_name

        # Mock the response from AdGroupAdService.mutate_ad_group_ads
        mock_mutate_response = MagicMock()
        mock_mutate_result = MagicMock()
        mock_mutate_result.resource_name = expected_resource_name # Should match the one constructed
        mock_mutate_response.results = [mock_mutate_result]
        mock_ad_group_ad_service.mutate_ad_group_ads.return_value = mock_mutate_response

        # Mock AdGroupAdOperation
        # The script builds this operation, so we need to be able to mock its creation
        # We can use a side_effect on get_type if it's used, or ensure the attributes of the operation are checked
        mock_operation_instance = MagicMock()

        # If get_type is used to create the operation object:
        def get_type_side_effect(type_name, version=None):
            if type_name == "AdGroupAdOperation":
                # Return a new MagicMock each time to allow modification in the script
                # without affecting subsequent calls if any (though not expected here)
                op_mock = MagicMock()
                # Pre-configure the 'update' attribute as it's accessed directly
                op_mock.update = MagicMock()
                return op_mock
            raise ValueError(f"Unexpected type: {type_name}")
        mock_google_ads_client.get_type.side_effect = get_type_side_effect


        # Call the main function of the example script
        with patch("builtins.print") as mock_print:
            pause_ad.main(mock_google_ads_client, mock_args.customer_id, mock_args.ad_group_id, mock_args.ad_id)

        # Assertions
        mock_google_ads_client.get_service.assert_called_once_with("AdGroupAdService")

        # Verify ad_group_ad_path was called correctly
        mock_ad_group_ad_service.ad_group_ad_path.assert_called_once_with(
            mock_args.customer_id, mock_args.ad_group_id, mock_args.ad_id
        )

        # Verify AdGroupAdService.mutate_ad_group_ads call
        mock_ad_group_ad_service.mutate_ad_group_ads.assert_called_once()
        _, mutate_kwargs = mock_ad_group_ad_service.mutate_ad_group_ads.call_args
        self.assertEqual(mutate_kwargs['customer_id'], mock_args.customer_id)

        operations = mutate_kwargs['operations']
        self.assertEqual(len(operations), 1)

        # Check the operation details
        operation_update = operations[0].update
        self.assertEqual(operation_update.resource_name, expected_resource_name)
        self.assertEqual(operation_update.status, expected_paused_status_enum)


        # Verify print output
        expected_print_calls = [
            call(f"Paused ad group ad {expected_resource_name}.")
        ]
        mock_print.assert_has_calls(expected_print_calls, any_order=False)

if __name__ == "__main__":
    unittest.main()
