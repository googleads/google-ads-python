import unittest
from unittest import mock
import argparse
import sys

# Mock Google Ads Client and Exception if not available in the environment
try:
    from google.ads.googleads.client import GoogleAdsClient
    from google.ads.googleads.errors import GoogleAdsException
except ImportError:
    GoogleAdsClient = mock.MagicMock()
    GoogleAdsException = type('GoogleAdsException', (Exception,), {})

# Import the module to be tested
from examples.campaign_management import set_ad_parameters as sap_script

class TestSetAdParameters(unittest.TestCase):

    @mock.patch.object(GoogleAdsClient, "load_from_storage")
    def setUp(self, mock_load_from_storage):
        self.mock_google_ads_client = mock.MagicMock(spec=GoogleAdsClient)
        self.mock_google_ads_client.configure_mock(version="v19")
        mock_load_from_storage.return_value = self.mock_google_ads_client

        self.mock_ad_group_criterion_service = mock.MagicMock()
        self.mock_ad_parameter_service = mock.MagicMock()

        self.mock_google_ads_client.get_service.side_effect = lambda service_name, version="v19": {
            "AdGroupCriterionService": self.mock_ad_group_criterion_service,
            "AdParameterService": self.mock_ad_parameter_service,
        }.get(service_name)

        # Mock path generation
        self.mock_ad_group_criterion_service.ad_group_criterion_path.side_effect = \
            lambda cid, agid, critid: f"customers/{cid}/adGroupCriteria/{agid}~{critid}"

        # Mock get_type for operations
        self.mock_ad_parameter_op = mock.MagicMock()
        self.mock_google_ads_client.get_type.return_value = self.mock_ad_parameter_op
        
        # Mock AdParameter for direct attribute assignment in script
        self.mock_ad_parameter_instance = mock.MagicMock()
        # When script does: ad_parameter = client.get_type("AdParameter")
        # then ad_parameter.ad_group_criterion = ..., etc.
        # We need get_type("AdParameterOperation").create (which is an AdParameter) to be configurable.
        # So, when get_type("AdParameterOperation") is called, its .create attribute should be this mock_ad_parameter_instance
        
        def get_type_side_effect(type_name, version=None):
            if type_name == "AdParameterOperation":
                # The script does: operation = client.get_type("AdParameterOperation")
                # operation.create.xyz = ...
                # So, operation.create should be a configurable mock.
                op_mock = mock.MagicMock()
                op_mock.create = mock.MagicMock() # This will be the AdParameter instance
                return op_mock
            elif type_name == "AdParameter": # Though script doesn't call get_type("AdParameter")
                 return mock.MagicMock() 
            return mock.MagicMock() # Default for other types if any

        self.mock_google_ads_client.get_type.side_effect = get_type_side_effect


    # The script doesn't have a separate create_ad_parameter helper function.
    # The logic is directly in main. So we will test that logic within test_main_success.

    @mock.patch("argparse.ArgumentParser")
    @mock.patch("builtins.print")
    def test_main_success(self, mock_print, mock_argparse):
        customer_id = "123"
        ad_group_id = "456"
        criterion_id = "789"
        mock_args = argparse.Namespace(
            customer_id=customer_id, ad_group_id=ad_group_id, criterion_id=criterion_id
        )
        mock_argparse.return_value.parse_args.return_value = mock_args

        ad_group_criterion_resource_name = f"customers/{customer_id}/adGroupCriteria/{ad_group_id}~{criterion_id}"
        self.mock_ad_group_criterion_service.ad_group_criterion_path.return_value = ad_group_criterion_resource_name

        # Mock response for mutate_ad_parameters
        mock_mutate_response = mock.MagicMock()
        mock_result1 = mock.MagicMock()
        mock_result1.resource_name = f"{ad_group_criterion_resource_name}/adParameters/1"
        mock_result2 = mock.MagicMock()
        mock_result2.resource_name = f"{ad_group_criterion_resource_name}/adParameters/2"
        mock_mutate_response.results = [mock_result1, mock_result2]
        self.mock_ad_parameter_service.mutate_ad_parameters.return_value = mock_mutate_response

        sap_script.main(
            self.mock_google_ads_client, customer_id, ad_group_id, criterion_id
        )

        self.mock_google_ads_client.get_service.assert_any_call("AdGroupCriterionService", version="v19")
        self.mock_google_ads_client.get_service.assert_any_call("AdParameterService", version="v19")

        self.mock_ad_group_criterion_service.ad_group_criterion_path.assert_called_once_with(
            customer_id, ad_group_id, criterion_id
        )

        self.mock_ad_parameter_service.mutate_ad_parameters.assert_called_once()
        call_args = self.mock_ad_parameter_service.mutate_ad_parameters.call_args
        self.assertEqual(call_args[1]['customer_id'], customer_id)
        
        operations = call_args[1]['operations']
        self.assertEqual(len(operations), 2)

        # Check operation 1 (parameter_index=1)
        op1_create = operations[0].create # This is the AdParameter mock
        self.assertEqual(op1_create.ad_group_criterion, ad_group_criterion_resource_name)
        self.assertEqual(op1_create.parameter_index, 1)
        self.assertEqual(op1_create.insertion_text, "100")

        # Check operation 2 (parameter_index=2)
        op2_create = operations[1].create
        self.assertEqual(op2_create.ad_group_criterion, ad_group_criterion_resource_name)
        self.assertEqual(op2_create.parameter_index, 2)
        self.assertEqual(op2_create.insertion_text, "$10") # From script: f"${10 * float(ad_group_id) / float(criterion_id)}"
                                                        # Using fixed value for simplicity, as ad_group_id/criterion_id can be varied.
                                                        # Let's use the script's logic for a more robust test.
        expected_insertion_text_param2 = f"${10 * float(ad_group_id) / float(criterion_id):.2f}"
        self.assertEqual(op2_create.insertion_text, expected_insertion_text_param2)


        mock_print.assert_any_call(
            f"Created ad parameter with resource name: '{mock_result1.resource_name}'"
        )
        mock_print.assert_any_call(
            f"Created ad parameter with resource name: '{mock_result2.resource_name}'"
        )

    @mock.patch("argparse.ArgumentParser")
    @mock.patch("builtins.print")
    @mock.patch("sys.exit")
    def test_main_google_ads_exception(self, mock_sys_exit, mock_print, mock_argparse):
        customer_id = "123"
        ad_group_id = "456"
        criterion_id = "789"
        mock_args = argparse.Namespace(
            customer_id=customer_id, ad_group_id=ad_group_id, criterion_id=criterion_id
        )
        mock_argparse.return_value.parse_args.return_value = mock_args
        
        ad_group_criterion_resource_name = f"customers/{customer_id}/adGroupCriteria/{ad_group_id}~{criterion_id}"
        self.mock_ad_group_criterion_service.ad_group_criterion_path.return_value = ad_group_criterion_resource_name


        # Create a mock GoogleAdsException instance
        mock_failure = mock.MagicMock()
        mock_error = mock.MagicMock()
        mock_error.message = "Test AdParameter Mutate Error"
        mock_failure.errors = [mock_error]
        google_ads_exception_instance = GoogleAdsException()
        google_ads_exception_instance._failure = mock_failure
        google_ads_exception_instance.request_id = "test_adparam_req_id"

        self.mock_ad_parameter_service.mutate_ad_parameters.side_effect = google_ads_exception_instance

        sap_script.main(
            self.mock_google_ads_client, customer_id, ad_group_id, criterion_id
        )

        printed_error = False
        for call in mock_print.call_args_list:
            if "Test AdParameter Mutate Error" in str(call[0]) and "ErrorCode" in str(call[0]):
                printed_error = True
                break
        self.assertTrue(printed_error, "GoogleAdsException error message was not printed correctly.")
        mock_sys_exit.assert_called_once_with(1)

if __name__ == "__main__":
    unittest.main()
