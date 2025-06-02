import argparse
import sys
import unittest
from io import StringIO
from unittest.mock import MagicMock, patch

from google.ads.googleads.errors import GoogleAdsException # Import GoogleAdsException
from google.ads.googleads.v19.common.types.ad_asset import AdTextAsset # Corrected import
from google.ads.googleads.v19.enums.types.ad_group_ad_status import AdGroupAdStatusEnum
from google.ads.googleads.v19.enums.types.served_asset_field_type import ServedAssetFieldTypeEnum
from google.ads.googleads.v19.resources.types.ad import Ad
from google.ads.googleads.v19.resources.types.ad_group_ad import AdGroupAd
from google.ads.googleads.v19.services.services.google_ads_service import (
    GoogleAdsServiceClient,
)
from google.ads.googleads.v19.services.types.google_ads_service import (
    GoogleAdsRow,
    SearchGoogleAdsResponse,
)

# Add the parent directory to the Python path to allow importing from sibling directories
# sys.path.append("../..") # No longer needed with relative import

from examples.basic_operations.get_responsive_search_ads import ( # Absolute import
    main,
    ad_text_assets_to_strs,
)


class TestGetResponsiveSearchAds(unittest.TestCase):
    def test_ad_text_assets_to_strs(self):
        assets = []
        asset1 = AdTextAsset()
        asset1.text = "Headline 1"
        asset1.pinned_field = ServedAssetFieldTypeEnum.ServedAssetFieldType.HEADLINE_1
        assets.append(asset1)

        asset2 = AdTextAsset()
        asset2.text = "Description 1"
        asset2.pinned_field = ServedAssetFieldTypeEnum.ServedAssetFieldType.DESCRIPTION_1
        assets.append(asset2)

        expected_output = [
            "\t Headline 1 pinned to HEADLINE_1",
            "\t Description 1 pinned to DESCRIPTION_1",
        ]
        self.assertEqual(ad_text_assets_to_strs(assets), expected_output)

    @patch("examples.basic_operations.get_responsive_search_ads.GoogleAdsClient") # Updated patch path
    def test_main_no_ads_found(self, mock_google_ads_client_constructor):
        mock_ads_client = MagicMock()
        mock_google_ads_service = MagicMock(spec=GoogleAdsServiceClient)
        mock_ads_client.get_service.return_value = mock_google_ads_service

        # Configure the mock GoogleAdsServiceClient to return an empty list of results
        mock_google_ads_service.search.return_value = SearchGoogleAdsResponse()

        mock_google_ads_client_constructor.load_from_storage.return_value = (
            mock_ads_client
        )

        # Redirect stdout to capture print statements
        captured_output = StringIO()
        sys.stdout = captured_output

        main(mock_ads_client, "test_customer_id")

        sys.stdout = sys.__stdout__  # Reset stdout
        self.assertIn(
            "No responsive search ads were found.", captured_output.getvalue()
        )
        mock_google_ads_service.search.assert_called_once()

    @patch("examples.basic_operations.get_responsive_search_ads.GoogleAdsClient") # Updated patch path
    def test_main_ads_found(self, mock_google_ads_client_constructor):
        mock_ads_client = MagicMock()
        mock_google_ads_service = MagicMock(spec=GoogleAdsServiceClient)
        mock_ads_client.get_service.return_value = mock_google_ads_service

        # Create mock ad data
        row1 = GoogleAdsRow()
        row1.ad_group_ad.ad.resource_name = "customers/123/ads/1"
        row1.ad_group_ad.status = AdGroupAdStatusEnum.AdGroupAdStatus.ENABLED
        # Headlines
        headline1 = AdTextAsset()
        headline1.text = "Test Headline 1"
        headline1.pinned_field = ServedAssetFieldTypeEnum.ServedAssetFieldType.HEADLINE_1
        row1.ad_group_ad.ad.responsive_search_ad.headlines.extend([headline1])
        # Descriptions
        description1 = AdTextAsset()
        description1.text = "Test Description 1"
        description1.pinned_field = ServedAssetFieldTypeEnum.ServedAssetFieldType.DESCRIPTION_1
        row1.ad_group_ad.ad.responsive_search_ad.descriptions.extend([description1])

        row2 = GoogleAdsRow()
        row2.ad_group_ad.ad.resource_name = "customers/123/ads/2"
        row2.ad_group_ad.status = AdGroupAdStatusEnum.AdGroupAdStatus.PAUSED
        headline2 = AdTextAsset()
        headline2.text = "Another Headline"
        headline2.pinned_field = ServedAssetFieldTypeEnum.ServedAssetFieldType.UNSPECIFIED
        row2.ad_group_ad.ad.responsive_search_ad.headlines.extend([headline2])


        mock_response = SearchGoogleAdsResponse()
        mock_response.results.extend([row1, row2])
        mock_google_ads_service.search.return_value = mock_response
        mock_google_ads_client_constructor.load_from_storage.return_value = (
            mock_ads_client
        )

        captured_output = StringIO()
        sys.stdout = captured_output

        main(mock_ads_client, "test_customer_id", ad_group_id="test_ad_group_id")

        sys.stdout = sys.__stdout__  # Reset stdout
        output_text = captured_output.getvalue()

        self.assertIn(
            'Responsive search ad with resource name "customers/123/ads/1", status ENABLED was found.',
            output_text,
        )
        self.assertIn("Headlines:\n\t Test Headline 1 pinned to HEADLINE_1", output_text)
        self.assertIn("Descriptions:\n\t Test Description 1 pinned to DESCRIPTION_1", output_text)

        self.assertIn(
            'Responsive search ad with resource name "customers/123/ads/2", status PAUSED was found.',
            output_text,
        )
        self.assertIn("Headlines:\n\t Another Headline pinned to UNSPECIFIED", output_text)
        # Check if the query was modified for ad_group_id
        self.assertTrue(
            "AND ad_group.id = test_ad_group_id"
            in mock_google_ads_service.search.call_args[1]["request"].query
        )

    @patch("examples.basic_operations.get_responsive_search_ads.GoogleAdsClient") # Updated patch path
    # Removed mock_sys_exit as main() itself doesn't call sys.exit()
    def test_main_google_ads_exception(self, mock_google_ads_client_constructor):
        mock_ads_client = MagicMock()
        mock_google_ads_service = MagicMock(spec=GoogleAdsServiceClient)
        mock_ads_client.get_service.return_value = mock_google_ads_service

        # Configure the mock GoogleAdsServiceClient to raise an exception
        # Use a real GoogleAdsException for type checking if possible,
        # but for this test, ensuring main re-raises is key.
        # We'll use the helper that creates a MagicMock that looks like one.
        mock_exception_to_raise = self._create_mock_google_ads_exception()
        mock_google_ads_service.search.side_effect = mock_exception_to_raise
        
        mock_google_ads_client_constructor.load_from_storage.return_value = (
            mock_ads_client
        )

        # Assert that calling main raises the GoogleAdsException (or the mock equivalent)
        with self.assertRaises(GoogleAdsException) as context: # Or type(mock_exception_to_raise)
            main(mock_ads_client, "test_customer_id")
        
        # Optionally, assert details about the raised exception
        # self.assertEqual(context.exception.request_id, "mock_request_id")


    def _create_mock_google_ads_exception(self):
        """Helper method to create a mock GoogleAdsException.
        Ideally, this would be a real GoogleAdsException instance, but
        constructing one can be complex. A MagicMock is used for simplicity here
        if we are only checking that an exception of this type is raised.
        For more detailed checks on the exception's attributes, a more realistic
        mock or a real instance would be better.
        """
        # For this test, we need an object that is an instance of GoogleAdsException.
        # We will instantiate GoogleAdsException directly.
        # The constructor typically takes: error, failure, request_id, call.
        # We'll use MagicMocks for the complex protobuf parts if needed by the constructor,
        # but the key is that the object itself is a proper exception.

        # These mocks are for the attributes that GoogleAdsException might store
        # and that the calling code (the main script's error handler) might access.
        mock_google_ads_error = MagicMock() # Represents the services.GoogleAdsError
        # If GoogleAdsError has a code() method that returns an object with a name attribute:
        mock_error_code = MagicMock()
        mock_error_code.name = "UNKNOWN_ERROR_FOR_TEST"
        mock_google_ads_error.code.return_value = mock_error_code
        
        mock_google_ads_failure = MagicMock() # Represents the errors.GoogleAdsFailure
        mock_error_detail = MagicMock()
        mock_error_detail.message = "Mocked error detail message"
        mock_field_path_element = MagicMock()
        mock_field_path_element.field_name = "mock_field_in_failure"
        mock_error_detail.location.field_path_elements = [mock_field_path_element]
        mock_google_ads_failure.errors = [mock_error_detail]

        # Instantiate the actual GoogleAdsException
        # The `call` argument is often a grpc.Call instance, using a mock for it.
        ex = GoogleAdsException(
            error=mock_google_ads_error,  # This should be a GoogleAdsError instance
            failure=mock_google_ads_failure, # This should be a GoogleAdsFailure instance
            request_id="mock_request_id_real_ex",
            call=MagicMock() # Mocking the gRPC call object
        )
        return ex


if __name__ == "__main__":
    unittest.main()
