import unittest
from unittest import mock
import argparse
import sys

# Mock Google Ads Client and Exception if not available in the environment
try:
    from google.ads.googleads.client import GoogleAdsClient
    from google.ads.googleads.errors import GoogleAdsException
    from google.protobuf import field_mask_pb2
    from google.ads.googleads.v19.utils import protobuf_helpers
except ImportError:
    GoogleAdsClient = mock.MagicMock()
    GoogleAdsException = type('GoogleAdsException', (Exception,), {})
    field_mask_pb2 = mock.MagicMock() # Mock FieldMask if protobuf is not available
    protobuf_helpers = mock.MagicMock()


# Import the module to be tested
from examples.campaign_management import update_campaign_criterion_bid_modifier as ucc_script

class TestUpdateCampaignCriterionBidModifier(unittest.TestCase):

    @mock.patch.object(GoogleAdsClient, "load_from_storage")
    def setUp(self, mock_load_from_storage):
        self.mock_google_ads_client = mock.MagicMock(spec=GoogleAdsClient)
        self.mock_google_ads_client.configure_mock(version="v19")
        mock_load_from_storage.return_value = self.mock_google_ads_client

        self.mock_campaign_criterion_service = mock.MagicMock()
        self.mock_google_ads_client.get_service.return_value = self.mock_campaign_criterion_service

        # Mock path generation
        self.mock_campaign_criterion_service.campaign_criterion_path.side_effect = \
            lambda cid, camp_id, crit_id: f"customers/{cid}/campaignCriteria/{camp_id}~{crit_id}"

        # Mock get_type for operations and CampaignCriterion
        # The script does: operation = client.get_type("CampaignCriterionOperation")
        # operation.update.resource_name = ...
        # operation.update.bid_modifier = ...
        # So, operation.update should be a configurable mock (CampaignCriterion instance)
        def get_type_side_effect(type_name, version=None):
            if type_name == "CampaignCriterionOperation":
                op_mock = mock.MagicMock()
                op_mock.update = mock.MagicMock() # This will be the CampaignCriterion mock
                # Mock the _pb attribute if protobuf_helpers.field_mask uses it
                op_mock.update._pb = mock.MagicMock() 
                return op_mock
            elif type_name == "CampaignCriterion": # Though script doesn't call get_type("CampaignCriterion")
                 return mock.MagicMock() 
            return mock.MagicMock()

        self.mock_google_ads_client.get_type.side_effect = get_type_side_effect
        
        # Mock protobuf_helpers.field_mask
        # This helper creates a FieldMask object. We want to capture its creation.
        self.mock_field_mask_instance = mock.MagicMock(spec=field_mask_pb2.FieldMask)
        if hasattr(protobuf_helpers, "field_mask"):
            self.mock_protobuf_field_mask_patcher = mock.patch.object(
                protobuf_helpers, "field_mask", return_value=self.mock_field_mask_instance
            )
        else: # Fallback if protobuf_helpers is a generic mock
             self.mock_protobuf_field_mask_patcher = mock.patch(
                "google.ads.googleads.v19.utils.protobuf_helpers.field_mask",
                return_value=self.mock_field_mask_instance
            )
        self.mock_protobuf_field_mask = self.mock_protobuf_field_mask_patcher.start()


    def tearDown(self):
        self.mock_protobuf_field_mask_patcher.stop()


    @mock.patch("argparse.ArgumentParser")
    @mock.patch("builtins.print")
    def test_main_success(self, mock_print, mock_argparse):
        customer_id = "123"
        campaign_id = "456"
        criterion_id = "789"
        bid_modifier_value = 1.5

        mock_args = argparse.Namespace(
            customer_id=customer_id,
            campaign_id=campaign_id,
            criterion_id=criterion_id,
            bid_modifier_value=bid_modifier_value,
        )
        mock_argparse.return_value.parse_args.return_value = mock_args

        campaign_criterion_resource_name = f"customers/{customer_id}/campaignCriteria/{campaign_id}~{criterion_id}"
        self.mock_campaign_criterion_service.campaign_criterion_path.return_value = campaign_criterion_resource_name

        # Mock response for mutate_campaign_criteria
        mock_mutate_response = mock.MagicMock()
        mock_result = mock.MagicMock()
        mock_result.resource_name = campaign_criterion_resource_name # Usually the same for updates
        mock_mutate_response.results = [mock_result]
        self.mock_campaign_criterion_service.mutate_campaign_criteria.return_value = mock_mutate_response

        ucc_script.main(
            self.mock_google_ads_client, customer_id, campaign_id, criterion_id, bid_modifier_value
        )

        self.mock_google_ads_client.get_service.assert_called_once_with("CampaignCriterionService", version="v19")
        self.mock_campaign_criterion_service.campaign_criterion_path.assert_called_once_with(
            customer_id, campaign_id, criterion_id
        )

        self.mock_campaign_criterion_service.mutate_campaign_criteria.assert_called_once()
        call_args = self.mock_campaign_criterion_service.mutate_campaign_criteria.call_args
        self.assertEqual(call_args[1]['customer_id'], customer_id)
        
        operations = call_args[1]['operations']
        self.assertEqual(len(operations), 1)
        
        operation_sent = operations[0]
        campaign_criterion_update = operation_sent.update # This is the CampaignCriterion mock

        self.assertEqual(campaign_criterion_update.resource_name, campaign_criterion_resource_name)
        self.assertEqual(campaign_criterion_update.bid_modifier, bid_modifier_value)

        # Assert that protobuf_helpers.field_mask was called correctly
        self.mock_protobuf_field_mask.assert_called_once_with(None, campaign_criterion_update._pb)
        self.assertEqual(operation_sent.update_mask, self.mock_field_mask_instance)


        mock_print.assert_any_call(
            f"Campaign criterion with resource name '{mock_result.resource_name}' was updated."
        )

    @mock.patch("argparse.ArgumentParser")
    @mock.patch("builtins.print")
    @mock.patch("sys.exit")
    def test_main_google_ads_exception(self, mock_sys_exit, mock_print, mock_argparse):
        customer_id = "123"
        campaign_id = "456"
        criterion_id = "789"
        bid_modifier_value = 1.5
        mock_args = argparse.Namespace(
            customer_id=customer_id,
            campaign_id=campaign_id,
            criterion_id=criterion_id,
            bid_modifier_value=bid_modifier_value,
        )
        mock_argparse.return_value.parse_args.return_value = mock_args
        
        campaign_criterion_resource_name = f"customers/{customer_id}/campaignCriteria/{campaign_id}~{criterion_id}"
        self.mock_campaign_criterion_service.campaign_criterion_path.return_value = campaign_criterion_resource_name

        # Create a mock GoogleAdsException instance
        mock_failure = mock.MagicMock()
        mock_error = mock.MagicMock()
        mock_error.message = "Test CampaignCriterion Mutate Error"
        mock_failure.errors = [mock_error]
        google_ads_exception_instance = GoogleAdsException()
        google_ads_exception_instance._failure = mock_failure
        google_ads_exception_instance.request_id = "test_crit_req_id"

        self.mock_campaign_criterion_service.mutate_campaign_criteria.side_effect = google_ads_exception_instance

        ucc_script.main(
             self.mock_google_ads_client, customer_id, campaign_id, criterion_id, bid_modifier_value
        )

        printed_error = False
        for call in mock_print.call_args_list:
            if "Test CampaignCriterion Mutate Error" in str(call[0]) and "ErrorCode" in str(call[0]):
                printed_error = True
                break
        self.assertTrue(printed_error, "GoogleAdsException error message was not printed correctly.")
        mock_sys_exit.assert_called_once_with(1)

if __name__ == "__main__":
    unittest.main()
