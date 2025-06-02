import sys
import unittest
from io import StringIO
from unittest.mock import MagicMock, patch

sys.path.append("../..")

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v19.resources.types.ad_group import AdGroup
from google.ads.googleads.v19.services.services.ad_group_service import (
    AdGroupServiceClient,
)
from google.ads.googleads.v19.services.types.ad_group_service import (
    AdGroupOperation,
    MutateAdGroupsResponse,
    MutateAdGroupResult,
)
from google.ads.googleads.v19.enums.types.ad_group_status import (
    AdGroupStatusEnum,
)
from google.protobuf import field_mask_pb2

from basic_operations.update_ad_group import main


class TestUpdateAdGroup(unittest.TestCase):
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

    @patch("basic_operations.update_ad_group.GoogleAdsClient.load_from_storage")
    def test_main_update_ad_group_success(self, mock_load_from_storage):
        mock_google_ads_client = MagicMock(spec=GoogleAdsClient)
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_ad_group_service = MagicMock(spec=AdGroupServiceClient)
        mock_google_ads_client.get_service.return_value = mock_ad_group_service

        # Configure client.get_type to return a real AdGroupOperation
        mock_google_ads_client.get_type.return_value = AdGroupOperation()

        # Mock enums
        mock_enums = MagicMock()
        mock_google_ads_client.enums = mock_enums
        mock_google_ads_client.enums.AdGroupStatusEnum.PAUSED = (
            AdGroupStatusEnum.AdGroupStatus.PAUSED
        )

        # Mock client.copy_from to simulate the field mask copying
        def mock_copy_from(destination_mask, source_field_mask):
            destination_mask.paths.extend(source_field_mask.paths)

        mock_google_ads_client.copy_from.side_effect = mock_copy_from
        
        customer_id = "test_customer_id"
        ad_group_id = "test_ad_group_id"
        cpc_bid_micros = 1000000  # Example bid amount
        expected_resource_name = (
            f"customers/{customer_id}/adGroups/{ad_group_id}"
        )
        mock_ad_group_service.ad_group_path.return_value = expected_resource_name

        mock_mutate_response = MutateAdGroupsResponse()
        mock_result = MutateAdGroupResult()
        mock_result.resource_name = expected_resource_name
        mock_mutate_response.results.append(mock_result)
        mock_ad_group_service.mutate_ad_groups.return_value = mock_mutate_response

        captured_output = StringIO()
        sys.stdout = captured_output

        main(mock_google_ads_client, customer_id, ad_group_id, cpc_bid_micros)

        sys.stdout = sys.__stdout__

        mock_google_ads_client.get_service.assert_called_once_with("AdGroupService")
        mock_ad_group_service.ad_group_path.assert_called_once_with(
            customer_id, ad_group_id
        )

        self.assertEqual(mock_ad_group_service.mutate_ad_groups.call_count, 1)
        args, kwargs = mock_ad_group_service.mutate_ad_groups.call_args
        self.assertEqual(kwargs["customer_id"], customer_id)
        
        sent_operations = kwargs["operations"]
        self.assertEqual(len(sent_operations), 1)
        operation = sent_operations[0]

        self.assertEqual(operation.update.resource_name, expected_resource_name)
        self.assertEqual(operation.update.status, AdGroupStatusEnum.AdGroupStatus.PAUSED)
        self.assertEqual(operation.update.cpc_bid_micros, cpc_bid_micros)

        expected_mask = field_mask_pb2.FieldMask()
        # Fields set: resource_name, status, cpc_bid_micros
        # The order might vary based on field numbers, use assertCountEqual
        expected_paths = ["resource_name", "status", "cpc_bid_micros"]
        self.assertCountEqual(operation.update_mask.paths, expected_paths)

        self.assertIn(
            f"Updated ad group {expected_resource_name}.",
            captured_output.getvalue(),
        )

    @patch("basic_operations.update_ad_group.GoogleAdsClient.load_from_storage")
    def test_main_update_ad_group_failure_api_error(self, mock_load_from_storage):
        mock_google_ads_client = MagicMock(spec=GoogleAdsClient)
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_ad_group_service = MagicMock(spec=AdGroupServiceClient)
        mock_google_ads_client.get_service.return_value = mock_ad_group_service

        mock_google_ads_client.get_type.return_value = AdGroupOperation()
        
        # Mock enums - needed for setting status before potential failure
        mock_enums = MagicMock()
        mock_google_ads_client.enums = mock_enums
        mock_google_ads_client.enums.AdGroupStatusEnum.PAUSED = (
            AdGroupStatusEnum.AdGroupStatus.PAUSED
        )
        
        # Mock client.copy_from - needed as it's called before mutate
        mock_google_ads_client.copy_from.side_effect = lambda dest, src: dest.paths.extend(src.paths)


        customer_id = "test_customer_id_fail"
        ad_group_id = "test_ad_group_id_fail"
        cpc_bid_micros = 2000000
        
        # Configure ad_group_path as it's called before mutate
        expected_resource_name_fail = (
            f"customers/{customer_id}/adGroups/{ad_group_id}" # Path uses the test IDs
        )
        mock_ad_group_service.ad_group_path.return_value = expected_resource_name_fail

        mock_api_exception = self._create_mock_google_ads_exception()
        mock_ad_group_service.mutate_ad_groups.side_effect = mock_api_exception

        with self.assertRaises(GoogleAdsException) as context:
            main(mock_google_ads_client, customer_id, ad_group_id, cpc_bid_micros)
        
        self.assertEqual(context.exception, mock_api_exception)
        mock_ad_group_service.mutate_ad_groups.assert_called_once()

if __name__ == "__main__":
    unittest.main()
