import unittest
import hashlib
from unittest.mock import patch, MagicMock, call, PropertyMock
import sys
import os
from io import StringIO

# Add the project root to sys.path to allow for relative imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from examples.remarketing.upload_enhanced_conversions_for_web import (
    normalize_and_hash,
    normalize_and_hash_email_address,
    main as main_sut,
)
from google.ads.googleads.client import GoogleAdsClient


class TestNormalizeAndHash(unittest.TestCase):
    """Tests for the normalize_and_hash function."""

    def _get_expected_hash(self, value_to_normalize):
        normalized_value = value_to_normalize.strip().lower()
        return hashlib.sha256(normalized_value.encode()).hexdigest()

    def test_simple_string(self):
        input_string = "test string"
        expected_hash = self._get_expected_hash(input_string)
        self.assertEqual(normalize_and_hash(input_string), expected_hash)

    def test_string_with_leading_trailing_spaces(self):
        input_string = "  test string  "
        expected_hash = self._get_expected_hash("test string")
        self.assertEqual(normalize_and_hash(input_string), expected_hash)

    def test_string_with_mixed_case(self):
        input_string = "Test String"
        expected_hash = self._get_expected_hash("test string")
        self.assertEqual(normalize_and_hash(input_string), expected_hash)

    def test_empty_string(self):
        input_string = ""
        expected_hash = self._get_expected_hash(input_string)
        self.assertEqual(normalize_and_hash(input_string), expected_hash)


class TestNormalizeAndHashEmailAddress(unittest.TestCase):
    """Tests for the normalize_and_hash_email_address function."""

    @patch("examples.remarketing.upload_enhanced_conversions_for_web.normalize_and_hash")
    def test_regular_email(self, mock_normalize_and_hash_inner):
        mock_normalize_and_hash_inner.return_value = "hashed_regular_email"
        email = "user@example.com"
        result = normalize_and_hash_email_address(email)
        mock_normalize_and_hash_inner.assert_called_once_with("user@example.com")
        self.assertEqual(result, "hashed_regular_email")

    @patch("examples.remarketing.upload_enhanced_conversions_for_web.normalize_and_hash")
    def test_email_with_leading_trailing_spaces_and_case(self, mock_normalize_and_hash_inner):
        mock_normalize_and_hash_inner.return_value = "hashed_spaced_email"
        email = "  User@Example.COM  "
        result = normalize_and_hash_email_address(email)
        mock_normalize_and_hash_inner.assert_called_once_with("user@example.com")
        self.assertEqual(result, "hashed_spaced_email")

    @patch("examples.remarketing.upload_enhanced_conversions_for_web.normalize_and_hash")
    def test_gmail_with_dots(self, mock_normalize_and_hash_inner):
        mock_normalize_and_hash_inner.return_value = "hashed_gmail_dots"
        email = "first.last.name@gmail.com"
        result = normalize_and_hash_email_address(email)
        mock_normalize_and_hash_inner.assert_called_once_with("firstlastname@gmail.com")
        self.assertEqual(result, "hashed_gmail_dots")

    @patch("examples.remarketing.upload_enhanced_conversions_for_web.normalize_and_hash")
    def test_googlemail_with_dots(self, mock_normalize_and_hash_inner):
        mock_normalize_and_hash_inner.return_value = "hashed_googlemail_dots"
        email = "another.user.name@googlemail.com"
        result = normalize_and_hash_email_address(email)
        mock_normalize_and_hash_inner.assert_called_once_with("anotherusername@googlemail.com")
        self.assertEqual(result, "hashed_googlemail_dots")

    @patch("examples.remarketing.upload_enhanced_conversions_for_web.normalize_and_hash")
    def test_other_domain_with_dots(self, mock_normalize_and_hash_inner):
        mock_normalize_and_hash_inner.return_value = "hashed_other_domain_dots"
        email = "name.with.dots@otherdomain.com"
        result = normalize_and_hash_email_address(email)
        mock_normalize_and_hash_inner.assert_called_once_with("name.with.dots@otherdomain.com")
        self.assertEqual(result, "hashed_other_domain_dots")

    @patch("examples.remarketing.upload_enhanced_conversions_for_web.normalize_and_hash")
    def test_gmail_with_plus_alias_and_dots(self, mock_normalize_and_hash_inner):
        mock_normalize_and_hash_inner.return_value = "hashed_gmail_plus_dots"
        email = "user.name+alias@gmail.com"
        result = normalize_and_hash_email_address(email)
        mock_normalize_and_hash_inner.assert_called_once_with("username+alias@gmail.com")
        self.assertEqual(result, "hashed_gmail_plus_dots")


@patch("google.ads.googleads.client.GoogleAdsClient.load_from_storage")
class TestMainFunctionForEnhancedWeb(unittest.TestCase):

    def setUp(self):
        self.mock_client = MagicMock(spec=GoogleAdsClient)
        self.mock_client.enums = MagicMock()

        self.mock_ca_upload_service = MagicMock(name="ConversionAdjustmentUploadService")
        self.mock_ca_service = MagicMock(name="ConversionActionService")

        def get_service_side_effect(service_name, version=None):
            if service_name == "ConversionAdjustmentUploadService":
                return self.mock_ca_upload_service
            elif service_name == "ConversionActionService":
                return self.mock_ca_service
            return MagicMock()
        self.mock_client.get_service.side_effect = get_service_side_effect

        self.mock_ca_service.conversion_action_path.return_value = "dummy_conversion_action_path"

        self.mock_client.enums.ConversionAdjustmentTypeEnum = MagicMock()
        self.mock_client.enums.ConversionAdjustmentTypeEnum.ENHANCEMENT = "ENHANCEMENT_ENUM_VAL"
        self.mock_client.enums.UserIdentifierSourceEnum = MagicMock()
        self.mock_client.enums.UserIdentifierSourceEnum.FIRST_PARTY = "FIRST_PARTY_ENUM_VAL"

        self.mock_conversion_adjustment = MagicMock(name="ConversionAdjustmentInstance")
        self.mock_gclid_date_time_pair = MagicMock(name="GclidDateTimePairInstance")
        self.mock_gclid_date_time_pair.gclid = None
        self.mock_conversion_adjustment.gclid_date_time_pair = self.mock_gclid_date_time_pair

        self._created_user_identifiers_for_test = []
        self._created_address_info_for_test = None

        def get_type_side_effect(type_name):
            if type_name == "ConversionAdjustment":
                self.mock_conversion_adjustment.user_identifiers = []
                self.mock_conversion_adjustment.order_id = None
                self.mock_conversion_adjustment.user_agent = None
                self.mock_gclid_date_time_pair.gclid = None
                self.mock_gclid_date_time_pair.conversion_date_time = None
                self.mock_conversion_adjustment.gclid_date_time_pair = self.mock_gclid_date_time_pair
                return self.mock_conversion_adjustment
            elif type_name == "UserIdentifier":
                new_identifier = MagicMock(name="UserIdentifierInstance")
                if len(self._created_user_identifiers_for_test) == 2:
                    self._created_address_info_for_test = MagicMock(name="AddressInfo_linked_to_AddressID")
                    new_identifier.address_info = self._created_address_info_for_test
                else:
                    new_identifier.address_info = MagicMock(name="AddressInfo_for_non_address_UID")
                self._created_user_identifiers_for_test.append(new_identifier)
                return new_identifier
            return MagicMock(name=f"DefaultMock_{type_name}")
        self.mock_client.get_type.side_effect = get_type_side_effect

        self.patch_normalize_email_web = patch(
            "examples.remarketing.upload_enhanced_conversions_for_web.normalize_and_hash_email_address",
            return_value="hashed_email_val"
        )

        def normalize_hash_side_effect(value_to_hash):
            if value_to_hash == "+1 800 5550102":
                return "hashed_phone_val"
            elif value_to_hash == "Alex":
                return "hashed_fn_val"
            elif value_to_hash == "Quinn":
                return "hashed_ln_val"
            return f"hashed_unexpected_{value_to_hash}"

        self.patch_normalize_hash_web = patch(
            "examples.remarketing.upload_enhanced_conversions_for_web.normalize_and_hash",
            side_effect=normalize_hash_side_effect
        )

        self.mock_normalize_email_sut = self.patch_normalize_email_web.start()
        self.mock_normalize_hash_sut = self.patch_normalize_hash_web.start()

        self.mock_upload_response = MagicMock(name="UploadResponse")
        self.mock_upload_response.partial_failure_error = None
        self.mock_upload_result = MagicMock(name="UploadResult")
        self.mock_upload_response.results = [self.mock_upload_result]
        self.mock_ca_upload_service.upload_conversion_adjustments.return_value = self.mock_upload_response

        self.patcher_stdout = patch('sys.stdout', new_callable=StringIO)
        self.mock_stdout = self.patcher_stdout.start()

    def tearDown(self):
        self.patch_normalize_email_web.stop()
        self.patch_normalize_hash_web.stop()
        self.patcher_stdout.stop()
        if hasattr(self.mock_upload_response, 'partial_failure_error'):
             self.mock_upload_response.partial_failure_error = None
        if hasattr(self, 'mock_gclid_date_time_pair'):
            self.mock_gclid_date_time_pair.gclid = None
            self.mock_gclid_date_time_pair.conversion_date_time = None
        if hasattr(self, 'mock_conversion_adjustment'):
            self.mock_conversion_adjustment.user_agent = None
            self.mock_conversion_adjustment.order_id = None


    def test_main_basic_success_all_args_provided(self, mock_load_storage):
        customer_id = "test_customer_123"
        conversion_action_id = "test_ca_456"
        order_id = "test_order_789"
        conversion_date_time_val = "2023-10-26 10:00:00-05:00"
        user_agent_val = "TestUserAgent/1.0"

        self._created_user_identifiers_for_test = []
        self._created_address_info_for_test = None
        self.mock_normalize_email_sut.reset_mock()
        self.mock_normalize_hash_sut.reset_mock()
        self.mock_ca_upload_service.upload_conversion_adjustments.reset_mock()
        self.mock_conversion_adjustment.user_identifiers = []

        self.mock_upload_result.conversion_action = "dummy_conversion_action_path"
        self.mock_upload_result.order_id = order_id
        self.mock_upload_response.partial_failure_error = None


        main_sut(
            self.mock_client,
            customer_id,
            conversion_action_id,
            order_id,
            conversion_date_time=conversion_date_time_val,
            user_agent=user_agent_val
        )

        self.mock_normalize_email_sut.assert_called_once_with("alex.2@example.com")
        self.mock_normalize_hash_sut.assert_any_call("+1 800 5550102")
        self.mock_normalize_hash_sut.assert_any_call("Alex")
        self.mock_normalize_hash_sut.assert_any_call("Quinn")
        self.assertEqual(self.mock_normalize_hash_sut.call_count, 3)

        self.assertEqual(len(self._created_user_identifiers_for_test), 3)
        self.assertEqual(len(self.mock_conversion_adjustment.user_identifiers), 3)

        email_identifier = None
        phone_identifier = None
        address_identifier = None

        for ident in self.mock_conversion_adjustment.user_identifiers:
            if hasattr(ident, 'hashed_email') and ident.hashed_email == "hashed_email_val":
                email_identifier = ident
            elif hasattr(ident, 'hashed_phone_number') and ident.hashed_phone_number == "hashed_phone_val":
                phone_identifier = ident
            elif ident.address_info is self._created_address_info_for_test and self._created_address_info_for_test is not None:
                address_identifier = ident

        self.assertIsNotNone(email_identifier, "Email identifier not found")
        self.assertEqual(email_identifier.user_identifier_source, "FIRST_PARTY_ENUM_VAL")

        self.assertIsNotNone(phone_identifier, "Phone identifier not found")

        self.assertIsNotNone(address_identifier, "Address identifier not found")
        self.assertIsNotNone(address_identifier.address_info, "AddressInfo not set on address identifier")

        self.assertIs(address_identifier.address_info, self._created_address_info_for_test)

        addr_info = address_identifier.address_info
        self.assertEqual(addr_info.hashed_first_name, "hashed_fn_val")
        self.assertEqual(addr_info.hashed_last_name, "hashed_ln_val")
        self.assertEqual(addr_info.country_code, "US")
        self.assertEqual(addr_info.postal_code, "94045")

        adj = self.mock_conversion_adjustment
        self.assertEqual(adj.adjustment_type, "ENHANCEMENT_ENUM_VAL")
        self.assertEqual(adj.conversion_action, "dummy_conversion_action_path")
        self.assertEqual(adj.order_id, order_id)
        self.assertEqual(adj.user_agent, user_agent_val)

        self.assertIsNotNone(adj.gclid_date_time_pair)
        self.assertIsNone(adj.gclid_date_time_pair.gclid)
        self.assertEqual(adj.gclid_date_time_pair.conversion_date_time, conversion_date_time_val)

        self.mock_ca_upload_service.upload_conversion_adjustments.assert_called_once_with(
            customer_id=customer_id,
            conversion_adjustments=[self.mock_conversion_adjustment],
            partial_failure=True
        )

        captured_output = self.mock_stdout.getvalue()
        self.assertIn(f"Uploaded conversion adjustment of {self.mock_upload_result.conversion_action} for order ID (", captured_output)
        self.assertIn(f", '{order_id}')", captured_output)

    def test_main_missing_optional_args(self, mock_load_storage):
        customer_id = "test_customer_123"
        conversion_action_id = "test_ca_456"
        order_id = "test_order_789_missing_opts"

        self._created_user_identifiers_for_test = []
        self._created_address_info_for_test = None
        self.mock_normalize_email_sut.reset_mock()
        self.mock_normalize_hash_sut.reset_mock()
        self.mock_ca_upload_service.upload_conversion_adjustments.reset_mock()
        self.mock_conversion_adjustment.user_identifiers = []
        self.mock_conversion_adjustment.user_agent = "previous_value" # Set to ensure it's cleared
        self.mock_gclid_date_time_pair.conversion_date_time = "previous_value" # Set to ensure it's cleared


        self.mock_upload_result.conversion_action = "dummy_conversion_action_path"
        self.mock_upload_result.order_id = order_id
        self.mock_upload_response.partial_failure_error = None

        main_sut(
            self.mock_client,
            customer_id,
            conversion_action_id,
            order_id,
            conversion_date_time=None,
            user_agent=None
        )

        self.mock_normalize_email_sut.assert_called_once_with("alex.2@example.com")
        self.assertEqual(self.mock_normalize_hash_sut.call_count, 3)
        self.assertEqual(len(self.mock_conversion_adjustment.user_identifiers), 3)

        adj = self.mock_conversion_adjustment
        self.assertEqual(adj.adjustment_type, "ENHANCEMENT_ENUM_VAL")
        self.assertEqual(adj.conversion_action, "dummy_conversion_action_path")
        self.assertEqual(adj.order_id, order_id)

        self.assertIsNone(adj.user_agent)
        self.assertIsNone(adj.gclid_date_time_pair.conversion_date_time)

        self.mock_ca_upload_service.upload_conversion_adjustments.assert_called_once()

        captured_output = self.mock_stdout.getvalue()
        self.assertIn(f"Uploaded conversion adjustment of {self.mock_upload_result.conversion_action} for order ID (", captured_output)
        self.assertIn(f", '{order_id}')", captured_output)

    def test_main_partial_failure_response(self, mock_load_storage):
        customer_id = "test_customer_123"
        conversion_action_id = "test_ca_456"
        order_id = "test_order_789_partial_fail"
        partial_failure_message = "Test partial failure from web."

        self._created_user_identifiers_for_test = []
        self._created_address_info_for_test = None
        self.mock_normalize_email_sut.reset_mock()
        self.mock_normalize_hash_sut.reset_mock()
        self.mock_ca_upload_service.upload_conversion_adjustments.reset_mock()
        self.mock_conversion_adjustment.user_identifiers = []

        # Configure response for partial failure
        self.mock_upload_response.partial_failure_error = MagicMock(message=partial_failure_message)
        # SUT for web does not iterate error_details, so just message is enough for partial_failure_error

        # Values for the result object, though not printed in partial failure case for this SUT
        self.mock_upload_result.conversion_action = "dummy_conversion_action_path"
        self.mock_upload_result.order_id = order_id

        main_sut(
            self.mock_client,
            customer_id,
            conversion_action_id,
            order_id,
            conversion_date_time=None,
            user_agent=None
        )

        # Core operations should still occur
        self.mock_normalize_email_sut.assert_called_once_with("alex.2@example.com")
        self.assertEqual(self.mock_normalize_hash_sut.call_count, 3)
        self.mock_ca_upload_service.upload_conversion_adjustments.assert_called_once()

        # Check for stdout messages
        captured_output = self.mock_stdout.getvalue()

        expected_partial_failure_stdout = f"Partial error encountered: {partial_failure_message}"
        self.assertIn(expected_partial_failure_stdout, captured_output)

        # Success message should NOT be printed if partial_failure_error is set
        unexpected_success_stdout = "Uploaded conversion adjustment of"
        self.assertNotIn(unexpected_success_stdout, captured_output)


if __name__ == "__main__":
    unittest.main()
