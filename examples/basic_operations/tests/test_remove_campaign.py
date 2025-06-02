import sys
import unittest
from io import StringIO
from unittest.mock import MagicMock, patch

sys.path.append("../..")

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v19.services.services.campaign_service import (
    CampaignServiceClient,
)
from google.ads.googleads.v19.services.types.campaign_service import (
    CampaignOperation,
    MutateCampaignsResponse,
    MutateCampaignResult,
)

from basic_operations.remove_campaign import main


class TestRemoveCampaign(unittest.TestCase):
    def _create_mock_google_ads_exception(self):
        mock_error = MagicMock()
        # Simulating a code() method that returns an object with a name attribute
        mock_error_code = MagicMock()
        mock_error_code.name = "TEST_ERROR_CODE"
        mock_error.code.return_value = mock_error_code
        
        mock_failure = MagicMock()
        mock_error_detail = MagicMock()
        mock_error_detail.message = "Test error message."
        # Ensure location and field_path_elements are mockable if accessed
        mock_error_detail.location.field_path_elements = []
        mock_failure.errors = [mock_error_detail]

        return GoogleAdsException(
            error=mock_error,
            failure=mock_failure,
            request_id="test_request_id",
            call=MagicMock(), # Mocking the gRPC call object
        )

    @patch("basic_operations.remove_campaign.GoogleAdsClient.load_from_storage")
    def test_main_remove_campaign_success(self, mock_load_from_storage):
        mock_google_ads_client = MagicMock(spec=GoogleAdsClient)
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_campaign_service = MagicMock(spec=CampaignServiceClient)
        mock_google_ads_client.get_service.return_value = mock_campaign_service

        # Configure client.get_type to return a real CampaignOperation
        # This allows us to inspect the 'remove' attribute directly.
        mock_google_ads_client.get_type.return_value = CampaignOperation()

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

        sys.stdout = sys.__stdout__  # Reset stdout

        mock_google_ads_client.get_service.assert_called_once_with("CampaignService")
        mock_campaign_service.campaign_path.assert_called_once_with(
            customer_id, campaign_id
        )
        
        # Assert that mutate_campaigns was called correctly
        self.assertEqual(mock_campaign_service.mutate_campaigns.call_count, 1)
        args, kwargs = mock_campaign_service.mutate_campaigns.call_args
        self.assertEqual(kwargs["customer_id"], customer_id)
        
        sent_operations = kwargs["operations"]
        self.assertEqual(len(sent_operations), 1)
        operation = sent_operations[0]
        self.assertEqual(operation.remove, expected_resource_name) # Key check for remove operation

        self.assertIn(
            f"Removed campaign {expected_resource_name}.",
            captured_output.getvalue(),
        )

    @patch("basic_operations.remove_campaign.GoogleAdsClient.load_from_storage")
    def test_main_remove_campaign_failure_api_error(self, mock_load_from_storage):
        mock_google_ads_client = MagicMock(spec=GoogleAdsClient)
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_campaign_service = MagicMock(spec=CampaignServiceClient)
        mock_google_ads_client.get_service.return_value = mock_campaign_service
        
        # Configure client.get_type for consistency, though not strictly needed for this error path
        # if the error happens before its usage for populating the operation.
        mock_google_ads_client.get_type.return_value = CampaignOperation()

        customer_id = "test_customer_id_fail"
        campaign_id = "test_campaign_id_fail"
        # Configure campaign_path even for failure test, as it's called before mutate
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
