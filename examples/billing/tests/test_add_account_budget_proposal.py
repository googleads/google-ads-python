import unittest
from unittest.mock import MagicMock, patch, call
from io import StringIO

from examples.billing.add_account_budget_proposal import main

class TestAddAccountBudgetProposal(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    def test_main_function(self, mock_stdout):
        # Mock GoogleAdsClient instance and its services/types/enums
        mock_client = MagicMock()
        mock_proposal_service = MagicMock()
        mock_billing_setup_service = MagicMock()
        mock_operation_type = MagicMock()
        mock_proposal_create_obj = MagicMock() # This will be operation.create

        # Configure client.get_service
        def get_service_side_effect(service_name):
            if service_name == "AccountBudgetProposalService":
                return mock_proposal_service
            elif service_name == "BillingSetupService":
                return mock_billing_setup_service
            return MagicMock() # Default mock for other services if any
        mock_client.get_service.side_effect = get_service_side_effect

        # Configure client.get_type for AccountBudgetProposalOperation
        mock_client.get_type.return_value = mock_operation_type
        # Configure the .create attribute of the operation type
        mock_operation_type.create = mock_proposal_create_obj

        # Configure enums
        mock_client.enums.AccountBudgetProposalTypeEnum.CREATE = "CREATE_ENUM_VAL"
        mock_client.enums.TimeTypeEnum.NOW = "NOW_ENUM_VAL"
        mock_client.enums.TimeTypeEnum.FOREVER = "FOREVER_ENUM_VAL"

        # Configure billing_setup_service.billing_setup_path
        expected_billing_setup_path = "customers/123/billingSetups/456"
        mock_billing_setup_service.billing_setup_path.return_value = expected_billing_setup_path

        # Configure response from mutate_account_budget_proposal
        mock_mutate_response = MagicMock()
        expected_proposal_resource_name = "customers/123/accountBudgetProposals/789"
        mock_mutate_response.result.resource_name = expected_proposal_resource_name
        mock_proposal_service.mutate_account_budget_proposal.return_value = mock_mutate_response

        # Test data
        customer_id = "123"
        billing_setup_id = "456"

        # Call the main function
        main(mock_client, customer_id, billing_setup_id)

        # --- Assertions ---

        # Assert get_service calls
        mock_client.get_service.assert_any_call("AccountBudgetProposalService")
        mock_client.get_service.assert_any_call("BillingSetupService")

        # Assert get_type call
        mock_client.get_type.assert_called_once_with("AccountBudgetProposalOperation")

        # Assert billing_setup_path call
        mock_billing_setup_service.billing_setup_path.assert_called_once_with(customer_id, billing_setup_id)

        # Assert that the attributes of the proposal object (mock_proposal_create_obj) were set correctly
        self.assertEqual(mock_proposal_create_obj.proposal_type, "CREATE_ENUM_VAL")
        self.assertEqual(mock_proposal_create_obj.billing_setup, expected_billing_setup_path)
        self.assertEqual(mock_proposal_create_obj.proposed_name, "Account Budget Proposal (example)")
        self.assertEqual(mock_proposal_create_obj.proposed_start_time_type, "NOW_ENUM_VAL")
        self.assertEqual(mock_proposal_create_obj.proposed_end_time_type, "FOREVER_ENUM_VAL")
        self.assertEqual(mock_proposal_create_obj.proposed_spending_limit_micros, 10000)
        # self.assertEqual(mock_proposal_create_obj.proposed_notes, 'Received prepayment of $0.01') # If notes were set

        # Assert mutate_account_budget_proposal call
        mock_proposal_service.mutate_account_budget_proposal.assert_called_once_with(
            customer_id=customer_id,
            operation=mock_operation_type, # The operation object itself was passed
        )

        # Assert output
        expected_output = f'Created account budget proposal "{expected_proposal_resource_name}".\n'
        self.assertEqual(mock_stdout.getvalue(), expected_output)

if __name__ == "__main__":
    unittest.main()
