import unittest
from unittest.mock import patch, MagicMock, call # Ensure call is imported

from examples.basic_operations import add_ad_groups

class TestAddAdGroups(unittest.TestCase):

    @patch("examples.basic_operations.add_ad_groups.argparse.ArgumentParser")
    @patch("examples.basic_operations.add_ad_groups.GoogleAdsClient.load_from_storage")
    def test_main(self, mock_load_from_storage, mock_argument_parser):
        # Mock the GoogleAdsClient
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client

        # Mock the GoogleAdsService
        mock_ga_service = MagicMock()
        mock_google_ads_client.get_service.return_value = mock_ga_service

        # Mock the AdGroupService
        mock_ad_group_service = MagicMock()
        # Ensure get_service is flexible enough to return different mocks based on input
        def get_service_side_effect(service_name, version=None): # Added version to match signature
            if service_name == "GoogleAdsService":
                return mock_ga_service
            elif service_name == "AdGroupService":
                return mock_ad_group_service
            raise ValueError(f"Unexpected service: {service_name}")
        mock_google_ads_client.get_service.side_effect = get_service_side_effect


        # Mock command line arguments
        mock_args = MagicMock()
        mock_args.customer_id = "1234567890"
        mock_args.campaign_id = "9876543210"
        mock_argument_parser.return_value.parse_args.return_value = mock_args

        # Mock the responses for service calls
        # For AdGroupService mutate
        mock_ad_group_operation_response = MagicMock()
        # Simulate that one ad group was created
        mock_ad_group_result = MagicMock()
        mock_ad_group_result.resource_name = "customers/1234567890/adGroups/AD_GROUP_ID_1"
        mock_ad_group_operation_response.results = [mock_ad_group_result]
        mock_ad_group_service.mutate_ad_groups.return_value = mock_ad_group_operation_response

        # Call the main function of the example script
        with patch("builtins.print") as mock_print:
            add_ad_groups.main(mock_google_ads_client, mock_args.customer_id, mock_args.campaign_id)

        # Assertions
        mock_load_from_storage.assert_called_once_with(version="v19")
        mock_google_ads_client.get_service.assert_any_call("AdGroupService")
        # Allow GoogleAdsService to be called or not, as it's used for campaign existence check which might be mocked differently or not reached in a minimal test
        # mock_google_ads_client.get_service.assert_any_call("GoogleAdsService")


        self.assertEqual(mock_ad_group_service.mutate_ad_groups.call_count, 1)
        # Check the first argument of the first call to mutate_ad_groups
        args, kwargs = mock_ad_group_service.mutate_ad_groups.call_args
        self.assertEqual(kwargs['customer_id'], "1234567890")
        operations = kwargs['operations']
        self.assertEqual(len(operations), 2) # Expecting two ad group operations

        # Example of checking one operation (can be more detailed)
        self.assertEqual(operations[0].create.name, f"Earth to Mars Cruises #{(0 + 1)}")
        self.assertEqual(operations[0].create.status, mock_google_ads_client.enums.AdGroupStatusEnum.PAUSED)
        self.assertEqual(operations[0].create.campaign, f"customers/1234567890/campaigns/9876543210")


        # Verify print output
        expected_print_calls = [
            call(f"Created ad group customers/1234567890/adGroups/AD_GROUP_ID_1.")
        ]
        mock_print.assert_has_calls(expected_print_calls, any_order=False)

if __name__ == "__main__":
    unittest.main()
