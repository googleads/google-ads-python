import unittest
from unittest import mock
import sys
import runpy
import argparse

# Assuming the script is in examples/travel relative to the execution root
from examples.travel import add_hotel_ad_group_bid_modifiers

class TestAddHotelAdGroupBidModifiers(unittest.TestCase):

    def setUp(self):
        self.mock_google_ads_client = mock.Mock(spec=add_hotel_ad_group_bid_modifiers.GoogleAdsClient)

        # Mock services
        self.mock_ad_group_service = mock.Mock()
        self.mock_ad_group_bid_modifier_service = mock.Mock()

        # Configure get_service
        def get_service_side_effect(service_name, version=None):
            if service_name == "AdGroupService":
                return self.mock_ad_group_service
            elif service_name == "AdGroupBidModifierService":
                return self.mock_ad_group_bid_modifier_service
            return mock.DEFAULT
        self.mock_google_ads_client.get_service.side_effect = get_service_side_effect

        # Mock enums
        self.mock_google_ads_client.enums = mock.Mock()
        self.mock_google_ads_client.enums.DayOfWeekEnum = mock.Mock()
        self.mock_google_ads_client.enums.DayOfWeekEnum.MONDAY = "MONDAY_ENUM_VALUE"

        # Mock get_type for AdGroupBidModifierOperation
        # This needs to return an object that has a 'create' attribute.
        # The 'create' attribute object then needs 'hotel_check_in_day', 
        # 'hotel_length_of_stay', 'ad_group', and 'bid_modifier' attributes.
        def get_type_side_effect(type_name, version=None):
            if type_name == "AdGroupBidModifierOperation":
                mock_operation_container = mock.Mock(name=f"{type_name}_OperationContainer")
                # The object that script assigns to, e.g. check_in_ag_bid_modifier
                created_object_mock = mock.Mock(name=f"{type_name}_Create") 
                
                # Setup nested criterion objects
                created_object_mock.hotel_check_in_day = mock.Mock(name="HotelCheckInDayInfo")
                created_object_mock.hotel_length_of_stay = mock.Mock(name="HotelLengthOfStayInfo")
                
                mock_operation_container.create = created_object_mock
                return mock_operation_container
            return mock.DEFAULT
        self.mock_google_ads_client.get_type.side_effect = get_type_side_effect

        # Mock AdGroupService's ad_group_path
        self.expected_ad_group_path = "customers/test_customer_id/adGroups/test_ad_group_id"
        self.mock_ad_group_service.ad_group_path.return_value = self.expected_ad_group_path
        
        # Mock AdGroupBidModifierService's mutate method
        self.mock_mutate_response = mock.Mock()
        self.expected_resource_name_1 = "customers/test_customer_id/adGroupBidModifiers/mod1"
        self.expected_resource_name_2 = "customers/test_customer_id/adGroupBidModifiers/mod2"
        result1 = mock.Mock()
        result1.resource_name = self.expected_resource_name_1
        result2 = mock.Mock()
        result2.resource_name = self.expected_resource_name_2
        self.mock_mutate_response.results = [result1, result2]
        self.mock_ad_group_bid_modifier_service.mutate_ad_group_bid_modifiers.return_value = self.mock_mutate_response

    @mock.patch('examples.travel.add_hotel_ad_group_bid_modifiers.main')
    @mock.patch('examples.travel.add_hotel_ad_group_bid_modifiers.GoogleAdsClient.load_from_storage')
    def test_google_ads_client_load(self, mock_load_from_storage, mock_main_script_func):
        """Tests that GoogleAdsClient.load_from_storage is called correctly."""
        mock_ads_client_instance = mock.Mock()
        mock_load_from_storage.return_value = mock_ads_client_instance

        original_argv = sys.argv
        test_argv = [
            'add_hotel_ad_group_bid_modifiers.py',
            '--customer_id', 'cust123',
            '--ad_group_id', 'ag456'
        ]
        sys.argv = test_argv
        try:
            runpy.run_module('examples.travel.add_hotel_ad_group_bid_modifiers', run_name='__main__', alter_sys=True)
        finally:
            sys.argv = original_argv

        mock_load_from_storage.assert_called_once_with(version="v19")
        mock_main_script_func.assert_called_once_with(
            mock_ads_client_instance,
            'cust123',
            'ag456'
        )

    @mock.patch('examples.travel.add_hotel_ad_group_bid_modifiers.main')
    @mock.patch('examples.travel.add_hotel_ad_group_bid_modifiers.GoogleAdsClient.load_from_storage')
    def test_argument_parsing(self, mock_load_from_storage, mock_main_script_func):
        """Tests correct parsing of command-line arguments."""
        mock_ads_client_instance = mock.Mock()
        mock_load_from_storage.return_value = mock_ads_client_instance

        expected_customer_id = "customer_test_789"
        expected_ad_group_id = "ad_group_test_000"

        original_argv = sys.argv
        test_argv = [
            'add_hotel_ad_group_bid_modifiers.py',
            '--customer_id', expected_customer_id,
            '--ad_group_id', expected_ad_group_id
        ]
        sys.argv = test_argv
        try:
            runpy.run_module('examples.travel.add_hotel_ad_group_bid_modifiers', run_name='__main__', alter_sys=True)
        finally:
            sys.argv = original_argv
        
        mock_load_from_storage.assert_called_once() # Called as part of __main__
        mock_main_script_func.assert_called_once_with(
            mock_ads_client_instance,
            expected_customer_id,
            expected_ad_group_id
        )

    @mock.patch('builtins.print')
    def test_main_function_logic_and_api_calls(self, mock_print):
        """Tests the main logic, API calls, and print statements."""
        customer_id = "test_customer_id"
        ad_group_id = "test_ad_group_id"

        # Call the actual main function from the script
        add_hotel_ad_group_bid_modifiers.main(
            self.mock_google_ads_client,
            customer_id,
            ad_group_id
        )

        # 1. Assert get_service calls
        expected_get_service_calls = [
            mock.call("AdGroupService"),
            mock.call("AdGroupBidModifierService"),
        ]
        self.assertEqual(self.mock_google_ads_client.get_service.call_args_list, expected_get_service_calls)

        # 2. Assert ad_group_path call (happens twice)
        self.mock_ad_group_service.ad_group_path.assert_has_calls([
            mock.call(customer_id, ad_group_id),
            mock.call(customer_id, ad_group_id)
        ])
        self.assertEqual(self.mock_ad_group_service.ad_group_path.call_count, 2)
        
        # 3. Assert get_type calls (happens twice for "AdGroupBidModifierOperation")
        # self.mock_google_ads_client.get_type.assert_called_with("AdGroupBidModifierOperation") - this only checks last call
        self.assertEqual(self.mock_google_ads_client.get_type.call_count, 2)
        self.mock_google_ads_client.get_type.assert_any_call("AdGroupBidModifierOperation")


        # 4. Assert mutate_ad_group_bid_modifiers call
        self.mock_ad_group_bid_modifier_service.mutate_ad_group_bid_modifiers.assert_called_once()
        args, kwargs = self.mock_ad_group_bid_modifier_service.mutate_ad_group_bid_modifiers.call_args
        
        self.assertEqual(kwargs['customer_id'], customer_id)
        self.assertEqual(len(kwargs['operations']), 2)
        
        op1_create = kwargs['operations'][0].create 
        op2_create = kwargs['operations'][1].create

        # Check operation 1 (Check-in day)
        self.assertEqual(op1_create.ad_group, self.expected_ad_group_path)
        self.assertEqual(op1_create.hotel_check_in_day.day_of_week, "MONDAY_ENUM_VALUE")
        self.assertEqual(op1_create.bid_modifier, 1.5)

        # Check operation 2 (Length of stay)
        self.assertEqual(op2_create.ad_group, self.expected_ad_group_path)
        self.assertEqual(op2_create.hotel_length_of_stay.min_nights, 3)
        self.assertEqual(op2_create.hotel_length_of_stay.max_nights, 7)
        self.assertEqual(op2_create.bid_modifier, 1.7)
        
        # 5. Assert print statements
        expected_print_calls = [
            mock.call(f"Added {len(self.mock_mutate_response.results)} hotel ad group bid modifiers:"),
            mock.call(self.expected_resource_name_1),
            mock.call(self.expected_resource_name_2),
        ]
        self.assertEqual(mock_print.call_args_list, expected_print_calls)

if __name__ == '__main__':
    unittest.main()
