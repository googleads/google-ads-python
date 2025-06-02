import unittest
from unittest.mock import patch, MagicMock, call
# argparse is no longer needed if test_script_runner is removed and main doesn't use it directly
# import argparse
import sys
# importlib is no longer needed if test_script_runner is removed.
# import importlib

sys.path.append("examples")
from travel import add_hotel_ad

class TestAddHotelAd(unittest.TestCase):

    @patch("travel.add_hotel_ad.GoogleAdsClient")
    def test_main(self, MockGoogleAdsClient):
        mock_client_instance = MockGoogleAdsClient.return_value

        customer_id = "test_customer_id"
        hotel_center_account_id = 12345
        cpc_bid_ceiling_micro_amount = 1000000

        mock_campaign_budget_service = MagicMock()
        mock_campaign_service = MagicMock()
        mock_ad_group_service = MagicMock()
        mock_ad_group_ad_service = MagicMock()

        mock_client_instance.get_service.side_effect = [
            mock_campaign_budget_service,
            mock_campaign_service,
            mock_ad_group_service,
            mock_ad_group_ad_service,
        ]

        mock_budget_response = MagicMock()
        mock_budget_response.results = [MagicMock(resource_name="budget_resource_name")]
        mock_campaign_budget_service.mutate_campaign_budgets.return_value = mock_budget_response

        mock_campaign_response = MagicMock()
        mock_campaign_response.results = [MagicMock(resource_name="campaign_resource_name")]
        mock_campaign_service.mutate_campaigns.return_value = mock_campaign_response

        mock_ad_group_response = MagicMock()
        mock_ad_group_response.results = [MagicMock(resource_name="ad_group_resource_name")]
        mock_ad_group_service.mutate_ad_groups.return_value = mock_ad_group_response

        mock_ad_group_ad_response = MagicMock()
        mock_ad_group_ad_response.results = [MagicMock(resource_name="ad_group_ad_resource_name")]
        mock_ad_group_ad_service.mutate_ad_group_ads.return_value = mock_ad_group_ad_response

        mock_client_instance.get_type.side_effect = lambda x: MagicMock(name=x)
        mock_client_instance.enums = MagicMock()
        # Example specific enum mock if needed by add_hotel_ad.py's main()
        # mock_client_instance.enums.BudgetDeliveryMethodEnum.STANDARD = "STANDARD"
        # mock_client_instance.enums.CampaignStatusEnum.PAUSED = "PAUSED"
        # mock_client_instance.enums.AdGroupStatusEnum.ENABLED = "ENABLED"
        # mock_client_instance.enums.AdGroupAdStatusEnum.ENABLED = "ENABLED"
        # mock_client_instance.enums.AdvertisingChannelTypeEnum.HOTEL = "HOTEL"


        with patch("builtins.print") as mock_print:
            add_hotel_ad.main(
                mock_client_instance,
                customer_id,
                hotel_center_account_id,
                cpc_bid_ceiling_micro_amount,
            )

        mock_campaign_budget_service.mutate_campaign_budgets.assert_called_once()
        # Example: check arguments of the call if necessary
        # budget_args, budget_kwargs = mock_campaign_budget_service.mutate_campaign_budgets.call_args
        # self.assertEqual(budget_kwargs['customer_id'], customer_id)
        # self.assertEqual(len(budget_kwargs['operations']), 1)
        # created_budget_op = budget_kwargs['operations'][0].create
        # self.assertTrue(created_budget_op.name.startswith("Interplanetary Budget "))


        mock_campaign_service.mutate_campaigns.assert_called_once()
        mock_ad_group_service.mutate_ad_groups.assert_called_once()
        mock_ad_group_ad_service.mutate_ad_group_ads.assert_called_once()

        expected_prints = [
            call("Created budget with resource name 'budget_resource_name'."),
            call("Added a hotel campaign with resource name 'campaign_resource_name'."),
            call(f"Added a hotel ad group with resource name 'ad_group_resource_name'."), # Corrected f-string usage
            call("Created hotel ad with resource name 'ad_group_ad_resource_name'."),
        ]
        mock_print.assert_has_calls(expected_prints, any_order=False)

if __name__ == "__main__":
    unittest.main()
