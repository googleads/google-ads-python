import unittest
from unittest.mock import patch, Mock, call, ANY
import io
import sys
from types import SimpleNamespace

# SUT (System Under Test)
from examples.remarketing import add_logical_user_list

class TestAddLogicalUserList(unittest.TestCase):

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_orchestration(self, mock_stdout):
        mock_client = Mock(name="GoogleAdsClient")
        test_customer_id = "dummy_customer_123"
        test_user_list_ids = ["ul_id_1", "ul_id_2"]

        # 1. Mock Setup
        mock_client.enums = SimpleNamespace(
            UserListLogicalRuleOperatorEnum=SimpleNamespace(ANY="MOCK_ANY_OPERATOR")
        )

        mock_user_list_service = Mock(name="UserListService")
        mock_client.get_service.return_value = mock_user_list_service

        def user_list_path_side_effect(customer_id, user_list_id):
            return f"customers/{customer_id}/userLists/{user_list_id}_mockpath"
        mock_user_list_service.user_list_path.side_effect = user_list_path_side_effect

        mock_mutate_response = Mock(name="MutateUserListsResponse")
        mock_mutate_result = Mock(name="MutateResult")
        # Ensure resource_name is a plain string for direct use in expected_stdout
        mock_resource_name_str = "mock_logical_ul_resource_name"
        mock_mutate_result.resource_name = mock_resource_name_str
        mock_mutate_response.results = [mock_mutate_result]
        mock_user_list_service.mutate_user_lists.return_value = mock_mutate_response

        created_logical_operands = []

        mock_logical_rule_info = Mock(name="UserListLogicalRuleInfo")
        mock_logical_rule_info.rule_operands = []

        mock_user_list = Mock(name="UserList")
        mock_logical_user_list_info = Mock(name="LogicalUserListInfo")
        mock_logical_user_list_info.rules = []
        mock_user_list.logical_user_list = mock_logical_user_list_info

        mock_operation = Mock(name="UserListOperation", create=mock_user_list)

        def get_type_side_effect(type_name):
            if type_name == "LogicalUserListOperandInfo":
                operand_mock = Mock(name=f"LogicalUserListOperandInfo_{len(created_logical_operands)}")
                created_logical_operands.append(operand_mock)
                return operand_mock
            elif type_name == "UserListLogicalRuleInfo":
                mock_logical_rule_info.rule_operands = []
                return mock_logical_rule_info
            elif type_name == "UserListOperation":
                mock_operation.create = mock_user_list
                mock_user_list.logical_user_list = mock_logical_user_list_info
                mock_logical_user_list_info.rules = []
                return mock_operation
            raise ValueError(f"Unexpected type_name '{type_name}' in get_type mock for main")

        mock_client.get_type.side_effect = get_type_side_effect

        # 2. Execution
        add_logical_user_list.main(mock_client, test_customer_id, test_user_list_ids)

        # 3. Assertions
        mock_client.get_service.assert_called_once_with("UserListService")

        expected_path_calls = [
            call(test_customer_id, ul_id) for ul_id in test_user_list_ids
        ]
        mock_user_list_service.user_list_path.assert_has_calls(expected_path_calls, any_order=True)
        self.assertEqual(mock_user_list_service.user_list_path.call_count, len(test_user_list_ids))

        get_type_calls_made = mock_client.get_type.mock_calls
        self.assertEqual(get_type_calls_made.count(call("LogicalUserListOperandInfo")), len(test_user_list_ids))
        self.assertIn(call("UserListLogicalRuleInfo"), get_type_calls_made)
        self.assertIn(call("UserListOperation"), get_type_calls_made)
        self.assertEqual(mock_client.get_type.call_count, len(test_user_list_ids) + 2)

        self.assertEqual(len(created_logical_operands), len(test_user_list_ids))
        for i, operand_mock in enumerate(created_logical_operands):
            expected_user_list_path = f"customers/{test_customer_id}/userLists/{test_user_list_ids[i]}_mockpath"
            self.assertEqual(operand_mock.user_list, expected_user_list_path)

        self.assertEqual(mock_logical_rule_info.operator, "MOCK_ANY_OPERATOR")
        self.assertEqual(len(mock_logical_rule_info.rule_operands), len(test_user_list_ids))
        for operand_mock in created_logical_operands:
            self.assertIn(operand_mock, mock_logical_rule_info.rule_operands)

        self.assertTrue(mock_user_list.name.startswith("My combination list of other user lists #"))
        self.assertEqual(len(mock_user_list.logical_user_list.rules), 1)
        self.assertIn(mock_logical_rule_info, mock_user_list.logical_user_list.rules)

        mock_user_list_service.mutate_user_lists.assert_called_once_with(
            customer_id=test_customer_id, operations=[mock_operation]
        )

        # Corrected expected_stdout: period inside the single quotes
        expected_stdout = (
            "Created logical user list with resource name "
            f"'{mock_resource_name_str}.'\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_stdout)


if __name__ == "__main__":
    unittest.main()
