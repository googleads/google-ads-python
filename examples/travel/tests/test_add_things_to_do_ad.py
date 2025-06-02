import unittest
from unittest.mock import patch, MagicMock, call
import argparse
import sys

# Add examples to sys.path
sys.path.append(".") # For `examples.utils.example_helpers`
sys.path.append("examples") # For `travel.add_things_to_do_ad`

from travel import add_things_to_do_ad


class TestAddThingsToDoAd(unittest.TestCase):

    @patch("travel.add_things_to_do_ad.GoogleAdsClient.load_from_storage")
    @patch("travel.add_things_to_do_ad.argparse.ArgumentParser")
    def test_main(self, mock_argument_parser, mock_load_client):
        mock_args = MagicMock()
        mock_args.customer_id = "test_customer_id"
        mock_args.things_to_do_center_account_id = 67890

        mock_parser_instance = mock_argument_parser.return_value
        mock_parser_instance.parse_args.return_value = mock_args

        mock_client = MagicMock()
        mock_load_client.return_value = mock_client

        mock_campaign_budget_service = MagicMock()
        mock_campaign_service = MagicMock()
        mock_ad_group_service = MagicMock()
        mock_ad_group_ad_service = MagicMock()

        mock_client.get_service.side_effect = [
            mock_campaign_budget_service,
            mock_campaign_service,
            mock_ad_group_service,
            mock_ad_group_ad_service,
        ]

        # Mock service responses
        mock_budget_response = MagicMock()
        mock_budget_response.results[0].resource_name = "budget_resource_name_ttd"
        mock_campaign_budget_service.mutate_campaign_budgets.return_value = mock_budget_response

        mock_campaign_response = MagicMock()
        mock_campaign_response.results[0].resource_name = "campaign_resource_name_ttd"
        mock_campaign_service.mutate_campaigns.return_value = mock_campaign_response

        mock_ad_group_response = MagicMock()
        mock_ad_group_response.results[0].resource_name = "ad_group_resource_name_ttd"
        mock_ad_group_service.mutate_ad_groups.return_value = mock_ad_group_response

        mock_ad_group_ad_response = MagicMock()
        mock_ad_group_ad_response.results[0].resource_name = "ad_group_ad_resource_name_ttd"
        mock_ad_group_ad_service.mutate_ad_group_ads.return_value = mock_ad_group_ad_response

        # Mock types and enums
        mock_client.get_type.side_effect = lambda x: MagicMock()
        mock_client.enums.BudgetDeliveryMethodEnum.STANDARD = "STANDARD"
        mock_client.enums.AdvertisingChannelTypeEnum.TRAVEL = "TRAVEL"
        mock_client.enums.AdvertisingChannelSubTypeEnum.TRAVEL_ACTIVITIES = "TRAVEL_ACTIVITIES"
        mock_client.enums.CampaignStatusEnum.PAUSED = "PAUSED"
        mock_client.enums.AdGroupTypeEnum.TRAVEL_ADS = "TRAVEL_ADS"
        mock_client.enums.AdGroupStatusEnum.ENABLED = "ENABLED"
        mock_client.enums.AdGroupAdStatusEnum.ENABLED = "ENABLED"


        with patch("builtins.print") as mock_print:
            add_things_to_do_ad.main(
                mock_client,
                mock_args.customer_id,
                mock_args.things_to_do_center_account_id,
            )

        mock_load_client.assert_called_once_with(version="v19")

        # Check service calls
        mock_campaign_budget_service.mutate_campaign_budgets.assert_called_once()
        campaign_budget_op = mock_campaign_budget_service.mutate_campaign_budgets.call_args[1]['operations'][0].create
        self.assertEqual(campaign_budget_op.explicitly_shared, True)


        mock_campaign_service.mutate_campaigns.assert_called_once()
        campaign_op = mock_campaign_service.mutate_campaigns.call_args[1]['operations'][0].create
        self.assertEqual(campaign_op.advertising_channel_type, "TRAVEL")
        self.assertEqual(campaign_op.advertising_channel_sub_type, "TRAVEL_ACTIVITIES")
        self.assertEqual(campaign_op.travel_campaign_settings.travel_account_id, 67890)
        self.assertTrue(hasattr(campaign_op, 'maximize_conversion_value'))
        self.assertEqual(campaign_op.network_settings.target_google_search, True)


        mock_ad_group_service.mutate_ad_groups.assert_called_once()
        ad_group_op = mock_ad_group_service.mutate_ad_groups.call_args[1]['operations'][0].create
        self.assertEqual(ad_group_op.type_, "TRAVEL_ADS")

        mock_ad_group_ad_service.mutate_ad_group_ads.assert_called_once()
        ad_group_ad_op = mock_ad_group_ad_service.mutate_ad_group_ads.call_args[1]['operations'][0].create
        self.assertTrue(hasattr(ad_group_ad_op.ad, 'travel_ad'))


        # Check print statements
        expected_prints = [
            call("Added a budget with resource name: 'budget_resource_name_ttd'."),
            call("Added a Things to do campaign with resource name: 'campaign_resource_name_ttd'."),
            call("Added an ad group with resource name: 'ad_group_resource_name_ttd'."),
            call("Added an ad group ad with resource name: 'ad_group_ad_resource_name_ttd'."),
        ]
        mock_print.assert_has_calls(expected_prints, any_order=False)

    @patch("travel.add_things_to_do_ad.main")
    @patch("travel.add_things_to_do_ad.GoogleAdsClient.load_from_storage")
    @patch("argparse.ArgumentParser")
    def test_script_runner(self, mock_argument_parser, mock_load_client, mock_main_function):
        mock_args = MagicMock()
        mock_args.customer_id = "test_customer_id_script_ttd"
        mock_args.things_to_do_center_account_id = 98765

        mock_parser_instance = mock_argument_parser.return_value
        mock_parser_instance.parse_args.return_value = mock_args

        mock_client = MagicMock()
        mock_load_client.return_value = mock_client

        with patch.object(add_things_to_do_ad, "__name__", "__main__"):
            import importlib
            importlib.reload(add_things_to_do_ad)

        mock_main_function.assert_called_once_with(
            mock_client,
            "test_customer_id_script_ttd",
            98765
        )

if __name__ == "__main__":
    unittest.main()
