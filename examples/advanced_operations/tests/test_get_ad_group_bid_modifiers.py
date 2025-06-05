import sys
import os
# Calculate the path to the project root directory
# __file__ is examples/advanced_operations/tests/test_name.py
# project_root is three levels up from the test file's directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import unittest
from unittest import mock
import sys

# sys.path.insert(0, '/app') # For subtask environment for this run - Keep commented out for final file

from examples.advanced_operations import get_ad_group_bid_modifiers

# Custom mock class to simulate proto_plus.Message behavior for AdGroupBidModifier
class MockProtoPlusAdGroupBidModifier(mock.Mock):
    _criterion_type_string = 'unknown' # Default, should be set per instance
    _pb_mock = None # Initialize to None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        parent_mock_name = kwargs.get('name', 'UnknownModifier')
        # Each instance will have its own _pb mock
        self._pb_mock = mock.Mock(name=f"Instance_pb_mock_for_{parent_mock_name}")
        # Configure WhichOneof on this _pb_mock
        self._pb_mock.WhichOneof.side_effect = self._get_criterion_type_string

    def _get_criterion_type_string(self, name_param): # Renamed to avoid conflict if 'name' is a real field
        if name_param == 'criterion':
            return self._criterion_type_string
        return None

    @staticmethod
    def pb(instance):
        # This staticmethod will be called by type(instance).pb(instance)
        # It should return the object that has the WhichOneof method.
        if not hasattr(instance, '_pb_mock') or instance._pb_mock is None:
            # Fallback if _pb_mock wasn't initialized for some reason (shouldn't happen with __init__)
            temp_pb_mock = mock.Mock(name="Static_pb_fallback_pb_mock")
            temp_pb_mock.WhichOneof.return_value = instance._criterion_type_string if hasattr(instance, '_criterion_type_string') else 'unknown'
            return temp_pb_mock
        return instance._pb_mock


class TestGetAdGroupBidModifiers(unittest.TestCase):

    def _setup_common_mocks(self, mock_google_ads_client):
        mock_google_ads_client.version = "v19"

        self.mock_google_ads_service = mock.Mock(name="GoogleAdsService")
        mock_google_ads_client.get_service.return_value = self.mock_google_ads_service

        # Mock Enums with .name attribute properly set up using PropertyMock
        self.device_enum_mock = mock.Mock(name="DeviceEnum")
        mock_mobile_member = mock.Mock(name="MobileEnumMember")
        type(mock_mobile_member).name = mock.PropertyMock(return_value="MOBILE")
        self.device_enum_mock.MOBILE = mock_mobile_member

        mock_tablet_member = mock.Mock(name="TabletEnumMember")
        type(mock_tablet_member).name = mock.PropertyMock(return_value="TABLET")
        self.device_enum_mock.TABLET = mock_tablet_member

        mock_desktop_member = mock.Mock(name="DesktopEnumMember")
        type(mock_desktop_member).name = mock.PropertyMock(return_value="DESKTOP")
        self.device_enum_mock.DESKTOP = mock_desktop_member
        mock_google_ads_client.enums.DeviceEnum = self.device_enum_mock

        # These are not used by get_ad_group_bid_modifiers.py for printing .name, but good practice if they were
        self.mock_criterion_type_keyword = mock.Mock(name="KeywordCriterionTypeMember")
        type(self.mock_criterion_type_keyword).name = mock.PropertyMock(return_value="KEYWORD")
        mock_google_ads_client.enums.CriterionTypeEnum.KEYWORD = self.mock_criterion_type_keyword

        self.mock_keyword_match_broad = mock.Mock(name="BroadMatchMember")
        type(self.mock_keyword_match_broad).name = mock.PropertyMock(return_value="BROAD")
        self.mock_keyword_match_exact = mock.Mock(name="ExactMatchMember")
        type(self.mock_keyword_match_exact).name = mock.PropertyMock(return_value="EXACT")
        mock_google_ads_client.enums.KeywordMatchTypeEnum.BROAD = self.mock_keyword_match_broad
        mock_google_ads_client.enums.KeywordMatchTypeEnum.EXACT = self.mock_keyword_match_exact

        self.search_request_mock = mock.Mock(name="SearchGoogleAdsRequest")
        mock_google_ads_client.get_type.return_value = self.search_request_mock

        return self.mock_google_ads_service, self.search_request_mock

    def _create_mock_row(self, campaign_id, ad_group_id, criterion_id,
                         bid_modifier_value, criterion_type_name_for_oneof,
                         device_type_enum_val=None):
        mock_row = mock.Mock(name=f"GoogleAdsRow_{criterion_id}")
        mock_row.campaign = mock.Mock(id=int(campaign_id))
        mock_row.ad_group = mock.Mock(id=int(ad_group_id))

        mock_modifier = MockProtoPlusAdGroupBidModifier(name=f"AdGroupBidModifier_{criterion_id}")
        mock_modifier.criterion_id = criterion_id
        mock_modifier.bid_modifier = bid_modifier_value
        mock_modifier._criterion_type_string = criterion_type_name_for_oneof

        if criterion_type_name_for_oneof == "device" and device_type_enum_val:
            # device_type_enum_val is already a mock with .name configured (e.g., self.device_enum_mock.MOBILE)
            mock_modifier.device = mock.Mock(type_=device_type_enum_val)

        mock_row.ad_group_bid_modifier = mock_modifier
        return mock_row

    @mock.patch("builtins.print")
    @mock.patch("examples.advanced_operations.get_ad_group_bid_modifiers.GoogleAdsClient.load_from_storage")
    def test_main_with_ad_group_id_and_device_criterion(self, mock_load_from_storage, mock_print):
        mock_google_ads_client = mock.Mock()
        mock_load_from_storage.return_value = mock_google_ads_client
        mock_google_ads_service, search_request_mock = self._setup_common_mocks(mock_google_ads_client)

        customer_id = "cust123"
        ad_group_id_str = "ag456"
        ad_group_id_int = 456

        mock_row_device = self._create_mock_row(
            campaign_id=12345, ad_group_id=ad_group_id_int, criterion_id=1001,
            bid_modifier_value=1.5, criterion_type_name_for_oneof="device",
            device_type_enum_val=self.device_enum_mock.MOBILE
        )
        mock_google_ads_service.search.return_value = [mock_row_device] # search returns an iterable of rows

        # Temporarily add sys.path for this execution context
        original_sys_path = list(sys.path)
        sys.path.insert(0, '/app')
        try:
            get_ad_group_bid_modifiers.main(mock_google_ads_client, customer_id, ad_group_id_str)
        finally:
            sys.path = original_sys_path


        # search_request_mock is configured by the script.
        self.assertEqual(search_request_mock.customer_id, customer_id)
        self.assertIn(f"WHERE ad_group.id = {ad_group_id_str}", search_request_mock.query) # Corrected: WHERE not AND
        mock_google_ads_service.search.assert_called_once_with(request=search_request_mock)

        expected_print_fragment = (
            f"Ad group bid modifier with criterion ID '{mock_row_device.ad_group_bid_modifier.criterion_id}', "
            f"bid modifier value '1.5', "
            f"device type 'MOBILE' " # Removed "and "
            f"was found in ad group with ID '{ad_group_id_int}' of campaign with ID '{mock_row_device.campaign.id}'."
        )

        # More robust check for the print assertion
        found_matching_print = False
        first_actual_print_for_diff = ""
        if mock_print.call_args_list:
            first_actual_print_for_diff = mock_print.call_args_list[0][0][0] # For diff if no match
            for actual_call in mock_print.call_args_list:
                if expected_print_fragment == actual_call[0][0]:
                    found_matching_print = True
                    break

        if not found_matching_print:
            self.assertEqual(repr(expected_print_fragment), repr(first_actual_print_for_diff),
                             f"Expected print not found. First actual print (repr): {repr(first_actual_print_for_diff)}")
        else:
            self.assertTrue(found_matching_print) # Should pass if found


    @mock.patch("builtins.print")
    @mock.patch("examples.advanced_operations.get_ad_group_bid_modifiers.GoogleAdsClient.load_from_storage")
    def test_main_without_ad_group_id(self, mock_load_from_storage, mock_print):
        mock_google_ads_client = mock.Mock()
        mock_load_from_storage.return_value = mock_google_ads_client
        mock_google_ads_service, search_request_mock = self._setup_common_mocks(mock_google_ads_client)

        customer_id = "cust789"
        campaign_id_int = 67890
        ad_group_id_int_for_row1 = 11122

        mock_row1 = self._create_mock_row(
            campaign_id=campaign_id_int, ad_group_id=ad_group_id_int_for_row1, criterion_id=2001,
            bid_modifier_value=1.2, criterion_type_name_for_oneof="device",
            device_type_enum_val=self.device_enum_mock.TABLET
        )
        mock_google_ads_service.search.return_value = [mock_row1]

        # Temporarily add sys.path for this execution context
        original_sys_path = list(sys.path)
        sys.path.insert(0, '/app')
        try:
            get_ad_group_bid_modifiers.main(mock_google_ads_client, customer_id, None)
        finally:
            sys.path = original_sys_path


        self.assertEqual(search_request_mock.customer_id, customer_id)
        self.assertNotIn("AND ad_group.id =", search_request_mock.query)
        mock_google_ads_service.search.assert_called_once_with(request=search_request_mock)

        expected_print_fragment = (
            f"Ad group bid modifier with criterion ID '{mock_row1.ad_group_bid_modifier.criterion_id}', "
            f"bid modifier value '1.2', "
            f"device type 'TABLET' " # Removed "and "
            f"was found in ad group with ID '{ad_group_id_int_for_row1}' of campaign with ID '{campaign_id_int}'."
        )
        # More robust check for the print assertion
        found_matching_print = False
        first_actual_print_for_diff = ""
        if mock_print.call_args_list:
            first_actual_print_for_diff = mock_print.call_args_list[0][0][0]
            for actual_call in mock_print.call_args_list:
                if expected_print_fragment == actual_call[0][0]:
                    found_matching_print = True
                    break

        if not found_matching_print:
            self.assertEqual(repr(expected_print_fragment), repr(first_actual_print_for_diff),
                             f"Expected print not found. First actual print (repr): {repr(first_actual_print_for_diff)}")
        else:
            self.assertTrue(found_matching_print)


if __name__ == '__main__':
    unittest.main()
