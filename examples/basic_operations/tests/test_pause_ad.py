import sys
import unittest
from io import StringIO
from unittest.mock import MagicMock, patch, call # ensure call is imported

# Add the parent directory to the Python path to allow importing from sibling directories
# This assumes the tests are run from the 'examples/basic_operations/tests/' directory
# or that the PYTHONPATH is set up appropriately.
sys.path.append("../..")

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v19.services.services.ad_group_ad_service import (
    AdGroupAdServiceClient,
)
from google.ads.googleads.v19.services.types.ad_group_ad_service import (
    AdGroupAdOperation,
    MutateAdGroupAdsResponse,
    MutateAdGroupAdResult,
)
from google.ads.googleads.v19.enums.types.ad_group_ad_status import (
    AdGroupAdStatusEnum,
)
from google.protobuf import field_mask_pb2

# Import the function to be tested
from basic_operations.pause_ad import main


class TestPauseAd(unittest.TestCase):
    # Helper to create a mock GoogleAdsException (can be shared or adapted from other tests)
    def _create_mock_google_ads_exception(self):
        mock_error = MagicMock()
        mock_error.code.return_value.name = "TEST_ERROR_CODE"
        mock_failure = MagicMock()
        mock_failure.errors = [MagicMock()]
        mock_failure.errors[0].message = "Test error message."
        mock_failure.errors[0].location.field_path_elements = []

        return GoogleAdsException(
            error=mock_error,
            failure=mock_failure,
            request_id="test_request_id",
            call=MagicMock(),
        )

    @patch("basic_operations.pause_ad.GoogleAdsClient.load_from_storage")
    def test_main_pause_ad_success(self, mock_load_from_storage):
        # --- Mock client and services ---
        mock_google_ads_client = MagicMock(spec=GoogleAdsClient)
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_ad_group_ad_service = MagicMock(spec=AdGroupAdServiceClient)
        mock_google_ads_client.get_service.return_value = (
            mock_ad_group_ad_service
        )

        # --- Configure mock client behavior ---
        # Mock get_type to return a real AdGroupAdOperation instance to be configured
        mock_google_ads_client.get_type.return_value = AdGroupAdOperation()
        # Mock enums - Create a mock for the 'enums' attribute
        mock_enums = MagicMock()
        mock_google_ads_client.enums = mock_enums
        # AdGroupAdStatusEnum.PAUSED is an enum member (usually an int)
        mock_google_ads_client.enums.AdGroupAdStatusEnum.PAUSED = AdGroupAdStatusEnum.AdGroupAdStatus.PAUSED

        # Mock client.copy_from to simulate the field mask copying
        def mock_copy_from(destination, source_field_mask):
            # In the real client, this copies fields from source to destination.
            # For the test, we need to ensure destination.paths gets populated
            # from source_field_mask.paths.
            # The source_field_mask is what protobuf_helpers.field_mask returns.
            destination.paths.extend(source_field_mask.paths)

        mock_google_ads_client.copy_from.side_effect = mock_copy_from

        # --- Configure mock service behavior ---
        customer_id = "test_customer_id"
        ad_group_id = "test_ad_group_id"
        ad_id = "test_ad_id"
        expected_resource_name = (
            f"customers/{customer_id}/adGroupAds/{ad_group_id}~{ad_id}"
        )
        mock_ad_group_ad_service.ad_group_ad_path.return_value = (
            expected_resource_name
        )

        # Mock the mutate response
        mock_mutate_response = MutateAdGroupAdsResponse()
        mock_result = MutateAdGroupAdResult()
        mock_result.resource_name = expected_resource_name
        mock_mutate_response.results.append(mock_result)
        mock_ad_group_ad_service.mutate_ad_group_ads.return_value = (
            mock_mutate_response
        )
        
        # --- Capture stdout ---
        captured_output = StringIO()
        sys.stdout = captured_output

        # --- Call the main function ---
        main(mock_google_ads_client, customer_id, ad_group_id, ad_id)

        # --- Assertions ---
        sys.stdout = sys.__stdout__  # Reset stdout

        # Check service calls
        mock_google_ads_client.get_service.assert_called_once_with(
            "AdGroupAdService"
        )
        mock_ad_group_ad_service.ad_group_ad_path.assert_called_once_with(
            customer_id, ad_group_id, ad_id
        )

        # Check the operation sent to mutate_ad_group_ads
        self.assertEqual(mock_ad_group_ad_service.mutate_ad_group_ads.call_count, 1)
        args, kwargs = mock_ad_group_ad_service.mutate_ad_group_ads.call_args
        self.assertEqual(kwargs["customer_id"], customer_id)
        
        sent_operations = kwargs["operations"]
        self.assertEqual(len(sent_operations), 1)
        operation = sent_operations[0]
        
        self.assertEqual(operation.update.resource_name, expected_resource_name)
        # This line was duplicated and the first instance was incorrect. Removing the incorrect one.
        # self.assertEqual(operation.update.status, AdGroupAdStatusEnum.PAUSED) 
        
        # Check update_mask (important for mutations)
        # The field_mask utility creates a FieldMask protobuf object.
        # We need to compare its 'paths' attribute.
        # Both 'resource_name' and 'status' are set on the ad_group_ad object,
        # so they will appear in the field mask.
        expected_mask = field_mask_pb2.FieldMask()
        # The order of paths can matter for direct list comparison.
        # Let's assume 'resource_name' then 'status' or check actual behavior.
        # Based on previous output, it's ['resource_name', 'status']
        expected_mask.paths.append("resource_name")
        expected_mask.paths.append("status")
        # Ensure we are comparing the .status field to the correct enum member value
        self.assertEqual(operation.update.status, AdGroupAdStatusEnum.AdGroupAdStatus.PAUSED)
        self.assertCountEqual(operation.update_mask.paths, expected_mask.paths) # Use assertCountEqual for path comparison


        # Check output
        self.assertIn(
            f"Paused ad group ad {expected_resource_name}.",
            captured_output.getvalue(),
        )

    @patch("basic_operations.pause_ad.GoogleAdsClient.load_from_storage")
    def test_main_pause_ad_failure_api_error(self, mock_load_from_storage):
        # --- Mock client and services ---
        mock_google_ads_client = MagicMock(spec=GoogleAdsClient)
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_ad_group_ad_service = MagicMock(spec=AdGroupAdServiceClient)
        mock_google_ads_client.get_service.return_value = (
            mock_ad_group_ad_service
        )
        
        # --- Configure mock client behavior ---
        mock_google_ads_client.get_type.return_value = AdGroupAdOperation()
        # Mock enums - Create a mock for the 'enums' attribute
        mock_enums = MagicMock()
        mock_google_ads_client.enums = mock_enums
        # AdGroupAdStatusEnum.PAUSED is an enum member (usually an int)
        mock_google_ads_client.enums.AdGroupAdStatusEnum.PAUSED = AdGroupAdStatusEnum.AdGroupAdStatus.PAUSED

        # --- Configure mock service behavior (specifically ad_group_ad_path) ---
        customer_id_fail = "test_customer_id_fail"
        ad_group_id_fail = "test_ad_group_id_fail"
        ad_id_fail = "test_ad_id_fail"
        expected_resource_name_fail = (
            f"customers/{customer_id_fail}/adGroupAds/{ad_group_id_fail}~{ad_id_fail}"
        )
        mock_ad_group_ad_service.ad_group_ad_path.return_value = (
            expected_resource_name_fail
        )

        # --- Configure mock service to raise an exception ---
        mock_api_exception = self._create_mock_google_ads_exception()
        mock_ad_group_ad_service.mutate_ad_group_ads.side_effect = (
            mock_api_exception
        )

        # --- Call main and assert exception ---
        with self.assertRaises(GoogleAdsException) as context:
            main(
                mock_google_ads_client,
                customer_id_fail, # Use specific IDs for this test
                ad_group_id_fail,
                ad_id_fail,
            )
        
        self.assertEqual(context.exception, mock_api_exception)
        # Verify mutate_ad_group_ads was called, leading to the exception
        mock_ad_group_ad_service.mutate_ad_group_ads.assert_called_once()


if __name__ == "__main__":
    unittest.main()
