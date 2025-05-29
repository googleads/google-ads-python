import unittest
from unittest import mock
import sys
import runpy
import argparse

from examples.travel import add_hotel_listing_group_tree

class TestAddHotelListingGroupTree(unittest.TestCase):

    def setUp(self):
        self.mock_google_ads_client = mock.Mock(spec=add_hotel_listing_group_tree.GoogleAdsClient)

        # Mock Services
        self.mock_ad_group_criterion_service = mock.Mock()
        self.mock_geo_target_constant_service = mock.Mock()

        def get_service_side_effect(service_name, version=None):
            if service_name == "AdGroupCriterionService":
                return self.mock_ad_group_criterion_service
            elif service_name == "GeoTargetConstantService":
                return self.mock_geo_target_constant_service
            return mock.DEFAULT
        self.mock_google_ads_client.get_service.side_effect = get_service_side_effect

        # Mock AdGroupCriterionService methods
        self.mock_agc_mutate_response = mock.Mock()
        self.mock_agc_results = [mock.Mock(resource_name=f"customers/cust_id/adGroupCriteria/final_{i}") for i in range(5)]
        self.mock_agc_mutate_response.results = self.mock_agc_results
        self.mock_ad_group_criterion_service.mutate_ad_group_criteria.return_value = self.mock_agc_mutate_response

        def ad_group_criterion_path_side_effect(customer_id, ad_group_id, criterion_id):
            return f"customers/{customer_id}/adGroupCriteria/{ad_group_id}~{criterion_id}" # Simpler format for temp IDs in test
        self.mock_ad_group_criterion_service.ad_group_criterion_path.side_effect = ad_group_criterion_path_side_effect
        
        # Mock GeoTargetConstantService methods
        self.expected_geo_target_path = "geoTargetConstants/2392"
        self.mock_geo_target_constant_service.geo_target_constant_path.return_value = self.expected_geo_target_path

        # Mock Enums
        self.mock_google_ads_client.enums.ListingGroupTypeEnum = mock.Mock()
        self.mock_google_ads_client.enums.ListingGroupTypeEnum.SUBDIVISION = "SUBDIVISION"
        self.mock_google_ads_client.enums.ListingGroupTypeEnum.UNIT = "UNIT"
        self.mock_google_ads_client.enums.AdGroupCriterionStatusEnum = mock.Mock()
        self.mock_google_ads_client.enums.AdGroupCriterionStatusEnum.ENABLED = "ENABLED"

        # Mock GetType
        def get_type_side_effect(type_name, version=None):
            mock_obj = mock.Mock(name=type_name)
            if type_name == "AdGroupCriterionOperation":
                # This target_for_create is what client.copy_from will populate.
                # It needs the full expected structure for assertions later.
                target_for_create = mock.Mock(name="AdGroupCriterion_TargetForCreateInOperation")
                target_for_create.listing_group = mock.Mock(name="ListingGroup_InTarget")
                target_for_create.listing_group.case_value = mock.Mock(name="CaseValue_InTarget")
                target_for_create.listing_group.case_value.hotel_class = mock.Mock(name="HotelClass_InTarget")
                target_for_create.listing_group.case_value.hotel_country_region = mock.Mock(name="HotelCountryRegion_InTarget")
                mock_obj.create = target_for_create
            elif type_name == "ListingGroupInfo":
                # This is used as a source for copy_from into ad_group_criterion.listing_group
                # and also for copy_from into its own case_value from a ListingDimensionInfo
                mock_obj.case_value = mock.Mock(name="ListingDimensionInfo_HolderForCaseValue")
            elif type_name == "ListingDimensionInfo":
                # Source for copy_from into ListingGroupInfo.case_value
                mock_obj.hotel_class = mock.Mock(name="HotelClassInfo_InDimension")
                mock_obj.hotel_country_region = mock.Mock(name="HotelCountryRegionInfo_InDimension")
            # HotelClassInfo and HotelCountryRegionInfo are sources for copy_from or direct value access
            elif type_name == "HotelClassInfo":
                # Can have .value assigned
                pass
            elif type_name == "HotelCountryRegionInfo":
                # Can have .country_region_criterion assigned
                pass
            return mock_obj
        self.mock_google_ads_client.get_type.side_effect = get_type_side_effect
        
        # Mock copy_from to simulate its behavior of populating the destination mock
        def actual_copy_from(destination_mock_outer, source_mock_outer):
            # This handles client.copy_from(operation.create, ad_group_criterion_object)
            # AND client.copy_from(listing_group_info.case_value, listing_dimension_info_object)
            # AND client.copy_from(other_hotels_listing_dimension_info.hotel_class, client.get_type("HotelClassInfo"))

            # Simple attribute transfer for top-level attributes
            # These are attributes directly on ad_group_criterion_object or listing_dimension_info_object
            # For AdGroupCriterion
            destination_mock_outer.ad_group = getattr(source_mock_outer, 'ad_group', None)
            destination_mock_outer.status = getattr(source_mock_outer, 'status', None)
            destination_mock_outer.resource_name = getattr(source_mock_outer, 'resource_name', None)
            destination_mock_outer.percent_cpc_bid_micros = getattr(source_mock_outer, 'percent_cpc_bid_micros', None)

            # For ListingGroup (source_mock_outer is ad_group_criterion_object)
            if hasattr(source_mock_outer, 'listing_group'):
                # destination_mock_outer is operation.create, so destination_mock_outer.listing_group is ListingGroup_InTarget
                dest_lg = destination_mock_outer.listing_group
                src_lg = source_mock_outer.listing_group
                dest_lg.type_ = getattr(src_lg, 'type_', None)
                dest_lg.parent_ad_group_criterion = getattr(src_lg, 'parent_ad_group_criterion', None)
                
                # For CaseValue (source_mock_outer.listing_group is ListingGroupInfo)
                # Here, destination_mock_outer is operation.create.listing_group
                # source_mock_outer is ad_group_criterion_object.listing_group
                if hasattr(src_lg, 'case_value'):
                    dest_cv = dest_lg.case_value 
                    src_cv = src_lg.case_value 
                    # Check if src_cv (ListingDimensionInfo) has hotel_class or hotel_country_region
                    if hasattr(src_cv, 'hotel_class') and src_cv.hotel_class.mock_calls: # Check if it was configured
                        dest_cv.hotel_class.value = getattr(src_cv.hotel_class, 'value', None)
                    elif hasattr(src_cv, 'hotel_country_region') and src_cv.hotel_country_region.mock_calls:
                        dest_cv.hotel_country_region.country_region_criterion = \
                            getattr(src_cv.hotel_country_region, 'country_region_criterion', None)
            
            # This part handles client.copy_from(listing_group_info.case_value, listing_dimension_info)
            # Here, destination_mock_outer is listing_group_info.case_value
            # source_mock_outer is listing_dimension_info
            if hasattr(source_mock_outer, 'hotel_class') and source_mock_outer.hotel_class.name == "HotelClassInfo_InDimension":
                 # Ensure destination_mock_outer is the case_value mock
                if destination_mock_outer.name == "ListingDimensionInfo_HolderForCaseValue" or \
                   destination_mock_outer.name == "CaseValue_InTarget":
                    destination_mock_outer.hotel_class = source_mock_outer.hotel_class
                    # If source_mock_outer.hotel_class.value was set, it's on source_mock_outer.hotel_class.value
                    # destination_mock_outer.hotel_class will now point to that mock.
                    
            if hasattr(source_mock_outer, 'hotel_country_region') and source_mock_outer.hotel_country_region.name == "HotelCountryRegionInfo_InDimension":
                if destination_mock_outer.name == "ListingDimensionInfo_HolderForCaseValue" or \
                   destination_mock_outer.name == "CaseValue_InTarget":
                    destination_mock_outer.hotel_country_region = source_mock_outer.hotel_country_region

            # This handles client.copy_from(listing_dimension_info.hotel_class, client.get_type("HotelClassInfo"))
            # Here, destination_mock_outer is listing_dimension_info.hotel_class
            # source_mock_outer is the simple mock from get_type("HotelClassInfo")
            # This is mainly to establish the oneof field. The source mock has no values.
            if source_mock_outer.name == "HotelClassInfo" and \
               (destination_mock_outer.name == "HotelClassInfo_InDimension" or destination_mock_outer.name == "HotelClass_InTarget"):
                # No actual value to copy, just marks hotel_class as the active oneof.
                # The mock structure should already handle this by providing hotel_class attribute.
                pass
            if source_mock_outer.name == "HotelCountryRegionInfo" and \
               (destination_mock_outer.name == "HotelCountryRegionInfo_InDimension" or destination_mock_outer.name == "HotelCountryRegion_InTarget"):
                pass


        self.mock_google_ads_client.copy_from = mock.Mock(side_effect=actual_copy_from)


    @mock.patch('examples.travel.add_hotel_listing_group_tree.main')
    @mock.patch('examples.travel.add_hotel_listing_group_tree.GoogleAdsClient.load_from_storage')
    def test_google_ads_client_load(self, mock_load_from_storage, mock_main_script_func):
        mock_ads_client_instance = mock.Mock()
        mock_load_from_storage.return_value = mock_ads_client_instance
        original_argv = sys.argv
        test_argv = [
            'add_hotel_listing_group_tree.py',
            '--customer_id', 'cust123',
            '--ad_group_id', 'ag456',
            '--percent_cpc_bid_micro_amount', '10000'
        ]
        sys.argv = test_argv
        try:
            runpy.run_module('examples.travel.add_hotel_listing_group_tree', run_name='__main__', alter_sys=True)
        finally:
            sys.argv = original_argv
        mock_load_from_storage.assert_called_once_with(version="v19")
        mock_main_script_func.assert_called_once_with(
            mock_ads_client_instance,
            'cust123',
            'ag456',
            10000
        )

    @mock.patch('examples.travel.add_hotel_listing_group_tree.main')
    @mock.patch('examples.travel.add_hotel_listing_group_tree.GoogleAdsClient.load_from_storage')
    def test_argument_parsing(self, mock_load_from_storage, mock_main_script_func):
        mock_ads_client_instance = mock.Mock()
        mock_load_from_storage.return_value = mock_ads_client_instance
        expected_customer_id = "customer_test_789"
        expected_ad_group_id = "ad_group_test_000"
        expected_bid_amount = 150000
        original_argv = sys.argv
        test_argv = [
            'add_hotel_listing_group_tree.py',
            '--customer_id', expected_customer_id,
            '--ad_group_id', expected_ad_group_id,
            '--percent_cpc_bid_micro_amount', str(expected_bid_amount)
        ]
        sys.argv = test_argv
        try:
            runpy.run_module('examples.travel.add_hotel_listing_group_tree', run_name='__main__', alter_sys=True)
        finally:
            sys.argv = original_argv
        mock_main_script_func.assert_called_once_with(
            mock_ads_client_instance,
            expected_customer_id,
            expected_ad_group_id,
            expected_bid_amount
        )

    @mock.patch('builtins.print')
    @mock.patch('examples.travel.add_hotel_listing_group_tree.next_temp_id', -1) # Reset before main call
    def test_main_function_logic_and_api_calls(self, mock_print, mock_next_temp_id_val_not_used):
        # mock_next_temp_id_val_not_used is the -1 value from the patch, not the mock object itself.
        # To control next_temp_id's value if the script modifies it, we'd need a different patching approach
        # or patch the module variable directly if the test framework allows.
        # For now, this test assumes that by patching it to -1 before main, the sequence -1, -2, ... will be used.
        # We will verify this by checking the resource_name attributes.
        
        customer_id = "test_cust_id"
        ad_group_id = "test_ad_group_id"
        percent_cpc_bid_micro_amount = 1200000

        # Call the actual main function
        add_hotel_listing_group_tree.main(
            self.mock_google_ads_client,
            customer_id,
            ad_group_id,
            percent_cpc_bid_micro_amount
        )

        # 1. Assert service calls
        self.mock_google_ads_client.get_service.assert_any_call("AdGroupCriterionService")
        self.mock_google_ads_client.get_service.assert_any_call("GeoTargetConstantService")
        self.mock_geo_target_constant_service.geo_target_constant_path.assert_called_once_with(2392)

        # 2. Assert mutate call
        self.mock_ad_group_criterion_service.mutate_ad_group_criteria.assert_called_once()
        args, kwargs = self.mock_ad_group_criterion_service.mutate_ad_group_criteria.call_args
        self.assertEqual(kwargs['customer_id'], customer_id)
        
        operations = kwargs['operations']
        self.assertEqual(len(operations), 5) # Root, 2 level-1, 2 level-2

        # Expected resource names based on mocked ad_group_criterion_path and sequential temp IDs
        # The actual next_temp_id is modified inside the script's functions.
        # Our patch sets the initial value.
        # The mock for ad_group_criterion_path needs to generate names based on this.
        # The script's logic: create_obj(..., next_temp_id), then next_temp_id -= 1
        
        # We need to check the *input* to ad_group_criterion_path for the temp_id
        # and then the *output* as the resource_name on the operation.create.
        
        # Check path calls (these are made inside create_ad_group_criterion)
        # The temp IDs passed to ad_group_criterion_path should be -1, -2, -3, -4, -5
        expected_agc_path_calls = [
            mock.call(customer_id, ad_group_id, -1), # Root
            mock.call(customer_id, ad_group_id, -2), # L1: 5-star (UNIT)
            mock.call(customer_id, ad_group_id, -3), # L1: Other (SUBDIVISION)
            mock.call(customer_id, ad_group_id, -4), # L2: Japan (UNIT)
            mock.call(customer_id, ad_group_id, -5)  # L2: Other Regions (UNIT)
        ]
        self.assertEqual(self.mock_ad_group_criterion_service.ad_group_criterion_path.call_args_list, expected_agc_path_calls)

        # Helper to generate expected temporary resource names for checking parent links
        def get_temp_resource_name(temp_id):
            return f"customers/{customer_id}/adGroupCriteria/{ad_group_id}~{temp_id}"

        # Root node (Op 0, ID -1)
        op0_create = operations[0].create
        self.assertEqual(op0_create.resource_name, get_temp_resource_name(-1))
        self.assertEqual(op0_create.listing_group.type_, "SUBDIVISION")
        self.assertFalse(op0_create.listing_group.parent_ad_group_criterion) # Root has no parent

        # Level 1: 5-star (Op 1, ID -2) - UNIT
        op1_create = operations[1].create
        self.assertEqual(op1_create.resource_name, get_temp_resource_name(-2))
        self.assertEqual(op1_create.listing_group.type_, "UNIT")
        self.assertEqual(op1_create.listing_group.parent_ad_group_criterion, get_temp_resource_name(-1)) # Parent is root
        self.assertEqual(op1_create.listing_group.case_value.hotel_class.value, 5)
        self.assertEqual(op1_create.percent_cpc_bid_micros, percent_cpc_bid_micro_amount)

        # Level 1: Other Hotels (Op 2, ID -3) - SUBDIVISION
        op2_create = operations[2].create
        self.assertEqual(op2_create.resource_name, get_temp_resource_name(-3))
        self.assertEqual(op2_create.listing_group.type_, "SUBDIVISION")
        self.assertEqual(op2_create.listing_group.parent_ad_group_criterion, get_temp_resource_name(-1)) # Parent is root
        # Case value for "other" hotel class should be an empty HotelClassInfo
        self.assertTrue(hasattr(op2_create.listing_group.case_value, 'hotel_class'))
        self.assertFalse(op2_create.listing_group.case_value.hotel_class.mock_calls) # No .value attribute set
        self.assertNotEqual(op2_create.percent_cpc_bid_micros, percent_cpc_bid_micro_amount) # No bid on subdivision

        # Level 2: Japan Hotels (Op 3, ID -4) - UNIT, parent is "Other Hotels" from L1
        op3_create = operations[3].create
        self.assertEqual(op3_create.resource_name, get_temp_resource_name(-4))
        self.assertEqual(op3_create.listing_group.type_, "UNIT")
        self.assertEqual(op3_create.listing_group.parent_ad_group_criterion, get_temp_resource_name(-3)) 
        self.assertEqual(op3_create.listing_group.case_value.hotel_country_region.country_region_criterion, self.expected_geo_target_path)
        self.assertEqual(op3_create.percent_cpc_bid_micros, percent_cpc_bid_micro_amount)
        
        # Level 2: Other Regions (Op 4, ID -5) - UNIT, parent is "Other Hotels" from L1
        op4_create = operations[4].create
        self.assertEqual(op4_create.resource_name, get_temp_resource_name(-5))
        self.assertEqual(op4_create.listing_group.type_, "UNIT")
        self.assertEqual(op4_create.listing_group.parent_ad_group_criterion, get_temp_resource_name(-3))
        # Case value for "other" country region
        self.assertTrue(hasattr(op4_create.listing_group.case_value, 'hotel_country_region'))
        self.assertFalse(op4_create.listing_group.case_value.hotel_country_region.mock_calls) # No .country_region_criterion set
        self.assertEqual(op4_create.percent_cpc_bid_micros, percent_cpc_bid_micro_amount)

        # 3. Print calls
        expected_print_calls = [
            mock.call(f"Added {len(self.mock_agc_results)} listing group info entities with resource names:"),
        ] + [mock.call(f"\t'{res.resource_name}'") for res in self.mock_agc_results]
        self.assertEqual(mock_print.call_args_list, expected_print_calls)

if __name__ == '__main__':
    unittest.main()
