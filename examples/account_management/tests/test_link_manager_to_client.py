import unittest
from unittest.mock import patch, MagicMock
import io
import sys

from examples.account_management import link_manager_to_client
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.v19.services.services.customer_client_link_service import CustomerClientLinkServiceClient
from google.ads.googleads.v19.services.services.customer_manager_link_service import CustomerManagerLinkServiceClient
from google.ads.googleads.v19.services.services.google_ads_service import GoogleAdsServiceClient
# Import the top-level enum type
from google.ads.googleads.v19.enums.types.manager_link_status import ManagerLinkStatusEnum as ActualManagerLinkStatusEnumType
from google.ads.googleads.v19.resources.types.customer_client_link import CustomerClientLink
from google.ads.googleads.v19.resources.types.customer_manager_link import CustomerManagerLink
from google.ads.googleads.v19.services.types import GoogleAdsRow

class TestLinkManagerToClient(unittest.TestCase):

    @patch('examples.account_management.link_manager_to_client.protobuf_helpers.field_mask')
    @patch('examples.account_management.link_manager_to_client.GoogleAdsClient')
    def test_main_links_manager_and_client(self, mock_google_ads_client_class, mock_field_mask_helper):
        # 1. Setup Mocks
        mock_client_instance = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client_class.load_from_storage.return_value = mock_client_instance

        mock_ccl_service = MagicMock(spec=CustomerClientLinkServiceClient)
        mock_cml_service = MagicMock(spec=CustomerManagerLinkServiceClient)
        mock_ga_service = MagicMock(spec=GoogleAdsServiceClient)

        def get_service_side_effect(service_name):
            if service_name == "CustomerClientLinkService":
                return mock_ccl_service
            elif service_name == "CustomerManagerLinkService":
                return mock_cml_service
            elif service_name == "GoogleAdsService":
                return mock_ga_service
            raise ValueError(f"Unexpected service requested: {service_name}")
        mock_client_instance.get_service.side_effect = get_service_side_effect

        # Mock client.get_type for operations
        mock_ccl_operation = MagicMock() # CustomerClientLinkOperation
        mock_cml_operation = MagicMock() # CustomerManagerLinkOperation

        def get_type_side_effect(type_name):
            if type_name == "CustomerClientLinkOperation":
                return mock_ccl_operation
            elif type_name == "CustomerManagerLinkOperation":
                return mock_cml_operation
            raise ValueError(f"Unexpected type requested by script: {type_name}")
        mock_client_instance.get_type.side_effect = get_type_side_effect

        # Mock client.enums.ManagerLinkStatusEnum
        # The script accesses client.enums.ManagerLinkStatusEnum.PENDING (or .ACTIVE)
        # This means mock_client_instance.enums.ManagerLinkStatusEnum should be the inner enum type
        # that actually has PENDING, ACTIVE as attributes.
        mock_client_instance.enums = MagicMock()
        mock_client_instance.enums.ManagerLinkStatusEnum = ActualManagerLinkStatusEnumType.ManagerLinkStatus

        # Mock client.copy_from (used for update_mask)
        # This can be a simple pass-through or we can inspect its args if needed
        mock_client_instance.copy_from = MagicMock()

        # Mock field_mask helper
        mock_field_mask_helper.return_value = MagicMock(paths=["status"]) # Simulating FieldMask(paths=['status'])


        # --- Phase 1: Manager Invites Client ---
        client_customer_id = "client123"
        manager_customer_id = "manager456"

        # Mock customer_path for CustomerClientLinkService
        expected_client_customer_resource_name = f"customers/{client_customer_id}"
        mock_ccl_service.customer_path.return_value = expected_client_customer_resource_name

        # Mock mutate_customer_client_link response
        mock_ccl_response = MagicMock()
        created_ccl_resource_name = f"customers/{manager_customer_id}/customerClientLinks/link1"
        mock_ccl_response.results = [MagicMock(resource_name=created_ccl_resource_name)]
        mock_ccl_service.mutate_customer_client_link.return_value = mock_ccl_response

        # --- Intermediate Search Call ---
        manager_link_id_val = 789
        mock_search_row = GoogleAdsRow() # Actual GoogleAdsRow
        mock_search_row.customer_client_link.manager_link_id = manager_link_id_val
        # The script uses response.result to iterate, so mock a container with a .result attribute
        mock_search_response_container = MagicMock()
        mock_search_response_container.result = iter([mock_search_row]) # .result is the iterator
        mock_ga_service.search.return_value = mock_search_response_container


        # --- Phase 2: Client Accepts Invitation ---
        # Mock customer_manager_link_path for CustomerManagerLinkService
        expected_cml_resource_name = f"customers/{client_customer_id}/customerManagerLinks/{manager_customer_id}~{manager_link_id_val}"
        mock_cml_service.customer_manager_link_path.return_value = expected_cml_resource_name

        # Mock mutate_customer_manager_link response
        mock_cml_response = MagicMock()
        updated_cml_resource_name = expected_cml_resource_name # Usually same after update
        mock_cml_response.results = [MagicMock(resource_name=updated_cml_resource_name)]
        mock_cml_service.mutate_customer_manager_link.return_value = mock_cml_response

        # 2. Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # 3. Call the main function
        link_manager_to_client.main(mock_client_instance, client_customer_id, manager_customer_id)

        # 4. Restore stdout
        sys.stdout = sys.__stdout__

        # 5. Assertions
        # Assert get_service calls
        mock_client_instance.get_service.assert_any_call("CustomerClientLinkService")
        mock_client_instance.get_service.assert_any_call("GoogleAdsService")
        mock_client_instance.get_service.assert_any_call("CustomerManagerLinkService")

        # Assert get_type calls
        mock_client_instance.get_type.assert_any_call("CustomerClientLinkOperation")
        mock_client_instance.get_type.assert_any_call("CustomerManagerLinkOperation")

        # Phase 1 Assertions (Manager Invites)
        mock_ccl_service.customer_path.assert_called_once_with(client_customer_id)
        mock_ccl_service.mutate_customer_client_link.assert_called_once()
        ccl_call_args = mock_ccl_service.mutate_customer_client_link.call_args
        self.assertEqual(ccl_call_args.kwargs['customer_id'], manager_customer_id)
        self.assertEqual(ccl_call_args.kwargs['operation'], mock_ccl_operation)
        self.assertEqual(mock_ccl_operation.create.client_customer, expected_client_customer_resource_name)
        self.assertEqual(mock_ccl_operation.create.status, ActualManagerLinkStatusEnumType.ManagerLinkStatus.PENDING)

        # Search Assertions
        mock_ga_service.search.assert_called_once()
        ga_search_call_args = mock_ga_service.search.call_args
        self.assertEqual(ga_search_call_args.kwargs['customer_id'], manager_customer_id)
        expected_query = f'''
        SELECT
            customer_client_link.manager_link_id
        FROM
            customer_client_link
        WHERE
            customer_client_link.resource_name = "{created_ccl_resource_name}"''' # Query uses the result from 1st mutation
        self.assertEqual(ga_search_call_args.kwargs['query'].strip(), expected_query.strip())

        # Phase 2 Assertions (Client Accepts)
        mock_cml_service.customer_manager_link_path.assert_called_once_with(
            client_customer_id, manager_customer_id, manager_link_id_val
        )
        # Assert client.copy_from was called for the update_mask
        # The script does: client.copy_from(manager_link_operation.update_mask, protobuf_helpers.field_mask(None, manager_link._pb))
        # We mocked protobuf_helpers.field_mask. The first arg to copy_from is manager_link_operation.update_mask
        mock_client_instance.copy_from.assert_called_once()
        copy_from_args = mock_client_instance.copy_from.call_args[0] # Positional args
        self.assertEqual(copy_from_args[0], mock_cml_operation.update_mask) # First arg is the target mask
        self.assertEqual(copy_from_args[1], mock_field_mask_helper.return_value) # Second arg is the source mask

        mock_cml_service.mutate_customer_manager_link.assert_called_once()
        cml_call_args = mock_cml_service.mutate_customer_manager_link.call_args
        self.assertEqual(cml_call_args.kwargs['customer_id'], client_customer_id)
        # operations is a list
        self.assertEqual(len(cml_call_args.kwargs['operations']), 1)
        self.assertEqual(cml_call_args.kwargs['operations'][0], mock_cml_operation)
        self.assertEqual(mock_cml_operation.update.resource_name, expected_cml_resource_name)
        self.assertEqual(mock_cml_operation.update.status, ActualManagerLinkStatusEnumType.ManagerLinkStatus.ACTIVE)
        # self.assertTrue("status" in mock_cml_operation.update_mask.paths) # Checked via mock_field_mask_helper

        # Verify printed output
        output = captured_output.getvalue()
        expected_output_phase1 = (
            f'Extended an invitation from customer "{manager_customer_id}" to '
            f'customer "{client_customer_id}" with client link resource_name '
            f'"{created_ccl_resource_name}"\n'
        )
        expected_output_phase2 = (
            "Client accepted invitation with resource_name: "
            f'"{updated_cml_resource_name}"\n'
        )
        self.assertIn(expected_output_phase1, output)
        self.assertIn(expected_output_phase2, output)

if __name__ == "__main__":
    unittest.main()
