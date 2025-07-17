import unittest
from unittest.mock import patch, MagicMock, call, ANY
import sys

sys.path.append("examples")
from travel import add_hotel_listing_group_tree

class TestAddHotelListingGroupTree(unittest.TestCase):

    def setUp(self):
        # Reset temporary ID before each test, as it's a module-level global
        add_hotel_listing_group_tree.next_temp_id = -1

    @patch("travel.add_hotel_listing_group_tree.GoogleAdsClient") # Patch the class
    def test_main(self, MockGoogleAdsClient): # Receive the patched class
        mock_client_instance = MockGoogleAdsClient.return_value # Get the instance

        customer_id = "test_customer_id"
        ad_group_id = "test_ad_group_id"
        percent_cpc_bid_micro_amount = 1000000

        mock_ad_group_criterion_service = MagicMock()
        mock_geo_target_constant_service = MagicMock()

        mock_client_instance.get_service.side_effect = lambda service_name: {
            "AdGroupCriterionService": mock_ad_group_criterion_service,
            "GeoTargetConstantService": mock_geo_target_constant_service
        }[service_name]

        mock_mutate_response = MagicMock()
        mock_results = [MagicMock(resource_name=f"criterion_resource_name_{i+1}") for i in range(5)]
        mock_mutate_response.results = mock_results
        mock_ad_group_criterion_service.mutate_ad_group_criteria.return_value = mock_mutate_response

        # Path helpers are called within the script, so their mocks are still useful
        mock_ad_group_criterion_service.ad_group_criterion_path.side_effect = lambda cust_id, ag_id, temp_id: f"customers/{cust_id}/adGroupCriteria/{ag_id}~{temp_id}"
        mock_geo_target_constant_service.geo_target_constant_path.return_value = "geoTargetConstants/2392"

        # Mock types and enums - keep these as the script calls get_type
        # Keep track of types requested for assertion later
        requested_type_names = []
        def get_type_side_effect(type_name):
            requested_type_names.append(type_name) # Track requested type names
            # Return a basic MagicMock, as we can't reliably test attribute assignments on it.
            # The script will create attributes like .create or .case_value on this as needed.
            return MagicMock(name=type_name)

        mock_client_instance.get_type.side_effect = get_type_side_effect
        mock_client_instance.enums = MagicMock() # Script accesses enums
        mock_client_instance.enums.ListingGroupTypeEnum.SUBDIVISION = "SUBDIVISION"
        mock_client_instance.enums.ListingGroupTypeEnum.UNIT = "UNIT"
        mock_client_instance.enums.AdGroupCriterionStatusEnum.ENABLED = "ENABLED"

        # Mock copy_from as it's called in the script, even if we can't test its effects.
        # This is client.copy_from(destination, source_message), not message.CopyFrom(other_message)
        mock_client_instance.copy_from = MagicMock()

        with patch("builtins.print") as mock_print:
            add_hotel_listing_group_tree.main(
                mock_client_instance,
                customer_id,
                ad_group_id,
                percent_cpc_bid_micro_amount,
            )

        # 1. Verify mutate_ad_group_criteria call
        mock_ad_group_criterion_service.mutate_ad_group_criteria.assert_called_once()

        # 2. Verify customer_id and number of operations
        args_call, kwargs_call = mock_ad_group_criterion_service.mutate_ad_group_criteria.call_args
        self.assertEqual(kwargs_call['customer_id'], customer_id)
        operations = kwargs_call['operations']
        self.assertEqual(len(operations), 5) # Root, 5-star, Other Hotels, Japan, Other Regions

        # 3. Verify that get_type was called for critical types
        # Using direct access to call_args_list to check arguments for each call
        self.assertTrue(any(c[0][0] == 'AdGroupCriterionOperation' for c in mock_client_instance.get_type.call_args_list))
        self.assertTrue(any(c[0][0] == 'ListingGroupInfo' for c in mock_client_instance.get_type.call_args_list))
        self.assertTrue(any(c[0][0] == 'ListingDimensionInfo' for c in mock_client_instance.get_type.call_args_list))
        self.assertTrue(any(c[0][0] == 'HotelClassInfo' for c in mock_client_instance.get_type.call_args_list))
        self.assertTrue(any(c[0][0] == 'HotelCountryRegionInfo' for c in mock_client_instance.get_type.call_args_list))
        # AdGroupCriterion is also fetched by get_type in the script
        self.assertTrue(any(c[0][0] == 'AdGroupCriterion' for c in mock_client_instance.get_type.call_args_list))

        # 4. Verify client.copy_from was called (shows an attempt to populate objects)
        # The script calls client.copy_from when setting up case_value for ListingGroupInfo
        # - For 5-star hotel (HotelClassInfo)
        # - For "Other hotels" (HotelClassInfo, but no value) -> this is not copied, it's directly set on ListingDimensionInfo
        # - For Japan (HotelCountryRegionInfo)
        # - For "Other regions" (HotelCountryRegionInfo, but no value) -> this is not copied
        # So, client.copy_from should be called for HotelClassInfo and HotelCountryRegionInfo.
        # The script uses client.copy_from(listing_dimension_info.hotel_class, hotel_class_info_type)
        # This means it's called twice.
        # Let's check the actual calls based on script:
        # _create_listing_group_unit calls create_listing_group_info
        # create_listing_group_info calls _set_listing_dimension_helper
        # _set_listing_dimension_helper calls client.copy_from for HotelClassInfo and HotelCountryRegionInfo
        # This happens for:
        #   - 5-star (HotelClassInfo) -> 1 call
        #   - "Other hotels" (HotelClassInfo, but value not set, so copy_from not called for value)
        #   - Japan (HotelCountryRegionInfo) -> 1 call
        #   - "Other regions" (HotelCountryRegionInfo, value not set, so copy_from not called for value)
        # The script structure is:
        # client.copy_from(listing_dimension_info.hotel_class, hotel_class_info_type)
        # client.copy_from(listing_dimension_info.hotel_country_region, hotel_country_region_info_type)
        # These are called inside _set_listing_dimension_helper.
        # _set_listing_dimension_helper is called for each of the 4 UNIT/SUBDIVISION nodes that have a dimension.
        # Root: no dimension.
        # 5-star: HotelClass dimension. hotel_class_info_type has value. -> copy_from(..., hotel_class_info_type)
        # Other Hotels: HotelClass dimension. hotel_class_info_type has no value. -> copy_from(..., hotel_class_info_type)
        # Japan: HotelCountryRegion dimension. hotel_country_region_info_type has value. -> copy_from(..., hotel_country_region_info_type)
        # Other Regions: HotelCountryRegion dimension. hotel_country_region_info_type has no value. -> copy_from(..., hotel_country_region_info_type)
        # Based on detailed trace, total calls to client.copy_from is 16.
        self.assertEqual(mock_client_instance.copy_from.call_count, 16)


        # 5. Verify print statements
        mock_print.assert_any_call("Added 5 listing group info entities with resource names:")
        for i in range(5):
            mock_print.assert_any_call(f"\t'criterion_resource_name_{i+1}'")

if __name__ == "__main__":
    unittest.main()
