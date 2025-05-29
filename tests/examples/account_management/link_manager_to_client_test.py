import unittest
from unittest.mock import patch, MagicMock

from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v19.enums.types import LinkStatusEnum
from examples.account_management.link_manager_to_client import main


class LinkManagerToClientTest(unittest.TestCase):

    @patch("examples.account_management.link_manager_to_client.GoogleAdsClient.load_from_storage")
    def test_link_manager_to_client_success(self, mock_load_from_storage):
        """Tests successfully linking a manager to a client (manager initiates)."""
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_customer_client_link_service = MagicMock()
        # Configure get_service to return the correct service mock
        mock_google_ads_client.get_service.return_value = mock_customer_client_link_service

        mock_mutate_response = MagicMock()
        mock_result = MagicMock()
        expected_resource_name = "customers/123/customerClientLinks/manager_link_id_val"
        mock_result.resource_name = expected_resource_name
        mock_mutate_response.results = [mock_result]
        mock_customer_client_link_service.mutate_customer_client_link.return_value = mock_mutate_response

        client_customer_id = "1111111111" # Client being linked
        manager_customer_id = "2222222222" # Manager initiating the link

        with patch("builtins.print") as mock_print:
            # manager_customer_id is provided, so script should try to create a new link
            main(mock_google_ads_client, client_customer_id, manager_customer_id=manager_customer_id, manager_link_id=None)

        mock_google_ads_client.get_service.assert_called_once_with(
            "CustomerClientLinkService", version="v19"
        )

        self.assertEqual(mock_customer_client_link_service.mutate_customer_client_link.call_count, 1)
        call_args = mock_customer_client_link_service.mutate_customer_client_link.call_args
        
        self.assertEqual(call_args[1]['customer_id'], client_customer_id)
        operation_arg = call_args[1]['operation']
        
        self.assertIsNotNone(operation_arg.create)
        link_object = operation_arg.create
        self.assertEqual(link_object.manager_customer, f"customers/{manager_customer_id}")
        self.assertEqual(link_object.status, LinkStatusEnum.LinkStatus.PENDING)

        expected_print_msg = (f"Extended an invitation from customer client "
                              f"{client_customer_id} to manager {manager_customer_id} "
                              f"with resource name {expected_resource_name}")
        printed_strings = [c[0][0] for c in mock_print.call_args_list if c[0]]
        self.assertTrue(any(expected_print_msg in s for s in printed_strings))


    @patch("examples.account_management.link_manager_to_client.GoogleAdsClient.load_from_storage")
    def test_client_accepts_invitation_success(self, mock_load_from_storage):
        """Tests client successfully accepting a manager's invitation."""
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_customer_manager_link_service = MagicMock()
        mock_google_ads_client.get_service.return_value = mock_customer_manager_link_service
        
        mock_mutate_response = MagicMock()
        mock_result = MagicMock()
        manager_link_id = "3333333333" # This is the ID of the link itself
        client_customer_id = "1111111111" # Client accepting the link
        expected_resource_name = f"customers/{client_customer_id}/customerManagerLinks/{manager_link_id}"
        mock_result.resource_name = expected_resource_name
        mock_mutate_response.results = [mock_result]
        mock_customer_manager_link_service.mutate_customer_manager_link.return_value = mock_mutate_response


        with patch("builtins.print") as mock_print:
            # manager_customer_id is None, manager_link_id is provided. Client accepts.
            main(mock_google_ads_client, client_customer_id, manager_customer_id=None, manager_link_id=manager_link_id)

        mock_google_ads_client.get_service.assert_called_once_with(
            "CustomerManagerLinkService", version="v19"
        )

        self.assertEqual(mock_customer_manager_link_service.mutate_customer_manager_link.call_count, 1)
        call_args = mock_customer_manager_link_service.mutate_customer_manager_link.call_args
        
        # The first argument to mutate_customer_manager_link is customer_id
        self.assertEqual(call_args[0][0], client_customer_id) 
        # The operations are in kwargs or as the second pos arg. The script passes it as the second pos arg.
        operations_arg_list = call_args[0][1] 
        self.assertEqual(len(operations_arg_list), 1)
        operation_arg = operations_arg_list[0]

        self.assertIsNotNone(operation_arg.update)
        link_object = operation_arg.update
        self.assertEqual(link_object.resource_name, f"customers/{client_customer_id}/customerManagerLinks/{manager_link_id}")
        self.assertEqual(link_object.status, LinkStatusEnum.LinkStatus.ACTIVE)
        
        # Check field mask
        self.assertIn("status", operation_arg.update_mask.paths)


        expected_print_msg = (f"Customer manager link with resource name {expected_resource_name} "
                              f"was updated for customer ID {client_customer_id} and manager link ID {manager_link_id}")
        printed_strings = [c[0][0] for c in mock_print.call_args_list if c[0]]
        self.assertTrue(any(expected_print_msg in s for s in printed_strings))


    @patch("examples.account_management.link_manager_to_client.GoogleAdsClient.load_from_storage")
    def test_link_manager_to_client_exception(self, mock_load_from_storage):
        """Tests GoogleAdsException when linking manager to client."""
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_customer_client_link_service = MagicMock()
        mock_google_ads_client.get_service.return_value = mock_customer_client_link_service

        mock_failure = MagicMock()
        mock_error = MagicMock()
        mock_error.message = "Test Exception: Link Manager to Client"
        mock_failure.errors = [mock_error]
        google_ads_exception = GoogleAdsException(mock_failure, "call", "trigger", "req_id", "err_enum")
        mock_customer_client_link_service.mutate_customer_client_link.side_effect = google_ads_exception
        
        client_customer_id = "1111111111"
        manager_customer_id = "2222222222"

        with patch("sys.exit") as mock_sys_exit, \
             patch("builtins.print") as mock_error_print:
            main(mock_google_ads_client, client_customer_id, manager_customer_id=manager_customer_id, manager_link_id=None)
            mock_sys_exit.assert_called_once_with(1)
            self.assertTrue(any("Test Exception: Link Manager to Client" in str(c[0]) for c in mock_error_print.call_args_list))


    @patch("examples.account_management.link_manager_to_client.GoogleAdsClient.load_from_storage")
    def test_client_accepts_invitation_exception(self, mock_load_from_storage):
        """Tests GoogleAdsException when client accepts invitation."""
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_customer_manager_link_service = MagicMock()
        mock_google_ads_client.get_service.return_value = mock_customer_manager_link_service

        mock_failure = MagicMock()
        mock_error = MagicMock()
        mock_error.message = "Test Exception: Client Accepts"
        mock_failure.errors = [mock_error]
        google_ads_exception = GoogleAdsException(mock_failure, "call", "trigger", "req_id", "err_enum")
        mock_customer_manager_link_service.mutate_customer_manager_link.side_effect = google_ads_exception

        client_customer_id = "1111111111"
        manager_link_id = "3333333333"

        with patch("sys.exit") as mock_sys_exit, \
             patch("builtins.print") as mock_error_print:
            main(mock_google_ads_client, client_customer_id, manager_customer_id=None, manager_link_id=manager_link_id)
            mock_sys_exit.assert_called_once_with(1)
            self.assertTrue(any("Test Exception: Client Accepts" in str(c[0]) for c in mock_error_print.call_args_list))


if __name__ == "__main__":
    unittest.main()
