import unittest
from unittest.mock import patch, MagicMock

from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v19.enums.types import AccessRoleEnum
from examples.account_management.invite_user_with_access_role import main


class InviteUserWithAccessRoleTest(unittest.TestCase):

    @patch("examples.account_management.invite_user_with_access_role.GoogleAdsClient.load_from_storage")
    def test_invite_user_success(self, mock_load_from_storage):
        """Tests the successful invitation of a user."""
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_invitation_service = MagicMock()
        mock_google_ads_client.get_service.return_value = mock_invitation_service

        # Mock the response from mutate_customer_user_access_invitation
        mock_mutate_response = MagicMock()
        mock_invitation_result = MagicMock()
        expected_resource_name = "customers/1234567890/customerUserAccessInvitations/98765"
        mock_invitation_result.resource_name = expected_resource_name
        mock_mutate_response.results = [mock_invitation_result] # results is a list
        mock_invitation_service.mutate_customer_user_access_invitation.return_value = mock_mutate_response

        customer_id = "1234567890"
        email_address = "testuser@example.com"
        # The script converts the string "ADMIN" to AccessRoleEnum.AccessRole.ADMIN
        # So we pass the string version as the script expects.
        access_role_str = "ADMIN" 
        expected_access_role_enum = AccessRoleEnum.AccessRole.ADMIN


        with patch("builtins.print") as mock_print:
            main(mock_google_ads_client, customer_id, email_address, access_role_str)

        # Assert that get_service was called correctly
        mock_google_ads_client.get_service.assert_called_once_with(
            "CustomerUserAccessInvitationService", version="v19"
        )

        # Assert that mutate_customer_user_access_invitation was called once
        self.assertEqual(mock_invitation_service.mutate_customer_user_access_invitation.call_count, 1)
        
        # Check the arguments of the call
        call_args = mock_invitation_service.mutate_customer_user_access_invitation.call_args
        # Expected: customer_id=customer_id, operation=operation
        self.assertEqual(call_args[1]['customer_id'], customer_id)
        
        operation_arg = call_args[1]['operation']
        # The operation should be a CustomerUserAccessInvitationOperation
        # with a 'create' field set to a CustomerUserAccessInvitation object
        self.assertIsNotNone(operation_arg.create)
        invitation_object = operation_arg.create
        self.assertEqual(invitation_object.email_address, email_address)
        self.assertEqual(invitation_object.access_role, expected_access_role_enum)
        # The script also sets access_creation_date_time, but it's set to client.datetime.now()
        # which is hard to match exactly. We'll trust it's set.

        # Assert that the success message with the resource name was printed
        expected_print_message = (f"Customer user access invitation with resource name "
                                  f"'{expected_resource_name}' created for customer ID "
                                  f"'{customer_id}' to email address '{email_address}' "
                                  f"with access role '{access_role_str}'.")
        
        printed_strings = [c[0][0] for c in mock_print.call_args_list if c[0]]
        self.assertTrue(any(expected_print_message in s for s in printed_strings))


    @patch("examples.account_management.invite_user_with_access_role.GoogleAdsClient.load_from_storage")
    def test_invite_user_google_ads_exception(self, mock_load_from_storage):
        """Tests handling of GoogleAdsException during user invitation."""
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_invitation_service = MagicMock()
        mock_google_ads_client.get_service.return_value = mock_invitation_service

        # Configure mutate_customer_user_access_invitation to raise GoogleAdsException
        mock_failure = MagicMock()
        mock_error = MagicMock()
        mock_error.message = "Test GoogleAdsException for invitation"
        mock_failure.errors = [mock_error]
        google_ads_exception = GoogleAdsException(
            mock_failure, "call", "trigger", "request_id", "error_code_enum"
        )
        mock_invitation_service.mutate_customer_user_access_invitation.side_effect = google_ads_exception

        customer_id = "1234567890"
        email_address = "testuser@example.com"
        access_role_str = "ADMIN"

        with patch("sys.exit") as mock_sys_exit, \
             patch("builtins.print") as mock_error_print:
            main(mock_google_ads_client, customer_id, email_address, access_role_str)
            
            mock_sys_exit.assert_called_once_with(1)
            # Check if the exception details were printed
            error_printed = False
            for call_args in mock_error_print.call_args_list:
                if "Test GoogleAdsException for invitation" in call_args[0][0]:
                    error_printed = True
                    break
            self.assertTrue(error_printed, "GoogleAdsException details not printed to console.")

        mock_google_ads_client.get_service.assert_called_once_with(
            "CustomerUserAccessInvitationService", version="v19"
        )
        mock_invitation_service.mutate_customer_user_access_invitation.assert_called_once()


    @patch("examples.account_management.invite_user_with_access_role.GoogleAdsClient.load_from_storage")
    def test_invite_user_invalid_role(self, mock_load_from_storage):
        """Tests invitation with an invalid access role string."""
        mock_google_ads_client = MagicMock() # Not strictly needed as it should fail before API call
        mock_load_from_storage.return_value = mock_google_ads_client
        
        customer_id = "1234567890"
        email_address = "testuser@example.com"
        invalid_access_role_str = "SUPER_ADMIN" # Not a valid role string in AccessRoleEnum

        # The script uses a try-except ValueError around AccessRoleEnum.AccessRole[access_role_str]
        # and then calls sys.exit(1) if it fails.
        with patch("sys.exit") as mock_sys_exit, \
             patch("builtins.print") as mock_error_print:
            main(mock_google_ads_client, customer_id, email_address, invalid_access_role_str)
            
            mock_sys_exit.assert_called_once_with(1)
            # Check if the specific error message for invalid role was printed
            # The script prints: f"Invalid access role '{access_role_str}'. Valid roles are: ..."
            error_message_found = False
            for call_args in mock_error_print.call_args_list:
                if f"Invalid access role '{invalid_access_role_str}'." in call_args[0][0]:
                    error_message_found = True
                    break
            self.assertTrue(error_message_found, "Invalid role error message not printed.")
        
        # Service should not have been called if role is invalid
        mock_google_ads_client.get_service.assert_not_called()


if __name__ == "__main__":
    unittest.main()
