import unittest
from unittest.mock import patch, MagicMock, ANY
import sys
from io import StringIO

# Correctly import the main function from the script to be tested
from examples.basic_operations.add_ad_groups import main as add_ad_groups_main

class TestAddAdGroups(unittest.TestCase):
    # Patch GoogleAdsClient.load_from_storage as that's what the script uses
    @patch("examples.basic_operations.add_ad_groups.GoogleAdsClient.load_from_storage")
    def test_add_ad_groups_mocked_service(self, mock_load_from_storage):
        # --- Setup Mocks ---
        mock_client = MagicMock()
        mock_load_from_storage.return_value = mock_client

        # Mock services
        mock_ad_group_service = mock_client.get_service("AdGroupService", version="v19")
        mock_campaign_service = mock_client.get_service("CampaignService", version="v19")

        # Mock responses
        mock_mutate_response = MagicMock()
        mock_ad_group_result = MagicMock()
        mock_ad_group_result.resource_name = "customers/1234567890/adGroups/NEW_AD_GROUP_ID"
        mock_mutate_response.results = [mock_ad_group_result]
        mock_ad_group_service.mutate_ad_groups.return_value = mock_mutate_response

        # Define test parameters
        customer_id = "1234567890"
        campaign_id = "CAMPAIGN_ID_123"
        expected_campaign_path = f"customers/{customer_id}/campaigns/{campaign_id}"

        # Mock campaign_path method
        mock_campaign_service.campaign_path.return_value = expected_campaign_path

        # --- Capture stdout ---
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        # --- Call the main function ---
        # The script's main function takes the client object, customer_id, and campaign_id
        add_ad_groups_main(mock_client, customer_id, campaign_id)

        # --- Restore stdout ---
        sys.stdout = old_stdout
        output = captured_output.getvalue().strip()

        # --- Assertions ---

        # 1. Assert mutate_ad_groups was called correctly
        mock_ad_group_service.mutate_ad_groups.assert_called_once_with(
            customer_id=customer_id,
            operations=[ANY]  # Using ANY for the operation list initially
        )

        # 2. Get the actual operation passed to mutate_ad_groups
        _, called_kwargs = mock_ad_group_service.mutate_ad_groups.call_args
        operations = called_kwargs["operations"]
        self.assertEqual(len(operations), 1)
        ad_group_operation = operations[0]

        # 3. Assert details of the ad group operation
        # For the name, since it contains a UUID, we check if it starts with the expected prefix.
        self.assertTrue(ad_group_operation.create.name.startswith("Earth to Mars cruises "))
        # Assert other properties
        self.assertEqual(ad_group_operation.create.status, mock_client.enums.AdGroupStatusEnum.ENABLED)
        self.assertEqual(ad_group_operation.create.campaign, expected_campaign_path)
        self.assertEqual(ad_group_operation.create.type_, mock_client.enums.AdGroupTypeEnum.SEARCH_STANDARD)
        self.assertEqual(ad_group_operation.create.cpc_bid_micros, 10000000)

        # 4. Assert that campaign_path was called correctly
        mock_campaign_service.campaign_path.assert_called_once_with(customer_id, campaign_id)

        # 5. Assert the script output
        expected_output = f"Created ad group {mock_ad_group_result.resource_name}."
        self.assertEqual(output, expected_output)

if __name__ == "__main__":
    unittest.main()
