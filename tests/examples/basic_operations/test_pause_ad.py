import unittest
from unittest.mock import patch, MagicMock, call

from examples.basic_operations import pause_ad

class TestPauseAd(unittest.TestCase):

    @patch("examples.basic_operations.pause_ad.argparse.ArgumentParser")
    @patch("examples.basic_operations.pause_ad.GoogleAdsClient.load_from_storage")
    def test_main(self, mock_load_from_storage, mock_argument_parser):
        # Mock the GoogleAdsClient
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client

        # Mock the AdGroupAdService
        mock_ad_group_ad_service = MagicMock()
        # Mock the GoogleAdsService (for fetching the ad to get its status)
        mock_google_ads_service = MagicMock()

        def get_service_side_effect(service_name, version=None):
            if service_name == "AdGroupAdService":
                return mock_ad_group_ad_service
            elif service_name == "GoogleAdsService":
                return mock_google_ads_service
            raise ValueError(f"Unexpected service: {service_name}")
        mock_google_ads_client.get_service.side_effect = get_service_side_effect

        # Mock client.get_type for AdGroupAdOperation and AdGroupAd
        mock_ad_group_ad_operation_type = MagicMock()
        mock_ad_group_ad_type = MagicMock()

        def get_type_side_effect(type_name, version=None):
            if type_name == "AdGroupAdOperation":
                return mock_ad_group_ad_operation_type
            elif type_name == "AdGroupAd": # For creating the ad object to update
                return mock_ad_group_ad_type
            raise ValueError(f"Unexpected type: {type_name}")
        mock_google_ads_client.get_type.side_effect = get_type_side_effect


        # Mock command line arguments
        mock_args = MagicMock()
        mock_args.customer_id = "1234567890"
        mock_args.ad_group_id = "ADGROUPID1"
        mock_args.ad_id = "ADID1"
        mock_argument_parser.return_value.parse_args.return_value = mock_args

        # Mock the response from GoogleAdsService.search to get current ad status
        mock_ad_row = MagicMock()
        # Simulate current status is ENABLED
        mock_ad_row.ad_group_ad.status = mock_google_ads_client.enums.AdGroupAdStatusEnum.ENABLED
        mock_ad_row.ad_group_ad.ad.id = mock_args.ad_id # ensure ad_id matches

        mock_search_response_batch = MagicMock()
        mock_search_response_batch.results = [mock_ad_row]
        mock_google_ads_service.search.return_value = iter([mock_search_response_batch]) # search returns an iterator

        # Mock the response for AdGroupAdService.mutate_ad_group_ads
        mock_mutate_response = MagicMock()
        mock_mutate_result = MagicMock()
        mock_mutate_result.resource_name = f"customers/{mock_args.customer_id}/adGroupAds/{mock_args.ad_group_id}~{mock_args.ad_id}"
        mock_mutate_response.results = [mock_mutate_result]
        mock_ad_group_ad_service.mutate_ad_group_ads.return_value = mock_mutate_response

        # Call the main function of the example script
        with patch("builtins.print") as mock_print:
            pause_ad.main(mock_google_ads_client, mock_args.customer_id, mock_args.ad_group_id, mock_args.ad_id)

        # Assertions
        mock_load_from_storage.assert_called_once_with(version="v19")

        # Check get_service calls
        mock_google_ads_client.get_service.assert_any_call("GoogleAdsService")
        mock_google_ads_client.get_service.assert_any_call("AdGroupAdService")

        # Check GoogleAdsService.search call
        expected_query = f"""
            SELECT ad_group_ad.ad.id, ad_group_ad.status
            FROM ad_group_ad
            WHERE ad_group.id = '{mock_args.ad_group_id}'
            AND ad_group_ad.ad.id = '{mock_args.ad_id}'"""
        mock_google_ads_service.search.assert_called_once_with(
            customer_id=mock_args.customer_id, query=expected_query
        )

        # Check AdGroupAdService.mutate_ad_group_ads call
        self.assertEqual(mock_ad_group_ad_service.mutate_ad_group_ads.call_count, 1)
        args_mutate, kwargs_mutate = mock_ad_group_ad_service.mutate_ad_group_ads.call_args
        self.assertEqual(kwargs_mutate['customer_id'], mock_args.customer_id)

        operation = kwargs_mutate['operations'][0]
        # Accessing attributes on the MagicMock returned by get_type
        self.assertEqual(operation.update.resource_name, f"customers/{mock_args.customer_id}/adGroupAds/{mock_args.ad_group_id}~{mock_args.ad_id}")
        self.assertEqual(operation.update.status, mock_google_ads_client.enums.AdGroupAdStatusEnum.PAUSED)

        # Verify print output
        expected_print_call = call(
            f"Ad group ad with resource name "
            f"'{mock_mutate_result.resource_name}' was paused."
        )
        mock_print.assert_has_calls([expected_print_call])

if __name__ == "__main__":
    unittest.main()
