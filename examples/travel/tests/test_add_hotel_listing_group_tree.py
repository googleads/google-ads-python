import unittest
from unittest.mock import patch, MagicMock, call, ANY
import argparse
import sys

# Add examples to sys.path
sys.path.append("examples")
from travel import add_hotel_listing_group_tree


class TestAddHotelListingGroupTree(unittest.TestCase):

    def setUp(self):
        # Reset temporary ID before each test
        add_hotel_listing_group_tree.next_temp_id = -1

    @patch("travel.add_hotel_listing_group_tree.GoogleAdsClient.load_from_storage")
    @patch("travel.add_hotel_listing_group_tree.argparse.ArgumentParser")
    def test_main(self, mock_argument_parser, mock_load_client):
        mock_args = MagicMock()
        mock_args.customer_id = "test_customer_id"
        mock_args.ad_group_id = "test_ad_group_id"
        mock_args.percent_cpc_bid_micro_amount = 1000000

        mock_parser_instance = mock_argument_parser.return_value
        mock_parser_instance.parse_args.return_value = mock_args

        mock_client = MagicMock()
        mock_load_client.return_value = mock_client

        mock_ad_group_criterion_service = MagicMock()
        mock_geo_target_constant_service = MagicMock()

        mock_client.get_service.side_effect = lambda service_name: {
            "AdGroupCriterionService": mock_ad_group_criterion_service,
            "GeoTargetConstantService": mock_geo_target_constant_service
        }[service_name]

        # Mock service responses
        mock_mutate_response = MagicMock()
        mock_result1 = MagicMock()
        mock_result1.resource_name = "criterion_resource_name_1"
        mock_result2 = MagicMock()
        mock_result2.resource_name = "criterion_resource_name_2"
        # ... add more results if needed, matching the number of operations
        mock_mutate_response.results = [mock_result1, mock_result2, MagicMock(), MagicMock(), MagicMock()]
        mock_ad_group_criterion_service.mutate_ad_group_criteria.return_value = mock_mutate_response

        # Mock path helpers
        mock_ad_group_criterion_service.ad_group_criterion_path.side_effect = lambda cust_id, ag_id, temp_id: f"customers/{cust_id}/adGroupCriteria/{ag_id}~{temp_id}"
        mock_geo_target_constant_service.geo_target_constant_path.return_value = "geoTargetConstants/2392"


        # Mock types and enums
        mock_client.get_type.side_effect = lambda type_name: MagicMock(type_name=type_name) # Store type_name for debugging
        mock_client.enums.ListingGroupTypeEnum.SUBDIVISION = "SUBDIVISION"
        mock_client.enums.ListingGroupTypeEnum.UNIT = "UNIT"
        mock_client.enums.AdGroupCriterionStatusEnum.ENABLED = "ENABLED"

        with patch("builtins.print") as mock_print:
            add_hotel_listing_group_tree.main(
                mock_client,
                mock_args.customer_id,
                mock_args.ad_group_id,
                mock_args.percent_cpc_bid_micro_amount,
            )

        mock_load_client.assert_called_once_with(version="v19")
        mock_ad_group_criterion_service.mutate_ad_group_criteria.assert_called_once()

        # Assert that operations were created and passed to mutate_ad_group_criteria
        args, kwargs = mock_ad_group_criterion_service.mutate_ad_group_criteria.call_args
        self.assertEqual(kwargs['customer_id'], "test_customer_id")
        operations = kwargs['operations']
        self.assertEqual(len(operations), 5) # Root, 5-star, Other Hotels, Japan, Other Regions

        # Example check for the root node operation (first operation)
        root_op_create = operations[0].create
        self.assertEqual(root_op_create.listing_group.type_, "SUBDIVISION")
        self.assertEqual(root_op_create.resource_name, "customers/test_customer_id/adGroupCriteria/test_ad_group_id~-1")

        # Example check for 5-star unit node (second operation)
        five_star_op_create = operations[1].create
        self.assertEqual(five_star_op_create.listing_group.type_, "UNIT")
        self.assertEqual(five_star_op_create.listing_group.parent_ad_group_criterion, "customers/test_customer_id/adGroupCriteria/test_ad_group_id~-1")
        self.assertTrue(hasattr(five_star_op_create.listing_group.case_value, 'hotel_class'))
        self.assertEqual(five_star_op_create.listing_group.case_value.hotel_class.value, 5)
        self.assertEqual(five_star_op_create.percent_cpc_bid_micros, 1000000)
        self.assertEqual(five_star_op_create.resource_name, "customers/test_customer_id/adGroupCriteria/test_ad_group_id~-2")


        # Check print statements (simplified for brevity)
        mock_print.assert_any_call("Added 5 listing group info entities with resource names:")
        mock_print.assert_any_call("\t'criterion_resource_name_1'")
        mock_print.assert_any_call("\t'criterion_resource_name_2'")


    @patch("travel.add_hotel_listing_group_tree.main")
    @patch("travel.add_hotel_listing_group_tree.GoogleAdsClient.load_from_storage")
    @patch("argparse.ArgumentParser")
    def test_script_runner(self, mock_argument_parser, mock_load_client, mock_main_function):
        mock_args = MagicMock()
        mock_args.customer_id = "test_customer_id_script"
        mock_args.ad_group_id = "test_ad_group_id_script"
        mock_args.percent_cpc_bid_micro_amount = 2000000

        mock_parser_instance = mock_argument_parser.return_value
        mock_parser_instance.parse_args.return_value = mock_args

        mock_client = MagicMock()
        mock_load_client.return_value = mock_client

        with patch.object(add_hotel_listing_group_tree, "__name__", "__main__"):
            import importlib
            importlib.reload(add_hotel_listing_group_tree) # Reload to reset global next_temp_id based on script's initial value
            add_hotel_listing_group_tree.next_temp_id = -1 # Explicitly reset after reload for test consistency

        mock_main_function.assert_called_once_with(
            mock_client,
            "test_customer_id_script",
            "test_ad_group_id_script",
            2000000
        )

if __name__ == "__main__":
    unittest.main()
