import unittest
import hashlib
from unittest.mock import patch, MagicMock, call, Mock
import sys
import os
from io import StringIO
from datetime import datetime as real_datetime_class, timedelta as real_timedelta_class

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from examples.remarketing.upload_store_sales_transactions import (
    normalize_and_hash,
    build_offline_user_data_job_operations,
    create_offline_user_data_job,
    print_google_ads_failures,
    add_transactions_to_offline_user_data_job,
    check_job_status,
    main as main_sut, # Added main SUT function
)
from google.ads.googleads.client import GoogleAdsClient


class TestNormalizeAndHashStoreSales(unittest.TestCase):
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


class TestBuildOperationsStoreSales(unittest.TestCase):

    def setUp(self):
        self.mock_client = MagicMock(spec=GoogleAdsClient)
        self.mock_client.enums = MagicMock()

        self.mock_ca_service = MagicMock(name="ConversionActionService")

        self.original_get_service_build_ops = getattr(self.mock_client, 'get_service', None)
        self.original_get_type_build_ops = getattr(self.mock_client, 'get_type', None)


        self.mock_client.get_service = MagicMock(return_value=self.mock_ca_service)
        self.mock_ca_service.conversion_action_path.return_value = "dummy_ca_path_val"

        self.mock_client.enums.ConsentStatusEnum = {
            "GRANTED": "ENUM_CONSENT_GRANTED",
            "DENIED": "ENUM_CONSENT_DENIED",
            "UNSPECIFIED": "ENUM_CONSENT_UNSPECIFIED",
        }

        self.created_operations = []
        self.created_user_identifiers = []

        def get_type_side_effect_for_build_ops(type_name):
            if type_name == "OfflineUserDataJobOperation":
                operation = MagicMock(name=f"OfflineUserDataJobOperation_{len(self.created_operations)}")
                user_data = MagicMock(name=f"UserData_on_Op_{len(self.created_operations)}")
                user_data.user_identifiers = []
                user_data.transaction_attribute = MagicMock(name=f"TransactionAttribute_on_Op_{len(self.created_operations)}")
                user_data.transaction_attribute.custom_value = None
                user_data.transaction_attribute.item_attribute = MagicMock(name=f"ItemAttribute_on_TA_{len(self.created_operations)}")

                user_data.consent = MagicMock(name=f"Consent_on_Op_{len(self.created_operations)}")
                user_data.consent.ad_user_data = None
                user_data.consent.ad_personalization = None
                operation.create = user_data
                self.created_operations.append(operation)
                return operation
            elif type_name == "UserIdentifier":
                identifier = MagicMock(name=f"UserIdentifier_{len(self.created_user_identifiers)}")
                identifier.address_info = MagicMock(name=f"AddressInfo_on_UID_{len(self.created_user_identifiers)}")
                self.created_user_identifiers.append(identifier)
                return identifier
            return MagicMock(name=f"DefaultMock_BuildOps_{type_name}")
        self.mock_client.get_type.side_effect = get_type_side_effect_for_build_ops

        def normalize_hash_side_effect_for_build_op(value_to_hash):
            if value_to_hash == "dana@example.com": return "hashed_dana@example.com"
            elif value_to_hash == "Dana": return "hashed_Dana"
            elif value_to_hash == "Quinn": return "hashed_Quinn"
            return f"hashed_unexpected_{value_to_hash}"

        self.patch_normalize_hash_sut = patch(
            "examples.remarketing.upload_store_sales_transactions.normalize_and_hash",
            side_effect=normalize_hash_side_effect_for_build_op
        )
        self.mock_normalize_hash = self.patch_normalize_hash_sut.start()
        self.addCleanup(self.patch_normalize_hash_sut.stop)

        self.patch_datetime_class_in_sut = patch(
            "examples.remarketing.upload_store_sales_transactions.datetime",
            autospec=True
        )
        self.mock_datetime_class_object_in_setup = self.patch_datetime_class_in_sut.start()
        self.addCleanup(self.patch_datetime_class_in_sut.stop)

        self.fixed_now_time = real_datetime_class(2023, 1, 31, 12, 0, 0)
        self.mock_datetime_class_object_in_setup.now.return_value = self.fixed_now_time

        def mock_timedelta_constructor(*args, **kwargs):
            if 'months' in kwargs and kwargs['months'] == 1:
                return real_timedelta_class(days=30)
            elif 'days' in kwargs and kwargs['days'] == 1:
                 return real_timedelta_class(days=1)
            return real_timedelta_class(*args, **kwargs)

        self.mock_datetime_class_object_in_setup.timedelta = MagicMock(side_effect=mock_timedelta_constructor)
        self.addCleanup(self._restore_original_client_methods_build_ops)

    def _restore_original_client_methods_build_ops(self):
        if self.original_get_service_build_ops:
            self.mock_client.get_service = self.original_get_service_build_ops
        if self.original_get_type_build_ops:
            self.mock_client.get_type = self.original_get_type_build_ops

    def test_build_operations_basic_case_no_optionals(self):
        customer_id_val = "test_customer_1"
        conversion_action_id_val = "ca_id_1"

        self.mock_normalize_hash.reset_mock()
        self.created_operations.clear()
        self.created_user_identifiers.clear()

        if hasattr(self.patch_datetime_class_in_sut, 'new') and hasattr(self.patch_datetime_class_in_sut.new, 'now'):
             self.patch_datetime_class_in_sut.new.now.reset_mock()
        if hasattr(self.patch_datetime_class_in_sut, 'new') and hasattr(self.patch_datetime_class_in_sut.new, 'timedelta'):
             self.patch_datetime_class_in_sut.new.timedelta.reset_mock()


        operations = build_offline_user_data_job_operations(
            client=self.mock_client,
            customer_id=customer_id_val,
            conversion_action_id=conversion_action_id_val,
            custom_value=None,
            item_id=None,
            merchant_center_account_id=None,
            country_code=None,
            language_code=None,
            quantity=None,
            ad_user_data_consent=None,
            ad_personalization_consent=None
        )

        self.assertEqual(len(operations), 2)
        self.assertEqual(len(self.created_operations), 2)

        expected_op1_tx_datetime = (self.fixed_now_time - real_timedelta_class(days=30)).strftime("%Y-%m-%d %H:%M:%S")
        expected_op2_tx_datetime = (self.fixed_now_time - real_timedelta_class(days=1)).strftime("%Y-%m-%d %H:%M:%S")

        op1_user_data = self.created_operations[0].create
        self.mock_normalize_hash.assert_any_call("dana@example.com")
        self.assertEqual(len(op1_user_data.user_identifiers), 2)

        email_identifier_op1 = None
        state_identifier_op1 = None
        for uid_mock in op1_user_data.user_identifiers:
            if getattr(uid_mock, 'hashed_email', None) == "hashed_dana@example.com":
                email_identifier_op1 = uid_mock
            else:
                state_identifier_op1 = uid_mock

        self.assertIsNotNone(email_identifier_op1, "Email identifier for Op1 not found")
        self.assertIsNotNone(state_identifier_op1, "State identifier for Op1 not found")

        self.assertEqual(email_identifier_op1.hashed_email, "hashed_dana@example.com")
        self.assertEqual(state_identifier_op1.address_info.state, "NY")
        self.assertIsInstance(state_identifier_op1.address_info.hashed_first_name, MagicMock)
        self.assertIsInstance(state_identifier_op1.address_info.hashed_last_name, MagicMock)
        self.assertIsInstance(state_identifier_op1.address_info.country_code, MagicMock)
        self.assertIsInstance(state_identifier_op1.address_info.postal_code, MagicMock)

        op1_tx_attr = op1_user_data.transaction_attribute
        self.assertEqual(op1_tx_attr.conversion_action, "dummy_ca_path_val")
        self.assertEqual(op1_tx_attr.currency_code, "USD")
        self.assertEqual(op1_tx_attr.transaction_amount_micros, 200000000)
        self.assertEqual(op1_tx_attr.transaction_date_time, expected_op1_tx_datetime)
        self.assertIsNone(op1_tx_attr.custom_value)
        self.assertIsInstance(op1_tx_attr.item_attribute.item_id, MagicMock)

        self.assertIsNone(op1_user_data.consent.ad_user_data)
        self.assertIsNone(op1_user_data.consent.ad_personalization)

        op2_user_data = self.created_operations[1].create
        self.mock_normalize_hash.assert_any_call("Dana")
        self.mock_normalize_hash.assert_any_call("Quinn")
        self.assertEqual(self.mock_normalize_hash.call_count, 3)

        self.assertEqual(len(op2_user_data.user_identifiers), 1)
        address_identifier_op2 = op2_user_data.user_identifiers[0]
        self.assertIsNotNone(address_identifier_op2.address_info)
        addr_info_op2 = address_identifier_op2.address_info
        self.assertEqual(addr_info_op2.hashed_first_name, "hashed_Dana")
        self.assertEqual(addr_info_op2.hashed_last_name, "hashed_Quinn")
        self.assertEqual(addr_info_op2.country_code, "US")
        self.assertEqual(addr_info_op2.postal_code, "10011")

        op2_tx_attr = op2_user_data.transaction_attribute
        self.assertEqual(op2_tx_attr.conversion_action, "dummy_ca_path_val")
        self.assertEqual(op2_tx_attr.currency_code, "EUR")
        self.assertEqual(op2_tx_attr.transaction_amount_micros, 450000000)
        self.assertEqual(op2_tx_attr.transaction_date_time, expected_op2_tx_datetime)
        self.assertIsNone(op2_tx_attr.custom_value)
        self.assertIsInstance(op2_tx_attr.item_attribute.item_id, MagicMock)

        self.assertIsNone(op2_user_data.consent.ad_user_data)
        self.assertIsNone(op2_user_data.consent.ad_personalization)

    def test_build_operations_with_custom_value(self):
        customer_id_val = "test_customer_cv"
        conversion_action_id_val = "ca_id_cv"
        custom_value_val = "test_custom_val_123"

        self.mock_normalize_hash.reset_mock()
        self.created_operations.clear()
        self.created_user_identifiers.clear()
        if hasattr(self.patch_datetime_class_in_sut, 'new') and hasattr(self.patch_datetime_class_in_sut.new, 'now'):
             self.patch_datetime_class_in_sut.new.now.reset_mock()
        if hasattr(self.patch_datetime_class_in_sut, 'new') and hasattr(self.patch_datetime_class_in_sut.new, 'timedelta'):
             self.patch_datetime_class_in_sut.new.timedelta.reset_mock()

        operations = build_offline_user_data_job_operations(
            client=self.mock_client,
            customer_id=customer_id_val,
            conversion_action_id=conversion_action_id_val,
            custom_value=custom_value_val,
            item_id=None,
            merchant_center_account_id=None,
            country_code=None,
            language_code=None,
            quantity=None,
            ad_user_data_consent=None,
            ad_personalization_consent=None
        )
        self.assertEqual(len(operations), 2)

        op1_user_data = self.created_operations[0].create
        self.assertEqual(op1_user_data.transaction_attribute.custom_value, custom_value_val)

        op2_user_data = self.created_operations[1].create
        self.assertIsNone(op2_user_data.transaction_attribute.custom_value)

        self.mock_normalize_hash.assert_any_call("dana@example.com")
        self.mock_normalize_hash.assert_any_call("Dana")
        self.mock_normalize_hash.assert_any_call("Quinn")
        self.assertEqual(self.mock_normalize_hash.call_count, 3)

        expected_op1_tx_datetime = (self.fixed_now_time - real_timedelta_class(days=30)).strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(op1_user_data.transaction_attribute.transaction_date_time, expected_op1_tx_datetime)
        expected_op2_tx_datetime = (self.fixed_now_time - real_timedelta_class(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(op2_user_data.transaction_attribute.transaction_date_time, expected_op2_tx_datetime)

    def test_build_operations_with_item_attributes(self):
        customer_id_val = "test_customer_item"
        conversion_action_id_val = "ca_id_item"
        item_id_val = "item123"
        merchant_id_val = 789000
        country_val = "DE"
        language_val = "de"
        quantity_val = 2

        self.mock_normalize_hash.reset_mock()
        self.created_operations.clear()
        self.created_user_identifiers.clear()
        if hasattr(self.patch_datetime_class_in_sut, 'new') and hasattr(self.patch_datetime_class_in_sut.new, 'now'):
             self.patch_datetime_class_in_sut.new.now.reset_mock()
        if hasattr(self.patch_datetime_class_in_sut, 'new') and hasattr(self.patch_datetime_class_in_sut.new, 'timedelta'):
             self.patch_datetime_class_in_sut.new.timedelta.reset_mock()

        operations = build_offline_user_data_job_operations(
            client=self.mock_client,
            customer_id=customer_id_val,
            conversion_action_id=conversion_action_id_val,
            custom_value=None,
            item_id=item_id_val,
            merchant_center_account_id=merchant_id_val,
            country_code=country_val,
            language_code=language_val,
            quantity=quantity_val,
            ad_user_data_consent=None,
            ad_personalization_consent=None
        )
        self.assertEqual(len(operations), 2)

        op1_user_data = self.created_operations[0].create
        self.assertIsInstance(op1_user_data.transaction_attribute.item_attribute.item_id, MagicMock)

        op2_user_data = self.created_operations[1].create
        item_attr_op2 = op2_user_data.transaction_attribute.item_attribute
        self.assertIsNotNone(item_attr_op2)
        self.assertEqual(item_attr_op2.item_id, item_id_val)
        self.assertEqual(item_attr_op2.merchant_id, merchant_id_val)
        self.assertEqual(item_attr_op2.country_code, country_val)
        self.assertEqual(item_attr_op2.language_code, language_val)
        self.assertEqual(item_attr_op2.quantity, quantity_val)

        self.mock_normalize_hash.assert_any_call("dana@example.com")
        self.mock_normalize_hash.assert_any_call("Dana")
        self.mock_normalize_hash.assert_any_call("Quinn")
        self.assertEqual(self.mock_normalize_hash.call_count, 3)

    def test_build_operations_with_consent(self):
        customer_id_val = "test_customer_consent"
        conversion_action_id_val = "ca_id_consent"
        ad_user_data_consent_str = "GRANTED"
        ad_personalization_consent_str = "DENIED"

        expected_ad_user_data_enum = "ENUM_CONSENT_GRANTED"
        expected_ad_personalization_enum = "ENUM_CONSENT_DENIED"


        self.mock_normalize_hash.reset_mock()
        self.created_operations.clear()
        self.created_user_identifiers.clear()
        if hasattr(self.patch_datetime_class_in_sut, 'new') and hasattr(self.patch_datetime_class_in_sut.new, 'now'):
             self.patch_datetime_class_in_sut.new.now.reset_mock()
        if hasattr(self.patch_datetime_class_in_sut, 'new') and hasattr(self.patch_datetime_class_in_sut.new, 'timedelta'):
             self.patch_datetime_class_in_sut.new.timedelta.reset_mock()

        operations = build_offline_user_data_job_operations(
            client=self.mock_client,
            customer_id=customer_id_val,
            conversion_action_id=conversion_action_id_val,
            custom_value=None,
            item_id=None,
            merchant_center_account_id=None,
            country_code=None,
            language_code=None,
            quantity=None,
            ad_user_data_consent=ad_user_data_consent_str,
            ad_personalization_consent=ad_personalization_consent_str
        )
        self.assertEqual(len(operations), 2)

        op1_user_data = self.created_operations[0].create
        self.assertEqual(op1_user_data.consent.ad_user_data, expected_ad_user_data_enum)
        self.assertEqual(op1_user_data.consent.ad_personalization, expected_ad_personalization_enum)

        op2_user_data = self.created_operations[1].create
        self.assertIsNone(op2_user_data.consent.ad_user_data)
        self.assertIsNone(op2_user_data.consent.ad_personalization)

        self.mock_normalize_hash.assert_any_call("dana@example.com")
        self.mock_normalize_hash.assert_any_call("Dana")
        self.mock_normalize_hash.assert_any_call("Quinn")
        self.assertEqual(self.mock_normalize_hash.call_count, 3)


class TestCreateOfflineUserDataJobStoreSales(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock(spec=GoogleAdsClient)
        self.mock_client.enums = MagicMock()

        self.mock_offline_user_data_job_service = MagicMock(name="OfflineUserDataJobService")

        self.mock_offline_user_data_job = MagicMock(name="OfflineUserDataJobInstance")
        self.mock_store_sales_metadata = MagicMock(name="StoreSalesMetadataInstance")
        self.mock_third_party_metadata = MagicMock(name="ThirdPartyMetadataInstance")

        self.mock_offline_user_data_job.store_sales_metadata = self.mock_store_sales_metadata
        self.mock_store_sales_metadata.third_party_metadata = self.mock_third_party_metadata

        self.original_get_type_create_job = getattr(self.mock_client, 'get_type', None)
        self.mock_client.get_type = MagicMock(return_value=self.mock_offline_user_data_job)


        self.mock_first_party_enum = Mock(name="FIRST_PARTY_ENUM_VAL")
        self.mock_third_party_enum = Mock(name="THIRD_PARTY_ENUM_VAL")

        self.mock_client.enums.OfflineUserDataJobTypeEnum = MagicMock()
        self.mock_client.enums.OfflineUserDataJobTypeEnum.STORE_SALES_UPLOAD_FIRST_PARTY = self.mock_first_party_enum
        self.mock_client.enums.OfflineUserDataJobTypeEnum.STORE_SALES_UPLOAD_THIRD_PARTY = self.mock_third_party_enum

        self.mock_create_job_response = MagicMock(name="CreateJobResponse")
        self.mock_create_job_response.resource_name = "dummy_job_resource_name"
        self.mock_offline_user_data_job_service.create_offline_user_data_job.return_value = self.mock_create_job_response

        self.patcher_stdout = patch('sys.stdout', new_callable=StringIO)
        self.mock_stdout = self.patcher_stdout.start()
        self.addCleanup(self.patcher_stdout.stop)

        self.addCleanup(self.mock_offline_user_data_job_service.reset_mock)
        self.addCleanup(self._restore_original_get_type_create_job)
        self.addCleanup(self.mock_offline_user_data_job.reset_mock)
        self.addCleanup(self.mock_store_sales_metadata.reset_mock)
        self.addCleanup(self.mock_third_party_metadata.reset_mock)

    def _restore_original_get_type_create_job(self):
        if self.original_get_type_create_job:
            self.mock_client.get_type = self.original_get_type_create_job


    def test_create_job_first_party_basic(self):
        customer_id_val = "cust_fp_basic"
        job_type_val = self.mock_first_party_enum

        self.mock_offline_user_data_job.type_ = None
        self.mock_offline_user_data_job.external_id = None
        self.mock_store_sales_metadata.loyalty_fraction = None
        self.mock_store_sales_metadata.transaction_upload_fraction = None
        self.mock_store_sales_metadata.custom_key = None
        self.mock_third_party_metadata.reset_mock()

        resource_name = create_offline_user_data_job(
            client=self.mock_client,
            offline_user_data_job_service=self.mock_offline_user_data_job_service,
            customer_id=customer_id_val,
            offline_user_data_job_type=job_type_val,
            external_id=None,
            advertiser_upload_date_time=None,
            bridge_map_version_id=None,
            partner_id=None,
            custom_key=None
        )

        self.assertEqual(resource_name, "dummy_job_resource_name")
        self.mock_client.get_type.assert_called_once_with("OfflineUserDataJob")

        job = self.mock_offline_user_data_job
        self.assertEqual(job.type_, job_type_val)
        self.assertIsNone(job.external_id)

        ssm = self.mock_store_sales_metadata
        self.assertEqual(ssm.loyalty_fraction, 0.7)
        self.assertEqual(ssm.transaction_upload_fraction, 1.0)
        self.assertIsNone(ssm.custom_key)
        self.assertEqual(self.mock_third_party_metadata.mock_calls, [])

        self.mock_offline_user_data_job_service.create_offline_user_data_job.assert_called_once_with(
            customer_id=customer_id_val, job=self.mock_offline_user_data_job
        )
        self.assertIn(f"Created an offline user data job with resource name '{resource_name}'.", self.mock_stdout.getvalue())

    def test_create_job_first_party_with_optionals(self):
        customer_id_val = "cust_fp_opts"
        job_type_val = self.mock_first_party_enum
        external_id_val = 12345
        custom_key_val = "my_custom_key"

        self.mock_offline_user_data_job.type_ = None
        self.mock_offline_user_data_job.external_id = None
        self.mock_store_sales_metadata.custom_key = None
        self.mock_third_party_metadata.reset_mock()

        resource_name = create_offline_user_data_job(
            client=self.mock_client,
            offline_user_data_job_service=self.mock_offline_user_data_job_service,
            customer_id=customer_id_val,
            offline_user_data_job_type=job_type_val,
            external_id=external_id_val,
            advertiser_upload_date_time=None,
            bridge_map_version_id=None,
            partner_id=None,
            custom_key=custom_key_val
        )

        self.assertEqual(resource_name, "dummy_job_resource_name")
        job = self.mock_offline_user_data_job
        self.assertEqual(job.type_, job_type_val)
        self.assertEqual(job.external_id, external_id_val)

        ssm = self.mock_store_sales_metadata
        self.assertEqual(ssm.loyalty_fraction, 0.7)
        self.assertEqual(ssm.transaction_upload_fraction, 1.0)
        self.assertEqual(ssm.custom_key, custom_key_val)

        self.assertEqual(self.mock_third_party_metadata.mock_calls, [])
        self.mock_offline_user_data_job_service.create_offline_user_data_job.assert_called_once_with(
            customer_id=customer_id_val, job=job
        )

    def test_create_job_third_party_all_args(self):
        customer_id_val = "cust_tp_all"
        job_type_val = self.mock_third_party_enum
        external_id_val = 67890
        custom_key_val = "tp_custom_key"
        advertiser_upload_dt_val = "2023-11-15 09:00:00+00:00"
        bridge_map_id_val = "bridge_v1"
        partner_id_val = 9876

        self.mock_offline_user_data_job.type_ = None
        self.mock_offline_user_data_job.external_id = None
        self.mock_store_sales_metadata.custom_key = None
        self.mock_third_party_metadata.reset_mock()
        self.mock_third_party_metadata.advertiser_upload_date_time = None
        self.mock_third_party_metadata.valid_transaction_fraction = None
        self.mock_third_party_metadata.partner_match_fraction = None
        self.mock_third_party_metadata.partner_upload_fraction = None
        self.mock_third_party_metadata.bridge_map_version_id = None
        self.mock_third_party_metadata.partner_id = None

        resource_name = create_offline_user_data_job(
            client=self.mock_client,
            offline_user_data_job_service=self.mock_offline_user_data_job_service,
            customer_id=customer_id_val,
            offline_user_data_job_type=job_type_val,
            external_id=external_id_val,
            advertiser_upload_date_time=advertiser_upload_dt_val,
            bridge_map_version_id=bridge_map_id_val,
            partner_id=partner_id_val,
            custom_key=custom_key_val
        )

        self.assertEqual(resource_name, "dummy_job_resource_name")
        job = self.mock_offline_user_data_job
        self.assertEqual(job.type_, job_type_val)
        self.assertEqual(job.external_id, external_id_val)

        ssm = self.mock_store_sales_metadata
        self.assertEqual(ssm.loyalty_fraction, 0.7)
        self.assertEqual(ssm.transaction_upload_fraction, 1.0)
        self.assertEqual(ssm.custom_key, custom_key_val)

        tpm = self.mock_third_party_metadata
        self.assertEqual(tpm.advertiser_upload_date_time, advertiser_upload_dt_val)
        self.assertEqual(tpm.valid_transaction_fraction, 1.0)
        self.assertEqual(tpm.partner_match_fraction, 1.0)
        self.assertEqual(tpm.partner_upload_fraction, 1.0)
        self.assertEqual(tpm.bridge_map_version_id, bridge_map_id_val)
        self.assertEqual(tpm.partner_id, partner_id_val)

        self.mock_offline_user_data_job_service.create_offline_user_data_job.assert_called_once_with(
            customer_id=customer_id_val, job=job
        )


class TestPrintGoogleAdsFailuresStoreSales(unittest.TestCase):
    class MockGoogleAdsFailureForTest(object):
        deserialize = None

    class PlainFailureMessagePlaceholder(object):
        pass

    def setUp(self):
        self.mock_client = MagicMock(spec=GoogleAdsClient)

        self.parsed_failure_object_mock = MagicMock(name="ParsedFailureObject_ForPrint")
        TestPrintGoogleAdsFailuresStoreSales.MockGoogleAdsFailureForTest.deserialize = MagicMock(
            return_value=self.parsed_failure_object_mock
        )

        self.plain_failure_message_instance = TestPrintGoogleAdsFailuresStoreSales.PlainFailureMessagePlaceholder()
        self.plain_failure_message_instance.__class__ = TestPrintGoogleAdsFailuresStoreSales.MockGoogleAdsFailureForTest

        self.original_get_type_print_failures = getattr(self.mock_client, 'get_type', None)
        def get_type_side_effect_for_print_failures(type_name):
            if type_name == "GoogleAdsFailure":
                return self.plain_failure_message_instance
            return MagicMock(name=f"Generic_Mock_For_PrintFailures_{type_name}")

        self.mock_client.get_type = MagicMock(side_effect=get_type_side_effect_for_print_failures)

        self.patcher_stdout = patch('sys.stdout', new_callable=StringIO)
        self.mock_stdout = self.patcher_stdout.start()
        self.addCleanup(self.patcher_stdout.stop)
        self.addCleanup(TestPrintGoogleAdsFailuresStoreSales.MockGoogleAdsFailureForTest.deserialize.reset_mock)
        self.addCleanup(self._restore_original_get_type_print_failures)

    def _restore_original_get_type_print_failures(self):
        if self.original_get_type_print_failures:
            self.mock_client.get_type = self.original_get_type_print_failures


    def test_single_detail_single_error(self):
        mock_detail1 = MagicMock(name="Detail1")
        mock_detail1.value = b"error_bytes_1"
        mock_status_obj = MagicMock(name="StatusObject")
        mock_status_obj.details = [mock_detail1]

        mock_error_location = MagicMock()
        mock_field_path_element = MagicMock(index=0)
        mock_error_location.field_path_elements = [mock_field_path_element]

        mock_error_code = Mock(name="ErrorCode_obj")
        mock_error_code.__str__ = Mock(return_value="CODE_A_STR")

        parsed_error = MagicMock(name="ParsedError1")
        parsed_error.location = mock_error_location
        parsed_error.message = "Specific error message for detail 1."
        parsed_error.error_code = mock_error_code

        self.parsed_failure_object_mock.errors = [parsed_error]
        TestPrintGoogleAdsFailuresStoreSales.MockGoogleAdsFailureForTest.deserialize.return_value = self.parsed_failure_object_mock

        print_google_ads_failures(self.mock_client, mock_status_obj)

        TestPrintGoogleAdsFailuresStoreSales.MockGoogleAdsFailureForTest.deserialize.assert_called_once_with(b"error_bytes_1")
        output = self.mock_stdout.getvalue()

        self.assertIn("A partial failure or warning at index 0 occurred.", output)
        self.assertIn("Message: Specific error message for detail 1.", output)
        self.assertIn("Code: CODE_A_STR", output)

    def test_multiple_details_and_errors(self):
        mock_detail1 = MagicMock(name="Detail1", value=b"error_bytes_1")
        mock_detail2 = MagicMock(name="Detail2", value=b"error_bytes_2")
        mock_status_obj = MagicMock(name="StatusObject_Multi", details=[mock_detail1, mock_detail2])

        parsed_error1_1 = MagicMock(name="ParsedError1.1")
        parsed_error1_1.location.field_path_elements = [MagicMock(index=0)]
        parsed_error1_1.message = "Error 1 for detail 1."
        parsed_error1_1.error_code = Mock(name="CODE_1_1_obj", __str__=lambda s: "CODE_1_1")
        parsed_failure_obj1 = MagicMock(name="ParsedFailure1", errors=[parsed_error1_1])

        parsed_error2_1 = MagicMock(name="ParsedError2.1")
        parsed_error2_1.location.field_path_elements = [MagicMock(index=1)]
        parsed_error2_1.message = "Error 1 for detail 2."
        parsed_error2_1.error_code = Mock(name="CODE_2_1_obj", __str__=lambda s: "CODE_2_1")

        parsed_error2_2 = MagicMock(name="ParsedError2.2")
        parsed_error2_2.location.field_path_elements = [MagicMock(index=2)]
        parsed_error2_2.message = "Error 2 for detail 2."
        parsed_error2_2.error_code = Mock(name="CODE_2_2_obj", __str__=lambda s: "CODE_2_2")
        parsed_failure_obj2 = MagicMock(name="ParsedFailure2", errors=[parsed_error2_1, parsed_error2_2])

        TestPrintGoogleAdsFailuresStoreSales.MockGoogleAdsFailureForTest.deserialize.side_effect = [
            parsed_failure_obj1, parsed_failure_obj2
        ]

        print_google_ads_failures(self.mock_client, mock_status_obj)

        self.assertEqual(TestPrintGoogleAdsFailuresStoreSales.MockGoogleAdsFailureForTest.deserialize.call_count, 2)
        TestPrintGoogleAdsFailuresStoreSales.MockGoogleAdsFailureForTest.deserialize.assert_any_call(b"error_bytes_1")
        TestPrintGoogleAdsFailuresStoreSales.MockGoogleAdsFailureForTest.deserialize.assert_any_call(b"error_bytes_2")

        output = self.mock_stdout.getvalue()
        self.assertIn("A partial failure or warning at index 0 occurred.\nMessage: Error 1 for detail 1.\nCode: CODE_1_1", output)
        self.assertIn("A partial failure or warning at index 1 occurred.\nMessage: Error 1 for detail 2.\nCode: CODE_2_1", output)
        self.assertIn("A partial failure or warning at index 2 occurred.\nMessage: Error 2 for detail 2.\nCode: CODE_2_2", output)

    def test_empty_details_list(self):
        mock_status_obj = MagicMock(name="StatusObject_Empty", details=[])

        print_google_ads_failures(self.mock_client, mock_status_obj)

        TestPrintGoogleAdsFailuresStoreSales.MockGoogleAdsFailureForTest.deserialize.assert_not_called()
        self.assertEqual(self.mock_stdout.getvalue(), "")


class TestAddTransactionsToJobStoreSales(unittest.TestCase):
    class MockGoogleAdsFailureForTestInAddTx(object):
        deserialize = None

    class PlainFailureMessagePlaceholderInAddTx(object):
        pass

    def setUp(self):
        self.mock_client = MagicMock(spec=GoogleAdsClient)

        self.mock_offline_user_data_job_service = MagicMock(name="OfflineUserDataJobService")
        self.mock_add_ops_response = MagicMock(name="AddOperationsResponse")
        self.mock_offline_user_data_job_service.add_offline_user_data_job_operations.return_value = self.mock_add_ops_response

        self.mock_add_ops_request = MagicMock(name="AddOfflineUserDataJobOperationsRequestInstance")

        self.parsed_failure_object_for_print_add_tx = MagicMock(name="ParsedFailureObject_ForAddTx")
        TestAddTransactionsToJobStoreSales.MockGoogleAdsFailureForTestInAddTx.deserialize = MagicMock(
            return_value=self.parsed_failure_object_for_print_add_tx
        )
        self.plain_failure_message_instance_for_add_tx = TestAddTransactionsToJobStoreSales.PlainFailureMessagePlaceholderInAddTx()
        self.plain_failure_message_instance_for_add_tx.__class__ = TestAddTransactionsToJobStoreSales.MockGoogleAdsFailureForTestInAddTx

        self.original_get_type_add_tx = getattr(self.mock_client, 'get_type', None)
        def get_type_side_effect_for_add_tx(type_name):
            if type_name == "AddOfflineUserDataJobOperationsRequest":
                self.mock_add_ops_request.operations = []
                return self.mock_add_ops_request
            elif type_name == "GoogleAdsFailure":
                return self.plain_failure_message_instance_for_add_tx
            return MagicMock(name=f"DefaultMock_AddTx_{type_name}")

        self.mock_client.get_type = MagicMock(side_effect=get_type_side_effect_for_add_tx)

        self.mock_op1 = Mock(name="Op1FromBuild")
        self.mock_op2 = Mock(name="Op2FromBuild")
        self.patch_build_ops = patch(
            "examples.remarketing.upload_store_sales_transactions.build_offline_user_data_job_operations",
            return_value=[self.mock_op1, self.mock_op2]
        )
        self.mocked_build_ops = self.patch_build_ops.start()
        self.addCleanup(self.patch_build_ops.stop)

        self.patch_print_failures = patch(
            "examples.remarketing.upload_store_sales_transactions.print_google_ads_failures"
        )
        self.mocked_print_failures = self.patch_print_failures.start()
        self.addCleanup(self.patch_print_failures.stop)

        self.patcher_stdout = patch('sys.stdout', new_callable=StringIO)
        self.mock_stdout = self.patcher_stdout.start()
        self.addCleanup(self.patcher_stdout.stop)

        self.addCleanup(self.mock_offline_user_data_job_service.reset_mock)
        self.addCleanup(self._restore_original_get_type_add_tx)
        self.addCleanup(TestAddTransactionsToJobStoreSales.MockGoogleAdsFailureForTestInAddTx.deserialize.reset_mock)

    def _restore_original_get_type_add_tx(self):
        if self.original_get_type_add_tx:
            self.mock_client.get_type = self.original_get_type_add_tx


    def test_add_transactions_success_no_failures_no_warnings(self):
        self.mock_add_ops_response.partial_failure_error = None
        self.mock_add_ops_response.warning = None

        dummy_customer_id = "cust_add_tx_succ"
        dummy_job_rn = "job_rn_succ"
        dummy_conv_action_id = "conv_act_succ"

        self.mocked_build_ops.reset_mock()
        self.mock_offline_user_data_job_service.add_offline_user_data_job_operations.reset_mock()
        self.mocked_print_failures.reset_mock()
        self.mock_client.get_type.reset_mock()


        add_transactions_to_offline_user_data_job(
            client=self.mock_client,
            offline_user_data_job_service=self.mock_offline_user_data_job_service,
            customer_id=dummy_customer_id,
            offline_user_data_job_resource_name=dummy_job_rn,
            conversion_action_id=dummy_conv_action_id,
            custom_value=None, item_id=None, merchant_center_account_id=None,
            country_code=None, language_code=None, quantity=None,
            ad_user_data_consent=None, ad_personalization_consent=None
        )

        self.mocked_build_ops.assert_called_once_with(
            self.mock_client, dummy_customer_id, dummy_conv_action_id,
            None, None, None, None, None, None, None, None
        )

        self.mock_client.get_type.assert_called_once_with("AddOfflineUserDataJobOperationsRequest")
        self.assertEqual(self.mock_add_ops_request.resource_name, dummy_job_rn)
        self.assertTrue(self.mock_add_ops_request.enable_partial_failure)
        self.assertTrue(self.mock_add_ops_request.enable_warnings)
        self.assertEqual(self.mock_add_ops_request.operations, [self.mock_op1, self.mock_op2])

        self.mock_offline_user_data_job_service.add_offline_user_data_job_operations.assert_called_once_with(
            request=self.mock_add_ops_request
        )
        self.mocked_print_failures.assert_not_called()
        self.assertIn(f"Successfully added {len([self.mock_op1, self.mock_op2])} to the offline user data job.", self.mock_stdout.getvalue())

    def test_add_transactions_with_partial_failure(self):
        mock_status_failure = MagicMock(name="StatusFailureObj")
        self.mock_add_ops_response.partial_failure_error = mock_status_failure
        self.mock_add_ops_response.warning = None

        dummy_customer_id = "cust_add_tx_fail"
        dummy_job_rn = "job_rn_fail"
        dummy_conv_action_id = "conv_act_fail"

        self.mocked_build_ops.reset_mock()
        self.mock_offline_user_data_job_service.add_offline_user_data_job_operations.reset_mock()
        self.mocked_print_failures.reset_mock()

        add_transactions_to_offline_user_data_job(
            client=self.mock_client,
            offline_user_data_job_service=self.mock_offline_user_data_job_service,
            customer_id=dummy_customer_id,
            offline_user_data_job_resource_name=dummy_job_rn,
            conversion_action_id=dummy_conv_action_id,
            custom_value=None, item_id=None, merchant_center_account_id=None,
            country_code=None, language_code=None, quantity=None,
            ad_user_data_consent=None, ad_personalization_consent=None
        )

        self.mocked_build_ops.assert_called_once()
        self.mock_offline_user_data_job_service.add_offline_user_data_job_operations.assert_called_once()

        # Corrected: SUT calls print_google_ads_failures with only one argument (the status object)
        self.mocked_print_failures.assert_called_once_with(mock_status_failure)
        self.assertNotIn("Successfully added", self.mock_stdout.getvalue())

    def test_add_transactions_with_warning(self):
        mock_status_warning = MagicMock(name="StatusWarningObj")
        self.mock_add_ops_response.partial_failure_error = None
        self.mock_add_ops_response.warning = mock_status_warning

        dummy_customer_id = "cust_add_tx_warn"
        dummy_job_rn = "job_rn_warn"
        dummy_conv_action_id = "conv_act_warn"

        self.mocked_build_ops.reset_mock()
        self.mock_offline_user_data_job_service.add_offline_user_data_job_operations.reset_mock()
        self.mocked_print_failures.reset_mock()

        add_transactions_to_offline_user_data_job(
            client=self.mock_client,
            offline_user_data_job_service=self.mock_offline_user_data_job_service,
            customer_id=dummy_customer_id,
            offline_user_data_job_resource_name=dummy_job_rn,
            conversion_action_id=dummy_conv_action_id,
            custom_value=None, item_id=None, merchant_center_account_id=None,
            country_code=None, language_code=None, quantity=None,
            ad_user_data_consent=None, ad_personalization_consent=None
        )

        self.mocked_build_ops.assert_called_once()
        self.mock_offline_user_data_job_service.add_offline_user_data_job_operations.assert_called_once()

        self.mocked_print_failures.assert_called_once_with(mock_status_warning)
        self.assertIn(f"Successfully added {len([self.mock_op1, self.mock_op2])} to the offline user data job.", self.mock_stdout.getvalue())

    def test_add_transactions_with_both_failure_and_warning(self):
        mock_status_failure = MagicMock(name="StatusFailureObj")
        mock_status_warning = MagicMock(name="StatusWarningObj")
        self.mock_add_ops_response.partial_failure_error = mock_status_failure
        self.mock_add_ops_response.warning = mock_status_warning

        dummy_customer_id = "cust_add_tx_both"
        dummy_job_rn = "job_rn_both"
        dummy_conv_action_id = "conv_act_both"

        self.mocked_build_ops.reset_mock()
        self.mock_offline_user_data_job_service.add_offline_user_data_job_operations.reset_mock()
        self.mocked_print_failures.reset_mock()

        add_transactions_to_offline_user_data_job(
            client=self.mock_client,
            offline_user_data_job_service=self.mock_offline_user_data_job_service,
            customer_id=dummy_customer_id,
            offline_user_data_job_resource_name=dummy_job_rn,
            conversion_action_id=dummy_conv_action_id,
            custom_value=None, item_id=None, merchant_center_account_id=None,
            country_code=None, language_code=None, quantity=None,
            ad_user_data_consent=None, ad_personalization_consent=None
        )

        self.mocked_build_ops.assert_called_once()
        self.mock_offline_user_data_job_service.add_offline_user_data_job_operations.assert_called_once()

        self.assertEqual(self.mocked_print_failures.call_count, 2)
        self.mocked_print_failures.assert_any_call(mock_status_failure)
        self.mocked_print_failures.assert_any_call(mock_status_warning)

        self.assertNotIn("Successfully added", self.mock_stdout.getvalue())


class TestCheckJobStatusStoreSales(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock(spec=GoogleAdsClient)
        self.mock_client.enums = MagicMock()

        self.mock_google_ads_service = MagicMock(name="GoogleAdsService")

        self.original_get_service_check_job = getattr(self.mock_client, 'get_service', None)
        self.mock_client.get_service = MagicMock(return_value=self.mock_google_ads_service)

        self.mock_job_type_obj_for_name_method = MagicMock(name="OfflineUserDataJobType_DOT_OfflineUserDataJobType")
        self.mock_job_type_obj_for_name_method.Name = Mock(side_effect=lambda val: f"TYPENAME_FOR_{val}")
        self.mock_client.enums.OfflineUserDataJobTypeEnum.OfflineUserDataJobType = self.mock_job_type_obj_for_name_method

        self.mock_job_status_obj_for_name_method = MagicMock(name="OfflineUserDataJobStatus_DOT_OfflineUserDataJobStatus")
        self.mock_job_status_obj_for_name_method.Name = Mock(side_effect=lambda val: f"STATUSNAME_FOR_{val}")

        self.status_val_failed = "FAILED_STATUS_VAL"
        self.status_val_pending = "PENDING_STATUS_VAL"
        self.status_val_running = "RUNNING_STATUS_VAL"
        self.status_val_success = "SUCCESS_STATUS_VAL"
        self.status_val_unknown = "UNKNOWN_STATUS_VAL"

        enum_status_parent_mock = MagicMock(name="OfflineUserDataJobStatusEnum_Parent")
        enum_status_parent_mock.OfflineUserDataJobStatus = self.mock_job_status_obj_for_name_method
        enum_status_parent_mock.FAILED = self.status_val_failed
        enum_status_parent_mock.PENDING = self.status_val_pending
        enum_status_parent_mock.RUNNING = self.status_val_running
        enum_status_parent_mock.SUCCESS = self.status_val_success
        self.mock_client.enums.OfflineUserDataJobStatusEnum = enum_status_parent_mock

        self.mock_googleads_row = MagicMock(name="GoogleAdsRow")
        self.mock_offline_user_data_job_from_search = MagicMock(name="OfflineUserDataJob_FromSearch")
        self.mock_googleads_row.offline_user_data_job = self.mock_offline_user_data_job_from_search

        self.mock_google_ads_service.search.return_value = [self.mock_googleads_row]

        self.patcher_stdout = patch('sys.stdout', new_callable=StringIO)
        self.mock_stdout = self.patcher_stdout.start()
        self.addCleanup(self.patcher_stdout.stop)
        self.addCleanup(self.mock_google_ads_service.reset_mock)
        self.addCleanup(self._restore_original_client_methods_check_job)

    def _restore_original_client_methods_check_job(self):
        if self.original_get_service_check_job:
            self.mock_client.get_service = self.original_get_service_check_job

    def test_job_status_success(self):
        customer_id = "dummy_customer_id_succ"
        job_resource_name = "dummy_job_rn_succ"
        job_id_from_sut = "job123"
        job_type_val_from_sut = 4

        self.mock_offline_user_data_job_from_search.id = job_id_from_sut
        self.mock_offline_user_data_job_from_search.status = self.status_val_success
        self.mock_offline_user_data_job_from_search.type = job_type_val_from_sut
        self.mock_offline_user_data_job_from_search.failure_reason = None

        check_job_status(self.mock_client, customer_id, job_resource_name)

        expected_query = f"""
        SELECT
          offline_user_data_job.resource_name,
          offline_user_data_job.id,
          offline_user_data_job.status,
          offline_user_data_job.type,
          offline_user_data_job.failure_reason
        FROM offline_user_data_job
        WHERE offline_user_data_job.resource_name =
          '{job_resource_name}'"""
        self.mock_google_ads_service.search.assert_called_once_with(customer_id=customer_id, query=expected_query)

        output = self.mock_stdout.getvalue()
        self.assertIn(f"Offline user data job ID {job_id_from_sut} with type 'TYPENAME_FOR_{job_type_val_from_sut}' has status STATUSNAME_FOR_{self.status_val_success}.", output)
        self.assertIn("The requested job has completed successfully.", output)
        self.assertNotIn("Failure reason:", output)
        self.assertNotIn("To check the status of the job periodically", output)

    def test_job_status_failed(self):
        customer_id = "dummy_customer_id_fail"
        job_resource_name = "dummy_job_rn_fail"
        job_id_from_sut = "job456"
        job_type_val_from_sut = 1
        failure_reason_val = "Test failure reason from SUT"

        self.mock_offline_user_data_job_from_search.id = job_id_from_sut
        self.mock_offline_user_data_job_from_search.status = self.status_val_failed
        self.mock_offline_user_data_job_from_search.type = job_type_val_from_sut
        self.mock_offline_user_data_job_from_search.failure_reason = failure_reason_val

        self.mock_google_ads_service.search.return_value = [self.mock_googleads_row]

        check_job_status(self.mock_client, customer_id, job_resource_name)

        output = self.mock_stdout.getvalue()
        self.assertIn(f"Offline user data job ID {job_id_from_sut} with type 'TYPENAME_FOR_{job_type_val_from_sut}' has status STATUSNAME_FOR_{self.status_val_failed}.", output)
        self.assertIn(f"\tFailure reason: {failure_reason_val}", output)
        self.assertNotIn("completed successfully", output)
        self.assertNotIn("To check the status of the job periodically", output)

    def test_job_status_pending(self):
        customer_id = "dummy_customer_id_pend"
        job_resource_name = "dummy_job_rn_pend"
        job_id_from_sut = "job789"
        job_type_val_from_sut = 2

        self.mock_offline_user_data_job_from_search.id = job_id_from_sut
        self.mock_offline_user_data_job_from_search.status = self.status_val_pending
        self.mock_offline_user_data_job_from_search.type = job_type_val_from_sut

        self.mock_google_ads_service.search.return_value = [self.mock_googleads_row]
        expected_query = f"""
        SELECT
          offline_user_data_job.resource_name,
          offline_user_data_job.id,
          offline_user_data_job.status,
          offline_user_data_job.type,
          offline_user_data_job.failure_reason
        FROM offline_user_data_job
        WHERE offline_user_data_job.resource_name =
          '{job_resource_name}'"""

        check_job_status(self.mock_client, customer_id, job_resource_name)

        output = self.mock_stdout.getvalue()
        self.assertIn(f"Offline user data job ID {job_id_from_sut} with type 'TYPENAME_FOR_{job_type_val_from_sut}' has status STATUSNAME_FOR_{self.status_val_pending}.", output)
        self.assertIn("To check the status of the job periodically", output)
        self.assertIn(expected_query, output)
        self.assertNotIn("completed successfully", output)
        self.assertNotIn("Failure reason:", output)

    def test_job_status_running(self):
        customer_id = "dummy_customer_id_run"
        job_resource_name = "dummy_job_rn_run"
        job_id_from_sut = "job012"
        job_type_val_from_sut = 3

        self.mock_offline_user_data_job_from_search.id = job_id_from_sut
        self.mock_offline_user_data_job_from_search.status = self.status_val_running
        self.mock_offline_user_data_job_from_search.type = job_type_val_from_sut

        self.mock_google_ads_service.search.return_value = [self.mock_googleads_row]
        expected_query = f"""
        SELECT
          offline_user_data_job.resource_name,
          offline_user_data_job.id,
          offline_user_data_job.status,
          offline_user_data_job.type,
          offline_user_data_job.failure_reason
        FROM offline_user_data_job
        WHERE offline_user_data_job.resource_name =
          '{job_resource_name}'"""

        check_job_status(self.mock_client, customer_id, job_resource_name)

        output = self.mock_stdout.getvalue()
        self.assertIn(f"Offline user data job ID {job_id_from_sut} with type 'TYPENAME_FOR_{job_type_val_from_sut}' has status STATUSNAME_FOR_{self.status_val_running}.", output)
        self.assertIn("To check the status of the job periodically", output)
        self.assertIn(expected_query, output)
        self.assertNotIn("completed successfully", output)
        self.assertNotIn("Failure reason:", output)

    def test_job_status_unknown_raises_error(self):
        customer_id = "dummy_customer_id_unk"
        job_resource_name = "dummy_job_rn_unk"
        job_id_from_sut = "job345"
        job_type_val_from_sut = 0

        self.mock_offline_user_data_job_from_search.id = job_id_from_sut
        self.mock_offline_user_data_job_from_search.status = self.status_val_unknown
        self.mock_offline_user_data_job_from_search.type = job_type_val_from_sut

        self.mock_google_ads_service.search.return_value = [self.mock_googleads_row]

        with self.assertRaisesRegex(ValueError, "Requested job has UNKNOWN or UNSPECIFIED status."):
            check_job_status(self.mock_client, customer_id, job_resource_name)


class TestMainFunctionStoreSales(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock(spec=GoogleAdsClient)
        # Ensure client.enums exists for main SUT function
        self.mock_client.enums = MagicMock()

        # Mock OfflineUserDataJobTypeEnum for argparse defaults in main
        # These need to be actual enum-like objects if SUT accesses .value or .name on them directly
        # SUT argparse default: googleads_client.enums.OfflineUserDataJobTypeEnum.STORE_SALES_UPLOAD_FIRST_PARTY
        # SUT argparse choices for consent: [e.name for e in googleads_client.enums.ConsentStatusEnum]

        # For OfflineUserDataJobTypeEnum default in argparse
        mock_first_party_job_type_enum_member = Mock(name="STORE_SALES_UPLOAD_FIRST_PARTY_MEMBER")
        # If SUT uses .value for default, then: mock_first_party_job_type_enum_member.value = some_int_val
        # However, argparse default directly takes the enum member.
        self.mock_client.enums.OfflineUserDataJobTypeEnum.STORE_SALES_UPLOAD_FIRST_PARTY = mock_first_party_job_type_enum_member

        # For ConsentStatusEnum choices in argparse
        # SUT: choices=[e.name for e in googleads_client.enums.ConsentStatusEnum]
        # This means googleads_client.enums.ConsentStatusEnum should be an iterable of objects having a .name attribute.
        # The dict used by other test classes' setUp won't work directly for this.
        # Let's make it a list of mocks for argparse.
        mock_consent_granted = Mock(name="GRANTED")
        mock_consent_denied = Mock(name="DENIED")
        mock_consent_unspecified = Mock(name="UNSPECIFIED")
        self.mock_client.enums.ConsentStatusEnum = [mock_consent_granted, mock_consent_denied, mock_consent_unspecified]


        self.mock_offline_user_data_job_service_for_main = MagicMock(name="OfflineUserDataJobService_for_main")
        self.mock_offline_user_data_job_service_for_main.run_offline_user_data_job = MagicMock(name="run_offline_job_mock")

        # Store original get_service for restoration
        self.original_get_service_main = getattr(self.mock_client, 'get_service', None)
        self.mock_client.get_service = MagicMock(return_value=self.mock_offline_user_data_job_service_for_main)

        self.patch_create_job = patch(
            "examples.remarketing.upload_store_sales_transactions.create_offline_user_data_job"
        )
        self.mocked_create_job = self.patch_create_job.start()
        self.mocked_create_job.return_value = "dummy_job_resource_name_from_create"
        self.addCleanup(self.patch_create_job.stop)

        self.patch_add_transactions = patch(
            "examples.remarketing.upload_store_sales_transactions.add_transactions_to_offline_user_data_job"
        )
        self.mocked_add_transactions = self.patch_add_transactions.start()
        self.addCleanup(self.patch_add_transactions.stop)

        self.patch_check_status = patch(
            "examples.remarketing.upload_store_sales_transactions.check_job_status"
        )
        self.mocked_check_status = self.patch_check_status.start()
        self.addCleanup(self.patch_check_status.stop)
        self.addCleanup(self._restore_original_client_methods_main)

    def _restore_original_client_methods_main(self):
        if self.original_get_service_main:
            self.mock_client.get_service = self.original_get_service_main


    def test_main_orchestration_flow(self, mock_load_storage): # mock_load_storage from class decorator
        # Dummy args for main function
        args_customer_id = "main_cust_id"
        args_conversion_action_id = 12345 # SUT argparse takes int
        args_offline_user_data_job_type = self.mock_client.enums.OfflineUserDataJobTypeEnum.STORE_SALES_UPLOAD_FIRST_PARTY # Use the mock
        args_external_id = 67890
        args_advertiser_upload_date_time = "2023-01-01 12:00:00+00:00"
        args_bridge_map_version_id = "v1"
        args_partner_id = 777
        args_custom_key = "ckey"
        args_custom_value = "cval" # This will be passed to add_transactions, not create_job
        args_item_id = "item001"
        args_merchant_center_account_id = 998877
        args_country_code = "US"
        args_language_code = "en"
        args_quantity = 1
        args_ad_user_data_consent = "GRANTED"
        args_ad_personalization_consent = "DENIED"

        main_sut(
            client=self.mock_client,
            customer_id=args_customer_id,
            conversion_action_id=args_conversion_action_id,
            offline_user_data_job_type=args_offline_user_data_job_type,
            external_id=args_external_id,
            advertiser_upload_date_time=args_advertiser_upload_date_time,
            bridge_map_version_id=args_bridge_map_version_id,
            partner_id=args_partner_id,
            custom_key=args_custom_key,
            custom_value=args_custom_value, # This is for add_transactions
            item_id=args_item_id,
            merchant_center_account_id=args_merchant_center_account_id,
            country_code=args_country_code,
            language_code=args_language_code,
            quantity=args_quantity,
            ad_user_data_consent=args_ad_user_data_consent,
            ad_personalization_consent=args_ad_personalization_consent
        )

        # Assert create_offline_user_data_job call
        self.mock_client.get_service.assert_called_with("OfflineUserDataJobService") # Main SUT calls this first
        self.mocked_create_job.assert_called_once_with(
            self.mock_client,
            self.mock_offline_user_data_job_service_for_main,
            args_customer_id,
            args_offline_user_data_job_type,
            args_external_id,
            args_advertiser_upload_date_time,
            args_bridge_map_version_id,
            args_partner_id,
            args_custom_key
        )

        # Assert add_transactions_to_offline_user_data_job call
        self.mocked_add_transactions.assert_called_once_with(
            self.mock_client,
            self.mock_offline_user_data_job_service_for_main,
            args_customer_id,
            "dummy_job_resource_name_from_create", # Result from create_job
            args_conversion_action_id,
            args_custom_value, # custom_value is for add_transactions
            args_item_id,
            args_merchant_center_account_id,
            args_country_code,
            args_language_code,
            args_quantity,
            args_ad_user_data_consent,
            args_ad_personalization_consent
        )

        # Assert run_offline_user_data_job service call
        self.mock_offline_user_data_job_service_for_main.run_offline_user_data_job.assert_called_once_with(
            resource_name="dummy_job_resource_name_from_create"
        )

        # Assert check_job_status call
        self.mocked_check_status.assert_called_once_with(
            self.mock_client,
            args_customer_id,
            "dummy_job_resource_name_from_create"
        )


if __name__ == "__main__":
    unittest.main()
