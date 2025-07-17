import unittest
from unittest.mock import patch, Mock, call, ANY
# hashlib is not needed as TestNormalizeAndHash is removed
import io
import sys
from types import SimpleNamespace
import uuid

# SUT (System Under Test)
from examples.remarketing import set_up_remarketing

# TestNormalizeAndHash class removed as normalize_and_hash is not in set_up_remarketing.py

class TestCreateUserList(unittest.TestCase):
    @patch('examples.remarketing.set_up_remarketing.uuid4')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_create_user_list_logic(self, mock_stdout, mock_sut_uuid4):
        mock_client = Mock(name="GoogleAdsClient")
        test_customer_id = "dummy_customer_id_for_ul"
        mock_ul_resource_name = "userLists/mock_ul_res_name_123"
        mock_uuid_obj = Mock(name="UUIDObject"); mock_uuid_obj.__str__ = Mock(return_value="mock-uuid-suffix")
        mock_sut_uuid4.return_value = mock_uuid_obj
        mock_client.enums = SimpleNamespace(
            UserListMembershipStatusEnum=SimpleNamespace(OPEN="MOCK_UL_OPEN"),
            UserListPrepopulationStatusEnum=SimpleNamespace(REQUESTED="MOCK_UL_PREPOP_REQUESTED"),
            UserListStringRuleItemOperatorEnum=SimpleNamespace(CONTAINS="MOCK_STRING_CONTAINS"),
            UserListFlexibleRuleOperatorEnum=SimpleNamespace(AND="MOCK_FLEX_AND")
        )
        mock_user_list_service = Mock(name="UserListService")
        mock_client.get_service.return_value = mock_user_list_service
        mock_mutate_response = Mock(name="MutateUserListsResponse")
        mock_mutate_result = Mock(name="MutateResult"); mock_mutate_result.resource_name = mock_ul_resource_name
        mock_mutate_response.results = [mock_mutate_result]
        mock_user_list_service.mutate_user_lists.return_value = mock_mutate_response
        mock_user_list = Mock(name="UserList"); mock_operation = Mock(name="UserListOperation", create=mock_user_list)
        mock_rule_based_user_list_info = Mock(name="RuleBasedUserListInfo")
        mock_user_list.rule_based_user_list = mock_rule_based_user_list_info
        mock_flexible_rule_user_list_info = Mock(name="FlexibleRuleUserListInfo")
        mock_flexible_rule_user_list_info.inclusive_operands = []
        mock_rule_based_user_list_info.flexible_rule_user_list = mock_flexible_rule_user_list_info
        mock_rule_operand = Mock(name="FlexibleRuleOperandInfo")
        mock_operand_rule_info = Mock(name="UserListRuleInfo_for_operand")
        mock_operand_rule_info.rule_item_groups = []
        mock_rule_operand.rule = mock_operand_rule_info
        mock_rule_item_group = Mock(name="UserListRuleItemGroupInfo")
        mock_rule_item_group.rule_items = []
        mock_rule_item = Mock(name="UserListRuleItemInfo")
        mock_rule_item.string_rule_item = Mock(name="StringRuleItemInfo")
        def get_type_side_effect(type_name):
            if type_name == "UserListOperation":
                mock_user_list.name = ""; mock_user_list.description = ""
                mock_user_list.membership_status = None; mock_user_list.membership_life_span = 0
                mock_user_list.rule_based_user_list = mock_rule_based_user_list_info
                mock_rule_based_user_list_info.prepopulation_status = None
                mock_rule_based_user_list_info.flexible_rule_user_list = mock_flexible_rule_user_list_info
                mock_flexible_rule_user_list_info.inclusive_rule_operator = None
                mock_flexible_rule_user_list_info.inclusive_operands = []
                mock_operation.create = mock_user_list; return mock_operation
            elif type_name == "FlexibleRuleOperandInfo":
                mock_operand_rule_info.rule_item_groups = []
                mock_rule_operand.rule = mock_operand_rule_info
                mock_rule_operand.lookback_window_days = 0; return mock_rule_operand
            elif type_name == "UserListRuleItemGroupInfo":
                mock_rule_item_group.rule_items = []; return mock_rule_item_group
            elif type_name == "UserListRuleItemInfo":
                mock_rule_item.string_rule_item = Mock(name="StringRuleItemInfo_Reset"); return mock_rule_item
            raise ValueError(f"Unexpected get_type call: {type_name}")
        mock_client.get_type.side_effect = get_type_side_effect
        returned_resource_name = set_up_remarketing.create_user_list(mock_client, test_customer_id)
        mock_client.get_service.assert_called_once_with("UserListService")
        expected_name = f"All visitors to example.com #{str(mock_uuid_obj)}"
        self.assertEqual(mock_user_list.name, expected_name)
        self.assertEqual(mock_user_list.description, "Any visitor to any page of example.com")
        self.assertEqual(mock_user_list.membership_status, "MOCK_UL_OPEN")
        self.assertEqual(mock_user_list.membership_life_span, 365)
        self.assertEqual(mock_rule_based_user_list_info.prepopulation_status, "MOCK_UL_PREPOP_REQUESTED")
        self.assertEqual(mock_rule_item.name, "url__"); self.assertEqual(mock_rule_item.string_rule_item.operator, "MOCK_STRING_CONTAINS")
        self.assertEqual(mock_rule_item.string_rule_item.value, "example.com"); self.assertIn(mock_rule_item, mock_rule_item_group.rule_items)
        self.assertEqual(len(mock_rule_item_group.rule_items), 1); self.assertIn(mock_rule_item_group, mock_operand_rule_info.rule_item_groups)
        self.assertEqual(len(mock_operand_rule_info.rule_item_groups), 1); self.assertEqual(mock_rule_operand.lookback_window_days, 7)
        self.assertEqual(mock_flexible_rule_user_list_info.inclusive_rule_operator, "MOCK_FLEX_AND")
        self.assertIn(mock_rule_operand, mock_flexible_rule_user_list_info.inclusive_operands)
        self.assertEqual(len(mock_flexible_rule_user_list_info.inclusive_operands), 1)
        mock_user_list_service.mutate_user_lists.assert_called_once_with(customer_id=test_customer_id, operations=[mock_operation])
        self.assertEqual(returned_resource_name, mock_ul_resource_name)
        expected_stdout = f"Created user list with resource name: '{mock_ul_resource_name}'\n"
        self.assertEqual(mock_stdout.getvalue(), expected_stdout)

class TestTargetAdsInAdGroupToUserList(unittest.TestCase):
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_target_ads_in_ad_group_to_user_list_success(self, mock_stdout):
        mock_client = Mock(name="GoogleAdsClient"); test_customer_id = "cust_target_123"; test_ad_group_id = "adgroup_id_456"
        test_user_list_rn = "userLists/ul_rn_789"; mock_ad_group_path = f"customers/{test_customer_id}/adGroups/{test_ad_group_id}"
        mock_criterion_rn = "adGroupCriteria/agc_rn_123"; mock_ad_group_service = Mock(name="AdGroupService")
        mock_ad_group_criterion_service = Mock(name="AdGroupCriterionService")
        def get_service_side_effect(service_name):
            if service_name == "AdGroupService": return mock_ad_group_service
            elif service_name == "AdGroupCriterionService": return mock_ad_group_criterion_service
            return Mock()
        mock_client.get_service.side_effect = get_service_side_effect
        mock_ad_group_service.ad_group_path.return_value = mock_ad_group_path
        mock_ad_group_criterion_operation = Mock(name="AdGroupCriterionOperation")
        mock_ad_group_criterion = Mock(name="AdGroupCriterion")
        mock_ad_group_criterion.user_list = Mock(name="UserListInfoOnCriterion")
        mock_ad_group_criterion_operation.create = mock_ad_group_criterion
        mock_client.get_type.return_value = mock_ad_group_criterion_operation
        mock_mutate_response = Mock(); mock_mutate_result = Mock(); mock_mutate_result.resource_name = mock_criterion_rn
        mock_mutate_response.results = [mock_mutate_result]
        mock_ad_group_criterion_service.mutate_ad_group_criteria.return_value = mock_mutate_response
        returned_rn = set_up_remarketing.target_ads_in_ad_group_to_user_list(
            mock_client, test_customer_id, test_ad_group_id, test_user_list_rn
        )
        mock_client.get_service.assert_any_call("AdGroupService"); mock_client.get_service.assert_any_call("AdGroupCriterionService")
        mock_ad_group_service.ad_group_path.assert_called_once_with(test_customer_id, test_ad_group_id)
        mock_client.get_type.assert_called_once_with("AdGroupCriterionOperation")
        self.assertEqual(mock_ad_group_criterion.ad_group, mock_ad_group_path)
        self.assertEqual(mock_ad_group_criterion.user_list.user_list, test_user_list_rn)
        mock_ad_group_criterion_service.mutate_ad_group_criteria.assert_called_once_with(
            customer_id=test_customer_id, operations=[mock_ad_group_criterion_operation]
        )
        self.assertEqual(returned_rn, mock_criterion_rn)
        expected_stdout = (
            "Successfully created ad group criterion with resource name: "
            f"'{mock_criterion_rn}' targeting user list with resource name: "
            f"'{test_user_list_rn}' and with ad group with ID "
            f"{test_ad_group_id}.\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_stdout)

class TestModifyAdGroupBids(unittest.TestCase):
    @patch('examples.remarketing.set_up_remarketing.protobuf_helpers.field_mask')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_modify_ad_group_bids_success(self, mock_stdout, mock_field_mask):
        mock_client = Mock(name="GoogleAdsClient"); test_customer_id = "cust_bid_mod_789"; test_agc_rn = "adGroupCriteria/agc_rn_for_bid_mod"
        bid_modifier_value = 1.5; mock_updated_agc_rn = "adGroupCriteria/updated_agc_rn"
        mock_field_mask_object = Mock(name="FieldMaskObject"); mock_ad_group_criterion_service = Mock(name="AdGroupCriterionService")
        mock_client.get_service.return_value = mock_ad_group_criterion_service
        mock_agc_operation = Mock(name="AdGroupCriterionOperation")
        mock_agc_to_update = Mock(name="AdGroupCriterionToUpdate"); mock_agc_to_update._pb = Mock(name="AdGroupCriterionProtobuf")
        mock_agc_operation.update = mock_agc_to_update
        mock_client.get_type.return_value = mock_agc_operation
        mock_client.copy_from = Mock(); mock_field_mask.return_value = mock_field_mask_object
        mock_mutate_response = Mock(); mock_mutate_result = Mock(); mock_mutate_result.resource_name = mock_updated_agc_rn
        mock_mutate_response.results = [mock_mutate_result]
        mock_ad_group_criterion_service.mutate_ad_group_criteria.return_value = mock_mutate_response
        set_up_remarketing.modify_ad_group_bids(
            mock_client, test_customer_id, test_agc_rn, bid_modifier_value
        )
        mock_client.get_service.assert_called_once_with("AdGroupCriterionService")
        mock_client.get_type.assert_called_once_with("AdGroupCriterionOperation")
        self.assertEqual(mock_agc_to_update.resource_name, test_agc_rn)
        self.assertEqual(mock_agc_to_update.bid_modifier, bid_modifier_value)
        mock_field_mask.assert_called_once_with(None, mock_agc_to_update._pb)
        mock_client.copy_from.assert_called_once_with(mock_agc_operation.update_mask, mock_field_mask_object)
        mock_ad_group_criterion_service.mutate_ad_group_criteria.assert_called_once_with(
            customer_id=test_customer_id, operations=[mock_agc_operation]
        )
        expected_stdout = f"Updated bid for ad group criterion with resource name: '{mock_updated_agc_rn}'\n"
        self.assertEqual(mock_stdout.getvalue(), expected_stdout)

class TestGetUserListAdGroupCriteria(unittest.TestCase):
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_get_criteria_success(self, mock_stdout):
        mock_client = Mock(name="GoogleAdsClient"); test_customer_id = "cust_get_criteria_123"; test_campaign_id = "camp_get_criteria_456"
        mock_google_ads_service = Mock(name="GoogleAdsService"); mock_client.get_service.return_value = mock_google_ads_service
        mock_search_request = Mock(name="SearchGoogleAdsRequest"); mock_client.get_type.return_value = mock_search_request
        mock_row1 = Mock(); mock_row1.ad_group_criterion.resource_name = "agc_rn_1"
        mock_row2 = Mock(); mock_row2.ad_group_criterion.resource_name = "agc_rn_2"
        mock_google_ads_service.search.return_value = [mock_row1, mock_row2]
        returned_criteria_rns = set_up_remarketing.get_user_list_ad_group_criteria(
            mock_client, test_customer_id, test_campaign_id
        )
        mock_client.get_service.assert_called_once_with("GoogleAdsService")
        mock_client.get_type.assert_called_once_with("SearchGoogleAdsRequest")
        self.assertEqual(mock_search_request.customer_id, test_customer_id)
        expected_query_core = (
            "SELECT ad_group_criterion.criterion_id FROM ad_group_criterion "
            f"WHERE campaign.id = {test_campaign_id} AND ad_group_criterion.type = USER_LIST"
        )
        self.assertEqual(" ".join(mock_search_request.query.split()), " ".join(expected_query_core.split()))
        mock_google_ads_service.search.assert_called_once_with(request=mock_search_request)
        self.assertEqual(len(returned_criteria_rns), 2); self.assertIn("agc_rn_1", returned_criteria_rns); self.assertIn("agc_rn_2", returned_criteria_rns)
        captured_stdout = mock_stdout.getvalue()
        expected_literal_print = "Ad group criterion with resource name '{resource_name}' was found.\n"
        self.assertEqual(captured_stdout.count(expected_literal_print), 2)

class TestRemoveExistingCriteriaFromAdGroup(unittest.TestCase):
    @patch('examples.remarketing.set_up_remarketing.get_user_list_ad_group_criteria')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_remove_criteria_success(self, mock_stdout, mock_get_user_list_criteria):
        mock_client = Mock(name="GoogleAdsClient"); test_customer_id = "cust_remove_criteria_123"; test_campaign_id = "camp_remove_criteria_456"
        mock_criteria_to_remove = ["agc_rn_to_remove_1", "agc_rn_to_remove_2"]
        mock_get_user_list_criteria.return_value = mock_criteria_to_remove
        mock_ad_group_criterion_service = Mock(name="AdGroupCriterionService")
        mock_client.get_service.return_value = mock_ad_group_criterion_service
        created_operations = []
        def get_type_op_side_effect(type_name):
            if type_name == "AdGroupCriterionOperation":
                op = Mock(name=f"AdGroupCriterionOperation_{len(created_operations)}"); created_operations.append(op); return op
            return Mock()
        mock_client.get_type.side_effect = get_type_op_side_effect
        mock_mutate_response = Mock(); mock_mutate_result = Mock(); mock_mutate_result.resource_name = "removed_agc_rn_1_from_response"
        mock_mutate_response.results = [mock_mutate_result]
        mock_ad_group_criterion_service.mutate_ad_group_criteria.return_value = mock_mutate_response
        set_up_remarketing.remove_existing_criteria_from_ad_group(mock_client, test_customer_id, test_campaign_id)
        mock_get_user_list_criteria.assert_called_once_with(mock_client, test_customer_id, test_campaign_id)
        self.assertEqual(mock_client.get_type.call_count, len(mock_criteria_to_remove))
        mock_client.get_type.assert_has_calls([call("AdGroupCriterionOperation")] * len(mock_criteria_to_remove))
        self.assertEqual(len(created_operations), len(mock_criteria_to_remove))
        for i, op in enumerate(created_operations): self.assertEqual(op.remove, mock_criteria_to_remove[i])
        mock_ad_group_criterion_service.mutate_ad_group_criteria.assert_called_once_with(
            customer_id=test_customer_id, operations=created_operations
        )
        expected_stdout = f"Successfully removed ad group criterion with resource name: 'removed_agc_rn_1_from_response'\n"
        self.assertEqual(mock_stdout.getvalue(), expected_stdout)

class TestTargetAdsInCampaignToUserList(unittest.TestCase):
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_target_ads_in_campaign_to_user_list_success(self, mock_stdout):
        mock_client = Mock(name="GoogleAdsClient")
        test_customer_id = "cust_target_camp_123"; test_campaign_id = "camp_id_for_targeting"
        test_user_list_rn = "userLists/ul_rn_for_camp_targeting"; mock_campaign_path_val = f"customers/{test_customer_id}/campaigns/{test_campaign_id}"
        mock_criterion_rn = "campaignCriteria/camp_crit_rn_123"; mock_campaign_service = Mock(name="CampaignService")
        mock_campaign_criterion_service = Mock(name="CampaignCriterionService")
        def get_service_side_effect(service_name):
            if service_name == "CampaignService": return mock_campaign_service
            elif service_name == "CampaignCriterionService": return mock_campaign_criterion_service
            return Mock()
        mock_client.get_service.side_effect = get_service_side_effect
        mock_campaign_service.campaign_path.return_value = mock_campaign_path_val
        mock_campaign_criterion_operation = Mock(name="CampaignCriterionOperation")
        mock_campaign_criterion = Mock(name="CampaignCriterion")
        mock_campaign_criterion.user_list = Mock(name="UserListInfoOnCampaignCriterion")
        mock_campaign_criterion_operation.create = mock_campaign_criterion
        mock_client.get_type.return_value = mock_campaign_criterion_operation
        mock_mutate_response = Mock(); mock_mutate_result = Mock(); mock_mutate_result.resource_name = mock_criterion_rn
        mock_mutate_response.results = [mock_mutate_result]
        mock_campaign_criterion_service.mutate_campaign_criteria.return_value = mock_mutate_response
        returned_rn = set_up_remarketing.target_ads_in_campaign_to_user_list(
            mock_client, test_customer_id, test_campaign_id, test_user_list_rn
        )
        mock_client.get_service.assert_any_call("CampaignService"); mock_client.get_service.assert_any_call("CampaignCriterionService")
        mock_campaign_service.campaign_path.assert_called_once_with(test_customer_id, test_campaign_id)
        mock_client.get_type.assert_called_once_with("CampaignCriterionOperation")
        self.assertEqual(mock_campaign_criterion.campaign, mock_campaign_path_val)
        self.assertEqual(mock_campaign_criterion.user_list.user_list, test_user_list_rn)
        mock_campaign_criterion_service.mutate_campaign_criteria.assert_called_once_with(
            customer_id=test_customer_id, operations=[mock_campaign_criterion_operation]
        )
        self.assertEqual(returned_rn, mock_criterion_rn)
        expected_stdout = (
            "Successfully created campaign criterion with resource name "
            f"'{mock_criterion_rn}' targeting user list with resource name "
            f"'{test_user_list_rn}' with campaign with ID {test_campaign_id}\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_stdout)

class TestModifyCampaignBids(unittest.TestCase):
    @patch('examples.remarketing.set_up_remarketing.protobuf_helpers.field_mask')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_modify_campaign_bids_success(self, mock_stdout, mock_field_mask):
        mock_client = Mock(name="GoogleAdsClient"); test_customer_id = "cust_camp_bid_mod_123"; test_cc_rn = "campaignCriteria/cc_rn_for_bid_mod"
        bid_modifier_value = 1.8; mock_updated_cc_rn = "campaignCriteria/updated_cc_rn"
        mock_field_mask_object = Mock(name="FieldMaskObject"); mock_campaign_criterion_service = Mock(name="CampaignCriterionService")
        mock_client.get_service.return_value = mock_campaign_criterion_service
        mock_cc_operation = Mock(name="CampaignCriterionOperation")
        mock_cc_to_update = Mock(name="CampaignCriterionToUpdate"); mock_cc_to_update._pb = Mock(name="CampaignCriterionProtobuf")
        mock_cc_operation.update = mock_cc_to_update
        mock_client.get_type.return_value = mock_cc_operation
        mock_client.copy_from = Mock(); mock_field_mask.return_value = mock_field_mask_object
        mock_mutate_response = Mock(); mock_mutate_result = Mock(); mock_mutate_result.resource_name = mock_updated_cc_rn
        mock_mutate_response.results = [mock_mutate_result]
        mock_campaign_criterion_service.mutate_campaign_criteria.return_value = mock_mutate_response
        set_up_remarketing.modify_campaign_bids(
            mock_client, test_customer_id, test_cc_rn, bid_modifier_value
        )
        mock_client.get_service.assert_called_once_with("CampaignCriterionService")
        mock_client.get_type.assert_called_once_with("CampaignCriterionOperation")
        self.assertEqual(mock_cc_to_update.resource_name, test_cc_rn)
        self.assertEqual(mock_cc_to_update.bid_modifier, bid_modifier_value)
        mock_field_mask.assert_called_once_with(None, mock_cc_to_update._pb)
        mock_client.copy_from.assert_called_once_with(mock_cc_operation.update_mask, mock_field_mask_object)
        mock_campaign_criterion_service.mutate_campaign_criteria.assert_called_once_with(
            customer_id=test_customer_id, operations=[mock_cc_operation]
        )
        expected_stdout = (
            "Successfully updated the bid for campaign criterion with resource "
            f"name: '{mock_updated_cc_rn}'\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_stdout)

class TestMainFunctionForSetUpRemarketing(unittest.TestCase):
    @patch('examples.remarketing.set_up_remarketing.modify_campaign_bids')
    @patch('examples.remarketing.set_up_remarketing.target_ads_in_campaign_to_user_list')
    @patch('examples.remarketing.set_up_remarketing.remove_existing_criteria_from_ad_group')
    @patch('examples.remarketing.set_up_remarketing.modify_ad_group_bids')
    @patch('examples.remarketing.set_up_remarketing.target_ads_in_ad_group_to_user_list')
    @patch('examples.remarketing.set_up_remarketing.create_user_list')
    def test_main_orchestration_logic(
        self,
        mock_create_user_list,
        mock_target_ads_in_ad_group, # Corrected name based on patch order
        mock_modify_ad_group_bids,
        mock_remove_existing_criteria,
        mock_target_ads_in_campaign, # Corrected name
        mock_modify_campaign_bids
    ):
        mock_client = Mock(name="GoogleAdsClient_for_main_setup")
        test_customer_id = "main_cust_123"
        test_campaign_id = "main_camp_123" # string
        test_ad_group_id = "main_adgroup_123" # string
        test_bid_modifier = 1.5 # float

        # Configure return values for patched helpers whose output is used
        mock_user_list_rn = "userLists/main_ul_rn"
        mock_agc_rn = "adGroupCriteria/main_agc_rn"
        mock_cc_rn = "campaignCriteria/main_cc_rn"

        mock_create_user_list.return_value = mock_user_list_rn
        mock_target_ads_in_ad_group.return_value = mock_agc_rn
        mock_target_ads_in_campaign.return_value = mock_cc_rn
        # Other helpers don't have their return values used by main for further calls

        set_up_remarketing.main(
            mock_client,
            test_customer_id,
            test_campaign_id,
            test_ad_group_id,
            test_bid_modifier
        )

        mock_create_user_list.assert_called_once_with(mock_client, test_customer_id)
        mock_target_ads_in_ad_group.assert_called_once_with(
            mock_client, test_customer_id, test_ad_group_id, mock_user_list_rn
        )
        mock_modify_ad_group_bids.assert_called_once_with(
            mock_client, test_customer_id, mock_agc_rn, test_bid_modifier
        )
        mock_remove_existing_criteria.assert_called_once_with(
            mock_client, test_customer_id, test_campaign_id
        )
        mock_target_ads_in_campaign.assert_called_once_with(
            mock_client, test_customer_id, test_campaign_id, mock_user_list_rn
        )
        mock_modify_campaign_bids.assert_called_once_with(
            mock_client, test_customer_id, mock_cc_rn, test_bid_modifier
        )


if __name__ == "__main__":
    unittest.main()
