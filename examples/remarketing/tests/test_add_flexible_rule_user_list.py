import unittest
from unittest.mock import patch, Mock, call, ANY
import io
import sys
from types import SimpleNamespace

# SUT (System Under Test)
from examples.remarketing import add_flexible_rule_user_list

class TestAddFlexibleRuleUserList(unittest.TestCase):

    # --- Tests for create_user_list_rule_info_from_url ---
    def test_create_user_list_rule_info_from_url_logic(self):
        mock_client = Mock(name="GoogleAdsClient_ForRuleInfo")

        mock_rule_item_info = Mock(name="UserListRuleItemInfo")
        mock_string_rule_item = Mock(name="StringRuleItemInfo")
        mock_rule_item_info.string_rule_item = mock_string_rule_item

        mock_group_info = Mock(name="UserListRuleItemGroupInfo")

        mock_rule_info = Mock(name="UserListRuleInfo")

        def get_type_side_effect(type_name):
            if type_name == "UserListRuleItemInfo":
                mock_string_rule_item.reset_mock()
                mock_rule_item_info.reset_mock()
                mock_rule_item_info.string_rule_item = mock_string_rule_item
                return mock_rule_item_info
            elif type_name == "UserListRuleItemGroupInfo":
                mock_group_info.rule_items = []
                return mock_group_info
            elif type_name == "UserListRuleInfo":
                mock_rule_info.rule_item_groups = []
                return mock_rule_info
            return Mock(name=f"DefaultMock_{type_name}")

        mock_client.get_type.side_effect = get_type_side_effect

        mock_client.enums = SimpleNamespace(
            UserListStringRuleItemOperatorEnum=SimpleNamespace(EQUALS="mock_equals_enum_val")
        )

        test_url = "http://test.com"

        returned_rule_info = add_flexible_rule_user_list.create_user_list_rule_info_from_url(
            mock_client, test_url
        )

        expected_get_type_calls = [
            call("UserListRuleItemInfo"),
            call("UserListRuleItemGroupInfo"),
            call("UserListRuleInfo"),
        ]
        mock_client.get_type.assert_has_calls(expected_get_type_calls, any_order=False)

        self.assertEqual(mock_rule_item_info.name, "url__")
        self.assertEqual(mock_string_rule_item.operator, "mock_equals_enum_val")
        self.assertEqual(mock_string_rule_item.value, test_url)

        self.assertEqual(len(mock_group_info.rule_items), 1)
        self.assertIn(mock_rule_item_info, mock_group_info.rule_items)

        self.assertEqual(len(mock_rule_info.rule_item_groups), 1)
        self.assertIn(mock_group_info, mock_rule_info.rule_item_groups)

        self.assertEqual(returned_rule_info, mock_rule_info)

    # --- Tests for main function ---
    @patch('examples.remarketing.add_flexible_rule_user_list.create_user_list_rule_info_from_url')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_orchestration(self, mock_stdout, mock_create_rule_info_func):
        mock_client = Mock(name="GoogleAdsClient_for_main")
        test_customer_id = "dummy_customer_main"

        mock_client.enums = SimpleNamespace(
            UserListFlexibleRuleOperatorEnum=SimpleNamespace(AND="mock_and_operator_enum"),
            UserListPrepopulationStatusEnum=SimpleNamespace(REQUESTED="mock_requested_enum"),
            UserListMembershipStatusEnum=SimpleNamespace(OPEN="mock_open_enum")
        )

        mock_user_list_service = Mock(name="UserListService")
        mock_client.get_service.return_value = mock_user_list_service

        mock_mutate_response = Mock()
        mock_resource_name_str = "mock_userlist_resource_name" # Plain string
        mock_result = Mock(); mock_result.resource_name = mock_resource_name_str
        mock_mutate_response.results = [mock_result]
        mock_user_list_service.mutate_user_lists.return_value = mock_mutate_response

        mock_flex_rules_info = Mock(name="FlexibleRuleUserListInfo")
        mock_flex_rules_info.inclusive_operands = []
        mock_flex_rules_info.exclusive_operands = []

        mock_rule_based_list_info = Mock(name="RuleBasedUserListInfo")

        mock_user_list_obj = Mock(name="UserList")
        mock_operation = Mock(name="UserListOperation", create=mock_user_list_obj)

        created_operand_info_mocks = []

        def main_get_type_side_effect(type_name):
            if type_name == "FlexibleRuleUserListInfo":
                mock_flex_rules_info.inclusive_operands = []
                mock_flex_rules_info.exclusive_operands = []
                return mock_flex_rules_info
            elif type_name == "FlexibleRuleOperandInfo":
                operand_mock = Mock(
                    name=f"FlexibleRuleOperandInfo_{len(created_operand_info_mocks)}",
                    lookback_window_days=None
                )
                created_operand_info_mocks.append(operand_mock)
                return operand_mock
            elif type_name == "RuleBasedUserListInfo":
                return mock_rule_based_list_info
            elif type_name == "UserListOperation":
                mock_operation.create = mock_user_list_obj
                return mock_operation
            return Mock(name=f"DefaultMock_Main_{type_name}")

        mock_client.get_type.side_effect = main_get_type_side_effect

        mock_rule_info1 = Mock(name="RuleInfo1_URL1")
        mock_rule_info2 = Mock(name="RuleInfo2_URL2")
        mock_rule_info3 = Mock(name="RuleInfo3_URL3")
        mock_create_rule_info_func.side_effect = [mock_rule_info1, mock_rule_info2, mock_rule_info3]

        url1 = "http://example.com/example1"
        url2 = "http://example.com/example2"
        url3 = "http://example.com/example3"

        add_flexible_rule_user_list.main(mock_client, test_customer_id)

        expected_rule_creation_calls = [
            call(mock_client, url1),
            call(mock_client, url2),
            call(mock_client, url3),
        ]
        mock_create_rule_info_func.assert_has_calls(expected_rule_creation_calls)
        self.assertEqual(mock_create_rule_info_func.call_count, 3)

        self.assertEqual(mock_flex_rules_info.inclusive_rule_operator, "mock_and_operator_enum")
        self.assertEqual(len(mock_flex_rules_info.inclusive_operands), 2)
        self.assertEqual(mock_flex_rules_info.inclusive_operands[0].rule, mock_rule_info1)
        self.assertEqual(mock_flex_rules_info.inclusive_operands[0].lookback_window_days, 7)
        self.assertEqual(mock_flex_rules_info.inclusive_operands[1].rule, mock_rule_info2)
        self.assertEqual(mock_flex_rules_info.inclusive_operands[1].lookback_window_days, 7)

        self.assertEqual(len(mock_flex_rules_info.exclusive_operands), 1)
        self.assertEqual(mock_flex_rules_info.exclusive_operands[0].rule, mock_rule_info3)
        self.assertIsNone(mock_flex_rules_info.exclusive_operands[0].lookback_window_days)

        self.assertEqual(mock_rule_based_list_info.prepopulation_status, "mock_requested_enum")
        self.assertEqual(mock_rule_based_list_info.flexible_rule_user_list, mock_flex_rules_info)

        expected_name_prefix = "All visitors to http://example.com/example1 AND http://example.com/example2 but NOT http://example.com/example3 #"
        self.assertTrue(
             mock_user_list_obj.name.startswith(expected_name_prefix),
             msg=f"Expected name to start with '{expected_name_prefix}', but got '{mock_user_list_obj.name}'"
        )

        expected_description = "Visitors of both http://example.com/example1 AND http://example.com/example2 but NOThttp://example.com/example3"
        self.assertEqual(mock_user_list_obj.description, expected_description)

        self.assertEqual(mock_user_list_obj.membership_status, "mock_open_enum")
        self.assertEqual(mock_user_list_obj.rule_based_user_list, mock_rule_based_list_info)

        mock_client.get_service.assert_called_once_with("UserListService")
        mock_user_list_service.mutate_user_lists.assert_called_once_with(
            customer_id=test_customer_id, operations=[mock_operation]
        )

        # Using a direct string literal matching the SUT's known print format
        # and the repr output from the previous failing test.
        expected_stdout = "Created user list with resource name: 'mock_userlist_resource_name.'\n"

        actual_output = mock_stdout.getvalue()
        if actual_output != expected_stdout:
            # This debug output will only show if the assertion is about to fail.
            print(f"DEBUG_EXPECTED_STDOUT_LITERAL_REPR: {repr(expected_stdout)}", file=sys.__stderr__)
            print(f"DEBUG_ACTUAL_STDOUT_REPR: {repr(actual_output)}", file=sys.__stderr__)
        self.assertEqual(actual_output, expected_stdout)


if __name__ == "__main__":
    unittest.main()
