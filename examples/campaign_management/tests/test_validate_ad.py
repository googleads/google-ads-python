import unittest
from unittest import mock
import argparse
import sys

# Mock Google Ads Client and Exception if not available in the environment
try:
    from google.ads.googleads.client import GoogleAdsClient
    from google.ads.googleads.errors import GoogleAdsException
    # For PolicyFindingErrorEnum and other enums used in Ad creation
    from google.ads.googleads.v19.enums.types import (
        ad_group_ad_status as ad_group_ad_status_enum_types,
        ad_strength as ad_strength_enum_types,
        served_asset_field_type as served_asset_field_type_enum_types,
    )
    from google.ads.googleads.v19.errors.types import (
        policy_finding_error as policy_finding_error_types,
        ErrorCode as error_code_types,
        ErrorDetails as error_details_types,
    )

except ImportError:
    GoogleAdsClient = mock.MagicMock()
    GoogleAdsException = type('GoogleAdsException', (Exception,), {})
    # Mock enums and error types if not available
    ad_group_ad_status_enum_types = mock.MagicMock()
    ad_strength_enum_types = mock.MagicMock()
    served_asset_field_type_enum_types = mock.MagicMock()
    policy_finding_error_types = mock.MagicMock()
    policy_finding_error_types.PolicyFindingErrorEnum.PolicyFindingError.POLICY_FINDING = "POLICY_FINDING_MOCK"
    error_code_types = mock.MagicMock()
    error_details_types = mock.MagicMock()


# Import the module to be tested
from examples.campaign_management import validate_ad as va_script

class TestValidateAd(unittest.TestCase):

    @mock.patch.object(GoogleAdsClient, "load_from_storage")
    def setUp(self, mock_load_from_storage):
        self.mock_google_ads_client = mock.MagicMock(spec=GoogleAdsClient)
        self.mock_google_ads_client.configure_mock(version="v19")
        mock_load_from_storage.return_value = self.mock_google_ads_client

        self.mock_ad_group_service = mock.MagicMock()
        self.mock_ad_group_ad_service = mock.MagicMock()

        self.mock_google_ads_client.get_service.side_effect = lambda service_name, version="v19": {
            "AdGroupService": self.mock_ad_group_service,
            "AdGroupAdService": self.mock_ad_group_ad_service,
        }.get(service_name)

        # Mock path generation
        self.mock_ad_group_service.ad_group_path.side_effect = \
            lambda cid, agid: f"customers/{cid}/adGroups/{agid}"

        # Mock get_type for operations and various Ad components
        # This is quite involved due to the nested structure of the Ad
        def get_type_side_effect(type_name, version=None):
            mocked_type = mock.MagicMock()
            if type_name == "AdGroupAdOperation":
                mocked_type.create = mock.MagicMock() # AdGroupAd
                mocked_type.create.ad = mock.MagicMock() # Ad
                mocked_type.create.ad.responsive_search_ad = mock.MagicMock() # ResponsiveSearchAdInfo
                # Initialize lists for repeated fields
                mocked_type.create.ad.responsive_search_ad.headlines = []
                mocked_type.create.ad.responsive_search_ad.descriptions = []
                mocked_type.create.ad.final_urls = []
            elif type_name == "AdTextAsset":
                pass # Simple mock is fine
            # Add other types if the script uses client.get_type("...") for them
            return mocked_type

        self.mock_google_ads_client.get_type.side_effect = get_type_side_effect
        
        # Mock enums on the client instance (as used by the script)
        self.mock_google_ads_client.enums.AdGroupAdStatusEnum = ad_group_ad_status_enum_types.AdGroupAdStatusEnum
        self.mock_google_ads_client.enums.AdStrengthEnum = ad_strength_enum_types.AdStrengthEnum
        self.mock_google_ads_client.enums.ServedAssetFieldTypeEnum = served_asset_field_type_enum_types.ServedAssetFieldTypeEnum
        self.mock_google_ads_client.enums.PolicyFindingErrorEnum = policy_finding_error_types.PolicyFindingErrorEnum


        # Prepare mock GoogleAdsError for PolicyFindingError
        self.mock_policy_finding_error = mock.MagicMock(spec=error_code_types.GoogleAdsError)
        self.mock_policy_finding_error.error_code.policy_finding_error = policy_finding_error_types.PolicyFindingErrorEnum.PolicyFindingError.POLICY_FINDING
        
        mock_policy_topic_entry = mock.MagicMock()
        mock_policy_topic_entry.topic = "Test Policy Topic"
        mock_policy_topic_entry.type_.name = "PROHIBITED_CONTENT" # Example type
        
        self.mock_policy_finding_error.details.policy_finding_details.policy_topic_entries = [mock_policy_topic_entry]
        
        # Prepare mock GoogleAdsError for a non-policy finding error
        self.mock_other_error = mock.MagicMock(spec=error_code_types.GoogleAdsError)
        # Example: Using AuthenticationErrorEnum.AUTHENTICATION_ERROR
        # Need to ensure this enum path exists or mock it appropriately
        if hasattr(error_code_types, "AuthenticationErrorEnum"):
            self.mock_other_error.error_code.authentication_error = error_code_types.AuthenticationErrorEnum.AUTHENTICATION_ERROR
        else: # Fallback if AuthenticationErrorEnum is not directly on error_code_types
            self.mock_other_error.error_code.authentication_error = "AUTHENTICATION_ERROR_MOCK"

        self.mock_other_error.message = "Some other API error occurred"


    @mock.patch("argparse.ArgumentParser")
    @mock.patch("builtins.print")
    @mock.patch("sys.exit") # To prevent test runner from exiting
    def test_main_with_policy_finding_error(self, mock_sys_exit, mock_print, mock_argparse):
        customer_id = "123"
        ad_group_id = "456"
        mock_args = argparse.Namespace(customer_id=customer_id, ad_group_id=ad_group_id)
        mock_argparse.return_value.parse_args.return_value = mock_args

        ad_group_resource_name = f"customers/{customer_id}/adGroups/{ad_group_id}"
        self.mock_ad_group_service.ad_group_path.return_value = ad_group_resource_name

        # Configure mutate_ad_group_ads to raise GoogleAdsException with policy finding
        mock_failure = mock.MagicMock(spec=error_code_types.GoogleAdsFailure)
        mock_failure.errors = [self.mock_policy_finding_error]
        
        policy_exception = GoogleAdsException(
            error=mock_failure,
            call=mock.MagicMock(), # Mock the gRPC call object
            message="Policy finding error occurred",
            errors=[self.mock_policy_finding_error] # Pass errors here too
        )
        policy_exception._failure = mock_failure # Set the _failure attribute

        self.mock_ad_group_ad_service.mutate_ad_group_ads.side_effect = policy_exception

        va_script.main(self.mock_google_ads_client, customer_id, ad_group_id)

        self.mock_google_ads_client.get_service.assert_any_call("AdGroupService", version="v19")
        self.mock_google_ads_client.get_service.assert_any_call("AdGroupAdService", version="v19")
        self.mock_ad_group_service.ad_group_path.assert_called_once_with(customer_id, ad_group_id)

        self.mock_ad_group_ad_service.mutate_ad_group_ads.assert_called_once()
        call_args = self.mock_ad_group_ad_service.mutate_ad_group_ads.call_args
        request_arg = call_args[1]['request']
        self.assertEqual(request_arg.customer_id, customer_id)
        self.assertTrue(request_arg.validate_only)
        self.assertFalse(request_arg.partial_failure) # As per script
        
        self.assertEqual(len(request_arg.operations), 1)
        ad_group_ad_op = request_arg.operations[0].create
        self.assertEqual(ad_group_ad_op.ad_group, ad_group_resource_name)
        self.assertEqual(ad_group_ad_op.status, self.mock_google_ads_client.enums.AdGroupAdStatusEnum.PAUSED)
        
        # Check ad details (ResponsiveSearchAd)
        rsa_info = ad_group_ad_op.ad.responsive_search_ad
        self.assertEqual(len(rsa_info.headlines), 3) # As per script
        self.assertEqual(rsa_info.headlines[0].text, "Cruise to Mars #1")
        self.assertEqual(rsa_info.headlines[0].pinned_field, self.mock_google_ads_client.enums.ServedAssetFieldTypeEnum.HEADLINE_1)
        self.assertEqual(len(rsa_info.descriptions), 2)
        self.assertEqual(rsa_info.descriptions[0].text, "Best Space Cruise Line")
        self.assertEqual(ad_group_ad_op.ad.final_urls[0], "http://www.example.com")


        # Assert print statements for policy findings
        mock_print.assert_any_call("Ad validation failed due to policy findings.")
        mock_print.assert_any_call(
            "\tPolicy topic entry with topic 'Test Policy Topic' and type "
            "'PROHIBITED_CONTENT' was found."
        )
        # sys.exit should not be called for policy finding errors as per script logic
        mock_sys_exit.assert_not_called()


    @mock.patch("argparse.ArgumentParser")
    @mock.patch("builtins.print")
    @mock.patch("sys.exit")
    def test_main_with_other_google_ads_exception(self, mock_sys_exit, mock_print, mock_argparse):
        customer_id = "123"
        ad_group_id = "457" # Different ad_group_id for a new call
        mock_args = argparse.Namespace(customer_id=customer_id, ad_group_id=ad_group_id)
        mock_argparse.return_value.parse_args.return_value = mock_args

        # Configure mutate_ad_group_ads to raise GoogleAdsException with other error
        mock_failure = mock.MagicMock(spec=error_code_types.GoogleAdsFailure)
        mock_failure.errors = [self.mock_other_error]

        other_exception = GoogleAdsException(
            error=mock_failure,
            call=mock.MagicMock(),
            message="Other API error",
            errors=[self.mock_other_error]
        )
        other_exception._failure = mock_failure
        other_exception.request_id = "test_req_id_other_error"


        self.mock_ad_group_ad_service.mutate_ad_group_ads.side_effect = other_exception

        va_script.main(self.mock_google_ads_client, customer_id, ad_group_id)

        # Assert print statements for the other error
        printed_error = False
        for call in mock_print.call_args_list:
            if "Some other API error occurred" in str(call[0]) and "ErrorCode" in str(call[0]): # Check for message and standard error printing
                printed_error = True
                break
        self.assertTrue(printed_error, "Non-policy GoogleAdsException error message was not printed correctly.")
        mock_sys_exit.assert_called_once_with(1)


    @mock.patch("argparse.ArgumentParser")
    @mock.patch("builtins.print")
    @mock.patch("sys.exit")
    def test_main_no_exception_from_mutate(self, mock_sys_exit, mock_print, mock_argparse):
        customer_id = "123"
        ad_group_id = "458"
        mock_args = argparse.Namespace(customer_id=customer_id, ad_group_id=ad_group_id)
        mock_argparse.return_value.parse_args.return_value = mock_args

        # Configure mutate_ad_group_ads to NOT raise an exception
        # This implies a successful validate_only call, meaning no policy violations found
        # or the API behaved in an unexpected way for validate_only=True.
        mock_mutate_response = mock.MagicMock() # A typical response object
        mock_mutate_response.results = [] # Usually empty for validate_only
        self.mock_ad_group_ad_service.mutate_ad_group_ads.return_value = mock_mutate_response

        va_script.main(self.mock_google_ads_client, customer_id, ad_group_id)

        # The script's current logic: if no GoogleAdsException, it prints "Ad validated successfully"
        mock_print.assert_any_call(
            "Ad validated successfully and can be saved."
        )
        mock_sys_exit.assert_not_called()


if __name__ == "__main__":
    unittest.main()
