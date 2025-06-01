import unittest
from unittest.mock import patch, Mock, call, ANY
import hashlib
import io
import sys
from types import SimpleNamespace

# SUT (System Under Test)
from examples.remarketing import add_customer_match_user_list

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
        self.mock_client = Mock(name="GoogleAdsClientMock")
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

        op1_user_data = operations[0].create
        self.assertIn(op1_user_data, self.user_data_mocks)
        self.assertEqual(len(op1_user_data.user_identifiers), 2)
        self.assertEqual(op1_user_data.user_identifiers[0].hashed_email, "hashed_dana@example.com_T")
        self.assertEqual(op1_user_data.user_identifiers[1].hashed_phone_number, "hashed_+1 800 5550101_T")

        op2_user_data = operations[1].create
        self.assertIn(op2_user_data, self.user_data_mocks)
        self.assertEqual(len(op2_user_data.user_identifiers), 3)
        self.assertEqual(op2_user_data.user_identifiers[0].hashed_email, "hashed_alex.2@example.com_T")
        self.assertEqual(op2_user_data.user_identifiers[1].hashed_phone_number, "hashed_+1 800 5550102_T")
        op2_address_identifier = op2_user_data.user_identifiers[2]
        self.assertEqual(op2_address_identifier.address_info.hashed_first_name, "hashed_Alex_F")
        self.assertEqual(op2_address_identifier.address_info.hashed_last_name, "hashed_Quinn_F")
        self.assertEqual(op2_address_identifier.address_info.country_code, "US")
        self.assertEqual(op2_address_identifier.address_info.postal_code, "94045")

        op3_user_data = operations[2].create
        self.assertIn(op3_user_data, self.user_data_mocks)
        self.assertEqual(len(op3_user_data.user_identifiers), 1)
        self.assertEqual(op3_user_data.user_identifiers[0].hashed_email, "hashed_charlie@example.com_T")


class TestCreateCustomerMatchUserList(unittest.TestCase):
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_create_list_success_and_returns_name(self, mock_stdout):
        mock_client = Mock(name="GoogleAdsClientMock_for_create_list")
        test_customer_id = "dummy_customer_123"
        mock_resource_name = f"customers/{test_customer_id}/userLists/user_list_mock_id"

        # Mock enums
        mock_client.enums = SimpleNamespace(
            CustomerMatchUploadKeyTypeEnum=SimpleNamespace(CONTACT_INFO="mock_contact_info_enum_val")
        )

        # Mock UserListService
        mock_user_list_service = Mock(name="UserListServiceMock")
        mock_client.get_service.return_value = mock_user_list_service

        # Mock UserListService response
        mock_mutate_response = Mock(name="MutateUserListsResponseMock")
        mock_result = Mock(name="UserListResultMock")
        mock_result.resource_name = mock_resource_name
        mock_mutate_response.results = [mock_result]
        mock_user_list_service.mutate_user_lists.return_value = mock_mutate_response

        # Mock client.get_type("UserListOperation")
        # SUT: user_list_operation = client.get_type("UserListOperation")
        #      user_list = user_list_operation.create
        #      user_list.crm_based_user_list (is an object on user_list)
        mock_user_list_operation = Mock(name="UserListOperationMock")
        mock_user_list_obj = Mock(name="UserListMock")
        mock_user_list_obj.crm_based_user_list = Mock(name="CrmBasedUserListInfoMock")
        mock_user_list_operation.create = mock_user_list_obj

        # Only one type is directly fetched by this SUT function
        mock_client.get_type.return_value = mock_user_list_operation

        # Call the function
        returned_resource_name = add_customer_match_user_list.create_customer_match_user_list(
            mock_client, test_customer_id
        )

        # Assertions
        mock_client.get_service.assert_called_once_with("UserListService")
        mock_client.get_type.assert_called_once_with("UserListOperation")

        mock_user_list_service.mutate_user_lists.assert_called_once()
        mutate_call_args = mock_user_list_service.mutate_user_lists.call_args
        self.assertEqual(mutate_call_args[1]['customer_id'], test_customer_id)

        operations_passed = mutate_call_args[1]['operations']
        self.assertEqual(len(operations_passed), 1)
        self.assertEqual(operations_passed[0], mock_user_list_operation) # Check same op object

        # Verify attributes of the UserList object (which is mock_user_list_obj)
        self.assertTrue(mock_user_list_obj.name.startswith("Customer Match list #"))
        self.assertEqual(
            mock_user_list_obj.description,
            "A list of customers that originated from email and physical addresses"
        )
        self.assertEqual(mock_user_list_obj.membership_life_span, 30)
        self.assertEqual(
            mock_user_list_obj.crm_based_user_list.upload_key_type,
            "mock_contact_info_enum_val" # The mocked enum value
        )

        # Assert return value
        self.assertEqual(returned_resource_name, mock_resource_name)

        # Assert stdout
        expected_sut_output = (
            f"User list with resource name '{mock_resource_name}' was created.\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_sut_output)


if __name__ == "__main__":
    unittest.main()
