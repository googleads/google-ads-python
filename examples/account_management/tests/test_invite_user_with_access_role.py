import unittest
from unittest.mock import patch, MagicMock
import io
import sys

from examples.account_management import invite_user_with_access_role
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.v19.services.services.customer_user_access_invitation_service import CustomerUserAccessInvitationServiceClient
from google.ads.googleads.v19.resources.types.customer_user_access_invitation import CustomerUserAccessInvitation
from google.ads.googleads.v19.enums.types.access_role import AccessRoleEnum

class TestInviteUserWithAccessRole(unittest.TestCase):

    @patch('examples.account_management.invite_user_with_access_role.GoogleAdsClient')
    def test_main_invites_user_correctly(self, mock_google_ads_client_class):
        # 1. Setup Mocks
        mock_client_instance = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client_class.load_from_storage.return_value = mock_client_instance

        mock_invitation_service = MagicMock(spec=CustomerUserAccessInvitationServiceClient)
        mock_client_instance.get_service.return_value = mock_invitation_service

        # Mock client.get_type calls
        # The script calls get_type("CustomerUserAccessInvitationOperation")
        # and then sets attributes on operation.create
        mock_operation = MagicMock() # This will be invitation_operation
        # mock_operation.create will be implicitly created as a MagicMock by attribute access in script

        def get_type_side_effect(type_name):
            if type_name == "CustomerUserAccessInvitationOperation":
                return mock_operation
            # No explicit call to get_type("CustomerUserAccessInvitation") in the script's main path
            raise ValueError(f"Unexpected type requested by script: {type_name}")

        mock_client_instance.get_type.side_effect = get_type_side_effect

        # Mock client.enums.AccessRoleEnum for role lookup
        mock_admin_enum_member = MagicMock()
        mock_admin_enum_member.value = AccessRoleEnum.AccessRole.ADMIN.value # Actual int value

        mock_client_instance.enums = MagicMock()
        # The script does client.enums.AccessRoleEnum[access_role_str]
        mock_access_role_enum_dict = {"ADMIN": mock_admin_enum_member}
        mock_client_instance.enums.AccessRoleEnum = mock_access_role_enum_dict

        # Mock the response from mutate_customer_user_access_invitation
        mock_mutate_response = MagicMock()
        # Script accesses response.result.resource_name
        mock_mutate_response.result = MagicMock()
        mock_mutate_response.result.resource_name = "customers/123/customerUserAccessInvitations/456"
        mock_invitation_service.mutate_customer_user_access_invitation.return_value = mock_mutate_response

        # 2. Prepare arguments for main function
        customer_id = "test_customer_123"
        email_address = "test@example.com"
        access_role_str_upper = "ADMIN" # Script uses this for lookup client.enums.AccessRoleEnum[access_role]
        expected_access_role_int_value = AccessRoleEnum.AccessRole.ADMIN.value


        # 3. Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # 4. Call the main function
        invite_user_with_access_role.main(
            mock_client_instance,
            customer_id,
            email_address,
            access_role_str_upper
        )

        # 5. Restore stdout
        sys.stdout = sys.__stdout__

        # 6. Assertions
        # Assert get_service was called
        mock_client_instance.get_service.assert_called_once_with("CustomerUserAccessInvitationService")

        # Assert get_type was called for "CustomerUserAccessInvitationOperation"
        mock_client_instance.get_type.assert_called_once_with("CustomerUserAccessInvitationOperation")
        # No direct call to get_type("CustomerUserAccessInvitation") in the script's logic for .create

        # Assert mutate_customer_user_access_invitation was called
        mock_invitation_service.mutate_customer_user_access_invitation.assert_called_once()

        # Get the call arguments for mutate
        call_args = mock_invitation_service.mutate_customer_user_access_invitation.call_args
        actual_customer_id_arg = call_args.kwargs.get('customer_id')
        # The operation passed to mutate is the mock_operation itself
        actual_operation_arg = call_args.kwargs.get('operation')

        self.assertEqual(actual_customer_id_arg, customer_id)
        self.assertEqual(actual_operation_arg, mock_operation) # Ensure the correct operation object was passed

        # Verify the attributes of mock_operation.create (which is where the script sets them)
        self.assertEqual(mock_operation.create.email_address, email_address)
        self.assertEqual(mock_operation.create.access_role, expected_access_role_int_value)

        # Verify printed output
        expected_output = (
            f"Customer user access invitation was sent for "
            f"customer ID: '{customer_id}', "
            f"email address {email_address}, and "
            f"access role {access_role_str_upper}. The invitation resource name is: "
            f"{mock_mutate_response.result.resource_name}\n"
        )
        self.assertEqual(captured_output.getvalue(), expected_output)

if __name__ == "__main__":
    unittest.main()
