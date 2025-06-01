import unittest
from unittest.mock import patch, Mock, call, ANY
import hashlib
import io
import sys
from types import SimpleNamespace

# SUT (System Under Test)
from examples.remarketing import add_customer_match_user_list

# Store original built-in type for restoration/delegation in tests
BUILTIN_TYPE_ORIGINAL = type

class TestNormalizeAndHash(unittest.TestCase):
    def _get_expected_hash(self, value_to_hash):
        return hashlib.sha256(value_to_hash.encode('utf-8')).hexdigest()

    def test_normalize_and_hash_with_remove_all_whitespace_true(self):
        test_cases = [
            ("  Test Mixed Case  ", "TestMixedCase"), ("UPPERCASE", "UPPERCASE"),
            ("lowercase", "lowercase"), ("  leading and trailing  ", "leadingandtrailing"),
            ("internal spaces only", "internalspacesonly"),
            ("Test.With.Dots@example.com", "Test.With.Dots@example.com"),
            ("Test+Plus@example.com", "Test+Plus@example.com"),
            ("", ""), ("   ", ""),
        ]
        for original_string, string_before_hash in test_cases:
            with self.subTest(original_string=original_string, remove_all_whitespace=True):
                expected_hash = self._get_expected_hash(string_before_hash)
                actual_hash = add_customer_match_user_list.normalize_and_hash(
                    original_string, True
                )
                self.assertEqual(actual_hash, expected_hash)

    def test_normalize_and_hash_with_remove_all_whitespace_false(self):
        test_cases = [
            ("  Test Mixed Case  ", "test mixed case"), ("UPPERCASE", "uppercase"),
            ("lowercase", "lowercase"), ("  leading and trailing  ", "leading and trailing"),
            ("internal spaces only", "internal spaces only"),
            ("  Internal Spaces Preserved  ", "internal spaces preserved"),
            ("Test.With.Dots@example.com", "test.with.dots@example.com"),
            ("Test+Plus@example.com", "test+plus@example.com"),
            ("", ""), ("   ", ""),
        ]
        for original_string, string_before_hash in test_cases:
            with self.subTest(original_string=original_string, remove_all_whitespace=False):
                expected_hash = self._get_expected_hash(string_before_hash)
                actual_hash = add_customer_match_user_list.normalize_and_hash(
                    original_string, False
                )
                self.assertEqual(actual_hash, expected_hash)


class TestBuildOfflineUserDataJobOperations(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock(name="GoogleAdsClientMock_BuildOps")
        self.mock_normalize_and_hash_patcher = patch(
            'examples.remarketing.add_customer_match_user_list.normalize_and_hash'
        )
        self.mock_normalize_and_hash = self.mock_normalize_and_hash_patcher.start()
        self.addCleanup(self.mock_normalize_and_hash_patcher.stop)

        def normalize_side_effect(s, remove_all_whitespace):
            flag = "T" if remove_all_whitespace else "F"
            return f"hashed_{s}_{flag}"
        self.mock_normalize_and_hash.side_effect = normalize_side_effect

        self.user_data_mocks = []
        self.user_identifier_mocks_created = []

        def get_type_side_effect(type_name):
            if type_name == "UserData":
                user_data_mock = Mock(name=f"UserDataMock_{len(self.user_data_mocks)}")
                user_data_mock.user_identifiers = []
                self.user_data_mocks.append(user_data_mock)
                return user_data_mock
            elif type_name == "UserIdentifier":
                uid_mock = Mock(name=f"UserIdentifierMock_{len(self.user_identifier_mocks_created)}")
                uid_mock.address_info = Mock(name=f"AddressInfoFor_UID_{len(self.user_identifier_mocks_created)}")
                self.user_identifier_mocks_created.append(uid_mock)
                return uid_mock
            elif type_name == "OfflineUserDataJobOperation":
                op_mock = Mock(name="OfflineUserDataJobOperationMock")
                return op_mock
            return Mock(name=f"DefaultMock_for_{type_name}")

        self.mock_client.get_type.side_effect = get_type_side_effect

    def test_build_operations_structure_and_hashing_calls(self):
        operations = add_customer_match_user_list.build_offline_user_data_job_operations(
            self.mock_client
        )
        expected_normalize_calls = [
            call("dana@example.com", True), call("+1 800 5550101", True),
            call("alex.2@example.com", True), call("+1 800 5550102", True),
            call("Alex", False), call("Quinn", False),
            call("charlie@example.com", True)
        ]
        self.mock_normalize_and_hash.assert_has_calls(expected_normalize_calls, any_order=False)
        self.assertEqual(self.mock_normalize_and_hash.call_count, len(expected_normalize_calls))
        self.assertEqual(len(operations), 3)
        op1_user_data = operations[0].create; self.assertEqual(len(op1_user_data.user_identifiers), 2)
        self.assertEqual(op1_user_data.user_identifiers[0].hashed_email, "hashed_dana@example.com_T")
        self.assertEqual(op1_user_data.user_identifiers[1].hashed_phone_number, "hashed_+1 800 5550101_T")
        op2_user_data = operations[1].create; self.assertEqual(len(op2_user_data.user_identifiers), 3)
        self.assertEqual(op2_user_data.user_identifiers[0].hashed_email, "hashed_alex.2@example.com_T")
        self.assertEqual(op2_user_data.user_identifiers[1].hashed_phone_number, "hashed_+1 800 5550102_T")
        op2_address_identifier = op2_user_data.user_identifiers[2]
        self.assertEqual(op2_address_identifier.address_info.hashed_first_name, "hashed_Alex_F")
        self.assertEqual(op2_address_identifier.address_info.hashed_last_name, "hashed_Quinn_F")
        self.assertEqual(op2_address_identifier.address_info.country_code, "US")
        self.assertEqual(op2_address_identifier.address_info.postal_code, "94045")
        op3_user_data = operations[2].create; self.assertEqual(len(op3_user_data.user_identifiers), 1)
        self.assertEqual(op3_user_data.user_identifiers[0].hashed_email, "hashed_charlie@example.com_T")


class TestCreateCustomerMatchUserList(unittest.TestCase):
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_create_list_success_and_returns_name(self, mock_stdout):
        mock_client = Mock(name="GoogleAdsClientMock_for_create_list")
        test_customer_id = "dummy_customer_123"
        mock_resource_name = f"customers/{test_customer_id}/userLists/user_list_mock_id"
        mock_client.enums = SimpleNamespace(
            CustomerMatchUploadKeyTypeEnum=SimpleNamespace(CONTACT_INFO="mock_contact_info_enum_val")
        )
        mock_user_list_service = Mock(name="UserListServiceMock")
        mock_client.get_service.return_value = mock_user_list_service
        mock_mutate_response = Mock(name="MutateUserListsResponseMock")
        mock_result = Mock(name="UserListResultMock"); mock_result.resource_name = mock_resource_name
        mock_mutate_response.results = [mock_result]
        mock_user_list_service.mutate_user_lists.return_value = mock_mutate_response
        mock_user_list_operation = Mock(name="UserListOperationMock")
        mock_user_list_obj = Mock(name="UserListMock")
        mock_user_list_obj.crm_based_user_list = Mock(name="CrmBasedUserListInfoMock")
        mock_user_list_operation.create = mock_user_list_obj
        mock_client.get_type.return_value = mock_user_list_operation

        returned_resource_name = add_customer_match_user_list.create_customer_match_user_list(
            mock_client, test_customer_id
        )
        mock_client.get_service.assert_called_once_with("UserListService")
        mock_client.get_type.assert_called_once_with("UserListOperation")
        mock_user_list_service.mutate_user_lists.assert_called_once()
        mutate_call_args = mock_user_list_service.mutate_user_lists.call_args
        self.assertEqual(mutate_call_args[1]['customer_id'], test_customer_id)
        operations_passed = mutate_call_args[1]['operations']
        self.assertEqual(operations_passed[0], mock_user_list_operation)
        self.assertTrue(mock_user_list_obj.name.startswith("Customer Match list #"))
        self.assertEqual(mock_user_list_obj.description, "A list of customers that originated from email and physical addresses")
        self.assertEqual(mock_user_list_obj.membership_life_span, 30)
        self.assertEqual(mock_user_list_obj.crm_based_user_list.upload_key_type, "mock_contact_info_enum_val")
        self.assertEqual(returned_resource_name, mock_resource_name)
        expected_sut_output = f"User list with resource name '{mock_resource_name}' was created.\n"
        self.assertEqual(mock_stdout.getvalue(), expected_sut_output)

class DecoyGoogleAdsFailureForTest:
    deserialize = Mock(name="DeserializeOnDecoyClass_ClassLevel")

class TestAddUsersToCustomerMatchUserList(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock(name="GoogleAdsClientMock_AddUsers")
        self.mock_client.enums = SimpleNamespace(
            OfflineUserDataJobTypeEnum=SimpleNamespace(CUSTOMER_MATCH_USER_LIST="mock_cm_user_list_type"),
            ConsentStatusEnum={
                "UNSPECIFIED": "mock_consent_unspecified", "GRANTED": "mock_consent_granted",
                "DENIED": "mock_consent_denied", "UNKNOWN": "mock_consent_unknown"
            }
        )
        self.mock_offline_job_service = Mock(name="OfflineUserDataJobServiceMock")
        self.mock_client.get_service.return_value = self.mock_offline_job_service

        self.build_ops_patcher = patch('examples.remarketing.add_customer_match_user_list.build_offline_user_data_job_operations')
        self.mock_build_ops = self.build_ops_patcher.start()
        self.addCleanup(self.build_ops_patcher.stop)

        self.check_status_patcher = patch('examples.remarketing.add_customer_match_user_list.check_job_status')
        self.mock_check_status = self.check_status_patcher.start()
        self.addCleanup(self.check_status_patcher.stop)

        self.test_customer_id = "cust_123"
        self.test_user_list_resource_name = "user_lists/ul_123"
        self.mock_job_resource_name_from_create = f"offlineUserDataJobs/{self.test_customer_id}/job_created_123"
        self.mock_job_resource_name_from_path = f"offlineUserDataJobs/{self.test_customer_id}/job_path_456"
        self.mock_operations_list = [Mock(name="Op1"), Mock(name="Op2")]

        self.mock_offline_job_type_obj = Mock(name="OfflineUserDataJobTypeMock")
        self.mock_offline_job_type_obj.customer_match_user_list_metadata = Mock(name="MetadataMock")
        self.mock_offline_job_type_obj.customer_match_user_list_metadata.consent = Mock(name="ConsentMock")

        self.current_add_ops_request_mock = None
        self.mock_failure_message_instance_of_decoy = DecoyGoogleAdsFailureForTest()

        self.original_get_type_side_effect = self._create_get_type_side_effect()
        self.mock_client.get_type.side_effect = self.original_get_type_side_effect

    def _create_get_type_side_effect(self):
        def get_type_side_effect_func(type_name):
            if type_name == "OfflineUserDataJob":
                self.mock_offline_job_type_obj.type_ = None
                self.mock_offline_job_type_obj.customer_match_user_list_metadata.user_list = None
                self.mock_offline_job_type_obj.customer_match_user_list_metadata.consent = Mock(ad_user_data=None, ad_personalization=None)
                return self.mock_offline_job_type_obj
            elif type_name == "AddOfflineUserDataJobOperationsRequest":
                self.current_add_ops_request_mock = Mock(name=f"AddOpsRequestTypeMockInstance_{self.mock_client.get_type.call_count}")
                return self.current_add_ops_request_mock
            elif type_name == "GoogleAdsFailure":
                return self.mock_failure_message_instance_of_decoy
            raise ValueError(f"Unexpected type_name '{type_name}' in get_type mock for AddUsers: {type_name}")
        return get_type_side_effect_func

    def _reset_shared_mocks_and_configs(self):
        self.mock_client.get_type.reset_mock()
        self.mock_client.get_service.reset_mock()
        self.mock_offline_job_service.reset_mock()
        self.mock_build_ops.reset_mock()
        self.mock_check_status.reset_mock()

        self.mock_build_ops.return_value = self.mock_operations_list
        self.mock_offline_job_service.create_offline_user_data_job.return_value = SimpleNamespace(resource_name=self.mock_job_resource_name_from_create)
        self.mock_offline_job_service.offline_user_data_job_path.return_value = self.mock_job_resource_name_from_path
        self.mock_offline_job_service.add_offline_user_data_job_operations.return_value = Mock(partial_failure_error=None)
        self.mock_client.get_type.side_effect = self.original_get_type_side_effect
        DecoyGoogleAdsFailureForTest.deserialize.reset_mock()


    @patch('sys.stdout', new_callable=io.StringIO)
    def test_create_new_job_run_job_true_consents_set(self, mock_stdout):
        self._reset_shared_mocks_and_configs()
        add_customer_match_user_list.add_users_to_customer_match_user_list(
            client=self.mock_client, customer_id=self.test_customer_id,
            user_list_resource_name=self.test_user_list_resource_name, run_job=True,
            offline_user_data_job_id=None, ad_user_data_consent="GRANTED",
            ad_personalization_consent="DENIED"
        )
        self.mock_client.get_type.assert_any_call("OfflineUserDataJob")
        self.mock_client.get_type.assert_any_call("AddOfflineUserDataJobOperationsRequest")
        self.assertEqual(self.mock_client.get_type.call_count, 2)
        self.mock_offline_job_service.create_offline_user_data_job.assert_called_once()
        created_job_arg = self.mock_offline_job_service.create_offline_user_data_job.call_args[1]['job']
        self.assertEqual(created_job_arg, self.mock_offline_job_type_obj)
        self.assertEqual(self.mock_offline_job_type_obj.type_, "mock_cm_user_list_type")
        self.assertEqual(self.mock_offline_job_type_obj.customer_match_user_list_metadata.user_list, self.test_user_list_resource_name)
        self.assertEqual(self.mock_offline_job_type_obj.customer_match_user_list_metadata.consent.ad_user_data, "mock_consent_granted")
        self.assertEqual(self.mock_offline_job_type_obj.customer_match_user_list_metadata.consent.ad_personalization, "mock_consent_denied")
        self.mock_build_ops.assert_called_once_with(self.mock_client)
        self.mock_offline_job_service.add_offline_user_data_job_operations.assert_called_once()
        self.assertIsNotNone(self.current_add_ops_request_mock); self.assertEqual(self.current_add_ops_request_mock.resource_name, self.mock_job_resource_name_from_create)
        self.assertEqual(self.current_add_ops_request_mock.operations, self.mock_operations_list); self.assertTrue(self.current_add_ops_request_mock.enable_partial_failure)
        self.mock_offline_job_service.run_offline_user_data_job.assert_called_once_with(resource_name=self.mock_job_resource_name_from_create)
        self.mock_check_status.assert_called_once_with(self.mock_client, self.test_customer_id, self.mock_job_resource_name_from_create)
        self.assertIn(f"Created an offline user data job with resource name: '{self.mock_job_resource_name_from_create}'.", mock_stdout.getvalue())
        self.assertIn("The operations are added to the offline user data job.", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_create_new_job_run_job_false(self, mock_stdout):
        self._reset_shared_mocks_and_configs()
        add_customer_match_user_list.add_users_to_customer_match_user_list(
            client=self.mock_client, customer_id=self.test_customer_id,
            user_list_resource_name=self.test_user_list_resource_name, run_job=False,
            offline_user_data_job_id=None, ad_user_data_consent="UNSPECIFIED",
            ad_personalization_consent=None
        )
        self.mock_client.get_type.assert_any_call("OfflineUserDataJob"); self.mock_client.get_type.assert_any_call("AddOfflineUserDataJobOperationsRequest")
        self.assertEqual(self.mock_client.get_type.call_count, 2); self.mock_offline_job_service.create_offline_user_data_job.assert_called_once()
        created_job_arg = self.mock_offline_job_service.create_offline_user_data_job.call_args[1]['job']
        self.assertEqual(created_job_arg.customer_match_user_list_metadata.consent.ad_user_data, "mock_consent_unspecified")
        self.assertIsNone(self.mock_offline_job_type_obj.customer_match_user_list_metadata.consent.ad_personalization, "ad_personalization should be None")
        self.mock_offline_job_service.add_offline_user_data_job_operations.assert_called_once()
        self.mock_offline_job_service.run_offline_user_data_job.assert_not_called(); self.mock_check_status.assert_not_called()
        self.assertIn(f"Not running offline user data job '{self.mock_job_resource_name_from_create}', as requested.", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_use_existing_job_run_job_true(self, mock_stdout):
        self._reset_shared_mocks_and_configs()
        test_existing_job_id = "existing_job_789"
        add_customer_match_user_list.add_users_to_customer_match_user_list(
            client=self.mock_client, customer_id=self.test_customer_id,
            user_list_resource_name=self.test_user_list_resource_name, run_job=True,
            offline_user_data_job_id=test_existing_job_id, ad_user_data_consent=None,
            ad_personalization_consent=None
        )
        self.mock_offline_job_service.offline_user_data_job_path.assert_called_once_with(self.test_customer_id, test_existing_job_id)
        self.mock_offline_job_service.create_offline_user_data_job.assert_not_called()
        self.mock_client.get_type.assert_called_once_with("AddOfflineUserDataJobOperationsRequest")
        self.mock_build_ops.assert_called_once_with(self.mock_client)
        self.mock_offline_job_service.add_offline_user_data_job_operations.assert_called_once()
        self.assertIsNotNone(self.current_add_ops_request_mock)
        self.assertEqual(self.current_add_ops_request_mock.resource_name, self.mock_job_resource_name_from_path)
        self.assertEqual(self.current_add_ops_request_mock.operations, self.mock_operations_list)
        self.assertTrue(self.current_add_ops_request_mock.enable_partial_failure)
        self.mock_offline_job_service.run_offline_user_data_job.assert_called_once_with(resource_name=self.mock_job_resource_name_from_path)
        self.mock_check_status.assert_called_once_with(self.mock_client, self.test_customer_id, self.mock_job_resource_name_from_path)
        self.assertNotIn("Created an offline user data job", mock_stdout.getvalue())
        self.assertIn("The operations are added to the offline user data job.", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_partial_failure_handling(self, mock_stdout):
        self._reset_shared_mocks_and_configs()

        mock_deserialized_failure_instance = Mock(name="DeserializedFailureInstance")
        mock_error = Mock(name="MockError")
        mock_error.location.field_path_elements = [Mock(index=0, field_name="some_field")]
        mock_error.message = "Msg1"

        mock_error_code_obj = Mock(name="ErrorCodeObject_for_str")
        mock_error_code_obj.__str__ = Mock(return_value="ErrorCodeName1")
        mock_error.error_code = mock_error_code_obj

        mock_deserialized_failure_instance.errors = [mock_error]

        DecoyGoogleAdsFailureForTest.deserialize.return_value = mock_deserialized_failure_instance

        mock_partial_failure = Mock(code=2, message="Partial failure occurred.")
        mock_error_detail = Mock(name="MockErrorDetail"); mock_error_detail.value = b"serialized_failure"
        mock_partial_failure.details = [mock_error_detail]
        self.mock_offline_job_service.add_offline_user_data_job_operations.return_value = Mock(partial_failure_error=mock_partial_failure)

        add_customer_match_user_list.add_users_to_customer_match_user_list(
            client=self.mock_client, customer_id=self.test_customer_id,
            user_list_resource_name=self.test_user_list_resource_name, run_job=False,
            offline_user_data_job_id=None, ad_user_data_consent=None,
            ad_personalization_consent=None
        )

        self.mock_offline_job_service.add_offline_user_data_job_operations.assert_called_once()
        self.mock_client.get_type.assert_any_call("GoogleAdsFailure")

        DecoyGoogleAdsFailureForTest.deserialize.assert_called_once_with(b"serialized_failure")

        captured_output = mock_stdout.getvalue()
        self.assertIn("A partial failure at index 0 occurred.", captured_output)
        self.assertIn("Error message: Msg1", captured_output)
        self.assertIn("Error code: ErrorCodeName1", captured_output)
        self.assertIn("The operations are added to the offline user data job.", captured_output)


class TestCheckJobStatus(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock(name="GoogleAdsClientMock_CheckStatus")
        self.mock_google_ads_service = Mock(name="GoogleAdsServiceMock_for_search")
        self.mock_client.get_service.return_value = self.mock_google_ads_service

        self.print_info_patcher = patch('examples.remarketing.add_customer_match_user_list.print_customer_match_user_list_info')
        self.mock_print_info = self.print_info_patcher.start()
        self.addCleanup(self.print_info_patcher.stop)

        self.test_customer_id = "cust_check_123"
        self.test_job_resource_name = "offlineUserDataJobs/job_check_456"
        self.test_user_list_name = "userLists/ul_check_789"

    def _create_mock_job_search_result_row(self, job_id_val, status_name_val, type_name_val, failure_reason_val, user_list_rn_val):
        mock_row = Mock(name="GoogleAdsRowMock")
        mock_job = mock_row.offline_user_data_job # Accessing this creates the attribute if it's a fresh Mock

        mock_job.id = job_id_val
        mock_job.status = Mock(name=f"StatusEnum_{status_name_val}"); mock_job.status.name = status_name_val
        mock_job.type_ = Mock(name=f"TypeEnum_{type_name_val}"); mock_job.type_.name = type_name_val
        mock_job.failure_reason = failure_reason_val
        mock_job.customer_match_user_list_metadata = Mock(name="MetadataMock_for_job")
        mock_job.customer_match_user_list_metadata.user_list = user_list_rn_val
        return mock_row

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_status_success(self, mock_stdout):
        mock_search_result_row = self._create_mock_job_search_result_row(
            "job_id_success", "SUCCESS", "CUSTOMER_MATCH_USER_LIST", None, self.test_user_list_name
        )
        self.mock_google_ads_service.search.return_value = [mock_search_result_row]

        add_customer_match_user_list.check_job_status(
            self.mock_client, self.test_customer_id, self.test_job_resource_name
        )

        self.mock_google_ads_service.search.assert_called_once() # Query check can be added if needed
        self.mock_print_info.assert_called_once_with(self.mock_client, self.test_customer_id, self.test_user_list_name)

        captured = mock_stdout.getvalue()
        self.assertIn("Offline user data job ID 'job_id_success' with type 'CUSTOMER_MATCH_USER_LIST' has status: SUCCESS", captured)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_status_failed(self, mock_stdout):
        mock_search_result_row = self._create_mock_job_search_result_row(
            "job_id_failed", "FAILED", "CUSTOMER_MATCH_USER_LIST", "Test Failure Reason", self.test_user_list_name
        )
        self.mock_google_ads_service.search.return_value = [mock_search_result_row]

        add_customer_match_user_list.check_job_status(
            self.mock_client, self.test_customer_id, self.test_job_resource_name
        )
        self.mock_print_info.assert_not_called()
        captured = mock_stdout.getvalue()
        self.assertIn("Offline user data job ID 'job_id_failed' with type 'CUSTOMER_MATCH_USER_LIST' has status: FAILED", captured)
        self.assertIn("\tFailure Reason: Test Failure Reason", captured)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_status_pending(self, mock_stdout):
        mock_search_result_row = self._create_mock_job_search_result_row(
            "job_id_pending", "PENDING", "CUSTOMER_MATCH_USER_LIST", None, self.test_user_list_name
        )
        self.mock_google_ads_service.search.return_value = [mock_search_result_row]

        add_customer_match_user_list.check_job_status(
            self.mock_client, self.test_customer_id, self.test_job_resource_name
        )
        self.mock_print_info.assert_not_called()
        captured = mock_stdout.getvalue()
        self.assertIn("Offline user data job ID 'job_id_pending' with type 'CUSTOMER_MATCH_USER_LIST' has status: PENDING", captured)
        self.assertIn("To check the status of the job periodically, use the following GAQL query", captured)
        self.assertIn(self.test_job_resource_name, captured) # Ensure query contains job name

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_status_running(self, mock_stdout):
        mock_search_result_row = self._create_mock_job_search_result_row(
            "job_id_running", "RUNNING", "CUSTOMER_MATCH_USER_LIST", None, self.test_user_list_name
        )
        self.mock_google_ads_service.search.return_value = [mock_search_result_row]

        add_customer_match_user_list.check_job_status(
            self.mock_client, self.test_customer_id, self.test_job_resource_name
        )
        self.mock_print_info.assert_not_called()
        captured = mock_stdout.getvalue()
        self.assertIn("Offline user data job ID 'job_id_running' with type 'CUSTOMER_MATCH_USER_LIST' has status: RUNNING", captured)
        self.assertIn("To check the status of the job periodically, use the following GAQL query", captured)

if __name__ == "__main__":
    unittest.main()
