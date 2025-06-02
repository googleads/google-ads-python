import unittest
from unittest.mock import patch, MagicMock, call
# import argparse # No longer needed
import sys
# import importlib # No longer needed

sys.path.append("examples")
from travel import add_hotel_ad_group_bid_modifiers

class TestAddHotelAdGroupBidModifiers(unittest.TestCase):

    @patch("travel.add_hotel_ad_group_bid_modifiers.GoogleAdsClient") # Patch the class
    def test_main(self, MockGoogleAdsClient): # Receive the patched class
        mock_client_instance = MockGoogleAdsClient.return_value # Get the instance

        customer_id = "test_customer_id"
        ad_group_id = "test_ad_group_id"

        mock_ad_group_service = MagicMock()
        mock_ad_group_bid_modifier_service = MagicMock()

        mock_client_instance.get_service.side_effect = [
            mock_ad_group_service,
            mock_ad_group_bid_modifier_service,
        ]

        mock_ad_group_service.ad_group_path.return_value = f"customers/test_customer_id/adGroups/test_ad_group_id"

        mock_response = MagicMock()
        mock_result1 = MagicMock()
        mock_result1.resource_name = "bid_modifier_resource_name_1"
        mock_result2 = MagicMock()
        mock_result2.resource_name = "bid_modifier_resource_name_2"
        mock_response.results = [mock_result1, mock_result2]
        mock_ad_group_bid_modifier_service.mutate_ad_group_bid_modifiers.return_value = mock_response

        mock_client_instance.get_type.side_effect = lambda x: MagicMock(name=x)
        mock_client_instance.enums = MagicMock()
        mock_client_instance.enums.DayOfWeekEnum.MONDAY = "MONDAY"
        # Add other enums if used by the main() of add_hotel_ad_group_bid_modifiers.py
        # e.g. mock_client_instance.enums.HotelLengthOfStayInfo = MagicMock() if it's an enum (it's a type)

        with patch("builtins.print") as mock_print:
            add_hotel_ad_group_bid_modifiers.main(
                mock_client_instance, # Pass the instance
                customer_id,
                ad_group_id,
            )

        # No assertion for load_from_storage here

        mock_ad_group_bid_modifier_service.mutate_ad_group_bid_modifiers.assert_called_once()

        # Check arguments of mutate_ad_group_bid_modifiers call
        args, kwargs = mock_ad_group_bid_modifier_service.mutate_ad_group_bid_modifiers.call_args
        self.assertEqual(kwargs['customer_id'], customer_id)
        operations = kwargs['operations']
        self.assertEqual(len(operations), 2)

        # Check properties of the first operation (check-in day)
        op1_create = operations[0].create
        self.assertEqual(op1_create.ad_group, f"customers/test_customer_id/adGroups/test_ad_group_id")
        self.assertEqual(op1_create.hotel_check_in_day.day_of_week, "MONDAY")
        self.assertEqual(op1_create.bid_modifier, 1.5)

        # Check properties of the second operation (length of stay)
        op2_create = operations[1].create
        self.assertEqual(op2_create.ad_group, f"customers/test_customer_id/adGroups/test_ad_group_id")
        self.assertEqual(op2_create.hotel_length_of_stay.min_nights, 3)
        self.assertEqual(op2_create.hotel_length_of_stay.max_nights, 7)
        self.assertEqual(op2_create.bid_modifier, 1.7)

        mock_ad_group_service.ad_group_path.assert_has_calls([
            call("test_customer_id", "test_ad_group_id"),
            call("test_customer_id", "test_ad_group_id")
        ])

        expected_prints = [
            call("Added 2 hotel ad group bid modifiers:"),
            call("bid_modifier_resource_name_1"),
            call("bid_modifier_resource_name_2"),
        ]
        mock_print.assert_has_calls(expected_prints, any_order=False)

if __name__ == "__main__":
    unittest.main()
