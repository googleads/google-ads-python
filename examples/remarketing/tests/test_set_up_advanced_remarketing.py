import unittest
from unittest.mock import patch, Mock, call, ANY
import io
import sys
from types import SimpleNamespace
# SUT imports uuid4 directly, so we don't need to import uuid here for patching uuid.uuid4

# SUT (System Under Test)
from examples.remarketing import set_up_advanced_remarketing

class TestSetUpAdvancedRemarketing(unittest.TestCase):

    @patch('examples.remarketing.set_up_advanced_remarketing.uuid4')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_orchestration(self, mock_stdout, mock_sut_uuid4):
        mock_client = Mock(name="GoogleAdsClient")
        test_customer_id = "dummy_customer_123"
        mock_user_list_resource_name = "userLists/mock_ul_resource_name"

        mock_uuid_obj = Mock(name="UUIDObject")
        mock_uuid_obj.__str__ = Mock(return_value="mock-uuid-string-123")
        mock_sut_uuid4.return_value = mock_uuid_obj

        # 1. Mock Enums
        mock_client.enums = SimpleNamespace(
            UserListMembershipStatusEnum=SimpleNamespace(OPEN="MOCK_MEMBERSHIP_OPEN"),
            UserListPrepopulationStatusEnum=SimpleNamespace(REQUESTED="MOCK_PREPOP_REQUESTED"),
            UserListStringRuleItemOperatorEnum=SimpleNamespace(EQUALS="MOCK_STRING_EQUALS"),
            UserListNumberRuleItemOperatorEnum=SimpleNamespace(GREATER_THAN="MOCK_NUM_GREATER_THAN"),
            UserListDateRuleItemOperatorEnum=SimpleNamespace(
                AFTER="MOCK_DATE_AFTER", BEFORE="MOCK_DATE_BEFORE"
            ),
            UserListFlexibleRuleOperatorEnum=SimpleNamespace(AND="MOCK_FLEX_OP_AND")
        )

        # 2. Mock Services
        mock_user_list_service = Mock(name="UserListService")
        mock_client.get_service.return_value = mock_user_list_service

        mock_mutate_response = Mock(name="MutateUserListsResponse")
        mock_mutate_result = Mock(name="MutateResult")
        mock_mutate_result.resource_name = mock_user_list_resource_name
        mock_mutate_response.results = [mock_mutate_result]
        mock_user_list_service.mutate_user_lists.return_value = mock_mutate_response

        # 3. Mock Types (via client.get_type side_effect)
        mock_user_list = Mock(name="UserList")
        mock_operation = Mock(name="UserListOperation", create=mock_user_list)
        mock_rule_based_user_list_info = Mock(name="RuleBasedUserListInfo")
        mock_flexible_rule_user_list_info = Mock(name="FlexibleRuleUserListInfo")
        mock_flexible_rule_user_list_info.inclusive_operands = []
        mock_rule_based_user_list_info.flexible_rule_user_list = mock_flexible_rule_user_list_info
        mock_user_list.rule_based_user_list = mock_rule_based_user_list_info

        mock_rule_operand = Mock(name="FlexibleRuleOperandInfo")
        mock_operand_rule_info = Mock(name="UserListRuleInfo_for_operand")
        mock_operand_rule_info.rule_item_groups = []
        mock_rule_operand.rule = mock_operand_rule_info

        self.created_rule_items = {}
        self.created_rule_groups = {}

        def get_type_side_effect(type_name):
            # mock_stdout.write(f"DEBUG_GET_TYPE: Called for '{type_name}'\n")
            if type_name == "UserListOperation":
                mock_user_list.name = ""
                mock_user_list.description = ""
                mock_user_list.membership_status = None
                mock_user_list.membership_life_span = 0
                mock_user_list.rule_based_user_list = mock_rule_based_user_list_info
                mock_rule_based_user_list_info.prepopulation_status = None
                mock_rule_based_user_list_info.flexible_rule_user_list = mock_flexible_rule_user_list_info
                mock_flexible_rule_user_list_info.inclusive_rule_operator = None
                mock_flexible_rule_user_list_info.inclusive_operands = []
                mock_operation.create = mock_user_list
                return mock_operation

            elif type_name == "FlexibleRuleOperandInfo":
                mock_operand_rule_info.rule_item_groups = []
                mock_rule_operand.rule = mock_operand_rule_info
                mock_rule_operand.lookback_window_days = 0
                return mock_rule_operand

            elif type_name == "UserListRuleItemGroupInfo":
                group_name = f"RuleGroup_{len(self.created_rule_groups)}"
                group_mock = Mock(name=group_name)
                group_mock.rule_items = []
                self.created_rule_groups[group_name] = group_mock
                return group_mock

            elif type_name == "UserListRuleItemInfo":
                item_name_suffix = len(self.created_rule_items)
                item_mock = Mock(name=f"RuleItem_{item_name_suffix}")
                item_mock.string_rule_item = Mock(name=f"StringRuleItem_{item_name_suffix}")
                item_mock.number_rule_item = Mock(name=f"NumberRuleItem_{item_name_suffix}")
                item_mock.date_rule_item = Mock(name=f"DateRuleItem_{item_name_suffix}")
                self.created_rule_items[f"item_{item_name_suffix}"] = item_mock
                return item_mock

            raise ValueError(f"Unexpected get_type call in main: {type_name}")

        mock_client.get_type.side_effect = get_type_side_effect

        # 4. Execution
        set_up_advanced_remarketing.main(mock_client, test_customer_id)

        # 5. Assertions
        mock_client.get_service.assert_called_once_with("UserListService")

        expected_name = f"My expression rule user list #{str(mock_uuid_obj)}"
        self.assertEqual(mock_user_list.name, expected_name)

        self.assertEqual(mock_user_list.description,
                         "Users who checked out in November or December OR visited the checkout page with more than one item in their cart"
        )
        self.assertEqual(mock_user_list.membership_status, "MOCK_MEMBERSHIP_OPEN")
        self.assertEqual(mock_user_list.membership_life_span, 90)

        self.assertEqual(mock_rule_based_user_list_info.prepopulation_status, "MOCK_PREPOP_REQUESTED")

        self.assertEqual(mock_flexible_rule_user_list_info.inclusive_rule_operator, "MOCK_FLEX_OP_AND")
        self.assertEqual(len(mock_flexible_rule_user_list_info.inclusive_operands), 1)
        self.assertIn(mock_rule_operand, mock_flexible_rule_user_list_info.inclusive_operands)

        self.assertEqual(mock_rule_operand.lookback_window_days, 7)

        operand_rule = mock_rule_operand.rule
        self.assertEqual(len(operand_rule.rule_item_groups), 2)

        group1 = operand_rule.rule_item_groups[0]
        group2 = operand_rule.rule_item_groups[1]

        self.assertEqual(len(group1.rule_items), 2)
        self.assertEqual(len(group2.rule_items), 2)

        checkout_rule = group1.rule_items[0]
        self.assertEqual(checkout_rule.name, "ecomm_pagetype")
        self.assertEqual(checkout_rule.string_rule_item.operator, "MOCK_STRING_EQUALS")
        self.assertEqual(checkout_rule.string_rule_item.value, "checkout")

        cart_size_rule = group1.rule_items[1]
        self.assertEqual(cart_size_rule.name, "cart_size")
        self.assertEqual(cart_size_rule.number_rule_item.operator, "MOCK_NUM_GREATER_THAN")
        self.assertEqual(cart_size_rule.number_rule_item.value, 1.0)

        start_date_rule = group2.rule_items[0]
        self.assertEqual(start_date_rule.name, "checkoutdate")
        self.assertEqual(start_date_rule.date_rule_item.operator, "MOCK_DATE_AFTER")
        self.assertEqual(start_date_rule.date_rule_item.value, "20191031")

        end_date_rule = group2.rule_items[1]
        self.assertEqual(end_date_rule.name, "checkoutdate")
        self.assertEqual(end_date_rule.date_rule_item.operator, "MOCK_DATE_BEFORE")
        self.assertEqual(end_date_rule.date_rule_item.value, "20200101")

        mock_user_list_service.mutate_user_lists.assert_called_once_with(
            customer_id=test_customer_id, operations=[mock_operation]
        )

        # Corrected expected_stdout: period inside the single quotes
        expected_stdout = (
            f"Created user list with resource name "
            f"'{mock_user_list_resource_name}.'\n"
        )
        # Using assertIn to be robust against debug prints if they were re-enabled
        self.assertIn(expected_stdout, mock_stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
