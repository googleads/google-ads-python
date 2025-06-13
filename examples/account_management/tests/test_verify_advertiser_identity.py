import unittest
from unittest.mock import patch, MagicMock
import io
import sys

from examples.account_management import verify_advertiser_identity
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.v19.services.services.identity_verification_service import IdentityVerificationServiceClient
# Attempting to import IdentityVerification from services.types
from google.ads.googleads.v19.services.types import IdentityVerification
# Import Enums by their top-level type name for clarity in mocking
from google.ads.googleads.v19.enums.types.identity_verification_program_status import IdentityVerificationProgramStatusEnum as ActualIdentityVerificationProgramStatusEnumType
from google.ads.googleads.v19.enums.types.identity_verification_program import IdentityVerificationProgramEnum as ActualIdentityVerificationProgramEnumType

class TestVerifyAdvertiserIdentity(unittest.TestCase):

    @patch('examples.account_management.verify_advertiser_identity.GoogleAdsClient')
    def test_main_unspecified_starts_verification(self, mock_google_ads_client_class):
        # 1. Setup Mocks
        mock_client_instance = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client_class.load_from_storage.return_value = mock_client_instance

        mock_id_verification_service = MagicMock(spec=IdentityVerificationServiceClient)
        mock_client_instance.get_service.return_value = mock_id_verification_service

        # Mock client.enums
        mock_client_instance.enums = MagicMock()
        # The script uses client.enums.IdentityVerificationProgramStatusEnum.UNSPECIFIED etc.
        # So, IdentityVerificationProgramStatusEnum should point to the inner enum with members.
        mock_client_instance.enums.IdentityVerificationProgramStatusEnum = ActualIdentityVerificationProgramStatusEnumType.IdentityVerificationProgramStatus
        # The script uses client.enums.IdentityVerificationProgramEnum.ADVERTISER_IDENTITY_VERIFICATION
        mock_client_instance.enums.IdentityVerificationProgramEnum = ActualIdentityVerificationProgramEnumType.IdentityVerificationProgram


        # --- Mock responses for IdentityVerificationService ---
        customer_id = "customer123"
        deadline_time = "2024-12-31 23:59:59"

        # Response for the FIRST call to get_identity_verification
        mock_verification_response_1 = MagicMock()
        mock_id_verification_1 = MagicMock(spec=IdentityVerification)
        mock_id_verification_1.identity_verification_requirement = MagicMock() # Explicit mock
        mock_id_verification_1.identity_verification_requirement.verification_completion_deadline_time = deadline_time
        mock_id_verification_1.verification_progress = MagicMock() # Explicit mock
        mock_id_verification_1.verification_progress.program_status = ActualIdentityVerificationProgramStatusEnumType.IdentityVerificationProgramStatus.UNSPECIFIED
        mock_verification_response_1.identity_verification = [mock_id_verification_1]

        # Response for the SECOND call to get_identity_verification (after starting)
        mock_verification_response_2 = MagicMock()
        mock_id_verification_2 = MagicMock(spec=IdentityVerification)
        mock_id_verification_2.identity_verification_requirement = MagicMock() # Explicit mock
        mock_id_verification_2.identity_verification_requirement.verification_completion_deadline_time = deadline_time # Assume same deadline
        mock_id_verification_2.verification_progress = MagicMock() # Explicit mock
        mock_id_verification_2.verification_progress.program_status = ActualIdentityVerificationProgramStatusEnumType.IdentityVerificationProgramStatus.PENDING_USER_ACTION
        mock_id_verification_2.verification_progress.action_url = "http://example.com/verify"
        mock_id_verification_2.verification_progress.invitation_link_expiration_time = "2025-01-15 23:59:59"
        mock_verification_response_2.identity_verification = [mock_id_verification_2]

        # Configure side_effect for multiple calls to get_identity_verification
        mock_id_verification_service.get_identity_verification.side_effect = [
            mock_verification_response_1,
            mock_verification_response_2
        ]

        # start_identity_verification doesn't return anything the script uses
        mock_id_verification_service.start_identity_verification.return_value = None

        # 2. Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # 3. Call the main function
        verify_advertiser_identity.main(mock_client_instance, customer_id)

        # 4. Restore stdout
        sys.stdout = sys.__stdout__

        # 5. Assertions
        # Assert get_service was called for IdentityVerificationService (3 times in this path)
        self.assertEqual(mock_client_instance.get_service.call_count, 3)
        mock_client_instance.get_service.assert_called_with("IdentityVerificationService") # Check it was this service

        # Assert get_identity_verification calls
        self.assertEqual(mock_id_verification_service.get_identity_verification.call_count, 2)
        mock_id_verification_service.get_identity_verification.assert_any_call(customer_id=customer_id)

        # Assert start_identity_verification call
        mock_id_verification_service.start_identity_verification.assert_called_once_with(
            customer_id=customer_id,
            verification_program=ActualIdentityVerificationProgramEnumType.IdentityVerificationProgram.ADVERTISER_IDENTITY_VERIFICATION
        )

        # Verify printed output
        output = captured_output.getvalue()

        # Expected output from FIRST get_identity_verification call
        # Expected output from FIRST get_identity_verification call
        # Script prints the integer value of the enum for status
        expected_status_val_1 = ActualIdentityVerificationProgramStatusEnumType.IdentityVerificationProgramStatus.UNSPECIFIED.value
        expected_output_get_1 = (
            f"Account {customer_id} has a verification completion deadline "
            f"of {deadline_time} and status {expected_status_val_1} for advertiser identity "
            "verification.\n"
        )

        # Expected output from SECOND get_identity_verification call
        # Script prints the integer value of the enum for status
        expected_status_val_2 = ActualIdentityVerificationProgramStatusEnumType.IdentityVerificationProgramStatus.PENDING_USER_ACTION.value
        expected_output_get_2 = (
            f"Account {customer_id} has a verification completion deadline "
            f"of {deadline_time} and status {expected_status_val_2} for advertiser identity "
            "verification.\n"
        )

        self.assertIn(expected_output_get_1, output)
        self.assertIn(expected_output_get_2, output)

        # Ensure that the PENDING_USER_ACTION specific message from main() is NOT printed in this scenario
        self.assertNotIn("The URL for the verification process is:", output)


    @patch('examples.account_management.verify_advertiser_identity.GoogleAdsClient')
    def test_main_pending_user_action_prints_details(self, mock_google_ads_client_class):
        # Test the scenario where status is PENDING_USER_ACTION on the first call
        mock_client_instance = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client_class.load_from_storage.return_value = mock_client_instance
        mock_id_verification_service = MagicMock(spec=IdentityVerificationServiceClient)
        mock_client_instance.get_service.return_value = mock_id_verification_service
        mock_client_instance.enums = MagicMock()
        mock_client_instance.enums.IdentityVerificationProgramStatusEnum = ActualIdentityVerificationProgramStatusEnumType.IdentityVerificationProgramStatus

        customer_id = "customer456"
        deadline_time = "2024-11-30 23:59:59"
        action_url = "http://example.com/action"
        invitation_expiration = "2024-10-31 23:59:59"

        mock_response = MagicMock()
        mock_verification = MagicMock(spec=IdentityVerification)
        mock_verification.identity_verification_requirement = MagicMock() # Explicit mock
        mock_verification.identity_verification_requirement.verification_completion_deadline_time = deadline_time
        mock_verification.verification_progress = MagicMock() # Explicit mock
        mock_verification.verification_progress.program_status = ActualIdentityVerificationProgramStatusEnumType.IdentityVerificationProgramStatus.PENDING_USER_ACTION
        mock_verification.verification_progress.action_url = action_url
        mock_verification.verification_progress.invitation_link_expiration_time = invitation_expiration
        mock_response.identity_verification = [mock_verification]
        mock_id_verification_service.get_identity_verification.return_value = mock_response

        captured_output = io.StringIO()
        sys.stdout = captured_output
        verify_advertiser_identity.main(mock_client_instance, customer_id)
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Script prints the integer value of the enum for status
        expected_status_val_pending = ActualIdentityVerificationProgramStatusEnumType.IdentityVerificationProgramStatus.PENDING_USER_ACTION.value
        expected_output_get = (
            f"Account {customer_id} has a verification completion deadline "
            f"of {deadline_time} and status {expected_status_val_pending} for advertiser identity "
            "verification.\n"
        )
        expected_output_main_pending_details = (
            "There is an advertiser identity verification session in "
            "progress. The URL for the verification process is: "
            f"{action_url} and it will expire at "
            f"{invitation_expiration}.\n"
        )
        self.assertIn(expected_output_get, output)
        self.assertIn(expected_output_main_pending_details, output)
        # In this path, get_service is called once (inside get_identity_verification)
        mock_client_instance.get_service.assert_called_once_with("IdentityVerificationService")
        mock_id_verification_service.start_identity_verification.assert_not_called()

    # TODO: Add tests for PENDING_REVIEW, SUCCESS, and no initial verification (None returned)

if __name__ == "__main__":
    unittest.main()
