import unittest
from unittest.mock import patch, MagicMock, call
import sys
import os
from io import StringIO

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from examples.remarketing.upload_offline_conversion import main as main_sut
from google.ads.googleads.client import GoogleAdsClient


@patch("google.ads.googleads.client.GoogleAdsClient.load_from_storage")
class TestUploadOfflineConversionMain(unittest.TestCase):

    def setUp(self):
        self.mock_client = MagicMock(spec=GoogleAdsClient)
        self.mock_client.enums = MagicMock()

        self.mock_conversion_upload_service = MagicMock(name="ConversionUploadService")
        self.mock_conversion_action_service = MagicMock(name="ConversionActionService")

        def get_service_side_effect(service_name, version=None):
            if service_name == "ConversionUploadService":
                return self.mock_conversion_upload_service
            elif service_name == "ConversionActionService":
                return self.mock_conversion_action_service
            return MagicMock(name=f"UnknownService_{service_name}")
        self.mock_client.get_service.side_effect = get_service_side_effect

        self.mock_conversion_action_service.conversion_action_path.return_value = "dummy_conversion_action_path"
        self.mock_conversion_upload_service.conversion_custom_variable_path.return_value = "dummy_custom_var_path"

        self.mock_click_conversion = MagicMock(name="ClickConversionInstance")
        self.mock_custom_variable = MagicMock(name="CustomVariableInstance")
        self.mock_upload_request = MagicMock(name="UploadClickConversionsRequestInstance")

        def get_type_side_effect(type_name):
            if type_name == "ClickConversion":
                self.mock_click_conversion.reset_mock()
                self.mock_click_conversion.custom_variables = []
                self.mock_click_conversion.consent = MagicMock(name="ConsentInstance_fresh")
                self.mock_click_conversion.consent.ad_user_data = None
                for attr in ['gclid', 'gbraid', 'wbraid', 'order_id', 'conversion_action',
                             'conversion_date_time', 'conversion_value', 'currency_code']:
                    setattr(self.mock_click_conversion, attr, None)
                return self.mock_click_conversion
            elif type_name == "CustomVariable":
                self.mock_custom_variable.reset_mock()
                for attr in ['conversion_custom_variable', 'value']:
                    setattr(self.mock_custom_variable, attr, None)
                return self.mock_custom_variable
            elif type_name == "UploadClickConversionsRequest":
                self.mock_upload_request.reset_mock()
                self.mock_upload_request.conversions = []
                self.mock_upload_request.customer_id = None
                self.mock_upload_request.partial_failure = None
                return self.mock_upload_request
            return MagicMock(name=f"DefaultMock_{type_name}")
        self.mock_client.get_type.side_effect = get_type_side_effect

        self.mock_client.enums.ConsentStatusEnum = {
            "GRANTED": "ENUM_CONSENT_GRANTED",
            "DENIED": "ENUM_CONSENT_DENIED",
            "UNSPECIFIED": "ENUM_CONSENT_UNSPECIFIED",
        }

        self.mock_upload_response = MagicMock(name="UploadClickConversionsResponse")
        self.mock_uploaded_conversion_result = MagicMock(name="UploadedConversionResult")
        self.mock_upload_response.results = [self.mock_uploaded_conversion_result]
        self.mock_upload_response.partial_failure_error = None
        self.mock_conversion_upload_service.upload_click_conversions.return_value = self.mock_upload_response

        self.patcher_stdout = patch('sys.stdout', new_callable=StringIO)
        self.mock_stdout = self.patcher_stdout.start()
        self.addCleanup(self.patcher_stdout.stop)
        self.addCleanup(self.mock_conversion_action_service.reset_mock)
        self.addCleanup(self.mock_conversion_upload_service.reset_mock)
        self.addCleanup(self.mock_client.reset_mock)


    def _common_asserts(self,
                        mock_click_conversion_obj,
                        customer_id,
                        conversion_action_id,
                        conversion_date_time,
                        conversion_value,
                        expected_gclid=None,
                        expected_gbraid=None,
                        expected_wbraid=None,
                        expected_order_id=None,
                        expect_custom_var=False,
                        expected_consent_val=None
                        ):

        self.mock_conversion_action_service.conversion_action_path.assert_called_once_with(
            customer_id, conversion_action_id
        )

        cc = mock_click_conversion_obj
        self.assertEqual(cc.conversion_action, "dummy_conversion_action_path")
        self.assertEqual(cc.conversion_date_time, conversion_date_time)
        self.assertEqual(cc.conversion_value, float(conversion_value))
        self.assertEqual(cc.currency_code, "USD")

        self.assertEqual(cc.gclid, expected_gclid)
        self.assertEqual(cc.gbraid, expected_gbraid)
        self.assertEqual(cc.wbraid, expected_wbraid)
        self.assertEqual(cc.order_id, expected_order_id)

        if expect_custom_var:
            self.assertIn(self.mock_custom_variable, cc.custom_variables)
            self.assertEqual(len(cc.custom_variables), 1)
        else:
            self.assertEqual(len(cc.custom_variables), 0)

        if expected_consent_val:
            self.assertEqual(cc.consent.ad_user_data, expected_consent_val)
        else:
            self.assertIsNone(cc.consent.ad_user_data)


        upload_request = self.mock_upload_request
        self.assertEqual(upload_request.customer_id, customer_id)
        self.assertIn(mock_click_conversion_obj, upload_request.conversions)
        self.assertEqual(len(upload_request.conversions), 1)
        self.assertTrue(upload_request.partial_failure)

        self.mock_conversion_upload_service.upload_click_conversions.assert_called_once_with(
            request=upload_request
        )


    def test_main_success_with_gclid(self, mock_load_storage):
        customer_id_val = "test_customer_gclid"
        conversion_action_id_val = "test_ca_gclid"
        gclid_val = "gclid_test_value_123"
        conversion_date_time_val = "2023-10-27 10:00:00-04:00"
        conversion_value_val = "100.50"

        self.mock_conversion_action_service.reset_mock()
        self.mock_conversion_upload_service.reset_mock()
        self.mock_client.get_type.reset_mock()

        self.mock_uploaded_conversion_result.gclid = gclid_val
        self.mock_uploaded_conversion_result.conversion_date_time = conversion_date_time_val
        self.mock_uploaded_conversion_result.conversion_action = "dummy_conversion_action_path"


        main_sut(
            client=self.mock_client,
            customer_id=customer_id_val,
            conversion_action_id=conversion_action_id_val,
            gclid=gclid_val,
            gbraid=None,
            wbraid=None,
            conversion_date_time=conversion_date_time_val,
            conversion_value=conversion_value_val,
            order_id=None,
            ad_user_data_consent=None,
            conversion_custom_variable_id=None,
            conversion_custom_variable_value=None
        )

        self._common_asserts(
            mock_click_conversion_obj=self.mock_click_conversion,
            customer_id=customer_id_val,
            conversion_action_id=conversion_action_id_val,
            conversion_date_time=conversion_date_time_val,
            conversion_value=conversion_value_val,
            expected_gclid=gclid_val
        )

        captured_output = self.mock_stdout.getvalue()
        expected_stdout_fragment = (
            f"Uploaded conversion that occurred at "
            f'"{self.mock_uploaded_conversion_result.conversion_date_time}" from '
            f'Google Click ID "{self.mock_uploaded_conversion_result.gclid}" '
            f'to "{self.mock_uploaded_conversion_result.conversion_action}"'
        )
        self.assertIn(expected_stdout_fragment, captured_output)

    def test_main_success_with_gbraid(self, mock_load_storage):
        customer_id_val = "test_customer_gbraid"
        conversion_action_id_val = "test_ca_gbraid"
        gbraid_val = "gbraid_test_value_456"
        conversion_date_time_val = "2023-10-28 11:00:00-04:00"
        conversion_value_val = "200.75"

        self.mock_conversion_action_service.reset_mock()
        self.mock_conversion_upload_service.reset_mock()
        self.mock_client.get_type.reset_mock()

        self.mock_uploaded_conversion_result.gclid = None
        self.mock_uploaded_conversion_result.conversion_date_time = conversion_date_time_val
        self.mock_uploaded_conversion_result.conversion_action = "dummy_conversion_action_path"

        main_sut(
            client=self.mock_client,
            customer_id=customer_id_val,
            conversion_action_id=conversion_action_id_val,
            gclid=None,
            gbraid=gbraid_val,
            wbraid=None,
            conversion_date_time=conversion_date_time_val,
            conversion_value=conversion_value_val,
            order_id=None,
            ad_user_data_consent=None,
            conversion_custom_variable_id=None,
            conversion_custom_variable_value=None
        )

        self._common_asserts(
            mock_click_conversion_obj=self.mock_click_conversion,
            customer_id=customer_id_val,
            conversion_action_id=conversion_action_id_val,
            conversion_date_time=conversion_date_time_val,
            conversion_value=conversion_value_val,
            expected_gbraid=gbraid_val
        )

        captured_output = self.mock_stdout.getvalue()
        expected_stdout_fragment = (
            f"Uploaded conversion that occurred at "
            f'"{conversion_date_time_val}" from '
            f'Google Click ID "None" '
            f'to "dummy_conversion_action_path"'
        )
        self.assertIn(expected_stdout_fragment, captured_output)

    def test_main_success_with_wbraid(self, mock_load_storage):
        customer_id_val = "test_customer_wbraid"
        conversion_action_id_val = "test_ca_wbraid"
        wbraid_val = "wbraid_test_value_789"
        conversion_date_time_val = "2023-10-29 12:00:00-04:00"
        conversion_value_val = "300.25"

        self.mock_conversion_action_service.reset_mock()
        self.mock_conversion_upload_service.reset_mock()
        self.mock_client.get_type.reset_mock()

        self.mock_uploaded_conversion_result.gclid = None
        self.mock_uploaded_conversion_result.conversion_date_time = conversion_date_time_val
        self.mock_uploaded_conversion_result.conversion_action = "dummy_conversion_action_path"

        main_sut(
            client=self.mock_client,
            customer_id=customer_id_val,
            conversion_action_id=conversion_action_id_val,
            gclid=None,
            gbraid=None,
            wbraid=wbraid_val,
            conversion_date_time=conversion_date_time_val,
            conversion_value=conversion_value_val,
            order_id=None,
            ad_user_data_consent=None,
            conversion_custom_variable_id=None,
            conversion_custom_variable_value=None
        )

        self._common_asserts(
            mock_click_conversion_obj=self.mock_click_conversion,
            customer_id=customer_id_val,
            conversion_action_id=conversion_action_id_val,
            conversion_date_time=conversion_date_time_val,
            conversion_value=conversion_value_val,
            expected_wbraid=wbraid_val
        )

        captured_output = self.mock_stdout.getvalue()
        expected_stdout_fragment = (
            f"Uploaded conversion that occurred at "
            f'"{conversion_date_time_val}" from '
            f'Google Click ID "None" '
            f'to "dummy_conversion_action_path"'
        )
        self.assertIn(expected_stdout_fragment, captured_output)

    def test_main_with_custom_variable(self, mock_load_storage):
        customer_id_val = "test_customer_cv"
        conversion_action_id_val = "test_ca_cv"
        gclid_val = "gclid_for_cv_test"
        conversion_date_time_val = "2023-10-30 13:00:00-04:00"
        conversion_value_val = "400.00"
        custom_var_id_val = "cv_id_123"
        custom_var_value_val = "cv_value_abc"

        self.mock_conversion_action_service.reset_mock()
        self.mock_conversion_upload_service.reset_mock()
        self.mock_client.get_type.reset_mock()

        self.mock_uploaded_conversion_result.gclid = gclid_val
        self.mock_uploaded_conversion_result.conversion_date_time = conversion_date_time_val
        self.mock_uploaded_conversion_result.conversion_action = "dummy_conversion_action_path"

        main_sut(
            client=self.mock_client,
            customer_id=customer_id_val,
            conversion_action_id=conversion_action_id_val,
            gclid=gclid_val,
            gbraid=None,
            wbraid=None,
            conversion_date_time=conversion_date_time_val,
            conversion_value=conversion_value_val,
            order_id=None,
            ad_user_data_consent=None,
            conversion_custom_variable_id=custom_var_id_val,
            conversion_custom_variable_value=custom_var_value_val
        )

        self._common_asserts(
            mock_click_conversion_obj=self.mock_click_conversion,
            customer_id=customer_id_val,
            conversion_action_id=conversion_action_id_val,
            conversion_date_time=conversion_date_time_val,
            conversion_value=conversion_value_val,
            expected_gclid=gclid_val,
            expect_custom_var=True
        )

        self.mock_client.get_type.assert_any_call("CustomVariable")
        self.mock_conversion_upload_service.conversion_custom_variable_path.assert_called_once_with(
            customer_id_val, custom_var_id_val
        )
        self.assertEqual(self.mock_custom_variable.conversion_custom_variable, "dummy_custom_var_path")
        self.assertEqual(self.mock_custom_variable.value, custom_var_value_val)

        captured_output = self.mock_stdout.getvalue()
        expected_stdout_fragment = (
            f"Uploaded conversion that occurred at "
            f'"{conversion_date_time_val}" from '
            f'Google Click ID "{gclid_val}" '
            f'to "dummy_conversion_action_path"'
        )
        self.assertIn(expected_stdout_fragment, captured_output)

    def test_main_with_order_id(self, mock_load_storage):
        customer_id_val = "test_customer_order_id"
        conversion_action_id_val = "test_ca_order_id"
        gclid_val = "gclid_for_order_id_test"
        order_id_val = "order_id_xyz_789"
        conversion_date_time_val = "2023-10-31 14:00:00-04:00"
        conversion_value_val = "500.50"

        self.mock_conversion_action_service.reset_mock()
        self.mock_conversion_upload_service.reset_mock()
        self.mock_client.get_type.reset_mock()

        self.mock_uploaded_conversion_result.gclid = gclid_val
        self.mock_uploaded_conversion_result.conversion_date_time = conversion_date_time_val
        self.mock_uploaded_conversion_result.conversion_action = "dummy_conversion_action_path"

        main_sut(
            client=self.mock_client,
            customer_id=customer_id_val,
            conversion_action_id=conversion_action_id_val,
            gclid=gclid_val,
            gbraid=None,
            wbraid=None,
            conversion_date_time=conversion_date_time_val,
            conversion_value=conversion_value_val,
            order_id=order_id_val,
            ad_user_data_consent=None,
            conversion_custom_variable_id=None,
            conversion_custom_variable_value=None
        )

        self._common_asserts(
            mock_click_conversion_obj=self.mock_click_conversion,
            customer_id=customer_id_val,
            conversion_action_id=conversion_action_id_val,
            conversion_date_time=conversion_date_time_val,
            conversion_value=conversion_value_val,
            expected_gclid=gclid_val,
            expected_order_id=order_id_val
        )

        captured_output = self.mock_stdout.getvalue()
        expected_stdout_fragment = (
            f"Uploaded conversion that occurred at "
            f'"{conversion_date_time_val}" from '
            f'Google Click ID "{gclid_val}" '
            f'to "dummy_conversion_action_path"'
        )
        self.assertIn(expected_stdout_fragment, captured_output)

    def test_main_with_ad_user_data_consent(self, mock_load_storage):
        customer_id_val = "test_customer_consent"
        conversion_action_id_val = "test_ca_consent"
        gclid_val = "gclid_for_consent_test"
        conversion_date_time_val = "2023-11-01 15:00:00-04:00"
        conversion_value_val = "600.00"
        ad_user_data_consent_val = "GRANTED" # String value as per SUT's argparse
        expected_enum_val = "ENUM_CONSENT_GRANTED" # From setUp mock

        self.mock_conversion_action_service.reset_mock()
        self.mock_conversion_upload_service.reset_mock()
        self.mock_client.get_type.reset_mock()

        self.mock_uploaded_conversion_result.gclid = gclid_val
        self.mock_uploaded_conversion_result.conversion_date_time = conversion_date_time_val
        self.mock_uploaded_conversion_result.conversion_action = "dummy_conversion_action_path"

        main_sut(
            client=self.mock_client,
            customer_id=customer_id_val,
            conversion_action_id=conversion_action_id_val,
            gclid=gclid_val,
            gbraid=None,
            wbraid=None,
            conversion_date_time=conversion_date_time_val,
            conversion_value=conversion_value_val,
            order_id=None,
            ad_user_data_consent=ad_user_data_consent_val, # Provide consent
            conversion_custom_variable_id=None,
            conversion_custom_variable_value=None
        )

        self._common_asserts(
            mock_click_conversion_obj=self.mock_click_conversion,
            customer_id=customer_id_val,
            conversion_action_id=conversion_action_id_val,
            conversion_date_time=conversion_date_time_val,
            conversion_value=conversion_value_val,
            expected_gclid=gclid_val,
            expected_consent_val=expected_enum_val # Key assertion
        )

        captured_output = self.mock_stdout.getvalue()
        expected_stdout_fragment = (
            f"Uploaded conversion that occurred at "
            f'"{conversion_date_time_val}" from '
            f'Google Click ID "{gclid_val}" '
            f'to "dummy_conversion_action_path"'
        )
        self.assertIn(expected_stdout_fragment, captured_output)


if __name__ == "__main__":
    unittest.main()
