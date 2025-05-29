import unittest
from unittest.mock import patch, Mock, MagicMock, call
import argparse
import sys
import io

from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.v19.services.types import CustomerUserAccessInvitationOperation
from google.ads.googleads.v19.resources.types import CustomerUserAccessInvitation
from google.ads.googleads.v19.enums.types import AccessRoleEnum

# Assuming invite_user_with_access_role.py is in examples.account_management
from examples.account_management.invite_user_with_access_role import main as invite_user_main

class TestInviteUserWithAccessRole(unittest.TestCase):
    def setUp(self):
        # This patch will mock the GoogleAdsClient class in the module where it's imported.
        self.mock_google_ads_client_patcher = patch('examples.account_management.invite_user_with_access_role.GoogleAdsClient')
        self.mock_google_ads_client_class = self.mock_google_ads_client_patcher.start()
        
        # Configure the mock class's load_from_storage method to return an instance.
        self.mock_google_ads_client_instance = MagicMock(spec=GoogleAdsClient)
        self.mock_google_ads_client_class.load_from_storage.return_value = self.mock_google_ads_client_instance
        
        # Mock the service
        self.mock_invitation_service = MagicMock()
        self.mock_google_ads_client_instance.get_service.return_value = self.mock_invitation_service

        # Mock the enums as they would be accessed from the client instance
        # self.mock_google_ads_client_instance.enums.AccessRoleEnum
        mock_access_role_enum_type = MagicMock()
        
        # Dynamically create mock enum members (ADMIN, STANDARD, etc.)
        for role_name, role_value in AccessRoleEnum.AccessRole.items():
            mock_enum_member = MagicMock()
            mock_enum_member.value = role_value # The script might use .value or rely on the enum object itself
            setattr(mock_access_role_enum_type, role_name, mock_enum_member)
            
        self.mock_google_ads_client_instance.enums = MagicMock()
        self.mock_google_ads_client_instance.enums.AccessRoleEnum = mock_access_role_enum_type
        
        # Capture stdout
        self.held_stdout = sys.stdout
        sys.stdout = io.StringIO()

    def tearDown(self):
        sys.stdout = self.held_stdout # Restore stdout
        self.mock_google_ads_client_patcher.stop()

    def test_main_success(self):
        customer_id = "test_customer_123"
        email_address = "user@example.com"
        access_role_str = "ADMIN"
        # The actual enum value that should be used in the operation
        expected_access_role_enum_value = AccessRoleEnum.AccessRole.ADMIN

        # Mock the service response
        mock_mutate_response = MagicMock()
        mock_mutate_response.results = [MagicMock()]
        mock_mutate_response.results[0].resource_name = "customers/123/customerUserAccessInvitations/invitation_XYZ"
        self.mock_invitation_service.mutate_customer_user_access_invitation.return_value = mock_mutate_response

        invite_user_main(self.mock_google_ads_client_instance, customer_id, email_address, access_role_str)

        self.mock_google_ads_client_instance.get_service.assert_called_once_with("CustomerUserAccessInvitationService", version="v19")
        
        # Check the call to mutate_customer_user_access_invitation
        self.mock_invitation_service.mutate_customer_user_access_invitation.assert_called_once()
        call_args = self.mock_invitation_service.mutate_customer_user_access_invitation.call_args
        
        # Verify customer_id
        self.assertEqual(call_args[1]['customer_id'], customer_id) # kwargs access
        
        # Verify operation
        operation_arg = call_args[1]['operation'] # Assuming operation is passed as a kwarg
        self.assertIsInstance(operation_arg, CustomerUserAccessInvitationOperation)
        
        # Verify operation.create (CustomerUserAccessInvitation)
        invitation_payload = operation_arg.create
        self.assertIsInstance(invitation_payload, CustomerUserAccessInvitation)
        self.assertEqual(invitation_payload.email_address, email_address)
        self.assertEqual(invitation_payload.access_role, expected_access_role_enum_value)

        output = sys.stdout.getvalue()
        self.assertIn(
            f"Customer user access invitation with resource name 'customers/123/customerUserAccessInvitations/invitation_XYZ' was created for customer ID '{customer_id}' to email address '{email_address}' with access role '{access_role_str}'.",
            output
        )

    @patch('sys.exit') # To check if sys.exit is called
    def test_main_google_ads_exception(self, mock_sys_exit):
        customer_id = "test_customer_error"
        email_address = "error@example.com"
        access_role_str = "STANDARD"

        # Configure mutate_customer_user_access_invitation to raise GoogleAdsException
        mock_error_payload = MagicMock()
        mock_error_payload.message = "Test GoogleAdsException for invitation"
        mock_failure = MagicMock()
        mock_failure.errors = [mock_error_payload]
        
        google_ads_exception = GoogleAdsException(
            error=None, call=None, failure=mock_failure, error_code=None,
            message="Simulated GoogleAdsException during invitation mutation"
        )
        self.mock_invitation_service.mutate_customer_user_access_invitation.side_effect = google_ads_exception

        invite_user_main(self.mock_google_ads_client_instance, customer_id, email_address, access_role_str)

        mock_sys_exit.assert_called_once_with(1)
        output = sys.stdout.getvalue()
        
        self.assertIn("Request with ID", output) 
        self.assertIn("Test GoogleAdsException for invitation", output)
        
        self.mock_invitation_service.mutate_customer_user_access_invitation.assert_called_once()

    @patch('examples.account_management.invite_user_with_access_role.GoogleAdsClient')
    @patch('examples.account_management.invite_user_with_access_role.main')
    @patch('argparse.ArgumentParser.parse_args')
    def test_argument_parser(self, mock_parse_args, mock_script_main_function, mock_google_ads_client_class_for_script):
        # This mock_google_ads_client_class_for_script is for the GoogleAdsClient imported in the SCRIPT's global scope,
        # which is used by the choices=lambda in add_argument.
        
        # Mock the client instance that load_from_storage would return in the script's __main__
        mock_script_client_instance = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client_class_for_script.load_from_storage.return_value = mock_script_client_instance

        # Mock the enums on this script-level client instance
        mock_access_role_enum_type_for_script = MagicMock()
        for role_name, role_value in AccessRoleEnum.AccessRole.items():
            # The choices lambda in the script's parser does:
            # choice.upper() for choice in googleads_client.enums.AccessRoleEnum.AccessRole.keys()
            # So, we need .keys() to return a list of strings.
            pass # No need to mock individual enum members if .keys() is mocked directly.

        # Mock .keys() to return a list of strings like ['ADMIN', 'STANDARD', ...]
        mock_access_role_enum_type_for_script.AccessRole.keys.return_value = [
            role_name for role_name in AccessRoleEnum.AccessRole.keys()
        ]
        mock_script_client_instance.enums.AccessRoleEnum = mock_access_role_enum_type_for_script


        test_customer_id_cli = "cli_customer_id"
        test_email_cli = "cli_user@example.com"
        test_role_cli = "ADMIN" # This should be uppercase to match the choices

        sys.argv = [
            "invite_user_with_access_role.py",
            "-c", test_customer_id_cli,
            "-e", test_email_cli,
            "-a", test_role_cli,
        ]

        # Mock parse_args to return the specified arguments
        mock_parse_args.return_value = argparse.Namespace(
            customer_id=test_customer_id_cli,
            email_address=test_email_cli,
            access_role=test_role_cli 
        )
        
        # Execute the script's main block using runpy
        import runpy
        runpy.run_module("examples.account_management.invite_user_with_access_role", run_name="__main__")

        # Assert that GoogleAdsClient.load_from_storage was called by the script's __main__
        mock_google_ads_client_class_for_script.load_from_storage.assert_called_once()
        
        mock_parse_args.assert_called_once()
        
        # Assert that the script's main function (which is mocked by @patch) was called correctly
        # The script's __main__ block calls: main(client, args.customer_id, args.email_address, args.access_role)
        mock_script_main_function.assert_called_once_with(
            mock_script_client_instance, # The client loaded by the script's __main__
            test_customer_id_cli,
            test_email_cli,
            test_role_cli
        )

if __name__ == "__main__":
    unittest.main()
