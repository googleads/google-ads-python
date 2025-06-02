import sys
import unittest
from io import StringIO
from unittest.mock import MagicMock, patch

sys.path.append("../..")

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v19.resources.types.google_ads_field import (
    GoogleAdsField,
)
from google.ads.googleads.v19.services.services.google_ads_field_service import (
    GoogleAdsFieldServiceClient,
)
from google.ads.googleads.v19.services.types.google_ads_field_service import (
    SearchGoogleAdsFieldsRequest,
    SearchGoogleAdsFieldsResponse,
)
# It's good to import the enums if we plan to set them with specific values
from google.ads.googleads.v19.enums.types.google_ads_field_category import (
    GoogleAdsFieldCategoryEnum,
)
from google.ads.googleads.v19.enums.types.google_ads_field_data_type import (
    GoogleAdsFieldDataTypeEnum,
)

from basic_operations.search_for_google_ads_fields import main


class TestSearchGoogleAdsFields(unittest.TestCase):
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

    @patch("basic_operations.search_for_google_ads_fields.GoogleAdsClient.load_from_storage")
    @patch("basic_operations.search_for_google_ads_fields.sys.exit")
    def test_main_no_fields_found(self, mock_sys_exit, mock_load_from_storage):
        mock_google_ads_client = MagicMock(spec=GoogleAdsClient)
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_gaf_service = MagicMock(spec=GoogleAdsFieldServiceClient)
        mock_google_ads_client.get_service.return_value = mock_gaf_service

        mock_google_ads_client.get_type.return_value = SearchGoogleAdsFieldsRequest()

        # Mock the response object to be iterable and have total_results_count
        mock_response = MagicMock() # Removed spec to allow __iter__
        mock_response.total_results_count = 0
        mock_response.__iter__.return_value = iter([]) # Make it iterable, yielding nothing
        mock_gaf_service.search_google_ads_fields.return_value = mock_response
        
        prefix = "nonexistent.prefix"
        captured_output = StringIO()
        sys.stdout = captured_output

        main(mock_google_ads_client, prefix)

        sys.stdout = sys.__stdout__  # Reset stdout

        self.assertIn(
            f"No GoogleAdsFields found with a name that begins with '{prefix}'.",
            captured_output.getvalue(),
        )
        mock_sys_exit.assert_called_once_with(0)

    @patch("basic_operations.search_for_google_ads_fields.GoogleAdsClient.load_from_storage")
    def test_main_fields_found(self, mock_load_from_storage):
        mock_google_ads_client = MagicMock(spec=GoogleAdsClient)
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_gaf_service = MagicMock(spec=GoogleAdsFieldServiceClient)
        mock_google_ads_client.get_service.return_value = mock_gaf_service

        mock_google_ads_client.get_type.return_value = SearchGoogleAdsFieldsRequest()

        # Create mock GoogleAdsField objects
        field1 = GoogleAdsField()
        field1.name = "campaign.id"
        field1.category = GoogleAdsFieldCategoryEnum.GoogleAdsFieldCategory.ATTRIBUTE # Requires enum instance
        field1.data_type = GoogleAdsFieldDataTypeEnum.GoogleAdsFieldDataType.INT64
        field1.selectable = True
        field1.filterable = True
        field1.sortable = True
        field1.is_repeated = False
        field1.selectable_with.extend(["ad_group.id", "customer.id"])

        field2 = GoogleAdsField()
        field2.name = "metrics.impressions"
        field2.category = GoogleAdsFieldCategoryEnum.GoogleAdsFieldCategory.METRIC
        field2.data_type = GoogleAdsFieldDataTypeEnum.GoogleAdsFieldDataType.INT64
        field2.selectable = True
        field2.filterable = False
        field2.sortable = True
        field2.is_repeated = False
        # No selectable_with for this field for simplicity in test

        # Mock the response object to be iterable and have total_results_count
        mock_response = MagicMock() # Removed spec to allow __iter__
        mock_response.total_results_count = 2
        # Make it iterable, yielding the mock fields
        mock_fields_list = [field1, field2]
        mock_response.__iter__.return_value = iter(mock_fields_list)
        mock_gaf_service.search_google_ads_fields.return_value = mock_response
        
        prefix = "campaign"
        captured_output = StringIO()
        sys.stdout = captured_output

        main(mock_google_ads_client, prefix)

        sys.stdout = sys.__stdout__  # Reset stdout
        output = captured_output.getvalue()

        # Check for field1 details
        self.assertIn("campaign.id:", output)
        self.assertIn(f"{'  category:':<16} ATTRIBUTE", output) # Enum.name gives string
        self.assertIn(f"{'  data type:':<16} INT64", output)
        self.assertIn(f"{'  selectable:':<16} {True}", output)
        self.assertIn(f"{'  filterable:':<16} {True}", output)
        self.assertIn(f"{'  sortable:':<16} {True}", output)
        self.assertIn(f"{'  repeated:':<16} {False}", output)
        self.assertIn("  selectable with:", output)
        self.assertIn("    ad_group.id", output) # Note: selectable_with gets sorted by the script
        self.assertIn("    customer.id", output)

        # Check for field2 details
        self.assertIn("metrics.impressions:", output)
        self.assertIn(f"{'  category:':<16} METRIC", output)
        # ... (add more assertions for field2 if needed, similar to field1)

    @patch("basic_operations.search_for_google_ads_fields.GoogleAdsClient.load_from_storage")
    def test_main_api_error(self, mock_load_from_storage):
        mock_google_ads_client = MagicMock(spec=GoogleAdsClient)
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_gaf_service = MagicMock(spec=GoogleAdsFieldServiceClient)
        mock_google_ads_client.get_service.return_value = mock_gaf_service
        
        mock_google_ads_client.get_type.return_value = SearchGoogleAdsFieldsRequest()

        mock_api_exception = self._create_mock_google_ads_exception()
        mock_gaf_service.search_google_ads_fields.side_effect = mock_api_exception

        with self.assertRaises(GoogleAdsException) as context:
            main(mock_google_ads_client, "any.prefix")
        
        self.assertEqual(context.exception, mock_api_exception)
        mock_gaf_service.search_google_ads_fields.assert_called_once()

if __name__ == "__main__":
    unittest.main()
