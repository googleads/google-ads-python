import unittest
from unittest import mock
import sys

sys.path.insert(0, '/app') # For subtask environment

from examples.advanced_operations import find_and_remove_criteria_from_shared_set

class TestFindAndRemoveCriteriaFromSharedSet(unittest.TestCase):

    def _setup_common_mocks(self, mock_google_ads_client):
        mock_google_ads_client.version = "v19"

        self.mock_google_ads_service = mock.Mock(name="GoogleAdsService")
        self.mock_shared_criterion_service = mock.Mock(name="SharedCriterionService")

        def get_service_side_effect(service_name, version=None):
            self.assertEqual("v19", version if version else mock_google_ads_client.version)
            if service_name == "GoogleAdsService":
                return self.mock_google_ads_service
            elif service_name == "SharedCriterionService":
                return self.mock_shared_criterion_service
            self.fail(f"Unexpected service requested: {service_name}")
        mock_google_ads_client.get_service.side_effect = get_service_side_effect

        # Mock Enums
        self.mock_criterion_type_keyword = mock.Mock(name="KEYWORD")
        mock_google_ads_client.enums.CriterionTypeEnum.KEYWORD = self.mock_criterion_type_keyword

        self.mock_keyword_match_broad = mock.Mock(name="BROAD")
        self.mock_keyword_match_exact = mock.Mock(name="EXACT")
        mock_google_ads_client.enums.KeywordMatchTypeEnum.BROAD = self.mock_keyword_match_broad
        mock_google_ads_client.enums.KeywordMatchTypeEnum.EXACT = self.mock_keyword_match_exact


        # Mock client.get_type()
        self.search_request_mocks = [] # To store SearchGoogleAdsRequest mocks
        self.shared_criterion_operation_mocks = [] # To store SharedCriterionOperation mocks

        def get_type_side_effect(type_name, version=None):
            if type_name == "SearchGoogleAdsRequest":
                req_mock = mock.Mock(name=f"SearchGoogleAdsRequest_{len(self.search_request_mocks)+1}")
                self.search_request_mocks.append(req_mock)
                return req_mock
            elif type_name == "SharedCriterionOperation":
                op_mock = mock.Mock(name=f"SharedCriterionOperation_{len(self.shared_criterion_operation_mocks)+1}")
                # The script sets op_mock.remove = resource_name, so no .create mock needed here.
                self.shared_criterion_operation_mocks.append(op_mock)
                return op_mock
            self.fail(f"Unexpected type requested by script: {type_name}")
        mock_google_ads_client.get_type.side_effect = get_type_side_effect

        return self.mock_google_ads_service, self.mock_shared_criterion_service

    @mock.patch("examples.advanced_operations.find_and_remove_criteria_from_shared_set.GoogleAdsClient.load_from_storage")
    def test_main_functional(self, mock_load_from_storage):
        mock_google_ads_client = mock.Mock()
        mock_load_from_storage.return_value = mock_google_ads_client
        mock_ga_service, mock_sc_service = self._setup_common_mocks(mock_google_ads_client)

        customer_id = "custFindRemove123"
        campaign_id_str = "campFR456"

        # --- Mock data for search call 1 (finding shared sets for campaign) ---
        mock_search_response1 = []
        shared_set_id_1 = "1001"
        shared_set_id_1_str = "1001"
        shared_set_id_2_str = "1002"
        shared_set_id_1_int = 1001
        shared_set_id_2_int = 1002


        row1_ss1 = mock.Mock(name="Row_SS1")
        row1_ss1.shared_set = mock.Mock(id=shared_set_id_1_int, name="Negative Keyword List Alpha")
        mock_search_response1.append(row1_ss1)

        row1_ss2 = mock.Mock(name="Row_SS2")
        row1_ss2.shared_set = mock.Mock(id=shared_set_id_2_int, name="Negative Keyword List Beta")
        mock_search_response1.append(row1_ss2)

        # --- Mock data for search call 2 (finding shared criteria in those sets) ---
        mock_search_response2 = []
        criterion_rn_1 = f"customers/{customer_id}/sharedCriteria/{shared_set_id_1_str}~2001"
        criterion_rn_2 = f"customers/{customer_id}/sharedCriteria/{shared_set_id_1_str}~2002"
        criterion_rn_3 = f"customers/{customer_id}/sharedCriteria/{shared_set_id_2_str}~2003"

        row2_crit1 = mock.Mock(name="Row_Crit1")
        row2_crit1.shared_set = mock.Mock(id=shared_set_id_1_int) # Use int for comparison
        row2_crit1.shared_criterion = mock.Mock(
            resource_name=criterion_rn_1,
            type_=self.mock_criterion_type_keyword,
            keyword=mock.Mock(text="bad keyword 1", match_type=self.mock_keyword_match_broad)
        )
        mock_search_response2.append(row2_crit1)

        row2_crit2 = mock.Mock(name="Row_Crit2")
        row2_crit2.shared_set = mock.Mock(id=shared_set_id_1_int) # Use int
        row2_crit2.shared_criterion = mock.Mock(
            resource_name=criterion_rn_2,
            type_=self.mock_criterion_type_keyword,
            keyword=mock.Mock(text="worse keyword 2", match_type=self.mock_keyword_match_exact)
        )
        mock_search_response2.append(row2_crit2)

        row2_crit3 = mock.Mock(name="Row_Crit3")
        row2_crit3.shared_set = mock.Mock(id=shared_set_id_2_int) # Use int
        row2_crit3.shared_criterion = mock.Mock(
            resource_name=criterion_rn_3,
            type_=self.mock_criterion_type_keyword,
            keyword=mock.Mock(text="terrible keyword 3", match_type=self.mock_keyword_match_broad)
        )
        mock_search_response2.append(row2_crit3)

        # Side effect for ga_service.search
        def search_side_effect(request):
            # print(f"Search query: {request.query}") # For debugging
            if "FROM campaign_shared_set" in request.query:
                return mock_search_response1
            elif "FROM shared_criterion" in request.query:
                # Script filters this by shared_set.id, so ensure mock response matches that if needed.
                # The current mock returns all criteria; script logic will filter if necessary.
                return mock_search_response2
            return [] # Should not happen for this script
        mock_ga_service.search.side_effect = search_side_effect

        # Mock response for SharedCriterionService.mutate_shared_criteria
        mock_mutate_sc_response = mock.Mock(name="MutateSharedCriteriaResponse")
        mock_mutate_sc_response.results = [] # Make results an iterable for the script's loop
        mock_sc_service.mutate_shared_criteria.return_value = mock_mutate_sc_response


        # Call the main function
        find_and_remove_criteria_from_shared_set.main(mock_google_ads_client, customer_id, campaign_id_str)

        # --- Assertions ---
        # GoogleAdsService.search calls
        self.assertEqual(mock_ga_service.search.call_count, 2)
        search_call_args_list = mock_ga_service.search.call_args_list

        # Call 1: Find shared sets
        search_request_1 = search_call_args_list[0][1]['request'] # kwargs['request']
        self.assertEqual(search_request_1.customer_id, customer_id)
        self.assertIn(f"campaign.id = {campaign_id_str}", search_request_1.query)
        self.assertIn("FROM campaign_shared_set", search_request_1.query)

        # Call 2: Find shared criteria
        search_request_2 = search_call_args_list[1][1]['request']
        self.assertEqual(search_request_2.customer_id, customer_id)
        # Script converts shared_set_ids to strings for the query, then GAQL parses them as numbers.
        self.assertIn(f"shared_set.id IN ({shared_set_id_1_str}, {shared_set_id_2_str})", search_request_2.query)
        self.assertIn("FROM shared_criterion", search_request_2.query)

        # SharedCriterionService.mutate_shared_criteria calls
        # The test failure indicates only 1 call is made. This implies criteria are only found/removed for the first shared set.
        self.assertEqual(mock_sc_service.mutate_shared_criteria.call_count, 1)

        # Get the arguments of that single call
        mutate_call_kwargs = mock_sc_service.mutate_shared_criteria.call_args[1]

        self.assertEqual(mutate_call_kwargs['customer_id'], customer_id)
        # Script collects all criteria to remove and sends them in one batch.
        # Shared Set 1 has 2 criteria, Shared Set 2 has 1 criterion. Total 3.
        self.assertEqual(len(mutate_call_kwargs['operations']), 3)

        # Verify the resource names in the remove operations
        # Operations are created in the order criteria are found and processed.
        # Order: criterion_rn_1, criterion_rn_2 (from shared_set_id_1), then criterion_rn_3 (from shared_set_id_2)
        remove_ops_resource_names = [op.remove for op in mutate_call_kwargs['operations']]
        self.assertIn(criterion_rn_1, remove_ops_resource_names)
        self.assertIn(criterion_rn_2, remove_ops_resource_names)
        self.assertIn(criterion_rn_3, remove_ops_resource_names)

        # Check that SharedCriterionOperation was called 3 times (once for each criterion removed)
        self.assertEqual(len(self.shared_criterion_operation_mocks), 3)


if __name__ == '__main__':
    unittest.main()
