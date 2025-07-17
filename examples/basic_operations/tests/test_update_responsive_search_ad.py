import sys
import unittest
from io import StringIO
from unittest.mock import MagicMock, patch, ANY

# sys.path.append("../..") # No longer needed with relative import

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v19.common.types.ad_asset import AdTextAsset # Corrected import
from google.ads.googleads.v19.resources.types.ad import Ad
from google.ads.googleads.v19.services.services.ad_service import AdServiceClient
from google.ads.googleads.v19.services.types.ad_service import (
    AdOperation,
    MutateAdsResponse,
    MutateAdResult,
)
from google.ads.googleads.v19.enums.types.served_asset_field_type import (
    ServedAssetFieldTypeEnum,
)
from google.protobuf import field_mask_pb2

# Import the function to be tested
from examples.basic_operations.update_responsive_search_ad import main # Absolute import


class TestUpdateResponsiveSearchAd(unittest.TestCase):
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

    @patch("examples.basic_operations.update_responsive_search_ad.uuid4") # Updated patch path
    @patch("examples.basic_operations.update_responsive_search_ad.GoogleAdsClient.load_from_storage") # Updated patch path
    def test_main_update_rsa_success(self, mock_load_from_storage, mock_uuid4):
        # Configure mock_uuid4 to return a fixed hex value
        mock_uuid_hex = "12345678"
        mock_uuid4_instance = MagicMock()
        mock_uuid4_instance.hex = mock_uuid_hex
        mock_uuid4.return_value = mock_uuid4_instance

        mock_google_ads_client = MagicMock(spec=GoogleAdsClient)
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_ad_service = MagicMock(spec=AdServiceClient)
        mock_google_ads_client.get_service.return_value = mock_ad_service

        # Mock get_type calls
        # For AdOperation, return a real instance
        mock_google_ads_client.get_type.side_effect = lambda type_name: (
            AdOperation() if type_name == "AdOperation" else
            AdTextAsset() if type_name == "AdTextAsset" else
            MagicMock() # Default for other types if any
        )

        # Mock enums
        mock_enums = MagicMock()
        mock_google_ads_client.enums = mock_enums
        mock_google_ads_client.enums.ServedAssetFieldTypeEnum.HEADLINE_1 = (
            ServedAssetFieldTypeEnum.ServedAssetFieldType.HEADLINE_1
        )

        # Mock client.copy_from
        def mock_copy_from(destination_mask, source_field_mask):
            destination_mask.paths.extend(source_field_mask.paths)
        mock_google_ads_client.copy_from.side_effect = mock_copy_from
        
        customer_id = "test_customer_id"
        ad_id = "test_ad_id"
        expected_resource_name = f"customers/{customer_id}/ads/{ad_id}"
        mock_ad_service.ad_path.return_value = expected_resource_name

        mock_mutate_response = MutateAdsResponse()
        mock_result = MutateAdResult()
        mock_result.resource_name = expected_resource_name
        mock_mutate_response.results.append(mock_result)
        mock_ad_service.mutate_ads.return_value = mock_mutate_response

        captured_output = StringIO()
        sys.stdout = captured_output

        main(mock_google_ads_client, customer_id, ad_id)

        sys.stdout = sys.__stdout__

        mock_google_ads_client.get_service.assert_called_once_with("AdService")
        mock_ad_service.ad_path.assert_called_once_with(customer_id, ad_id)

        self.assertEqual(mock_ad_service.mutate_ads.call_count, 1)
        args, kwargs = mock_ad_service.mutate_ads.call_args
        self.assertEqual(kwargs["customer_id"], customer_id)
        
        sent_operations = kwargs["operations"]
        self.assertEqual(len(sent_operations), 1)
        operation = sent_operations[0]

        self.assertEqual(operation.update.resource_name, expected_resource_name)
        
        # Assertions for responsive_search_ad headlines
        rsa_headlines = operation.update.responsive_search_ad.headlines
        self.assertEqual(len(rsa_headlines), 3)
        # Headline 1 with UUID
        self.assertEqual(rsa_headlines[0].text, f"Cruise to Pluto #{mock_uuid_hex}")
        self.assertEqual(rsa_headlines[0].pinned_field, ServedAssetFieldTypeEnum.ServedAssetFieldType.HEADLINE_1)
        # Other headlines
        self.assertEqual(rsa_headlines[1].text, "Tickets on sale now")
        self.assertEqual(rsa_headlines[2].text, "Buy your tickets now")

        # Assertions for responsive_search_ad descriptions
        rsa_descriptions = operation.update.responsive_search_ad.descriptions
        self.assertEqual(len(rsa_descriptions), 2)
        self.assertEqual(rsa_descriptions[0].text, "Best space cruise ever.")
        self.assertEqual(rsa_descriptions[1].text, "The most wonderful space experience you will ever have.")

        # Assertions for final_urls
        self.assertIn("https://www.example.com", operation.update.final_urls)
        self.assertIn("https://www.example.com/mobile", operation.update.final_mobile_urls)

        # Assertions for update_mask
        # Based on the test failure, field_mask lists specific sub-fields of responsive_search_ad
        # when its repeated fields (headlines, descriptions) are modified.
        expected_paths = [
            "resource_name",
            "responsive_search_ad.headlines",
            "responsive_search_ad.descriptions",
            "final_urls",
            "final_mobile_urls"
        ]
        self.assertCountEqual(operation.update_mask.paths, expected_paths)

        self.assertIn(
            f'Ad with resource name "{expected_resource_name}" was updated.',
            captured_output.getvalue(),
        )

    @patch("examples.basic_operations.update_responsive_search_ad.GoogleAdsClient.load_from_storage") # Updated patch path
    def test_main_update_rsa_failure_api_error(self, mock_load_from_storage):
        mock_google_ads_client = MagicMock(spec=GoogleAdsClient)
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_ad_service = MagicMock(spec=AdServiceClient)
        mock_google_ads_client.get_service.return_value = mock_ad_service
        
        # Mock get_type calls
        mock_google_ads_client.get_type.side_effect = lambda type_name: (
            AdOperation() if type_name == "AdOperation" else
            AdTextAsset() if type_name == "AdTextAsset" else
            MagicMock()
        )
        
        # Mock enums
        mock_enums = MagicMock()
        mock_google_ads_client.enums = mock_enums
        mock_google_ads_client.enums.ServedAssetFieldTypeEnum.HEADLINE_1 = (
            ServedAssetFieldTypeEnum.ServedAssetFieldType.HEADLINE_1
        )
        
        # Mock client.copy_from
        mock_google_ads_client.copy_from.side_effect = lambda dest, src: dest.paths.extend(src.paths)

        customer_id = "test_customer_id_fail"
        ad_id = "test_ad_id_fail"
        mock_ad_service.ad_path.return_value = f"customers/{customer_id}/ads/{ad_id}"


        mock_api_exception = self._create_mock_google_ads_exception()
        mock_ad_service.mutate_ads.side_effect = mock_api_exception

        with self.assertRaises(GoogleAdsException) as context:
            main(mock_google_ads_client, customer_id, ad_id)
        
        self.assertEqual(context.exception, mock_api_exception)
        mock_ad_service.mutate_ads.assert_called_once()

if __name__ == "__main__":
    unittest.main()
