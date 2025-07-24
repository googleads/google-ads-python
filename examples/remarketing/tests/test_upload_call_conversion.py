import unittest
from unittest.mock import patch, Mock, call, ANY
import io
import sys
from types import SimpleNamespace

# SUT (System Under Test)
from examples.remarketing import upload_call_conversion

class TestUploadCallConversionMain(unittest.TestCase):

    def setUp(self):
        self.mock_client = Mock(name="GoogleAdsClient")
        self.test_customer_id = "dummy_customer_id"
        self.test_conversion_action_id = "dummy_conv_action_id"
        self.test_caller_id = "+12345678900"
        self.test_call_start_date_time = "2023-01-01 12:00:00+00:00"
        self.test_conversion_date_time = "2023-01-01 12:05:00+00:00"
        self.test_conversion_value = 25.50

        self.mock_consent_status_enum_dict = {
            "GRANTED": "MOCK_CONSENT_GRANTED_ENUM_VAL",
            "DENIED": "MOCK_CONSENT_DENIED_ENUM_VAL",
            "UNSPECIFIED": "MOCK_CONSENT_UNSPECIFIED_ENUM_VAL"
        }
        self.mock_client.enums = SimpleNamespace(
            ConsentStatusEnum=self.mock_consent_status_enum_dict
        )

        self.mock_conversion_upload_service = Mock(name="ConversionUploadService")
        self.mock_conversion_action_service = Mock(name="ConversionActionService")

        def get_service_side_effect(service_name):
            if service_name == "ConversionUploadService":
                return self.mock_conversion_upload_service
            elif service_name == "ConversionActionService":
                return self.mock_conversion_action_service
            return Mock(name=f"UnknownService_{service_name}")
        self.mock_client.get_service.side_effect = get_service_side_effect

        self.mock_conversion_action_service.conversion_action_path.return_value = \
            f"customers/{self.test_customer_id}/conversionActions/{self.test_conversion_action_id}_mock_path"

        self.mock_upload_response = Mock(name="UploadCallConversionsResponse")
        self.mock_uploaded_conversion_result = Mock(name="UploadedCallConversion")

        self.mock_call_conversion_obj = Mock(name="CallConversionInstance")
        self.mock_custom_variable_obj = Mock(name="CustomVariableInstance")
        self.mock_upload_request_obj = Mock(name="UploadCallConversionsRequestInstance")

        def get_type_side_effect(type_name):
            if type_name == "CallConversion":
                self.mock_call_conversion_obj.custom_variables = []
                self.mock_call_conversion_obj.consent = Mock(
                    name="ConsentInstance_Reset", ad_user_data=None, ad_personalization=None
                )
                for attr in ["conversion_action", "caller_id", "call_start_date_time",
                             "conversion_date_time", "conversion_value", "currency_code"]:
                    setattr(self.mock_call_conversion_obj, attr, None)
                return self.mock_call_conversion_obj
            elif type_name == "CustomVariable":
                self.mock_custom_variable_obj.conversion_custom_variable = None
                self.mock_custom_variable_obj.value = None
                return self.mock_custom_variable_obj
            elif type_name == "UploadCallConversionsRequest":
                self.mock_upload_request_obj.customer_id = None
                self.mock_upload_request_obj.conversions = []
                self.mock_upload_request_obj.partial_failure = None
                return self.mock_upload_request_obj
            return Mock(name=f"DefaultMock_{type_name}")
        self.mock_client.get_type.side_effect = get_type_side_effect

    def _configure_default_success_response(self):
        self.mock_upload_response.partial_failure_error = None
        self.mock_uploaded_conversion_result.conversion_action = self.mock_conversion_action_service.conversion_action_path.return_value
        self.mock_uploaded_conversion_result.call_start_date_time = self.test_call_start_date_time
        self.mock_uploaded_conversion_result.caller_id = self.test_caller_id
        self.mock_upload_response.results = [self.mock_uploaded_conversion_result]
        self.mock_conversion_upload_service.upload_call_conversions.return_value = self.mock_upload_response

    def _common_asserts_basic_conversion(self):
        self.mock_conversion_action_service.conversion_action_path.assert_called_once_with(
            self.test_customer_id, self.test_conversion_action_id
        )
        self.mock_client.get_type.assert_any_call("CallConversion")
        self.mock_client.get_type.assert_any_call("UploadCallConversionsRequest")

        cc = self.mock_call_conversion_obj
        self.assertEqual(cc.conversion_action, self.mock_conversion_action_service.conversion_action_path.return_value)
        self.assertEqual(cc.caller_id, self.test_caller_id)
        self.assertEqual(cc.call_start_date_time, self.test_call_start_date_time)
        self.assertEqual(cc.conversion_date_time, self.test_conversion_date_time)
        self.assertEqual(cc.conversion_value, self.test_conversion_value)
        self.assertEqual(cc.currency_code, "USD")

        req = self.mock_upload_request_obj
        self.assertEqual(req.customer_id, self.test_customer_id)
        self.assertIn(self.mock_call_conversion_obj, req.conversions)
        self.assertEqual(len(req.conversions), 1)
        self.assertTrue(req.partial_failure)

        self.mock_conversion_upload_service.upload_call_conversions.assert_called_once_with(
            request=self.mock_upload_request_obj
        )

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_basic_success(self, mock_stdout):
        self._configure_default_success_response()
        upload_call_conversion.main(
            self.mock_client, self.test_customer_id, self.test_conversion_action_id,
            self.test_caller_id, self.test_call_start_date_time, self.test_conversion_date_time,
            self.test_conversion_value, None, None, None
        )
        self._common_asserts_basic_conversion()
        self.assertEqual(len(self.mock_call_conversion_obj.custom_variables), 0)
        self.assertIsNone(self.mock_call_conversion_obj.consent.ad_user_data)
        expected_msg_fragment = (
            f"Uploaded call conversion that occurred at '{self.test_call_start_date_time}' "
            f"for caller ID '{self.test_caller_id}' "
            f"to the conversion action with resource name '{self.mock_uploaded_conversion_result.conversion_action}'."
        )
        self.assertIn(expected_msg_fragment, mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_with_custom_variable(self, mock_stdout):
        self._configure_default_success_response()
        custom_var_id = "cv_id_123"
        custom_var_value = "cv_val_abc"
        upload_call_conversion.main(
            self.mock_client, self.test_customer_id, self.test_conversion_action_id,
            self.test_caller_id, self.test_call_start_date_time, self.test_conversion_date_time,
            self.test_conversion_value, custom_var_id, custom_var_value, None
        )
        self._common_asserts_basic_conversion()
        self.mock_client.get_type.assert_any_call("CustomVariable")
        self.assertEqual(len(self.mock_call_conversion_obj.custom_variables), 1)
        custom_var_mock_in_list = self.mock_call_conversion_obj.custom_variables[0]
        self.assertEqual(custom_var_mock_in_list, self.mock_custom_variable_obj) # Check it's the one from get_type
        self.assertEqual(self.mock_custom_variable_obj.conversion_custom_variable, custom_var_id)
        self.assertEqual(self.mock_custom_variable_obj.value, custom_var_value)
        self.assertIsNone(self.mock_call_conversion_obj.consent.ad_user_data)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_with_ad_user_data_consent(self, mock_stdout):
        self._configure_default_success_response()
        upload_call_conversion.main(
            self.mock_client, self.test_customer_id, self.test_conversion_action_id,
            self.test_caller_id, self.test_call_start_date_time, self.test_conversion_date_time,
            self.test_conversion_value, None, None, "GRANTED"
        )
        self._common_asserts_basic_conversion()
        self.assertEqual(self.mock_call_conversion_obj.consent.ad_user_data, "MOCK_CONSENT_GRANTED_ENUM_VAL")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_with_partial_failure(self, mock_stdout):
        self._configure_default_success_response() # Base success response
        self.mock_upload_response.partial_failure_error = Mock(message="Partial failure test message.")

        upload_call_conversion.main(
            self.mock_client, self.test_customer_id, self.test_conversion_action_id,
            self.test_caller_id, self.test_call_start_date_time, self.test_conversion_date_time,
            self.test_conversion_value, None, None, None
        )
        self._common_asserts_basic_conversion() # SUT still processes results after partial failure
        self.assertIn("Partial error occurred: 'Partial failure test message.'", mock_stdout.getvalue())
        # Check success message is also printed
        expected_success_msg_fragment = (
            f"Uploaded call conversion that occurred at '{self.test_call_start_date_time}'"
        )
        self.assertIn(expected_success_msg_fragment, mock_stdout.getvalue())


    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_result_indicates_failure(self, mock_stdout):
        self._configure_default_success_response() # Base success response
        self.mock_uploaded_conversion_result.call_start_date_time = None # Simulate failed upload for this result

        upload_call_conversion.main(
            self.mock_client, self.test_customer_id, self.test_conversion_action_id,
            self.test_caller_id, self.test_call_start_date_time, self.test_conversion_date_time,
            self.test_conversion_value, None, None, None
        )
        self._common_asserts_basic_conversion()
        # The success message relies on call_start_date_time being present on the result.
        # SUT: if uploaded_call_conversion.call_start_date_time: print(...)
        unexpected_success_msg_fragment = (
            f"Uploaded call conversion that occurred at"
        ) # Don't include the value as it would be None
        self.assertNotIn(unexpected_success_msg_fragment, mock_stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
