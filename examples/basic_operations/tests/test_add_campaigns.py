import unittest
from unittest.mock import patch, MagicMock, ANY
import sys
from io import StringIO
import datetime

# Correctly import the main function from the script to be tested
from examples.basic_operations.add_campaigns import main as add_campaigns_main
from google.ads.googleads.v19.common.types.bidding import ManualCpc

class TestAddCampaigns(unittest.TestCase):
    @patch("examples.basic_operations.add_campaigns.datetime.date")
    @patch("examples.basic_operations.add_campaigns.GoogleAdsClient.load_from_storage")
    def test_add_campaigns_mocked_service(self, mock_load_from_storage, mock_date):
        # --- Setup Mocks ---
        mock_client = MagicMock()
        mock_load_from_storage.return_value = mock_client

        # Configure get_type to return distinct mocks for different type_name arguments
        # to prevent interference between budget and campaign object creation.
        def get_type_side_effect(type_name, version=None): # Added version to match potential signature
            mock_type_instance = MagicMock(name=f"MockTypeInstance_{type_name}")
            # Ensure .create is also a unique mock for each type instance
            mock_type_instance.create = MagicMock(name=f"MockCreateFor_{type_name}")
            return mock_type_instance
        mock_client.get_type.side_effect = get_type_side_effect

        # Mock datetime to control start and end dates
        fixed_today = datetime.date(2024, 1, 1) # Real datetime.date for calculations
        expected_start_date_str = (fixed_today + datetime.timedelta(days=1)).strftime("%Y%m%d")
        expected_end_date_str = (fixed_today + datetime.timedelta(days=1) + datetime.timedelta(weeks=4)).strftime("%Y%m%d")

        # Configure the mock_date object (which is mocking ...add_campaigns.datetime.date)
        mock_date.today.return_value = fixed_today

        def mock_strftime_side_effect(date_obj, format_str):
            # This function will be called by the script's datetime.date.strftime(date_obj, format_str)
            # We expect format_str to be "%Y%m%d"
            if date_obj == (fixed_today + datetime.timedelta(days=1)): # This is start_time in script
                return expected_start_date_str
            elif date_obj == (fixed_today + datetime.timedelta(days=1) + datetime.timedelta(weeks=4)): # This is end_time in script
                return expected_end_date_str
            # Fallback for safety, though not expected to be hit in this test
            return "UNEXPECTED_STRFTIME_CALL"
        mock_date.strftime.side_effect = mock_strftime_side_effect


        # Mock CampaignBudgetService
        mock_budget_service = mock_client.get_service("CampaignBudgetService", version="v19")
        mock_budget_mutate_response = MagicMock()
        mock_budget_result = MagicMock()
        mock_budget_resource_name = "customers/1234567890/campaignBudgets/BUDGET_ID_123"
        mock_budget_result.resource_name = mock_budget_resource_name
        mock_budget_mutate_response.results = [mock_budget_result]
        mock_budget_service.mutate_campaign_budgets.return_value = mock_budget_mutate_response

        # Mock CampaignService
        mock_campaign_service = mock_client.get_service("CampaignService", version="v19")
        mock_campaign_mutate_response = MagicMock()
        mock_campaign_result = MagicMock()
        mock_campaign_result.resource_name = "customers/1234567890/campaigns/CAMPAIGN_ID_456"
        mock_campaign_mutate_response.results = [mock_campaign_result]
        mock_campaign_service.mutate_campaigns.return_value = mock_campaign_mutate_response

        customer_id = "1234567890"

        # --- Capture stdout ---
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        # --- Call the main function ---
        add_campaigns_main(mock_client, customer_id)

        # --- Restore stdout ---
        sys.stdout = old_stdout
        output = captured_output.getvalue().strip()

        # --- Assertions for CampaignBudgetService ---
        mock_budget_service.mutate_campaign_budgets.assert_called_once_with(
            customer_id=customer_id,
            operations=[ANY]
        )
        _, budget_call_kwargs = mock_budget_service.mutate_campaign_budgets.call_args
        budget_operations = budget_call_kwargs["operations"]
        self.assertEqual(len(budget_operations), 1)
        budget_operation = budget_operations[0]

        self.assertTrue(budget_operation.create.name.startswith("Interplanetary Budget "))
        self.assertEqual(budget_operation.create.delivery_method, mock_client.enums.BudgetDeliveryMethodEnum.STANDARD)
        self.assertEqual(budget_operation.create.amount_micros, 500000)

        # --- Assertions for CampaignService ---
        mock_campaign_service.mutate_campaigns.assert_called_once_with(
            customer_id=customer_id,
            operations=[ANY]
        )
        _, campaign_call_kwargs = mock_campaign_service.mutate_campaigns.call_args
        campaign_operations = campaign_call_kwargs["operations"]
        self.assertEqual(len(campaign_operations), 1)
        campaign_operation = campaign_operations[0].create # Access the .create attribute

        self.assertTrue(campaign_operation.name.startswith("Interplanetary Cruise "))
        self.assertEqual(campaign_operation.advertising_channel_type, mock_client.enums.AdvertisingChannelTypeEnum.SEARCH)
        self.assertEqual(campaign_operation.status, mock_client.enums.CampaignStatusEnum.PAUSED)
        self.assertIsInstance(campaign_operation.manual_cpc, ManualCpc)
        self.assertEqual(campaign_operation.campaign_budget, mock_budget_resource_name)

        self.assertEqual(campaign_operation.network_settings.target_google_search, True)
        self.assertEqual(campaign_operation.network_settings.target_search_network, True)
        self.assertEqual(campaign_operation.network_settings.target_partner_search_network, False)
        self.assertEqual(campaign_operation.network_settings.target_content_network, True)

        self.assertEqual(campaign_operation.start_date, expected_start_date_str)
        self.assertEqual(campaign_operation.end_date, expected_end_date_str)


        # --- Assert script output ---
        expected_output = f"Created campaign {mock_campaign_result.resource_name}."
        self.assertEqual(output, expected_output)

if __name__ == "__main__":
    unittest.main()
