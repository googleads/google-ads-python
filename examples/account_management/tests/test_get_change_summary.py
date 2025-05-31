import unittest
from unittest.mock import patch, MagicMock
import io
import sys

from examples.account_management import get_change_summary # Assuming this is the script name
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.v19.services.services.google_ads_service import GoogleAdsServiceClient
from google.ads.googleads.v19.services.types import GoogleAdsRow # Using consistent import path
from google.ads.googleads.v19.services.types import SearchGoogleAdsRequest # Corrected path

class TestGetChangeSummary(unittest.TestCase):

    @patch('examples.account_management.get_change_summary.GoogleAdsClient')
    def test_main_prints_change_summary(self, mock_google_ads_client_class):
        # 1. Setup Mocks
        mock_client_instance = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client_class.load_from_storage.return_value = mock_client_instance

        mock_google_ads_service = MagicMock(spec=GoogleAdsServiceClient)
        mock_client_instance.get_service.return_value = mock_google_ads_service

        # 2. Prepare arguments for main function
        customer_id = "test_customer_789"

        # 3. Mock the response for googleads_service.search()
        mock_rows_data = [
            {
                "change_status_resource_name": "customers/123/changeStatus/A",
                "resource_type_name": "CAMPAIGN",
                "specific_resource_name": "customers/123/campaigns/1",
                "last_change_date_time": "2023-03-10 09:00:00",
                "resource_status_name": "ENABLED"
            },
            {
                "change_status_resource_name": "customers/123/changeStatus/B",
                "resource_type_name": "AD_GROUP",
                "specific_resource_name": "customers/123/adGroups/1",
                "last_change_date_time": "2023-03-10 10:00:00",
                "resource_status_name": "PAUSED"
            },
            {
                "change_status_resource_name": "customers/123/changeStatus/C",
                "resource_type_name": "AD_GROUP_AD",
                "specific_resource_name": "customers/123/adGroupAds/1",
                "last_change_date_time": "2023-03-10 11:00:00",
                "resource_status_name": "ENABLED"
            },
        ]

        mock_google_ads_rows = []
        for data in mock_rows_data:
            row = MagicMock(spec=GoogleAdsRow)
            row.change_status = MagicMock() # Explicitly define change_status
            cs = row.change_status # cs is also a MagicMock now

            cs.resource_name = data["change_status_resource_name"]
            cs.last_change_date_time = data["last_change_date_time"]

            cs.resource_type = MagicMock() # Mock for enum
            cs.resource_type.name = data["resource_type_name"]

            cs.resource_status = MagicMock() # Mock for enum
            cs.resource_status.name = data["resource_status_name"]

            # Set specific resource name fields based on resource_type_name
            if data["resource_type_name"] == "CAMPAIGN":
                cs.campaign = data["specific_resource_name"]
            elif data["resource_type_name"] == "AD_GROUP":
                cs.ad_group = data["specific_resource_name"]
            elif data["resource_type_name"] == "AD_GROUP_AD":
                cs.ad_group_ad = data["specific_resource_name"]
            # Add other resource types if needed for more comprehensive tests

            mock_google_ads_rows.append(row)

        # search returns an iterable of rows directly
        mock_google_ads_service.search.return_value = iter(mock_google_ads_rows)

        # Mock client.get_type for SearchGoogleAdsRequest
        mock_search_request = MagicMock(spec=SearchGoogleAdsRequest)
        mock_client_instance.get_type.return_value = mock_search_request

        # 4. Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # 5. Call the main function
        get_change_summary.main(mock_client_instance, customer_id)

        # 6. Restore stdout
        sys.stdout = sys.__stdout__

        # 7. Assertions
        # Assert get_type was called for SearchGoogleAdsRequest
        mock_client_instance.get_type.assert_called_once_with("SearchGoogleAdsRequest")

        # Assert search was called with the request object
        mock_google_ads_service.search.assert_called_once_with(request=mock_search_request)

        # Verify attributes of the search_request object
        self.assertEqual(mock_search_request.customer_id, customer_id)
        actual_query_arg = mock_search_request.query

        # Verify query content
        self.assertIn("change_status.last_change_date_time DURING LAST_14_DAYS", actual_query_arg) # Corrected date range
        self.assertIn("ORDER BY change_status.last_change_date_time", actual_query_arg)
        self.assertIn("LIMIT 10000", actual_query_arg)
        self.assertIn("change_status.resource_name", actual_query_arg)
        self.assertIn("change_status.resource_type", actual_query_arg)

        # Verify printed output (individual lines, no summary counts)
        output = captured_output.getvalue()
        expected_lines = []
        for data in mock_rows_data:
            # Determine specific resource name for the print statement
            # This logic must exactly match the script's if/elif block for resource_name
            script_resource_name = "UNKNOWN"
            if data["resource_type_name"] == "AD_GROUP":
                script_resource_name = data["specific_resource_name"]
            elif data["resource_type_name"] == "AD_GROUP_AD":
                script_resource_name = data["specific_resource_name"]
            elif data["resource_type_name"] == "CAMPAIGN":
                script_resource_name = data["specific_resource_name"]
            # ... (add other elif conditions from script if testing those types)

            expected_lines.append(
                f"On '{data['last_change_date_time']}', change status "
                f"'{data['change_status_resource_name']}' shows that a resource type of "
                f"'{data['resource_type_name']}' with resource name '{script_resource_name}' was "
                f"{data['resource_status_name']}\n"
            )

        expected_output = "".join(expected_lines)
        self.assertEqual(output, expected_output)

if __name__ == "__main__":
    unittest.main()
