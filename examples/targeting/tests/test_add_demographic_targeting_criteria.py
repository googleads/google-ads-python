import unittest
from unittest.mock import MagicMock, patch, call
import sys

# Add the examples directory to the system path to import the script
sys.path.append(".")

from examples.targeting.add_demographic_targeting_criteria import main

class TestAddDemographicTargetingCriteria(unittest.TestCase):
    @patch("examples.targeting.add_demographic_targeting_criteria.GoogleAdsClient.load_from_storage")
    def test_main_function_calls(self, mock_load_client):
        # Mock IDs
        MOCK_CUSTOMER_ID = "1234567890"
        MOCK_AD_GROUP_ID = "9876543210"

        # Create a mock GoogleAdsClient
        mock_google_ads_client = MagicMock()
        mock_load_client.return_value = mock_google_ads_client

        # Mock the AdGroupCriterionService
        mock_ad_group_criterion_service = MagicMock()
        
        # Mock the AdGroupService (for ad_group_path)
        mock_ad_group_service = MagicMock()

        def get_service_side_effect(service_name, version=None):
            if service_name == "AdGroupCriterionService":
                return mock_ad_group_criterion_service
            elif service_name == "AdGroupService":
                return mock_ad_group_service
            return MagicMock()

        mock_google_ads_client.get_service.side_effect = get_service_side_effect
        
        # Expected ad_group resource name
        expected_ad_group_rname = mock_ad_group_service.ad_group_path(
            MOCK_CUSTOMER_ID, MOCK_AD_GROUP_ID
        )

        # Mock the get_type method for AdGroupCriterionOperation
        def get_type_side_effect(type_name):
            if type_name == "AdGroupCriterionOperation":
                # Return a new MagicMock each time for distinct operations
                return MagicMock()
            return MagicMock()

        mock_google_ads_client.get_type.side_effect = get_type_side_effect
        
        # Mock enums
        GenderTypeEnum = mock_google_ads_client.enums.GenderTypeEnum
        AgeRangeTypeEnum = mock_google_ads_client.enums.AgeRangeTypeEnum
        
        # Call the main function
        main(mock_google_ads_client, MOCK_CUSTOMER_ID, MOCK_AD_GROUP_ID)

        # Assert that mutate_ad_group_criteria was called
        mock_ad_group_criterion_service.mutate_ad_group_criteria.assert_called_once()

        # Get the arguments passed to mutate_ad_group_criteria
        args, kwargs = mock_ad_group_criterion_service.mutate_ad_group_criteria.call_args
        
        self.assertEqual(kwargs["customer_id"], MOCK_CUSTOMER_ID)
        operations = kwargs["operations"]
        self.assertEqual(len(operations), 2)  # Gender and Age Range

        # --- Verify Gender Criterion Operation ---
        gender_operation = operations[0]
        created_gender_criterion = gender_operation.create
        self.assertEqual(created_gender_criterion.ad_group, expected_ad_group_rname)
        self.assertEqual(created_gender_criterion.gender.type_, GenderTypeEnum.MALE)
        # In the script, gender is positive targeting, so .negative should not be True
        # A non-existent attribute or one that is False would be fine.
        # We'll check it's not explicitly True. If it's not set, getattr will raise AttributeError.
        # If it's set to False, this check will pass.
        self.assertNotEqual(getattr(created_gender_criterion, 'negative', False), True)


        # --- Verify Age Range Criterion Operation (Negative) ---
        age_range_operation = operations[1]
        created_age_range_criterion = age_range_operation.create
        self.assertEqual(created_age_range_criterion.ad_group, expected_ad_group_rname)
        self.assertEqual(created_age_range_criterion.age_range.type_, AgeRangeTypeEnum.AGE_RANGE_18_24)
        self.assertTrue(created_age_range_criterion.negative)


if __name__ == "__main__":
    unittest.main()
