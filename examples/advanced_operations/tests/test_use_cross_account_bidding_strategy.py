import unittest
from unittest import mock
import sys
import uuid # Script uses uuid

# sys.path.insert(0, '/app') # For subtask environment - REMOVED

from examples.advanced_operations import use_cross_account_bidding_strategy
from google.protobuf import field_mask_pb2 # For creating FieldMask

class TestUseCrossAccountBiddingStrategy(unittest.TestCase):

    def _setup_common_mocks(self, mock_google_ads_client):
        mock_google_ads_client.version = "v19"
        self.mock_objects_created_by_get_type = {}

        # Mock Services
        self.mock_bidding_strategy_service = mock.Mock(name="BiddingStrategyService")
        self.mock_google_ads_service = mock.Mock(name="GoogleAdsService") # For search_stream
        self.mock_campaign_service = mock.Mock(name="CampaignService")

        def get_service_side_effect(service_name, version=None):
            self.assertEqual("v19", version if version else mock_google_ads_client.version)
            service_map = {
                "BiddingStrategyService": self.mock_bidding_strategy_service,
                "GoogleAdsService": self.mock_google_ads_service,
                "CampaignService": self.mock_campaign_service,
            }
            if service_name in service_map:
                return service_map[service_name]
            self.fail(f"Unexpected service requested: {service_name}")
        mock_google_ads_client.get_service.side_effect = get_service_side_effect

        # Mock Enums
        mock_google_ads_client.enums.BiddingStrategyTypeEnum.TARGET_SPEND = "TARGET_SPEND_TYPE"

        # Mock client.get_type()
        def get_type_side_effect(type_name, version=None):
            if type_name == "BiddingStrategyOperation":
                op_mock = mock.Mock(name=type_name)
                create_mock = mock.Mock(name="BiddingStrategy_Create")
                create_mock.target_spend = mock.Mock(name="TargetSpend_on_BiddingStrategy")
                op_mock.create = create_mock
                self.mock_objects_created_by_get_type["BiddingStrategy"] = create_mock
                return op_mock
            elif type_name == "CampaignOperation":
                op_mock = mock.Mock(name=type_name)
                update_mock = mock.Mock(name="Campaign_Update")
                # For field_mask: campaign_update_mock._pb.DESCRIPTOR.fields_by_name
                mock_pb = mock.Mock(name="_pb_for_CampaignUpdate")
                mock_descriptor = mock.Mock(name="DESCRIPTOR_for_Campaign_pb")
                # Add fields that are expected to be in the update_mask
                mock_descriptor.fields_by_name = ["bidding_strategy"]
                mock_pb.DESCRIPTOR = mock_descriptor
                update_mock._pb = mock_pb
                op_mock.update = update_mock
                self.mock_objects_created_by_get_type["Campaign_update"] = update_mock
                return op_mock
            elif type_name == "TargetSpend": # Though script gets it via bidding_strategy.target_spend
                return mock.Mock(name="TargetSpend")
            elif type_name == "FieldMask": # For protobuf_helpers.field_mask
                # The field_mask function itself creates this, but if script asks for it by type
                return field_mask_pb2.FieldMask

            self.fail(f"Unexpected type requested by script: {type_name}")
        mock_google_ads_client.get_type.side_effect = get_type_side_effect

        return (self.mock_bidding_strategy_service, self.mock_google_ads_service,
                self.mock_campaign_service)

    @mock.patch("examples.advanced_operations.use_cross_account_bidding_strategy.uuid4") # Corrected patch target
    @mock.patch("examples.advanced_operations.use_cross_account_bidding_strategy.GoogleAdsClient.load_from_storage")
    def test_main_functional(self, mock_load_from_storage, mock_script_uuid4): # Renamed mock arg
        mock_google_ads_client = mock.Mock()
        mock_load_from_storage.return_value = mock_google_ads_client
        mock_script_uuid4.return_value = "mock-strategy-uuid" # Configure the correct mock

        (mock_bidding_strategy_service, mock_google_ads_service,
         mock_campaign_service) = self._setup_common_mocks(mock_google_ads_client)

        customer_id = "clientCust123"
        manager_customer_id = "managerCust456"
        campaign_id_str = "camp789"

        strategy_name_base = "Maximize Clicks #mock-strategy-uuid" # Corrected: script uses '#'
        # This will be the name of the strategy created by manager and then found by client

        # Expected resource names
        expected_bidding_strategy_rn = f"customers/{manager_customer_id}/biddingStrategies/bs1001"
        # The ID for accessible strategy can be different from the one created if we want to test that logic
        # For simplicity, let's assume the accessible strategy found IS the one created by the manager.
        # So, its ID would be bs1001, and owner_customer_id would be manager_customer_id.
        # The resource name for accessible_bidding_strategy is the same as bidding_strategy.

        expected_campaign_rn = f"customers/{customer_id}/campaigns/{campaign_id_str}"

        # Configure service responses
        mock_bidding_strategy_service.mutate_bidding_strategies.return_value = mock.Mock(
            results=[mock.Mock(resource_name=expected_bidding_strategy_rn)]
        )
        mock_campaign_service.mutate_campaigns.return_value = mock.Mock(
            results=[mock.Mock(resource_name=expected_campaign_rn)] # Campaign update response
        )
        mock_campaign_service.campaign_path.return_value = expected_campaign_rn


        # --- Mock data for search_stream calls ---
        # Search 1: List manager's bidding strategies
        mock_search_stream_response1 = []
        row1_bs = mock.Mock(name="Row_BiddingStrategy_Manager")
        row1_bs.bidding_strategy = mock.Mock(
            id="1001", # Corresponds to bs1001 in expected_bidding_strategy_rn
            name=strategy_name_base,
            type_="TARGET_SPEND_TYPE",
            currency_code="USD" # Script sets this
        )
        mock_search_stream_response1.append(row1_bs)

        # Search 2: List accessible bidding strategies for client
        mock_search_stream_response2 = []
        row2_abs = mock.Mock(name="Row_AccessibleBiddingStrategy_Client")
        row2_abs.accessible_bidding_strategy = mock.Mock(
            resource_name=expected_bidding_strategy_rn, # Full RN
            id="1001",
            name=strategy_name_base,
            type_="TARGET_SPEND_TYPE",
            owner_customer_id=manager_customer_id,
            owner_descriptive_name="Manager Account Name"
        )
        mock_search_stream_response2.append(row2_abs)

        # Store customer_id from test method scope for use in side_effect
        self.current_client_customer_id_for_test = customer_id

        def search_stream_side_effect_fn(*, customer_id: str, query: str):
            # manager_customer_id is from the outer scope of test_main_functional
            if "FROM bidding_strategy" in query and customer_id == manager_customer_id:
                mock_stream_response = mock.Mock(name="SearchStreamResponse_ForManagerBS")
                mock_stream_response.results = mock_search_stream_response1 # List of GoogleAdsRow mocks
                return iter([mock_stream_response])
            # self.current_client_customer_id_for_test is the client's customer_id
            elif "FROM accessible_bidding_strategy" in query and customer_id == self.current_client_customer_id_for_test:
                mock_stream_response = mock.Mock(name="SearchStreamResponse_ForClientABS")
                mock_stream_response.results = mock_search_stream_response2 # List of GoogleAdsRow mocks
                return iter([mock_stream_response])
            self.fail(f"Unexpected search query or customer_id for search_stream: Query='{query}', CustID='{customer_id}'")
            return iter([]) # Should not be reached in a successful test
        mock_google_ads_service.search_stream.side_effect = search_stream_side_effect_fn

        # Call main
        use_cross_account_bidding_strategy.main(
            mock_google_ads_client, customer_id, manager_customer_id, campaign_id_str
        )

        # --- Assertions ---
        # 1. BiddingStrategyService - Create strategy under manager
        mock_bidding_strategy_service.mutate_bidding_strategies.assert_called_once()
        bs_call_args = mock_bidding_strategy_service.mutate_bidding_strategies.call_args
        self.assertEqual(bs_call_args[1]['customer_id'], manager_customer_id) # Check kwargs
        bs_payload = self.mock_objects_created_by_get_type.get("BiddingStrategy") # This is the BiddingStrategy_Create mock
        self.assertIsNotNone(bs_payload, "BiddingStrategy mock not found in mock_objects_created_by_get_type")
        # bs_payload is the mock object itself, not a list.
        self.assertEqual(bs_payload.name, strategy_name_base)
        # self.assertEqual(bs_payload.type_, "TARGET_SPEND_TYPE") # Script doesn't set type_ directly on create
        self.assertEqual(bs_payload.currency_code, "USD")
        self.assertIsNotNone(bs_payload.target_spend) # Verifies that the script set the target_spend oneof field

        # 2. GoogleAdsService.search_stream - List manager's strategies
        self.assertEqual(mock_google_ads_service.search_stream.call_count, 2)
        search_call1_kwargs = mock_google_ads_service.search_stream.call_args_list[0][1] # [call_idx][args_or_kwargs_tuple_idx (1 for kwargs)]
        self.assertEqual(search_call1_kwargs['customer_id'], manager_customer_id)
        self.assertIn("FROM bidding_strategy", search_call1_kwargs['query'])
        # The script's first search query does not filter by name, it lists all.

        # 3. GoogleAdsService.search_stream - List accessible strategies for client
        search_call2_kwargs = mock_google_ads_service.search_stream.call_args_list[1][1]
        self.assertEqual(search_call2_kwargs['customer_id'], customer_id) # client customer_id
        self.assertIn("FROM accessible_bidding_strategy", search_call2_kwargs['query'])
        # The script's second search query does not filter by owner_customer_id or id by default.
        # It iterates through results later to find the specific strategy.


        # 4. CampaignService.campaign_path - Called by script
        mock_campaign_service.campaign_path.assert_called_once_with(customer_id, campaign_id_str)

        # 5. CampaignService.mutate_campaigns - Update client campaign
        mock_campaign_service.mutate_campaigns.assert_called_once()
        campaign_call_args = mock_campaign_service.mutate_campaigns.call_args
        self.assertEqual(campaign_call_args[1]['customer_id'], customer_id) # Check kwargs
        campaign_update_payload = self.mock_objects_created_by_get_type.get("Campaign_update") # This is Campaign_Update mock
        self.assertIsNotNone(campaign_update_payload, "Campaign_update mock not found")
        self.assertEqual(campaign_update_payload.resource_name, expected_campaign_rn)
        self.assertEqual(campaign_update_payload.bidding_strategy, expected_bidding_strategy_rn)

        # Check update_mask from the CampaignOperation sent
        mutate_kwargs = campaign_call_args[1] # Keyword arguments
        self.assertIn('operations', mutate_kwargs)
        campaign_operations_list = mutate_kwargs['operations']
        self.assertEqual(len(campaign_operations_list), 1)
        campaign_operation_sent = campaign_operations_list[0] # This is the CampaignOperation object
        self.assertIn("bidding_strategy", campaign_operation_sent.update_mask.paths)


if __name__ == '__main__':
    unittest.main()
