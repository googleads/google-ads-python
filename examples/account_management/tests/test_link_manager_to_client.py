import unittest
from unittest.mock import patch, Mock, MagicMock, call
import argparse
import sys
import io

from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.v19.services.types import (
    CustomerClientLinkOperation,
    CustomerManagerLinkOperation,
)
from google.ads.googleads.v19.resources.types import (
    CustomerClientLink,
    CustomerManagerLink,
)
from google.ads.googleads.v19.enums.types import ManagerLinkStatusEnum
from google.protobuf.field_mask_pb2 import FieldMask

# Assuming link_manager_to_client.py is in examples.account_management
from examples.account_management.link_manager_to_client import main as link_manager_main

# Define constants for IDs to be used in tests
CLIENT_CUSTOMER_ID = "client_test_id_123"
MANAGER_CUSTOMER_ID = "manager_test_id_456"
MOCK_MANAGER_LINK_ID = "mock_manager_link_789"

class TestLinkManagerToClient(unittest.TestCase):
    @patch('examples.account_management.link_manager_to_client.GoogleAdsClient')
    def setUp(self, mock_google_ads_client_class):
        # Mock the GoogleAdsClient instance
        self.mock_google_ads_client = mock_google_ads_client_class.load_from_storage.return_value
        
        # Mock services
        self.mock_ccl_service = MagicMock() # CustomerClientLinkService
        self.mock_ga_service = MagicMock()   # GoogleAdsService
        self.mock_cml_service = MagicMock() # CustomerManagerLinkService

        # Configure get_service to return the correct mock service
        def get_service_side_effect(service_name, version="v19"):
            if service_name == "CustomerClientLinkService":
                return self.mock_ccl_service
            elif service_name == "GoogleAdsService":
                return self.mock_ga_service
            elif service_name == "CustomerManagerLinkService":
                return self.mock_cml_service
            raise ValueError(f"Unknown service: {service_name}")
        self.mock_google_ads_client.get_service.side_effect = get_service_side_effect

        # Mock enums (ManagerLinkStatusEnum)
        # The script accesses members like ManagerLinkStatusEnum.PENDING
        # These members should have a .value attribute if the script uses it,
        # or just be the enum member itself if passed directly.
        # The script uses .value for status in CustomerClientLinkOperation.
        # And for status in CustomerManagerLinkOperation.
        mock_manager_link_status_enum_type = MagicMock()
        for status_name, status_value in ManagerLinkStatusEnum.ManagerLinkStatus.items():
            mock_enum_member = MagicMock()
            mock_enum_member.value = status_value # e.g., PENDING.value
            setattr(mock_manager_link_status_enum_type, status_name, mock_enum_member)
        
        self.mock_google_ads_client.enums = MagicMock()
        self.mock_google_ads_client.enums.ManagerLinkStatusEnum = mock_manager_link_status_enum_type
        
        # Mock path methods for services
        # These are typically on the client instance, not the service directly,
        # but the script calls client.get_service("...").customer_path(...)
        # So, the mock service needs to have these path methods.
        self.mock_ccl_service.customer_path.return_value = f"customers/{CLIENT_CUSTOMER_ID}"
        # For CustomerManagerLink resource name construction in step 3:
        # client.get_service("CustomerManagerLinkService").customer_manager_link_path(
        # client_customer_id, manager_customer_id, manager_link_id
        # )
        self.mock_cml_service.customer_manager_link_path.return_value = (
            f"customers/{CLIENT_CUSTOMER_ID}/customerManagerLinks/{MANAGER_CUSTOMER_ID}~{MOCK_MANAGER_LINK_ID}"
        )

        # Capture stdout
        self.held_stdout = sys.stdout
        sys.stdout = io.StringIO()

    def tearDown(self):
        sys.stdout = self.held_stdout # Restore stdout
        patch.stopall() # Stop all patches started with @patch

    def test_main_link_success(self):
        # Step 1: Extend invitation (CustomerClientLinkService)
        mock_ccl_response = MagicMock()
        mock_ccl_response.results = [MagicMock()]
        mock_ccl_response.results[0].resource_name = "test_client_link_resource_name"
        self.mock_ccl_service.mutate_customer_client_link.return_value = mock_ccl_response

        # Step 2: Search for manager_link_id (GoogleAdsService)
        mock_ga_row = MagicMock()
        # The script accesses nested attributes like: row.customer_client_link.manager_link_id
        mock_ga_row.customer_client_link = MagicMock()
        mock_ga_row.customer_client_link.manager_link_id = MOCK_MANAGER_LINK_ID
        self.mock_ga_service.search.return_value = [mock_ga_row] # Must be iterable

        # Step 3: Accept invitation (CustomerManagerLinkService)
        mock_cml_response = MagicMock()
        mock_cml_response.results = [MagicMock()]
        # The resource name for the result of CustomerManagerLink mutation
        mock_cml_response.results[0].resource_name = (
            f"customers/{CLIENT_CUSTOMER_ID}/customerManagerLinks/{MANAGER_CUSTOMER_ID}~{MOCK_MANAGER_LINK_ID}_accepted"
        )
        self.mock_cml_service.mutate_customer_manager_link.return_value = mock_cml_response
        
        # Mock client.copy_from for FieldMask
        # The script does: client.copy_from(manager_link_operation.update_mask, update_mask)
        # where update_mask is created by protobuf_helpers.field_mask.
        # We can mock copy_from to simplify or ensure the mock manager_link has _pb.
        self.mock_google_ads_client.copy_from = Mock()


        link_manager_main(self.mock_google_ads_client, CLIENT_CUSTOMER_ID, MANAGER_CUSTOMER_ID)

        # --- Assertions for Step 1 ---
        self.mock_google_ads_client.get_service.assert_any_call("CustomerClientLinkService", version="v19")
        self.mock_ccl_service.mutate_customer_client_link.assert_called_once()
        ccl_call_args = self.mock_ccl_service.mutate_customer_client_link.call_args
        self.assertEqual(ccl_call_args[1]['customer_id'], MANAGER_CUSTOMER_ID)
        ccl_operation = ccl_call_args[1]['operation']
        self.assertIsInstance(ccl_operation, CustomerClientLinkOperation)
        self.assertEqual(ccl_operation.create.client_customer, f"customers/{CLIENT_CUSTOMER_ID}")
        self.assertEqual(ccl_operation.create.status, self.mock_google_ads_client.enums.ManagerLinkStatusEnum.PENDING.value)

        # --- Assertions for Step 2 ---
        self.mock_google_ads_client.get_service.assert_any_call("GoogleAdsService", version="v19")
        self.mock_ga_service.search.assert_called_once()
        ga_call_args = self.mock_ga_service.search.call_args
        self.assertEqual(ga_call_args[1]['customer_id'], MANAGER_CUSTOMER_ID)
        expected_query = (
            "SELECT customer_client_link.manager_link_id FROM customer_client_link "
            'WHERE customer_client_link.resource_name = "test_client_link_resource_name"'
        )
        self.assertEqual(ga_call_args[1]['query'], expected_query)

        # --- Assertions for Step 3 ---
        self.mock_google_ads_client.get_service.assert_any_call("CustomerManagerLinkService", version="v19")
        self.mock_cml_service.mutate_customer_manager_link.assert_called_once()
        cml_call_args = self.mock_cml_service.mutate_customer_manager_link.call_args
        self.assertEqual(cml_call_args[1]['customer_id'], CLIENT_CUSTOMER_ID)
        cml_operations_list = cml_call_args[1]['operations']
        self.assertEqual(len(cml_operations_list), 1)
        cml_operation = cml_operations_list[0]
        self.assertIsInstance(cml_operation, CustomerManagerLinkOperation)
        
        expected_manager_link_resource_name = (
            f"customers/{CLIENT_CUSTOMER_ID}/customerManagerLinks/{MANAGER_CUSTOMER_ID}~{MOCK_MANAGER_LINK_ID}"
        )
        self.assertEqual(cml_operation.update.resource_name, expected_manager_link_resource_name)
        self.assertEqual(cml_operation.update.status, self.mock_google_ads_client.enums.ManagerLinkStatusEnum.ACTIVE.value)
        
        # Assert that copy_from was called for the update_mask
        # The script uses client.copy_from(manager_link_operation.update_mask, update_mask_from_proto_helper)
        # The first argument to copy_from is the target (operation.update_mask)
        # The second is the source (FieldMask(paths=["status"]))
        self.mock_google_ads_client.copy_from.assert_called_once()
        copy_from_call_args = self.mock_google_ads_client.copy_from.call_args
        self.assertIsInstance(copy_from_call_args[0][0], FieldMask) # Target FieldMask in operation
        self.assertIsInstance(copy_from_call_args[0][1], FieldMask) # Source FieldMask
        self.assertEqual(copy_from_call_args[0][1].paths, ["status"])


        output = sys.stdout.getvalue()
        self.assertIn(
            f"Extended an invitation from customer ID {MANAGER_CUSTOMER_ID} to customer ID {CLIENT_CUSTOMER_ID} with resource name test_client_link_resource_name",
            output
        )
        self.assertIn(
            f"Client {CLIENT_CUSTOMER_ID} accepted manager link {expected_manager_link_resource_name} from manager {MANAGER_CUSTOMER_ID}.",
            output
        )

    @patch('sys.exit')
    def test_main_google_ads_exception_on_invite(self, mock_sys_exit):
        # Configure CustomerClientLinkService to raise GoogleAdsException
        mock_error_payload = MagicMock()
        mock_error_payload.message = "Test GoogleAdsException on invite"
        mock_failure = MagicMock()
        mock_failure.errors = [mock_error_payload]
        google_ads_exception = GoogleAdsException(
            error=None, call=None, failure=mock_failure, error_code=None,
            message="Simulated GoogleAdsException during invitation"
        )
        self.mock_ccl_service.mutate_customer_client_link.side_effect = google_ads_exception

        link_manager_main(self.mock_google_ads_client, "client_id_err_invite", "manager_id_err_invite")

        mock_sys_exit.assert_called_once_with(1)
        output = sys.stdout.getvalue()
        self.assertIn("Request with ID", output)
        self.assertIn("Test GoogleAdsException on invite", output)
        self.mock_ccl_service.mutate_customer_client_link.assert_called_once()
        self.mock_ga_service.search.assert_not_called() # Should exit before search
        self.mock_cml_service.mutate_customer_manager_link.assert_not_called() # Should exit before accept

    @patch('sys.exit')
    def test_main_google_ads_exception_on_search(self, mock_sys_exit):
        # Step 1: Successful invitation
        mock_ccl_response = MagicMock()
        mock_ccl_response.results = [MagicMock()]
        mock_ccl_response.results[0].resource_name = "test_client_link_for_search_fail"
        self.mock_ccl_service.mutate_customer_client_link.return_value = mock_ccl_response
        
        # Configure GoogleAdsService to raise GoogleAdsException
        mock_error_payload = MagicMock()
        mock_error_payload.message = "Test GoogleAdsException on search"
        mock_failure = MagicMock()
        mock_failure.errors = [mock_error_payload]
        google_ads_exception = GoogleAdsException(
            error=None, call=None, failure=mock_failure, error_code=None,
            message="Simulated GoogleAdsException during search"
        )
        self.mock_ga_service.search.side_effect = google_ads_exception

        link_manager_main(self.mock_google_ads_client, "client_id_err_search", "manager_id_err_search")

        mock_sys_exit.assert_called_once_with(1)
        output = sys.stdout.getvalue()
        self.assertIn("Request with ID", output)
        self.assertIn("Test GoogleAdsException on search", output)
        self.mock_ccl_service.mutate_customer_client_link.assert_called_once()
        self.mock_ga_service.search.assert_called_once()
        self.mock_cml_service.mutate_customer_manager_link.assert_not_called() # Should exit before accept

    @patch('sys.exit')
    def test_main_google_ads_exception_on_accept(self, mock_sys_exit):
        # Step 1: Successful invitation
        mock_ccl_response = MagicMock()
        mock_ccl_response.results = [MagicMock()]
        mock_ccl_response.results[0].resource_name = "test_client_link_for_accept_fail"
        self.mock_ccl_service.mutate_customer_client_link.return_value = mock_ccl_response

        # Step 2: Successful search
        mock_ga_row = MagicMock()
        mock_ga_row.customer_client_link.manager_link_id = "manager_link_for_accept_fail"
        self.mock_ga_service.search.return_value = [mock_ga_row]

        # Configure CustomerManagerLinkService to raise GoogleAdsException
        mock_error_payload = MagicMock()
        mock_error_payload.message = "Test GoogleAdsException on accept"
        mock_failure = MagicMock()
        mock_failure.errors = [mock_error_payload]
        google_ads_exception = GoogleAdsException(
            error=None, call=None, failure=mock_failure, error_code=None,
            message="Simulated GoogleAdsException during acceptance"
        )
        self.mock_cml_service.mutate_customer_manager_link.side_effect = google_ads_exception
        
        # Mock client.copy_from as it's called before the mutate call
        self.mock_google_ads_client.copy_from = Mock()


        link_manager_main(self.mock_google_ads_client, "client_id_err_accept", "manager_id_err_accept")

        mock_sys_exit.assert_called_once_with(1)
        output = sys.stdout.getvalue()
        self.assertIn("Request with ID", output)
        self.assertIn("Test GoogleAdsException on accept", output)
        self.mock_ccl_service.mutate_customer_client_link.assert_called_once()
        self.mock_ga_service.search.assert_called_once()
        self.mock_cml_service.mutate_customer_manager_link.assert_called_once()

    # Patch the main function in the script to check if it's called by __main__
    @patch('examples.account_management.link_manager_to_client.main')
    # Patch ArgumentParser.parse_args to control returned arguments
    @patch('argparse.ArgumentParser.parse_args')
    # The GoogleAdsClient is already patched in setUp by the class decorator for TestLinkManagerToClient
    def test_argument_parser(self, mock_parse_args, mock_script_main_function):
        # mock_google_ads_client_class is available from setUp due to class-level patch
        # self.mock_google_ads_client is the instance returned by load_from_storage

        test_cli_client_id = "cli_client_id_789"
        test_cli_manager_id = "cli_manager_id_101"

        sys.argv = [
            "link_manager_to_client.py",
            "-c", test_cli_client_id,
            "-m", test_cli_manager_id,
        ]

        # Mock parse_args to return the customer_id and manager_customer_id
        mock_parse_args.return_value = argparse.Namespace(
            customer_id=test_cli_client_id,
            manager_customer_id=test_cli_manager_id
        )
        
        # Execute the script's main block using runpy
        # This will trigger argument parsing and the call to the script's main()
        import runpy
        runpy.run_module("examples.account_management.link_manager_to_client", run_name="__main__")

        # Assert that GoogleAdsClient.load_from_storage was called (done by __main__ block)
        # This is implicitly tested as self.mock_google_ads_client would be used if called.
        # The class-level patch in setUp ensures load_from_storage returns self.mock_google_ads_client.
        # So, we can check if the mock_script_main_function was called with this instance.
        
        mock_parse_args.assert_called_once()
        
        # Assert that the script's main function (which is mocked) was called correctly
        # The script's __main__ block calls: main(client, args.customer_id, args.manager_customer_id)
        mock_script_main_function.assert_called_once_with(
            self.mock_google_ads_client, # This is the client instance from setUp
            test_cli_client_id,
            test_cli_manager_id
        )


if __name__ == "__main__":
    unittest.main()
