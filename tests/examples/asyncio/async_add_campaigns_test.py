import unittest
import sys
from unittest.mock import MagicMock, AsyncMock, patch

# Mocking modules before import because the environment seems to lack dependencies
mock_google = MagicMock()
sys.modules["google"] = mock_google
sys.modules["google.ads"] = mock_google
sys.modules["google.ads.googleads"] = mock_google
sys.modules["google.ads.googleads.client"] = mock_google
sys.modules["google.ads.googleads.errors"] = mock_google
sys.modules["google.ads.googleads.v23"] = mock_google
sys.modules["google.ads.googleads.v23.resources"] = mock_google
sys.modules["google.ads.googleads.v23.resources.types"] = mock_google
sys.modules["google.ads.googleads.v23.resources.types.campaign"] = mock_google
sys.modules["google.ads.googleads.v23.resources.types.campaign_budget"] = mock_google
sys.modules["google.ads.googleads.v23.services"] = mock_google
sys.modules["google.ads.googleads.v23.services.services"] = mock_google
sys.modules["google.ads.googleads.v23.services.services.campaign_budget_service"] = mock_google
sys.modules["google.ads.googleads.v23.services.services.campaign_service"] = mock_google
sys.modules["google.ads.googleads.v23.services.types"] = mock_google
sys.modules["google.ads.googleads.v23.services.types.campaign_budget_service"] = mock_google
sys.modules["google.ads.googleads.v23.services.types.campaign_service"] = mock_google
sys.modules["google.ads.googleads.v23.services.types.google_ads_service"] = mock_google

from examples.asyncio import async_add_campaigns


class TestAsyncAddCampaigns(unittest.IsolatedAsyncioTestCase):
    async def test_main(self):
        # Setup Mocks
        mock_client_instance = MagicMock() # Mock the client instance directly
        mock_googleads_service = AsyncMock()
        mock_client_instance.get_service.return_value = mock_googleads_service

        mock_budget_op = MagicMock(name="BudgetOp")
        mock_campaign_op = MagicMock(name="CampaignOp")
        mock_mutate_op_budget = MagicMock(name="MutateOpBudget")
        mock_mutate_op_campaign = MagicMock(name="MutateOpCampaign")
        mock_manual_cpc = MagicMock(name="ManualCpc")

        # side_effect for get_type calls:
        # 1. CampaignBudgetOperation
        # 2. MutateOperation (for budget)
        # 3. CampaignOperation
        # 4. ManualCpc
        # 5. MutateOperation (for campaign)
        mock_client_instance.get_type.side_effect = [
            mock_budget_op,
            mock_mutate_op_budget,
            mock_campaign_op,
            mock_manual_cpc,
            mock_mutate_op_campaign,
        ]

        # Setup inner objects
        mock_budget = mock_budget_op.create
        mock_campaign = mock_campaign_op.create
        
        # Setup response
        mock_response = MagicMock()
        mock_campaign_result = MagicMock()
        mock_campaign_result.resource_name = "customers/123/campaigns/456"
        
        # response.mutate_operation_responses[1].campaign_result
        mock_response.mutate_operation_responses = [
            MagicMock(), # budget result
            MagicMock(campaign_result=mock_campaign_result) # campaign result
        ]
        
        mock_googleads_service.mutate.return_value = mock_response

        customer_id = "1234567890"

        await async_add_campaigns.main(mock_client_instance, customer_id)

        # Verification
        
        # Check if service was retrieved correctly
        mock_client_instance.get_service.assert_called_with("GoogleAdsService", is_async=True)

        # Verify Budget Resource Name
        expected_budget_resource_name = f"customers/{customer_id}/campaignBudgets/-1"
        self.assertEqual(mock_budget.resource_name, expected_budget_resource_name)
        
        # Verify Campaign references Budget
        self.assertEqual(mock_campaign.campaign_budget, expected_budget_resource_name)

        # Verify MutateOperations were constructed
        self.assertEqual(mock_mutate_op_budget.campaign_budget_operation, mock_budget_op)
        self.assertEqual(mock_mutate_op_campaign.campaign_operation, mock_campaign_op)

        # Verify GoogleAdsService.mutate called with correct operations
        mock_googleads_service.mutate.assert_called_once()
        call_args = mock_googleads_service.mutate.call_args
        self.assertEqual(call_args.kwargs["customer_id"], customer_id)
        
        operations = call_args.kwargs["mutate_operations"]
        self.assertEqual(len(operations), 2)
        self.assertEqual(operations[0], mock_mutate_op_budget)
        self.assertEqual(operations[1], mock_mutate_op_campaign)
