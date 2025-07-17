import unittest
from unittest.mock import patch, Mock, ANY, call
import io
import sys
from types import SimpleNamespace

from examples.remarketing import add_conversion_based_user_list

class TestAddConversionBasedUserList(unittest.TestCase):

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_success_path(self, mock_stdout):
        mock_googleads_client = Mock(name="GoogleAdsClientMock")

        enums_holder = Mock(name="EnumsHolder")
        mock_user_list_membership_status_enum = SimpleNamespace(OPEN="mock_open_status_value")
        enums_holder.UserListMembershipStatusEnum = mock_user_list_membership_status_enum
        mock_googleads_client.enums = enums_holder

        mock_user_list_service = Mock(name="UserListServiceMock")
        mock_conversion_action_service = Mock(name="ConversionActionServiceMock")

        def get_service_side_effect(service_name):
            if service_name == "UserListService":
                return mock_user_list_service
            elif service_name == "ConversionActionService":
                return mock_conversion_action_service
            return Mock()

        mock_googleads_client.get_service.side_effect = get_service_side_effect

        created_user_list_action_infos = []
        def get_type_side_effect(type_name):
            mock_stdout.write(f"DEBUG_GET_TYPE: Called with '{type_name}'\n")
            if type_name == "UserListOperation":
                operation_mock = Mock(name="UserListOperationMock")
                operation_mock.create = Mock(name="UserListMock")
                operation_mock.create.basic_user_list = Mock(name="BasicUserListInfoMock")
                # Initialize actions as a list so .extend can be called on it by SUT
                operation_mock.create.basic_user_list.actions = []
                return operation_mock
            elif type_name == "UserListActionInfo":
                action_info_mock = Mock(name=f"UserListActionInfoMock_{len(created_user_list_action_infos)}")
                created_user_list_action_infos.append(action_info_mock)
                return action_info_mock
            return Mock()

        mock_googleads_client.get_type.side_effect = get_type_side_effect

        def conversion_action_path_side_effect(customer_id, conversion_action_id):
            return f"customers/{customer_id}/conversionActions/{conversion_action_id}_mock_path"
        mock_conversion_action_service.conversion_action_path.side_effect = conversion_action_path_side_effect

        mock_mutate_response = Mock(name="MutateUserListsResponseMock")
        mock_result = Mock(name="UserListResultMock")
        mock_result.resource_name = "mock_user_list_resource_name" # SUT adds single quotes and a period.
        mock_mutate_response.results = [mock_result]
        mock_user_list_service.mutate_user_lists.return_value = mock_mutate_response

        test_customer_id = "1234567890"
        test_conversion_action_ids = ["action_id_1", "action_id_2"]

        add_conversion_based_user_list.main(
            mock_googleads_client, test_customer_id, test_conversion_action_ids
        )

        mock_googleads_client.get_service.assert_any_call("UserListService")
        mock_googleads_client.get_service.assert_any_call("ConversionActionService")

        expected_conversion_action_path_calls = [
            call(test_customer_id, action_id) for action_id in test_conversion_action_ids
        ]
        mock_conversion_action_service.conversion_action_path.assert_has_calls(
            expected_conversion_action_path_calls, any_order=True
        )
        self.assertEqual(
            mock_conversion_action_service.conversion_action_path.call_count,
            len(test_conversion_action_ids)
        )

        mock_googleads_client.get_type.assert_any_call("UserListOperation")
        self.assertEqual(
            sum(1 for c in mock_googleads_client.get_type.mock_calls if c == call("UserListActionInfo")),
            len(test_conversion_action_ids)
        )

        mock_user_list_service.mutate_user_lists.assert_called_once()
        mutate_call_args = mock_user_list_service.mutate_user_lists.call_args
        self.assertEqual(mutate_call_args[1]['customer_id'], test_customer_id)

        operations = mutate_call_args[1]['operations']
        self.assertEqual(len(operations), 1)
        created_user_list_operation = operations[0]
        created_user_list = created_user_list_operation.create

        self.assertTrue(created_user_list.name.startswith("Example BasicUserList #"))
        self.assertEqual(created_user_list.description, "A list of people who have triggered one or more conversion actions")
        self.assertEqual(created_user_list.membership_status, "mock_open_status_value")
        self.assertEqual(created_user_list.membership_life_span, 365)

        basic_user_list_info = created_user_list.basic_user_list
        self.assertEqual(len(basic_user_list_info.actions), len(test_conversion_action_ids))

        # Check that the UserListActionInfo mocks we captured were indeed appended to the list
        # and that their conversion_action attribute was set correctly.
        for i, action_id in enumerate(test_conversion_action_ids):
            # Assuming the order of actions in basic_user_list_info.actions
            # matches the order of test_conversion_action_ids and thus created_user_list_action_infos
            action_info_in_list = basic_user_list_info.actions[i]
            self.assertIn(action_info_in_list, created_user_list_action_infos)
            expected_path = f"customers/{test_customer_id}/conversionActions/{action_id}_mock_path"
            self.assertEqual(action_info_in_list.conversion_action, expected_path)

        # Corrected expected_sut_output
        expected_sut_output = (
            "Created basic user list with resource name "
            f"'{mock_result.resource_name}.'"  # Matches SUT: single quotes, period inside
        )

        captured_value = mock_stdout.getvalue()
        self.assertIn(expected_sut_output, captured_value) # SUT print adds a newline, assertIn handles this.

        # Check that debug prints are also there
        self.assertIn("DEBUG_GET_TYPE: Called with 'UserListOperation'", captured_value)
        # Check for UserListActionInfo calls based on the number of IDs
        action_info_call_count = captured_value.count("DEBUG_GET_TYPE: Called with 'UserListActionInfo'")
        self.assertEqual(action_info_call_count, len(test_conversion_action_ids))

if __name__ == "__main__":
    unittest.main()
