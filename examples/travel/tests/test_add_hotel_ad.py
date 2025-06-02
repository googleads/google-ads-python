import unittest
from unittest.mock import patch, MagicMock, call
import argparse
import sys

# Add examples to sys.path to be able to import add_hotel_ad
sys.path.append("examples")
from travel import add_hotel_ad


class TestAddHotelAd(unittest.TestCase):

    @patch("travel.add_hotel_ad.GoogleAdsClient.load_from_storage")
    @patch("travel.add_hotel_ad.argparse.ArgumentParser")
    def test_main(self, mock_argument_parser, mock_load_client):
        # Mock command line arguments
        mock_args = MagicMock()
        mock_args.customer_id = "test_customer_id"
        mock_args.hotel_center_account_id = 12345
        mock_args.cpc_bid_ceiling_micro_amount = 1000000

        mock_parser_instance = mock_argument_parser.return_value
        mock_parser_instance.parse_args.return_value = mock_args

        # Mock GoogleAdsClient and its services
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
        mock_budget_response.results[0].resource_name = "budget_resource_name"
        mock_campaign_budget_service.mutate_campaign_budgets.return_value = mock_budget_response

        mock_campaign_response = MagicMock()
        mock_campaign_response.results[0].resource_name = "campaign_resource_name"
        mock_campaign_service.mutate_campaigns.return_value = mock_campaign_response

        mock_ad_group_response = MagicMock()
        mock_ad_group_response.results[0].resource_name = "ad_group_resource_name"
        mock_ad_group_service.mutate_ad_groups.return_value = mock_ad_group_response

        mock_ad_group_ad_response = MagicMock()
        mock_ad_group_ad_response.results[0].resource_name = "ad_group_ad_resource_name"
        mock_ad_group_ad_service.mutate_ad_group_ads.return_value = mock_ad_group_ad_response

        # Mock types
        mock_client.get_type.side_effect = lambda x: MagicMock()
        mock_client.enums = MagicMock()


        # Call the main function
        with patch("builtins.print") as mock_print:
            add_hotel_ad.main(
                mock_client,
                mock_args.customer_id,
                mock_args.hotel_center_account_id,
                mock_args.cpc_bid_ceiling_micro_amount,
            )

        # Assertions
        mock_load_client.assert_called_once_with(version="v19")

        # Check service calls
        mock_campaign_budget_service.mutate_campaign_budgets.assert_called_once()
        mock_campaign_service.mutate_campaigns.assert_called_once()
        mock_ad_group_service.mutate_ad_groups.assert_called_once()
        mock_ad_group_ad_service.mutate_ad_group_ads.assert_called_once()

        # Check print statements
        expected_prints = [
            call("Created budget with resource name 'budget_resource_name'."),
            call("Added a hotel campaign with resource name 'campaign_resource_name'."),
            call("Added a hotel ad group with resource name 'ad_group_resource_name'."),
            call("Created hotel ad with resource name 'ad_group_ad_resource_name'."),
        ]
        mock_print.assert_has_calls(expected_prints, any_order=False)

    @patch("travel.add_hotel_ad.main")
    @patch("travel.add_hotel_ad.GoogleAdsClient.load_from_storage")
    @patch("argparse.ArgumentParser")
    def test_script_runner(self, mock_argument_parser, mock_load_client, mock_main_function):
        # Mock command line arguments
        mock_args = MagicMock()
        mock_args.customer_id = "test_customer_id"
        mock_args.hotel_center_account_id = 12345
        mock_args.cpc_bid_ceiling_micro_amount = 1000000

        mock_parser_instance = mock_argument_parser.return_value
        mock_parser_instance.parse_args.return_value = mock_args

        mock_client = MagicMock()
        mock_load_client.return_value = mock_client

        # Run the script's if __name__ == "__main__": block
        with patch.object(add_hotel_ad, "__name__", "__main__"):
            # Need to reload the module to trigger the if __name__ == "__main__" block
            import importlib
            importlib.reload(add_hotel_ad)

        mock_main_function.assert_called_once_with(
            mock_client,
            "test_customer_id",
            12345,
            1000000
        )


if __name__ == "__main__":
    unittest.main()
