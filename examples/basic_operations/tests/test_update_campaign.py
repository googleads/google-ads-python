import sys
import unittest
from io import StringIO
from unittest.mock import MagicMock, patch

sys.path.append("../..")

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v19.resources.types.campaign import Campaign
from google.ads.googleads.v19.services.services.campaign_service import (
    CampaignServiceClient,
)
from google.ads.googleads.v19.services.types.campaign_service import (
    CampaignOperation,
    MutateCampaignsResponse,
    MutateCampaignResult,
)
from google.ads.googleads.v19.enums.types.campaign_status import (
    CampaignStatusEnum,
)
from google.protobuf import field_mask_pb2

from basic_operations.update_campaign import main


class TestUpdateCampaign(unittest.TestCase):
    def _create_mock_google_ads_exception(self):
        mock_error = MagicMock()
        mock_error_code = MagicMock()
        mock_error_code.name = "TEST_ERROR_CODE"
        mock_error.code.return_value = mock_error_code
        mock_failure = MagicMock()
        mock_error_detail = MagicMock()
        mock_error_detail.message = "Test error message."
        mock_error_detail.location.field_path_elements = []
        mock_failure.errors = [mock_error_detail]
        return GoogleAdsException(
            error=mock_error,
            failure=mock_failure,
            request_id="test_request_id",
            call=MagicMock(),
        )

    @patch("basic_operations.update_campaign.GoogleAdsClient.load_from_storage")
    def test_main_update_campaign_success(self, mock_load_from_storage):
        mock_google_ads_client = MagicMock(spec=GoogleAdsClient)
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_campaign_service = MagicMock(spec=CampaignServiceClient)
        mock_google_ads_client.get_service.return_value = mock_campaign_service

        mock_google_ads_client.get_type.return_value = CampaignOperation()

        mock_enums = MagicMock()
        mock_google_ads_client.enums = mock_enums
        mock_google_ads_client.enums.CampaignStatusEnum.PAUSED = (
            CampaignStatusEnum.CampaignStatus.PAUSED
        )

        def mock_copy_from(destination_mask, source_field_mask):
            destination_mask.paths.extend(source_field_mask.paths)
        mock_google_ads_client.copy_from.side_effect = mock_copy_from
        
        customer_id = "test_customer_id"
        campaign_id = "test_campaign_id"
        expected_resource_name = (
            f"customers/{customer_id}/campaigns/{campaign_id}"
        )
        mock_campaign_service.campaign_path.return_value = expected_resource_name

        mock_mutate_response = MutateCampaignsResponse()
        mock_result = MutateCampaignResult()
        mock_result.resource_name = expected_resource_name
        mock_mutate_response.results.append(mock_result)
        mock_campaign_service.mutate_campaigns.return_value = mock_mutate_response

        captured_output = StringIO()
        sys.stdout = captured_output

        main(mock_google_ads_client, customer_id, campaign_id)

        sys.stdout = sys.__stdout__

        mock_google_ads_client.get_service.assert_called_once_with("CampaignService")
        mock_campaign_service.campaign_path.assert_called_once_with(
            customer_id, campaign_id
        )

        self.assertEqual(mock_campaign_service.mutate_campaigns.call_count, 1)
        args, kwargs = mock_campaign_service.mutate_campaigns.call_args
        self.assertEqual(kwargs["customer_id"], customer_id)
        
        sent_operations = kwargs["operations"]
        self.assertEqual(len(sent_operations), 1)
        operation = sent_operations[0]

        self.assertEqual(operation.update.resource_name, expected_resource_name)
        self.assertEqual(operation.update.status, CampaignStatusEnum.CampaignStatus.PAUSED)
        # Verify nested attribute for network_settings
        self.assertEqual(operation.update.network_settings.target_search_network, False)

        expected_mask = field_mask_pb2.FieldMask()
        # Fields set: resource_name, status, network_settings.target_search_network
        # Note: nested fields are often represented as "network_settings.target_search_network"
        # However, if target_search_network defaults to False, setting it to False
        # will not be included in the field_mask.
        # Assuming target_search_network defaults to False.
        expected_paths = ["resource_name", "status"]
        self.assertCountEqual(operation.update_mask.paths, expected_paths)

        self.assertIn(
            f"Updated campaign {expected_resource_name}.",
            captured_output.getvalue(),
        )

    @patch("basic_operations.update_campaign.GoogleAdsClient.load_from_storage")
    def test_main_update_campaign_failure_api_error(self, mock_load_from_storage):
        mock_google_ads_client = MagicMock(spec=GoogleAdsClient)
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_campaign_service = MagicMock(spec=CampaignServiceClient)
        mock_google_ads_client.get_service.return_value = mock_campaign_service

        mock_google_ads_client.get_type.return_value = CampaignOperation()
        
        mock_enums = MagicMock()
        mock_google_ads_client.enums = mock_enums
        mock_google_ads_client.enums.CampaignStatusEnum.PAUSED = (
            CampaignStatusEnum.CampaignStatus.PAUSED
        )
        
        mock_google_ads_client.copy_from.side_effect = lambda dest, src: dest.paths.extend(src.paths)

        customer_id = "test_customer_id_fail"
        campaign_id = "test_campaign_id_fail"
        
        expected_resource_name_fail = (
            f"customers/{customer_id}/campaigns/{campaign_id}"
        )
        mock_campaign_service.campaign_path.return_value = expected_resource_name_fail

        mock_api_exception = self._create_mock_google_ads_exception()
        mock_campaign_service.mutate_campaigns.side_effect = mock_api_exception

        with self.assertRaises(GoogleAdsException) as context:
            main(mock_google_ads_client, customer_id, campaign_id)
        
        self.assertEqual(context.exception, mock_api_exception)
        mock_campaign_service.mutate_campaigns.assert_called_once()

if __name__ == "__main__":
    unittest.main()
