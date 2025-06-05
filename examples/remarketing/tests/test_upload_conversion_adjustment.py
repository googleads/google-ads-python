import unittest
from unittest.mock import patch, Mock, call, ANY
import io
import sys
from types import SimpleNamespace

# Add the project root to sys.path to allow for relative imports
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))


# SUT (System Under Test)
from examples.remarketing import upload_conversion_adjustment

class TestUploadConversionAdjustmentMain(unittest.TestCase):

    # Inner class to serve as the mock type for GoogleAdsFailure
    class MockGoogleAdsFailureForTest(object):
        deserialize = None # Will be replaced by a Mock instance

    # Simple placeholder class for the instance returned by get_type("GoogleAdsFailure")
    class PlainFailureMessagePlaceholder(object):
        pass

    def setUp(self):
        self.mock_client = Mock(name="GoogleAdsClient")
        self.test_customer_id = "dummy_customer_id"
        self.test_conversion_action_id = "dummy_conv_action_id"
        self.test_order_id = "test_order_id_123"
        self.test_adjustment_date_time = "2023-01-15 10:00:00+00:00"

        self.mock_restatement_enum_member = Mock(value=1, name="RESTATEMENT")
        self.mock_retraction_enum_member = Mock(value=2, name="RETRACTION")

        mock_ca_type_enum_main_mock = Mock(name="ConversionAdjustmentTypeEnum_MainMock")
        mock_ca_type_enum_main_mock.RESTATEMENT = self.mock_restatement_enum_member
        mock_ca_type_enum_main_mock.RETRACTION = self.mock_retraction_enum_member

        def cat_getitem_side_effect(key):
            if key == "RESTATEMENT": return self.mock_restatement_enum_member
            if key == "RETRACTION": return self.mock_retraction_enum_member
            raise KeyError(key)
        mock_ca_type_enum_main_mock.__getitem__ = Mock(side_effect=cat_getitem_side_effect)

        self.mock_consent_status_enum_dict = {
            "GRANTED": "MOCK_CONSENT_GRANTED_ENUM_VAL",
            "DENIED": "MOCK_CONSENT_DENIED_ENUM_VAL",
            "UNSPECIFIED": "MOCK_CONSENT_UNSPECIFIED_ENUM_VAL"
        }
        self.mock_client.enums = SimpleNamespace(
            ConversionAdjustmentTypeEnum=mock_ca_type_enum_main_mock,
            ConsentStatusEnum=self.mock_consent_status_enum_dict
        )

        self.mock_adjustment_upload_service = Mock(name="ConversionAdjustmentUploadService")
        self.mock_conversion_action_service = Mock(name="ConversionActionService")

        def get_service_side_effect(service_name):
            if service_name == "ConversionAdjustmentUploadService":
                return self.mock_adjustment_upload_service
            elif service_name == "ConversionActionService":
                return self.mock_conversion_action_service
            return Mock(name=f"UnknownService_{service_name}")
        self.mock_client.get_service.side_effect = get_service_side_effect

        self.mock_conversion_action_service.conversion_action_path.return_value = \
            f"customers/{self.test_customer_id}/conversionActions/{self.test_conversion_action_id}_mock_path"

        self.mock_upload_response = Mock(name="UploadConversionAdjustmentsResponse")
        self.mock_adjustment_result = Mock(name="ConversionAdjustmentResult")

        self.mock_conversion_adjustment_obj = Mock(name="ConversionAdjustmentInstance")
        self.mock_restatement_value_obj = Mock(name="RestatementValueInstance")
        self.mock_conversion_adjustment_obj.restatement_value = self.mock_restatement_value_obj

        self.mock_upload_request_obj = Mock(name="UploadConversionAdjustmentsRequestInstance")

        # --- Setup for GoogleAdsFailure mocking using __class__ ---
        self.parsed_failure_object_mock = Mock(name="ParsedFailureObject_Global")
        TestUploadConversionAdjustmentMain.MockGoogleAdsFailureForTest.deserialize = Mock(
            return_value=self.parsed_failure_object_mock
        )

        # Use an instance of the plain placeholder class
        self.plain_failure_message_instance = TestUploadConversionAdjustmentMain.PlainFailureMessagePlaceholder()
        # Assign its __class__ to our mock type
        self.plain_failure_message_instance.__class__ = TestUploadConversionAdjustmentMain.MockGoogleAdsFailureForTest
        # --- End setup ---

        def get_type_side_effect(type_name):
            if type_name == "ConversionAdjustment":
                for attr in ["conversion_action", "adjustment_type", "adjustment_date_time", "order_id"]:
                    setattr(self.mock_conversion_adjustment_obj, attr, None)
                self.mock_restatement_value_obj.adjusted_value = None
                self.mock_restatement_value_obj.currency_code = None
                self.mock_conversion_adjustment_obj.restatement_value = self.mock_restatement_value_obj
                return self.mock_conversion_adjustment_obj
            elif type_name == "UploadConversionAdjustmentsRequest":
                self.mock_upload_request_obj.customer_id = None
                self.mock_upload_request_obj.conversion_adjustments = []
                self.mock_upload_request_obj.partial_failure = None
                return self.mock_upload_request_obj
            elif type_name == "GoogleAdsFailure":
                # Return the instance of PlainFailureMessagePlaceholder
                return self.plain_failure_message_instance
            return Mock(name=f"DefaultMock_{type_name}")
        self.mock_client.get_type.side_effect = get_type_side_effect

    def _configure_successful_response(self, adjustment_type_enum_member):
        self.mock_upload_response.partial_failure_error = Mock(details=None, name="NoErrorPartialFailureMock")
        self.mock_upload_response.partial_failure_error.error_details = []
        self.mock_adjustment_result.conversion_action = self.mock_conversion_action_service.conversion_action_path.return_value
        self.mock_adjustment_result.adjustment_type = adjustment_type_enum_member
        self.mock_adjustment_result.adjustment_date_time = self.test_adjustment_date_time
        self.mock_adjustment_result.order_id = self.test_order_id

        self.mock_upload_response.results = [self.mock_adjustment_result]
        self.mock_adjustment_upload_service.upload_conversion_adjustments.return_value = self.mock_upload_response

    def _common_asserts_basic_adjustment(self, adjustment_type_enum_member):
        self.mock_conversion_action_service.conversion_action_path.assert_called_once_with(
            self.test_customer_id, self.test_conversion_action_id
        )
        self.mock_client.get_type.assert_any_call("ConversionAdjustment")
        self.mock_client.get_type.assert_any_call("UploadConversionAdjustmentsRequest")

        adj = self.mock_conversion_adjustment_obj
        self.assertEqual(adj.conversion_action, self.mock_conversion_action_service.conversion_action_path.return_value)
        self.assertEqual(adj.adjustment_type, adjustment_type_enum_member.value)
        self.assertEqual(adj.adjustment_date_time, self.test_adjustment_date_time)
        self.assertEqual(adj.order_id, self.test_order_id)

        req = self.mock_upload_request_obj
        self.assertEqual(req.customer_id, self.test_customer_id)
        self.assertIn(self.mock_conversion_adjustment_obj, req.conversion_adjustments)
        self.assertEqual(len(req.conversion_adjustments), 1)
        self.assertTrue(req.partial_failure)

        self.mock_adjustment_upload_service.upload_conversion_adjustments.assert_called_once_with(
            request=self.mock_upload_request_obj
        )

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_restatement_success_with_value(self, mock_stdout):
        restatement_enum_member = self.mock_client.enums.ConversionAdjustmentTypeEnum.RESTATEMENT
        self._configure_successful_response(adjustment_type_enum_member=restatement_enum_member)

        test_restatement_value_str = "10.5"

        upload_conversion_adjustment.main(
            client=self.mock_client,
            customer_id=self.test_customer_id,
            conversion_action_id=self.test_conversion_action_id,
            adjustment_type="RESTATEMENT",
            order_id=self.test_order_id,
            adjustment_date_time=self.test_adjustment_date_time,
            restatement_value=test_restatement_value_str
        )

        self._common_asserts_basic_adjustment(restatement_enum_member)

        self.assertEqual(self.mock_restatement_value_obj.adjusted_value, float(test_restatement_value_str))
        self.assertIsNone(self.mock_restatement_value_obj.currency_code)

        expected_stdout_fragment = (
            f"Uploaded conversion adjustment for conversion action "
            f"'{self.mock_adjustment_result.conversion_action}' and order "
            f"ID '{self.mock_adjustment_result.order_id}'."
        )
        self.assertIn(expected_stdout_fragment, mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_retraction_success(self, mock_stdout):
        retraction_enum_member = self.mock_client.enums.ConversionAdjustmentTypeEnum.RETRACTION
        self._configure_successful_response(adjustment_type_enum_member=retraction_enum_member)

        upload_conversion_adjustment.main(
            client=self.mock_client, customer_id=self.test_customer_id,
            conversion_action_id=self.test_conversion_action_id, adjustment_type="RETRACTION",
            order_id=self.test_order_id, adjustment_date_time=self.test_adjustment_date_time,
            restatement_value=None
        )
        self._common_asserts_basic_adjustment(retraction_enum_member)
        self.assertIsNone(self.mock_restatement_value_obj.adjusted_value)
        self.assertIsNone(self.mock_restatement_value_obj.currency_code)

        expected_stdout_fragment = (
            f"Uploaded conversion adjustment for conversion action "
            f"'{self.mock_adjustment_result.conversion_action}' and order "
            f"ID '{self.mock_adjustment_result.order_id}'."
        )
        self.assertIn(expected_stdout_fragment, mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_restatement_no_value(self, mock_stdout):
        restatement_enum_member = self.mock_client.enums.ConversionAdjustmentTypeEnum.RESTATEMENT
        self._configure_successful_response(adjustment_type_enum_member=restatement_enum_member)

        upload_conversion_adjustment.main(
            client=self.mock_client, customer_id=self.test_customer_id,
            conversion_action_id=self.test_conversion_action_id, adjustment_type="RESTATEMENT",
            order_id=self.test_order_id, adjustment_date_time=self.test_adjustment_date_time,
            restatement_value=None
        )
        self._common_asserts_basic_adjustment(restatement_enum_member)
        self.assertIsNone(self.mock_restatement_value_obj.adjusted_value)
        self.assertIsNone(self.mock_restatement_value_obj.currency_code)

        expected_stdout_fragment = (
            f"Uploaded conversion adjustment for conversion action "
            f"'{self.mock_adjustment_result.conversion_action}' and order "
            f"ID '{self.mock_adjustment_result.order_id}'."
        )
        self.assertIn(expected_stdout_fragment, mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_partial_failure_error(self, mock_stdout):
        mock_single_error = Mock(name="SingleError")
        mock_field_path_element = Mock(index=0, field_name="test_field")
        mock_single_error.location.field_path_elements = [mock_field_path_element]
        mock_single_error.message = "Specific error for index 0."
        mock_error_code_obj = Mock(name="ErrorCodeObject_for_str_in_partial_failure")
        mock_error_code_obj.__str__ = Mock(return_value="TEST_ERROR_CODE_NAME")
        mock_single_error.error_code = mock_error_code_obj
        self.parsed_failure_object_mock.errors = [mock_single_error] # Configure return of deserialize

        TestUploadConversionAdjustmentMain.MockGoogleAdsFailureForTest.deserialize.reset_mock()

        mock_error_detail_val = Mock(name="ErrorDetailValue")
        mock_error_detail_val.value = b"serialized_error_bytes_content"
        self.mock_upload_response.partial_failure_error = Mock(
            details=[mock_error_detail_val], message="Mock partial failure message." # SUT uses this message
        )
        # SUT iterates over partial_failure_error.error_details in the print loop
        self.mock_upload_response.partial_failure_error.error_details = [mock_error_detail_val]


        self.mock_adjustment_result.conversion_action = "ca_path_for_partial_fail"
        self.mock_adjustment_result.adjustment_type = self.mock_client.enums.ConversionAdjustmentTypeEnum.RETRACTION
        self.mock_adjustment_result.order_id = self.test_order_id
        self.mock_upload_response.results = [self.mock_adjustment_result]
        self.mock_adjustment_upload_service.upload_conversion_adjustments.return_value = self.mock_upload_response

        upload_conversion_adjustment.main(
            client=self.mock_client, customer_id=self.test_customer_id,
            conversion_action_id=self.test_conversion_action_id, adjustment_type="RETRACTION",
            order_id=self.test_order_id, adjustment_date_time=self.test_adjustment_date_time,
            restatement_value=None
        )

        self._common_asserts_basic_adjustment(self.mock_client.enums.ConversionAdjustmentTypeEnum.RETRACTION)
        self.mock_client.get_type.assert_any_call("GoogleAdsFailure")
        TestUploadConversionAdjustmentMain.MockGoogleAdsFailureForTest.deserialize.assert_called_once_with(b"serialized_error_bytes_content")

        captured_output = mock_stdout.getvalue()
        self.assertIn("A partial failure at index 0 occurred", captured_output)
        self.assertIn("Error message: Specific error for index 0.", captured_output)
        self.assertIn("Error code: TEST_ERROR_CODE_NAME", captured_output)
        unexpected_success_fragment = (
             f"Uploaded conversion adjustment for conversion action "
            f"'{self.mock_adjustment_result.conversion_action}' and order "
            f"ID '{self.mock_adjustment_result.order_id}'."
        )
        self.assertNotIn(unexpected_success_fragment, captured_output)


    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_result_indicates_failure_via_no_order_id(self, mock_stdout):
        retraction_enum_member = self.mock_client.enums.ConversionAdjustmentTypeEnum.RETRACTION
        self._configure_successful_response(adjustment_type_enum_member=retraction_enum_member)
        self.mock_adjustment_result.order_id = None

        upload_conversion_adjustment.main(
            self.mock_client, self.test_customer_id, self.test_conversion_action_id,
            "RETRACTION", self.test_order_id, self.test_adjustment_date_time, None
        )
        self._common_asserts_basic_adjustment(retraction_enum_member)

        expected_stdout_fragment = (
            f"Uploaded conversion adjustment for conversion action "
            f"'{self.mock_adjustment_result.conversion_action}' and order "
            f"ID 'None'."
        )
        self.assertIn(expected_stdout_fragment, mock_stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
