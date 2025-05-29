import unittest
from unittest import mock
import argparse
import sys

# Assuming google.ads.googleads.client and google.ads.googleads.errors are available in the environment
# If not, these will need to be mocked more extensively or the environment needs to be set up
try:
    from google.ads.googleads.client import GoogleAdsClient
    from google.ads.googleads.errors import GoogleAdsException
except ImportError:
    # Mock these classes if they are not available in the testing environment
    GoogleAdsClient = mock.MagicMock()
    GoogleAdsException = type('GoogleAdsException', (Exception,), {})

# This assumes add_campaign_labels.py is in the parent directory and can be imported.
# If the structure is different, this import will need to be adjusted.
# For simplicity, we'll assume it can be imported. If not, we might need to use sys.path manipulations
# or mock the module itself if we are only testing the logic within main.
# For now, let's try to import it directly.
from examples.campaign_management import add_campaign_labels


class TestAddCampaignLabels(unittest.TestCase):
    @mock.patch("examples.campaign_management.add_campaign_labels.GoogleAdsClient.load_from_storage")
    def setUp(self, mock_load_from_storage):
        self.mock_google_ads_client = mock.MagicMock(spec=GoogleAdsClient)
        mock_load_from_storage.return_value = self.mock_google_ads_client
        
        # Configure the client to specify the version
        self.mock_google_ads_client.configure_mock(version="v19")

        self.mock_campaign_label_service = mock.MagicMock()
        self.mock_campaign_service = mock.MagicMock()
        self.mock_label_service = mock.MagicMock()

        self.mock_google_ads_client.get_service.side_effect = lambda service_name, version: {
            "CampaignLabelService": self.mock_campaign_label_service,
            "CampaignService": self.mock_campaign_service,
            "LabelService": self.mock_label_service,
        }.get(service_name)
        
        # Mock the label_path and campaign_path methods
        self.mock_label_service.label_path.side_effect = lambda customer_id, label_id: f"customers/{customer_id}/labels/{label_id}"
        self.mock_campaign_service.campaign_path.side_effect = lambda customer_id, campaign_id: f"customers/{customer_id}/campaigns/{campaign_id}"


    @mock.patch("argparse.ArgumentParser")
    @mock.patch("builtins.print")
    def test_main_success(self, mock_print, mock_argparse_parser):
        mock_args = argparse.Namespace(
            customer_id="1234567890",
            label_id="987654321",
            campaign_ids=["111111111", "222222222"]
        )
        mock_argparse_parser.return_value.parse_args.return_value = mock_args

        # Mock the CampaignLabelOperation
        mock_campaign_label_operation = mock.MagicMock()
        self.mock_google_ads_client.get_type.return_value = mock_campaign_label_operation
        
        # Mock the mutate_campaign_labels response
        mock_mutate_response = mock.MagicMock()
        mock_result = mock.MagicMock()
        mock_result.resource_name = "customers/1234567890/campaignLabels/111111111~987654321"
        mock_mutate_response.results = [mock_result]
        self.mock_campaign_label_service.mutate_campaign_labels.return_value = mock_mutate_response

        add_campaign_labels.main(
            self.mock_google_ads_client,
            mock_args.customer_id,
            mock_args.label_id,
            mock_args.campaign_ids
        )

        self.mock_google_ads_client.get_service.assert_any_call("CampaignLabelService", version="v19")
        self.mock_google_ads_client.get_service.assert_any_call("CampaignService", version="v19")
        self.mock_google_ads_client.get_service.assert_any_call("LabelService", version="v19")
        
        self.mock_label_service.label_path.assert_called_once_with("1234567890", "987654321")
        
        self.mock_campaign_service.campaign_path.assert_any_call("1234567890", "111111111")
        self.mock_campaign_service.campaign_path.assert_any_call("1234567890", "222222222")
        self.assertEqual(self.mock_campaign_service.campaign_path.call_count, 2)

        self.mock_campaign_label_service.mutate_campaign_labels.assert_called_once()
        args, kwargs = self.mock_campaign_label_service.mutate_campaign_labels.call_args
        self.assertEqual(kwargs['customer_id'], "1234567890")
        self.assertEqual(len(kwargs['operations']), 2)
        
        # Check that the operations were created correctly
        # Assuming get_type was called to create CampaignLabelOperation instances
        self.mock_google_ads_client.get_type.assert_called_with("CampaignLabelOperation", version="v19")
        
        # Check print statements
        mock_print.assert_any_call(
            "Created campaign label with resource name: "
            "'customers/1234567890/campaignLabels/111111111~987654321'."
        )


    @mock.patch("argparse.ArgumentParser")
    @mock.patch("builtins.print")
    @mock.patch("sys.exit")
    def test_main_google_ads_exception(self, mock_sys_exit, mock_print, mock_argparse_parser):
        mock_args = argparse.Namespace(
            customer_id="1234567890",
            label_id="987654321",
            campaign_ids=["111111111"]
        )
        mock_argparse_parser.return_value.parse_args.return_value = mock_args

        # Mock the CampaignLabelOperation
        mock_campaign_label_operation = mock.MagicMock()
        self.mock_google_ads_client.get_type.return_value = mock_campaign_label_operation

        # Configure the service to raise GoogleAdsException
        # Create a mock GoogleAdsException instance
        mock_failure = mock.MagicMock()
        mock_error = mock.MagicMock()
        mock_error.message = "Test error message"
        mock_failure.errors = [mock_error]
        
        # The exception instance needs a _failure attribute
        google_ads_exception_instance = GoogleAdsException()
        google_ads_exception_instance._failure = mock_failure

        self.mock_campaign_label_service.mutate_campaign_labels.side_effect = google_ads_exception_instance

        add_campaign_labels.main(
            self.mock_google_ads_client,
            mock_args.customer_id,
            mock_args.label_id,
            mock_args.campaign_ids
        )

        self.mock_campaign_label_service.mutate_campaign_labels.assert_called_once()
        
        # Check print statements for error handling
        mock_print.assert_any_call(
            "Request with ID '{google_ads_exception_instance.request_id}' failed with status " # Note: request_id won't be populated here
            "'{google_ads_exception_instance.failure.errors[0].error_code.name}' and includes the following errors:"
        ) # This assertion is a bit fragile due to the f-string in the original code.
        # A more robust check would be to check for parts of the string.
        
        printed_error_message = False
        for call_args in mock_print.call_args_list:
            if "Test error message" in call_args[0][0] and "ErrorCode.UNSPECIFIED" in call_args[0][0]: # Assuming default error code if not set
                 printed_error_message = True
                 break
        self.assertTrue(printed_error_message, "Expected error message was not printed.")


        printed_error_details = False
        for call_args in mock_print.call_args_list:
            if "Error with message" in call_args[0][0] and "Test error message" in call_args[0][0]:
                 printed_error_details = True
                 break
        self.assertTrue(printed_error_details, "Expected error details were not printed.")


        mock_sys_exit.assert_called_once_with(1)

if __name__ == "__main__":
    unittest.main()
