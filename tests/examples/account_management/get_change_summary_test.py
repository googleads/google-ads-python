import unittest
from unittest.mock import patch, MagicMock

from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v19.enums.types import (
    ChangeStatusResourceTypeEnum,
    ChangeStatusOperationEnum,
)
from examples.account_management.get_change_summary import main


class GetChangeSummaryTest(unittest.TestCase):

    def _create_mock_change_status_row(
        self,
        resource_name="customers/123/changeStatus/XYZ",
        last_change_date_time="2023-10-26 10:00:00",
        resource_type=ChangeStatusResourceTypeEnum.ChangeStatusResourceType.CAMPAIGN,
        campaign_resource_name="customers/123/campaigns/ABC",
        ad_group_resource_name=None, # Set if resource_type is AD_GROUP or AD
        resource_status=ChangeStatusOperationEnum.ChangeStatusOperation.CHANGED,
        # The script also checks for specific resource links like:
        # row.change_status.ad_group_ad, row.change_status.ad_group_criterion, etc.
        # These are not directly used for the printed counts but for details if the script were extended.
        # For this script, the main thing is resource_type and campaign/ad_group links.
    ):
        """Helper to create a mock GoogleAdsRow representing a ChangeStatus."""
        mock_row = MagicMock()
        status = mock_row.change_status

        status.resource_name = resource_name
        status.last_change_date_time = last_change_date_time
        status.resource_type = resource_type
        status.resource_status = resource_status
        status.campaign = campaign_resource_name
        
        if ad_group_resource_name:
            status.ad_group = ad_group_resource_name
        
        # Add other specific resource links if the script starts using them for printing
        # e.g. status.ad_group_ad = "customers/123/adGroupAds/DEF"

        return mock_row

    @patch("examples.account_management.get_change_summary.GoogleAdsClient.load_from_storage")
    def test_get_change_summary_success(self, mock_load_from_storage):
        """Tests the successful retrieval and printing of change summary."""
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_google_ads_service = MagicMock()
        mock_google_ads_client.get_service.return_value = mock_google_ads_service

        customer_id = "1234567890"

        # Mock rows for the search response
        mock_row_campaign_change1 = self._create_mock_change_status_row(
            resource_type=ChangeStatusResourceTypeEnum.ChangeStatusResourceType.CAMPAIGN,
            campaign_resource_name=f"customers/{customer_id}/campaigns/1",
            last_change_date_time="2023-10-25 09:00:00"
        )
        mock_row_campaign_change2 = self._create_mock_change_status_row(
            resource_type=ChangeStatusResourceTypeEnum.ChangeStatusResourceType.CAMPAIGN,
            campaign_resource_name=f"customers/{customer_id}/campaigns/2",
            last_change_date_time="2023-10-26 10:00:00"
        )
        mock_row_adgroup_change1 = self._create_mock_change_status_row(
            resource_type=ChangeStatusResourceTypeEnum.ChangeStatusResourceType.AD_GROUP,
            campaign_resource_name=f"customers/{customer_id}/campaigns/1", # Belongs to campaign 1
            ad_group_resource_name=f"customers/{customer_id}/adGroups/101",
            last_change_date_time="2023-10-26 11:00:00"
        )
        
        # The script uses GoogleAdsService.search(), which returns an iterable directly, not batches.
        mock_google_ads_service.search.return_value = [
            mock_row_campaign_change1, 
            mock_row_campaign_change2,
            mock_row_adgroup_change1
        ]

        with patch("builtins.print") as mock_print:
            main(mock_google_ads_client, customer_id)

        mock_google_ads_client.get_service.assert_called_once_with(
            "GoogleAdsService", version="v19"
        )

        # Construct the expected query (from the script)
        # The script uses date_range="LAST_14_DAYS"
        expected_query = f"""
        SELECT
            change_status.resource_name,
            change_status.last_change_date_time,
            change_status.resource_type,
            change_status.campaign,
            change_status.ad_group,
            change_status.resource_status,
            change_status.ad_group_ad,
            change_status.ad_group_criterion,
            change_status.campaign_criterion
        FROM change_status
        WHERE change_status.last_change_date_time DURING LAST_14_DAYS
        AND change_status.resource_status != 'UNSPECIFIED'
        ORDER BY change_status.last_change_date_time DESC
        LIMIT 10000""" # LIMIT is also in the script
        
        normalized_expected_query = " ".join(expected_query.split())
        
        # search takes (customer_id, query, page_size)
        self.assertEqual(mock_google_ads_service.search.call_args[0][0], customer_id)
        actual_query = mock_google_ads_service.search.call_args[0][1]
        normalized_actual_query = " ".join(actual_query.split())
        self.assertEqual(normalized_actual_query, normalized_expected_query)


        # Assertions for print calls
        # The script prints:
        # "X campaign(s) found changed in the last 14 days:"
        # "Customer ID: customer_id_of_campaign, Campaign ID: campaign_id, Resource Name: campaign_resource_name, Last Change Time: time"
        # and similar for Ad Groups.

        printed_strings = [c[0][0] for c in mock_print.call_args_list if c[0]]

        # Based on our mock data: 2 changed campaigns, 1 changed ad group.
        # The script collects unique campaign IDs that had changes.
        self.assertTrue(any("2 campaign(s) found changed in the last 14 days" in s for s in printed_strings))
        
        # Check for campaign details (order might vary due to set iteration)
        expected_campaign1_print = (f"Customer ID {customer_id}, Campaign ID "
                                    f"{mock_row_campaign_change1.change_status.campaign.split('/')[-1]}, "
                                    f"Resource Name {mock_row_campaign_change1.change_status.campaign} "
                                    f"was changed at {mock_row_campaign_change1.change_status.last_change_date_time}.")
        expected_campaign2_print = (f"Customer ID {customer_id}, Campaign ID "
                                    f"{mock_row_campaign_change2.change_status.campaign.split('/')[-1]}, "
                                    f"Resource Name {mock_row_campaign_change2.change_status.campaign} "
                                    f"was changed at {mock_row_campaign_change2.change_status.last_change_date_time}.")
        
        self.assertTrue(any(expected_campaign1_print in s for s in printed_strings))
        self.assertTrue(any(expected_campaign2_print in s for s in printed_strings))

        # The script also counts changed ad groups and prints their details.
        # The ad group mock_row_adgroup_change1 is associated with campaign 1.
        self.assertTrue(any("1 ad group(s) found changed in the last 14 days" in s for s in printed_strings))
        expected_adgroup1_print = (f"Customer ID {customer_id}, Ad Group ID "
                                   f"{mock_row_adgroup_change1.change_status.ad_group.split('/')[-1]}, "
                                   f"Resource Name {mock_row_adgroup_change1.change_status.ad_group} "
                                   f"was changed at {mock_row_adgroup_change1.change_status.last_change_date_time}.")
        self.assertTrue(any(expected_adgroup1_print in s for s in printed_strings))


    @patch("examples.account_management.get_change_summary.GoogleAdsClient.load_from_storage")
    def test_get_change_summary_google_ads_exception(self, mock_load_from_storage):
        """Tests handling of GoogleAdsException during change summary retrieval."""
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_google_ads_service = MagicMock()
        mock_google_ads_client.get_service.return_value = mock_google_ads_service

        # Configure search to raise GoogleAdsException
        mock_failure = MagicMock()
        mock_error = MagicMock()
        mock_error.message = "Test GoogleAdsException for change_summary"
        mock_failure.errors = [mock_error]
        google_ads_exception = GoogleAdsException(
            mock_failure, "call", "trigger", "request_id", "error_code_enum"
        )
        mock_google_ads_service.search.side_effect = google_ads_exception

        customer_id = "1234567890"

        with patch("sys.exit") as mock_sys_exit, \
             patch("builtins.print") as mock_error_print:
            main(mock_google_ads_client, customer_id)
            
            mock_sys_exit.assert_called_once_with(1)
            # Check if the exception details were printed
            error_printed = False
            for call_args in mock_error_print.call_args_list:
                if "Test GoogleAdsException for change_summary" in call_args[0][0]:
                    error_printed = True
                    break
            self.assertTrue(error_printed, "GoogleAdsException details not printed to console.")

        mock_google_ads_client.get_service.assert_called_once_with(
            "GoogleAdsService", version="v19"
        )
        mock_google_ads_service.search.assert_called_once()


if __name__ == "__main__":
    unittest.main()
