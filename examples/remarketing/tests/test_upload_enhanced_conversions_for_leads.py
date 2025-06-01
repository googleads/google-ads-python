import unittest
import hashlib
from unittest.mock import patch, MagicMock, call, PropertyMock
import sys
import os
from io import StringIO # Import StringIO

# Add the project root to sys.path to allow for relative imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

# Assuming the SUT is in examples.remarketing.upload_enhanced_conversions_for_leads
from examples.remarketing.upload_enhanced_conversions_for_leads import (
    normalize_and_hash,
    normalize_and_hash_email_address,
    main,
)
from google.ads.googleads.client import GoogleAdsClient


class TestNormalizeAndHashLTV(unittest.TestCase):
    """Tests for the normalize_and_hash function (LTV variant)."""

    def _get_expected_hash(self, value_to_normalize):
        """Helper function to generate SHA-256 hash as per SUT."""
        # SUT's normalize_and_hash logic: value.strip().lower().encode()
        normalized_value = value_to_normalize.strip().lower()
        return hashlib.sha256(normalized_value.encode()).hexdigest()

    def test_simple_string(self):
        input_string = "test string"
        expected_hash = self._get_expected_hash(input_string)
        self.assertEqual(normalize_and_hash(input_string), expected_hash)

    def test_string_with_leading_trailing_spaces(self):
        input_string = "  test string  "
        # normalize_and_hash will strip spaces
        expected_hash = self._get_expected_hash("test string")
        self.assertEqual(normalize_and_hash(input_string), expected_hash)

    def test_string_with_mixed_case(self):
        input_string = "Test String"
        # normalize_and_hash will lowercase
        expected_hash = self._get_expected_hash("test string")
        self.assertEqual(normalize_and_hash(input_string), expected_hash)

    def test_empty_string(self):
        input_string = ""
        expected_hash = self._get_expected_hash(input_string)
        self.assertEqual(normalize_and_hash(input_string), expected_hash)


class TestNormalizeAndHashEmailLTV(unittest.TestCase):
    """Tests for the normalize_and_hash_email_address function (LTV variant)."""

    @patch("examples.remarketing.upload_enhanced_conversions_for_leads.normalize_and_hash")
    def test_regular_email(self, mock_normalize_and_hash):
        mock_normalize_and_hash.return_value = "hashed_regular_email"
        email = "user@example.com"
        result = normalize_and_hash_email_address(email)
        mock_normalize_and_hash.assert_called_once_with("user@example.com")
        self.assertEqual(result, "hashed_regular_email")

    @patch("examples.remarketing.upload_enhanced_conversions_for_leads.normalize_and_hash")
    def test_email_with_leading_trailing_spaces(self, mock_normalize_and_hash):
        mock_normalize_and_hash.return_value = "hashed_spaced_email"
        email = "  user@example.com  "
        result = normalize_and_hash_email_address(email)
        # SUT normalize_and_hash_email_address calls strip() then lower()
        mock_normalize_and_hash.assert_called_once_with("user@example.com")
        self.assertEqual(result, "hashed_spaced_email")

    @patch("examples.remarketing.upload_enhanced_conversions_for_leads.normalize_and_hash")
    def test_mixed_case_email(self, mock_normalize_and_hash):
        mock_normalize_and_hash.return_value = "hashed_mixed_case_email"
        email = "User@Example.COM"
        result = normalize_and_hash_email_address(email)
        mock_normalize_and_hash.assert_called_once_with("user@example.com")
        self.assertEqual(result, "hashed_mixed_case_email")

    @patch("examples.remarketing.upload_enhanced_conversions_for_leads.normalize_and_hash")
    def test_gmail_with_dots(self, mock_normalize_and_hash):
        mock_normalize_and_hash.return_value = "hashed_gmail_dots"
        email = "first.last@gmail.com"
        result = normalize_and_hash_email_address(email)
        # SUT removes dots from local part for gmail.com
        mock_normalize_and_hash.assert_called_once_with("firstlast@gmail.com")
        self.assertEqual(result, "hashed_gmail_dots")

    @patch("examples.remarketing.upload_enhanced_conversions_for_leads.normalize_and_hash")
    def test_googlemail_with_dots(self, mock_normalize_and_hash):
        mock_normalize_and_hash.return_value = "hashed_googlemail_dots"
        email = "first.last@googlemail.com"
        result = normalize_and_hash_email_address(email)
        # SUT removes dots from local part for googlemail.com
        mock_normalize_and_hash.assert_called_once_with("firstlast@googlemail.com")
        self.assertEqual(result, "hashed_googlemail_dots")

    @patch("examples.remarketing.upload_enhanced_conversions_for_leads.normalize_and_hash")
    def test_gmail_without_dots(self, mock_normalize_and_hash):
        mock_normalize_and_hash.return_value = "hashed_gmail_no_dots"
        email = "firstlast@gmail.com"
        result = normalize_and_hash_email_address(email)
        mock_normalize_and_hash.assert_called_once_with("firstlast@gmail.com")
        self.assertEqual(result, "hashed_gmail_no_dots")

    @patch("examples.remarketing.upload_enhanced_conversions_for_leads.normalize_and_hash")
    def test_other_domain_with_dots(self, mock_normalize_and_hash):
        mock_normalize_and_hash.return_value = "hashed_other_domain_dots"
        email = "first.last@otherdomain.com"
        result = normalize_and_hash_email_address(email)
        # Dots are preserved for non-Google domains
        mock_normalize_and_hash.assert_called_once_with("first.last@otherdomain.com")
        self.assertEqual(result, "hashed_other_domain_dots")

    @patch("examples.remarketing.upload_enhanced_conversions_for_leads.normalize_and_hash")
    def test_email_with_no_at_symbol(self, mock_normalize_and_hash):
        mock_normalize_and_hash.return_value = "hashed_no_at"
        email = "userexample.com"
        result = normalize_and_hash_email_address(email)
        mock_normalize_and_hash.assert_called_once_with("userexample.com")
        self.assertEqual(result, "hashed_no_at")

    @patch("examples.remarketing.upload_enhanced_conversions_for_leads.normalize_and_hash")
    def test_gmail_with_plus_alias(self, mock_normalize_and_hash):
        mock_normalize_and_hash.return_value = "hashed_gmail_plus"
        email = "user.name+alias@gmail.com"
        result = normalize_and_hash_email_address(email)
        mock_normalize_and_hash.assert_called_once_with("username+alias@gmail.com")
        self.assertEqual(result, "hashed_gmail_plus")

    @patch("examples.remarketing.upload_enhanced_conversions_for_leads.normalize_and_hash")
    def test_empty_email_string(self, mock_normalize_and_hash):
        mock_normalize_and_hash.return_value = "hashed_empty_email"
        email = ""
        result = normalize_and_hash_email_address(email)
        mock_normalize_and_hash.assert_called_once_with("")
        self.assertEqual(result, "hashed_empty_email")


@patch("google.ads.googleads.client.GoogleAdsClient.load_from_storage")
class TestMainFunctionForEnhancedLeads(unittest.TestCase):

    def setUp(self):
        self.mock_client = MagicMock(spec=GoogleAdsClient)
        self.mock_client.enums = MagicMock()
        self.mock_conversion_upload_service = MagicMock()

        self.mock_click_conversion_instance = MagicMock()
        self.mock_click_conversion_instance.user_identifiers = []
        self.mock_click_conversion_instance.session_attributes_key_value_pairs = MagicMock()
        self.mock_click_conversion_instance.session_attributes_key_value_pairs.key_value_pairs = []
        self.mock_click_conversion_instance.consent = MagicMock()

        self._created_user_identifiers = []
        self._created_session_attributes = []

        def get_type_side_effect(type_name):
            if type_name == "ClickConversion":
                self.mock_click_conversion_instance.ResetMock()
                self.mock_click_conversion_instance.user_identifiers = []
                self.mock_click_conversion_instance.session_attributes_key_value_pairs = MagicMock()
                self.mock_click_conversion_instance.session_attributes_key_value_pairs.key_value_pairs = []
                self.mock_click_conversion_instance.consent = MagicMock()

                self.mock_click_conversion_instance.order_id = None
                self.mock_click_conversion_instance.gclid = None
                self.mock_click_conversion_instance.session_attributes_encoded = None
                self.mock_click_conversion_instance.consent.ad_user_data = None
                self.mock_click_conversion_instance.conversion_action = ""
                self.mock_click_conversion_instance.conversion_date_time = ""
                self.mock_click_conversion_instance.conversion_value = 0.0
                self.mock_click_conversion_instance.currency_code = ""
                return self.mock_click_conversion_instance
            elif type_name == "UserIdentifier":
                new_identifier = MagicMock()
                new_identifier.hashed_email = None
                new_identifier.hashed_phone_number = None
                new_identifier.user_identifier_source = None
                self._created_user_identifiers.append(new_identifier)
                return new_identifier
            elif type_name == "SessionAttributeKeyValuePair":
                new_session_attr = MagicMock()
                new_session_attr.session_attribute_key = None
                new_session_attr.session_attribute_value = None
                self._created_session_attributes.append(new_session_attr)
                return new_session_attr
            return MagicMock()

        self.mock_client.get_type.side_effect = get_type_side_effect

        self.mock_client.enums.UserIdentifierSourceEnum = MagicMock()
        self.mock_client.enums.UserIdentifierSourceEnum.FIRST_PARTY = "ENUM_FIRST_PARTY"

        self.mock_client.enums.ConsentStatusEnum = {
            "GRANTED": "ENUM_CONSENT_GRANTED",
            "DENIED": "ENUM_CONSENT_DENIED",
            "UNSPECIFIED": "ENUM_CONSENT_UNSPECIFIED",
            "UNKNOWN": "ENUM_CONSENT_UNKNOWN",
        }

        self.mock_conversion_action_service = MagicMock()
        def get_service_side_effect(service_name, version=None):
            if service_name == "ConversionUploadService":
                return self.mock_conversion_upload_service
            elif service_name == "ConversionActionService":
                return self.mock_conversion_action_service
            return MagicMock()
        self.mock_client.get_service.side_effect = get_service_side_effect
        self.mock_conversion_action_service.conversion_action_path.return_value = "dummy_conversion_action_path"

        self.patched_normalize_email = patch(
            "examples.remarketing.upload_enhanced_conversions_for_leads.normalize_and_hash_email_address",
            return_value="hashed_email_value"
        )
        self.patched_normalize_hash = patch(
            "examples.remarketing.upload_enhanced_conversions_for_leads.normalize_and_hash",
            return_value="hashed_phone_value"
        )
        self.mock_normalize_email = self.patched_normalize_email.start()
        self.mock_normalize_hash = self.patched_normalize_hash.start()

        self.mock_upload_response = MagicMock()
        self.mock_upload_response.partial_failure_error = None
        self.mock_upload_result = MagicMock()
        self.mock_upload_response.results = [self.mock_upload_result]
        self.mock_conversion_upload_service.upload_click_conversions.return_value = self.mock_upload_response

        self.patcher_stdout = patch('sys.stdout', new_callable=StringIO)
        self.mock_stdout = self.patcher_stdout.start()

    def tearDown(self):
        self.patched_normalize_email.stop()
        self.patched_normalize_hash.stop()
        self.patcher_stdout.stop()
        self._created_user_identifiers = []
        self._created_session_attributes = []
        if hasattr(self, 'mock_upload_response') and self.mock_upload_response:
            self.mock_upload_response.partial_failure_error = None


    def test_main_basic_success_only_required_args(self, mock_load_storage):
        customer_id = "1234567890"
        conversion_action_id = "987654321"

        expected_conversion_date_time = "2024-07-30 10:00:00"
        expected_conversion_value = 25.5
        expected_currency_code = "USD"

        self._created_user_identifiers = []
        self.mock_click_conversion_instance.user_identifiers = []
        self._created_session_attributes = []
        self.mock_click_conversion_instance.session_attributes_key_value_pairs.key_value_pairs = []


        self.mock_upload_result.conversion_data_time = expected_conversion_date_time
        self.mock_upload_result.conversion_action = "dummy_conversion_action_path"
        self.mock_upload_response.partial_failure_error = None

        main(
            self.mock_client,
            customer_id,
            conversion_action_id,
            conversion_date_time=expected_conversion_date_time,
            conversion_value=expected_conversion_value,
            order_id=None,
            gclid=None,
            ad_user_data_consent=None
        )

        self.mock_normalize_email.assert_called_once_with("alex.2@example.com")
        self.mock_normalize_hash.assert_called_once_with("+1 800 5550102")

        self.assertEqual(len(self._created_user_identifiers), 2)
        self.assertEqual(len(self.mock_click_conversion_instance.user_identifiers), 2)

        email_identifier_on_cc = next((id_mock for id_mock in self.mock_click_conversion_instance.user_identifiers if hasattr(id_mock, "hashed_email") and id_mock.hashed_email == "hashed_email_value"), None)
        phone_identifier_on_cc = next((id_mock for id_mock in self.mock_click_conversion_instance.user_identifiers if hasattr(id_mock, "hashed_phone_number") and id_mock.hashed_phone_number == "hashed_phone_value"), None)

        self.assertIsNotNone(email_identifier_on_cc, "Email identifier mock not found on ClickConversion.")
        self.assertEqual(email_identifier_on_cc.user_identifier_source, "ENUM_FIRST_PARTY")

        self.assertIsNotNone(phone_identifier_on_cc, "Phone identifier mock not found on ClickConversion.")
        self.assertIsNone(phone_identifier_on_cc.user_identifier_source)

        cc = self.mock_click_conversion_instance
        self.assertEqual(cc.conversion_action, "dummy_conversion_action_path")
        self.assertEqual(cc.conversion_date_time, expected_conversion_date_time)
        self.assertEqual(cc.conversion_value, expected_conversion_value)
        self.assertEqual(cc.currency_code, expected_currency_code)

        self.assertIsNone(cc.order_id)
        self.assertIsNone(cc.gclid)
        self.assertIsNone(cc.consent.ad_user_data)
        self.assertIsNone(cc.session_attributes_encoded)
        self.assertEqual(len(cc.session_attributes_key_value_pairs.key_value_pairs), 0)

        self.mock_conversion_upload_service.upload_click_conversions.assert_called_once_with(
            customer_id=customer_id,
            conversions=[self.mock_click_conversion_instance],
            partial_failure=True
        )

        expected_output_message = (
            f"Uploaded conversion that occurred at "
            f"{expected_conversion_date_time} to "
            f"dummy_conversion_action_path."
        )

        all_stdout = self.mock_stdout.getvalue()
        self.assertIn(expected_output_message, all_stdout,
                      f"Expected stdout not found. Captured: '{all_stdout}'. Expected: '{expected_output_message}'")

    def test_main_with_gclid_and_order_id(self, mock_load_storage):
        customer_id = "1234567890"
        conversion_action_id = "987654321"
        expected_gclid = "test_gclid_value"
        expected_order_id = "test_order_id_value"
        expected_conversion_date_time = "2024-07-31 11:00:00"
        expected_conversion_value = 50.0
        expected_currency_code = "USD"

        self._created_user_identifiers = []
        self.mock_click_conversion_instance.user_identifiers = []
        self._created_session_attributes = []
        self.mock_click_conversion_instance.session_attributes_key_value_pairs.key_value_pairs = []


        self.mock_upload_result.conversion_data_time = expected_conversion_date_time
        self.mock_upload_result.conversion_action = "dummy_conversion_action_path"
        self.mock_upload_response.partial_failure_error = None

        main(
            self.mock_client,
            customer_id,
            conversion_action_id,
            conversion_date_time=expected_conversion_date_time,
            conversion_value=expected_conversion_value,
            order_id=expected_order_id,
            gclid=expected_gclid,
            ad_user_data_consent=None
        )

        cc = self.mock_click_conversion_instance
        self.assertEqual(cc.gclid, expected_gclid)
        self.assertEqual(cc.order_id, expected_order_id)

        self.mock_normalize_email.assert_called_once_with("alex.2@example.com")
        self.mock_normalize_hash.assert_called_once_with("+1 800 5550102")
        self.assertEqual(len(self.mock_click_conversion_instance.user_identifiers), 2)
        self.assertEqual(cc.conversion_action, "dummy_conversion_action_path")
        self.assertEqual(cc.conversion_date_time, expected_conversion_date_time)
        self.assertEqual(cc.conversion_value, expected_conversion_value)
        self.assertEqual(cc.currency_code, expected_currency_code)
        self.assertIsNone(cc.consent.ad_user_data)
        self.assertIsNone(cc.session_attributes_encoded)
        self.assertEqual(len(cc.session_attributes_key_value_pairs.key_value_pairs), 0)

        self.mock_conversion_upload_service.upload_click_conversions.assert_called_once_with(
            customer_id=customer_id,
            conversions=[self.mock_click_conversion_instance],
            partial_failure=True
        )

        expected_output_message = (
            f"Uploaded conversion that occurred at "
            f"{expected_conversion_date_time} to "
            f"dummy_conversion_action_path."
        )
        all_stdout = self.mock_stdout.getvalue()
        self.assertIn(expected_output_message, all_stdout,
                      f"Expected stdout not found. Captured: '{all_stdout}'. Expected: '{expected_output_message}'")

    def test_main_with_ad_user_data_consent(self, mock_load_storage):
        customer_id = "1234567890"
        conversion_action_id = "987654321"
        expected_conversion_date_time = "2024-08-01 12:00:00"
        expected_conversion_value = 75.0
        expected_currency_code = "USD"
        ad_user_data_consent_str = "GRANTED"
        expected_consent_enum_value = "ENUM_CONSENT_GRANTED"

        self._created_user_identifiers = []
        self.mock_click_conversion_instance.user_identifiers = []
        self._created_session_attributes = []
        self.mock_click_conversion_instance.session_attributes_key_value_pairs.key_value_pairs = []
        self.mock_click_conversion_instance.consent = MagicMock()
        self.mock_click_conversion_instance.consent.ad_user_data = None


        self.mock_upload_result.conversion_data_time = expected_conversion_date_time
        self.mock_upload_result.conversion_action = "dummy_conversion_action_path"
        self.mock_upload_response.partial_failure_error = None

        main(
            self.mock_client,
            customer_id,
            conversion_action_id,
            conversion_date_time=expected_conversion_date_time,
            conversion_value=expected_conversion_value,
            order_id=None,
            gclid=None,
            ad_user_data_consent=ad_user_data_consent_str
        )

        cc = self.mock_click_conversion_instance
        self.assertEqual(cc.consent.ad_user_data, expected_consent_enum_value)

        self.mock_normalize_email.assert_called_once_with("alex.2@example.com")
        self.mock_normalize_hash.assert_called_once_with("+1 800 5550102")
        self.assertEqual(len(self.mock_click_conversion_instance.user_identifiers), 2)
        self.assertEqual(cc.conversion_action, "dummy_conversion_action_path")
        self.assertEqual(cc.conversion_date_time, expected_conversion_date_time)
        self.assertEqual(cc.conversion_value, expected_conversion_value)
        self.assertEqual(cc.currency_code, expected_currency_code)
        self.assertIsNone(cc.order_id)
        self.assertIsNone(cc.gclid)
        self.assertIsNone(cc.session_attributes_encoded)
        self.assertEqual(len(cc.session_attributes_key_value_pairs.key_value_pairs), 0)

        self.mock_conversion_upload_service.upload_click_conversions.assert_called_once_with(
            customer_id=customer_id,
            conversions=[self.mock_click_conversion_instance],
            partial_failure=True
        )

        expected_output_message = (
            f"Uploaded conversion that occurred at "
            f"{expected_conversion_date_time} to "
            f"dummy_conversion_action_path."
        )
        all_stdout = self.mock_stdout.getvalue()
        self.assertIn(expected_output_message, all_stdout,
                      f"Expected stdout not found. Captured: '{all_stdout}'. Expected: '{expected_output_message}'")

    def test_main_with_session_attributes_encoded(self, mock_load_storage):
        customer_id = "1234567890"
        conversion_action_id = "987654321"
        expected_conversion_date_time = "2024-08-02 13:00:00"
        expected_conversion_value = 100.0
        expected_currency_code = "USD"
        session_attributes_encoded_val = "encoded_session_string_123"

        self._created_user_identifiers = []
        self.mock_click_conversion_instance.user_identifiers = []
        self._created_session_attributes = []
        self.mock_click_conversion_instance.session_attributes_key_value_pairs.key_value_pairs = []
        self.mock_click_conversion_instance.session_attributes_encoded = None


        self.mock_upload_result.conversion_data_time = expected_conversion_date_time
        self.mock_upload_result.conversion_action = "dummy_conversion_action_path"
        self.mock_upload_response.partial_failure_error = None

        main(
            self.mock_client,
            customer_id,
            conversion_action_id,
            conversion_date_time=expected_conversion_date_time,
            conversion_value=expected_conversion_value,
            order_id=None,
            gclid=None,
            ad_user_data_consent=None,
            session_attributes_encoded=session_attributes_encoded_val
        )

        cc = self.mock_click_conversion_instance
        self.assertEqual(cc.session_attributes_encoded, session_attributes_encoded_val)
        self.assertEqual(len(cc.session_attributes_key_value_pairs.key_value_pairs), 0)
        self.assertEqual(len(self._created_session_attributes), 0)


        self.mock_normalize_email.assert_called_once_with("alex.2@example.com")
        self.mock_normalize_hash.assert_called_once_with("+1 800 5550102")
        self.assertEqual(len(self.mock_click_conversion_instance.user_identifiers), 2)
        self.assertEqual(cc.conversion_action, "dummy_conversion_action_path")
        self.assertEqual(cc.conversion_date_time, expected_conversion_date_time)
        self.assertEqual(cc.conversion_value, expected_conversion_value)
        self.assertEqual(cc.currency_code, expected_currency_code)
        self.assertIsNone(cc.order_id)
        self.assertIsNone(cc.gclid)
        self.assertIsNone(cc.consent.ad_user_data)

        self.mock_conversion_upload_service.upload_click_conversions.assert_called_once_with(
            customer_id=customer_id,
            conversions=[self.mock_click_conversion_instance],
            partial_failure=True
        )

        expected_output_message = (
            f"Uploaded conversion that occurred at "
            f"{expected_conversion_date_time} to "
            f"dummy_conversion_action_path."
        )
        all_stdout = self.mock_stdout.getvalue()
        self.assertIn(expected_output_message, all_stdout,
                      f"Expected stdout not found. Captured: '{all_stdout}'. Expected: '{expected_output_message}'")

    def test_main_with_session_attributes_dict(self, mock_load_storage):
        customer_id = "1234567890"
        conversion_action_id = "987654321"
        expected_conversion_date_time = "2024-08-03 14:00:00"
        expected_conversion_value = 120.0
        expected_currency_code = "USD"
        session_attributes_dict_val = {"keyA": "valA", "keyB": "valB"}

        self._created_user_identifiers = []
        self.mock_click_conversion_instance.user_identifiers = []
        self._created_session_attributes = []
        self.mock_click_conversion_instance.session_attributes_key_value_pairs.key_value_pairs = []
        self.mock_click_conversion_instance.session_attributes_encoded = None


        self.mock_upload_result.conversion_data_time = expected_conversion_date_time
        self.mock_upload_result.conversion_action = "dummy_conversion_action_path"
        self.mock_upload_response.partial_failure_error = None

        main(
            self.mock_client,
            customer_id,
            conversion_action_id,
            conversion_date_time=expected_conversion_date_time,
            conversion_value=expected_conversion_value,
            order_id=None,
            gclid=None,
            ad_user_data_consent=None,
            session_attributes_dict=session_attributes_dict_val
        )

        cc = self.mock_click_conversion_instance
        self.assertIsNone(cc.session_attributes_encoded)

        self.assertEqual(len(self._created_session_attributes), 2)
        self.assertEqual(len(cc.session_attributes_key_value_pairs.key_value_pairs), 2)

        expected_pairs_on_cc = []
        for mock_pair in cc.session_attributes_key_value_pairs.key_value_pairs:
            expected_pairs_on_cc.append({
                "key": mock_pair.session_attribute_key,
                "value": mock_pair.session_attribute_value
            })

        self.assertIn({"key": "keyA", "value": "valA"}, expected_pairs_on_cc)
        self.assertIn({"key": "keyB", "value": "valB"}, expected_pairs_on_cc)

        mock_for_keyA = next((p for p in self._created_session_attributes if p.session_attribute_key == "keyA"), None)
        self.assertIsNotNone(mock_for_keyA)
        self.assertEqual(mock_for_keyA.session_attribute_value, "valA")

        mock_for_keyB = next((p for p in self._created_session_attributes if p.session_attribute_key == "keyB"), None)
        self.assertIsNotNone(mock_for_keyB)
        self.assertEqual(mock_for_keyB.session_attribute_value, "valB")

        self.mock_normalize_email.assert_called_once_with("alex.2@example.com")
        self.mock_normalize_hash.assert_called_once_with("+1 800 5550102")
        self.assertEqual(len(self.mock_click_conversion_instance.user_identifiers), 2)
        self.assertEqual(cc.conversion_action, "dummy_conversion_action_path")
        self.assertEqual(cc.conversion_date_time, expected_conversion_date_time)
        self.assertEqual(cc.conversion_value, expected_conversion_value)
        self.assertEqual(cc.currency_code, expected_currency_code)
        self.assertIsNone(cc.order_id)
        self.assertIsNone(cc.gclid)
        self.assertIsNone(cc.consent.ad_user_data)

        self.mock_conversion_upload_service.upload_click_conversions.assert_called_once_with(
            customer_id=customer_id,
            conversions=[self.mock_click_conversion_instance],
            partial_failure=True
        )

        expected_output_message = (
            f"Uploaded conversion that occurred at "
            f"{expected_conversion_date_time} to "
            f"dummy_conversion_action_path."
        )
        all_stdout = self.mock_stdout.getvalue()
        self.assertIn(expected_output_message, all_stdout,
                      f"Expected stdout not found. Captured: '{all_stdout}'. Expected: '{expected_output_message}'")

    def test_main_value_error_on_both_session_attributes(self, mock_load_storage):
        customer_id = "1234567890"
        conversion_action_id = "987654321"
        expected_conversion_date_time = "2024-08-04 15:00:00"
        expected_conversion_value = 150.0

        expected_error_message = ("Only one of 'session_attributes_encoded' or "
                                  "'session_attributes_dict' can be set.")

        with self.assertRaisesRegex(ValueError, expected_error_message):
            main(
                self.mock_client,
                customer_id,
                conversion_action_id,
                conversion_date_time=expected_conversion_date_time,
                conversion_value=expected_conversion_value,
                order_id=None,
                gclid=None,
                ad_user_data_consent=None,
                session_attributes_encoded="some_encoded_string",
                session_attributes_dict={"key": "val"}
            )

        self.mock_conversion_upload_service.upload_click_conversions.assert_not_called()
        self.mock_normalize_email.assert_not_called()
        self.mock_normalize_hash.assert_not_called()

    def test_main_partial_failure_response(self, mock_load_storage):
        customer_id = "1234567890"
        conversion_action_id = "987654321"
        expected_conversion_date_time = "2024-08-05 16:00:00"
        expected_conversion_value = 180.0
        partial_failure_message = "Partial failure test message."

        self._created_user_identifiers = []
        self.mock_click_conversion_instance.user_identifiers = []
        self._created_session_attributes = []
        self.mock_click_conversion_instance.session_attributes_key_value_pairs.key_value_pairs = []

        mock_partial_failure_error = MagicMock()
        mock_partial_failure_error.message = partial_failure_message
        self.mock_upload_response.partial_failure_error = mock_partial_failure_error

        # SUT will not print result if partial_failure_error is set.
        # So, these specific values on mock_upload_result are not strictly needed for stdout check in this case.
        # self.mock_upload_result.conversion_data_time = expected_conversion_date_time
        # self.mock_upload_result.conversion_action = "dummy_conversion_action_path"


        main(
            self.mock_client,
            customer_id,
            conversion_action_id,
            conversion_date_time=expected_conversion_date_time,
            conversion_value=expected_conversion_value,
            order_id=None,
            gclid=None,
            ad_user_data_consent=None
        )

        self.mock_normalize_email.assert_called_once_with("alex.2@example.com")
        self.mock_normalize_hash.assert_called_once_with("+1 800 5550102")
        self.mock_conversion_upload_service.upload_click_conversions.assert_called_once()

        all_stdout = self.mock_stdout.getvalue()

        expected_partial_failure_stdout = f"Partial error encountered: {partial_failure_message}"
        self.assertIn(expected_partial_failure_stdout, all_stdout)

        # If partial_failure_error is present, the success message is not printed.
        unexpected_success_stdout = (
            f"Uploaded conversion that occurred at "
            f"{expected_conversion_date_time} to "
            f"dummy_conversion_action_path."
        )
        self.assertNotIn(unexpected_success_stdout, all_stdout)


if __name__ == "__main__":
    unittest.main()
