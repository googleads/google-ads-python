import unittest
from unittest.mock import patch, MagicMock, call
import argparse
import sys

# Add examples to sys.path
sys.path.append("examples")
from travel import add_hotel_ad_group_bid_modifiers


class TestAddHotelAdGroupBidModifiers(unittest.TestCase):

    @patch("travel.add_hotel_ad_group_bid_modifiers.GoogleAdsClient.load_from_storage")
    @patch("travel.add_hotel_ad_group_bid_modifiers.argparse.ArgumentParser")
    def test_main(self, mock_argument_parser, mock_load_client):
        mock_args = MagicMock()
        mock_args.customer_id = "test_customer_id"
        mock_args.ad_group_id = "test_ad_group_id"

        mock_parser_instance = mock_argument_parser.return_value
        mock_parser_instance.parse_args.return_value = mock_args

        mock_client = MagicMock()
        mock_load_client.return_value = mock_client

        mock_ad_group_service = MagicMock()
        mock_ad_group_bid_modifier_service = MagicMock()

        mock_client.get_service.side_effect = [
            mock_ad_group_service,
            mock_ad_group_bid_modifier_service,
        ]

        # Mock ad_group_path
        mock_ad_group_service.ad_group_path.return_value = f"customers/test_customer_id/adGroups/test_ad_group_id"

        # Mock service responses
        mock_response = MagicMock()
        mock_result1 = MagicMock()
        mock_result1.resource_name = "bid_modifier_resource_name_1"
        mock_result2 = MagicMock()
        mock_result2.resource_name = "bid_modifier_resource_name_2"
        mock_response.results = [mock_result1, mock_result2]
        mock_ad_group_bid_modifier_service.mutate_ad_group_bid_modifiers.return_value = mock_response

        # Mock types and enums
        mock_client.get_type.side_effect = lambda x: MagicMock()
        mock_client.enums.DayOfWeekEnum.MONDAY = "MONDAY" # Example enum value

        with patch("builtins.print") as mock_print:
            add_hotel_ad_group_bid_modifiers.main(
                mock_client,
                mock_args.customer_id,
                mock_args.ad_group_id,
            )

        mock_load_client.assert_called_once_with(version="v19")
        mock_ad_group_bid_modifier_service.mutate_ad_group_bid_modifiers.assert_called_once()

        # Check ad_group_path calls
        mock_ad_group_service.ad_group_path.assert_has_calls([
            call("test_customer_id", "test_ad_group_id"), # For check-in modifier
            call("test_customer_id", "test_ad_group_id")  # For length-of-stay modifier
        ])

        # Check print statements
        expected_prints = [
            call("Added 2 hotel ad group bid modifiers:"),
            call("bid_modifier_resource_name_1"),
            call("bid_modifier_resource_name_2"),
        ]
        mock_print.assert_has_calls(expected_prints, any_order=False)

    @patch("travel.add_hotel_ad_group_bid_modifiers.main")
    @patch("travel.add_hotel_ad_group_bid_modifiers.GoogleAdsClient.load_from_storage")
    @patch("argparse.ArgumentParser")
    def test_script_runner(self, mock_argument_parser, mock_load_client, mock_main_function):
        mock_args = MagicMock()
        mock_args.customer_id = "test_customer_id_script"
        mock_args.ad_group_id = "test_ad_group_id_script"

        mock_parser_instance = mock_argument_parser.return_value
        mock_parser_instance.parse_args.return_value = mock_args

        mock_client = MagicMock()
        mock_load_client.return_value = mock_client

        with patch.object(add_hotel_ad_group_bid_modifiers, "__name__", "__main__"):
            import importlib
            importlib.reload(add_hotel_ad_group_bid_modifiers)

        mock_main_function.assert_called_once_with(
            mock_client,
            "test_customer_id_script",
            "test_ad_group_id_script"
        )

if __name__ == "__main__":
    unittest.main()
