import unittest
from unittest.mock import Mock, patch, call
import argparse
import sys

# Assuming the script is in examples.targeting relative to the project root
try:
    from examples.targeting import add_demographic_targeting_criteria
except ImportError:
    import add_demographic_targeting_criteria

_TEST_CUSTOMER_ID = "1234567890"
_TEST_AD_GROUP_ID = "9876543210"
_DUMMY_AD_GROUP_RESOURCE_NAME = f"customers/{_TEST_CUSTOMER_ID}/adGroups/{_TEST_AD_GROUP_ID}"

# Enum integer values (based on Google Ads API documentation)
_GENDER_TYPE_MALE = 10
_AGE_RANGE_TYPE_18_24 = 503001


class TestAddDemographicTargetingCriteria(unittest.TestCase):
    @patch("examples.targeting.add_demographic_targeting_criteria.GoogleAdsClient.load_from_storage")
    def setUp(self, mock_load_from_storage):
        self.mock_google_ads_client = Mock()
        mock_load_from_storage.return_value = self.mock_google_ads_client

        # Mock services
        self.mock_ad_group_service = Mock()
        self.mock_ad_group_criterion_service = Mock()

        # Configure get_service to return the right mock for each service name
        def get_service_side_effect(service_name, version=None):
            if service_name == "AdGroupService":
                return self.mock_ad_group_service
            elif service_name == "AdGroupCriterionService":
                return self.mock_ad_group_criterion_service
            return Mock() # Default mock for other services
        self.mock_google_ads_client.get_service.side_effect = get_service_side_effect

        # Mock ad_group_path
        self.mock_ad_group_service.ad_group_path.return_value = _DUMMY_AD_GROUP_RESOURCE_NAME

        # Mock enums
        mock_gender_type_enum = Mock()
        mock_gender_type_enum.MALE = _GENDER_TYPE_MALE
        self.mock_google_ads_client.enums.GenderTypeEnum = mock_gender_type_enum

        mock_age_range_type_enum = Mock()
        mock_age_range_type_enum.AGE_RANGE_18_24 = _AGE_RANGE_TYPE_18_24
        self.mock_google_ads_client.enums.AgeRangeTypeEnum = mock_age_range_type_enum

        # Mock AdGroupCriterionOperation creation (client.get_type)
        # The script calls this twice, expecting two distinct operation objects.
        self.mock_gender_op = Mock(spec=["create"])
        self.mock_age_range_op = Mock(spec=["create"])

        get_type_side_effects = [self.mock_gender_op, self.mock_age_range_op]
        self.mock_google_ads_client.get_type.side_effect = lambda type_name: (
            get_type_side_effects.pop(0) if type_name == "AdGroupCriterionOperation"
            and get_type_side_effects else Mock()
        )

        # Mock response for mutate_ad_group_criteria
        self.mock_mutate_response = Mock()
        self.mock_mutate_response.results = [Mock(resource_name="gender_result_rn"), Mock(resource_name="age_range_result_rn")]
        self.mock_ad_group_criterion_service.mutate_ad_group_criteria.return_value = self.mock_mutate_response

    @patch("builtins.print") # Patch print for this test method
    def test_main_logic(self, mock_print): # Add mock_print argument
        """Tests the core logic of the main function."""
        add_demographic_targeting_criteria.main(
            self.mock_google_ads_client, _TEST_CUSTOMER_ID, _TEST_AD_GROUP_ID
        )

        # Verify AdGroupService.ad_group_path was called
        self.mock_ad_group_service.ad_group_path.assert_called_once_with(
            _TEST_CUSTOMER_ID, _TEST_AD_GROUP_ID
        )

        # Verify client.get_type("AdGroupCriterionOperation") was called twice
        self.assertEqual(self.mock_google_ads_client.get_type.call_count, 2)
        self.mock_google_ads_client.get_type.assert_any_call("AdGroupCriterionOperation")

        # Verify gender criterion operation
        self.assertEqual(self.mock_gender_op.create.ad_group, _DUMMY_AD_GROUP_RESOURCE_NAME)
        self.assertEqual(self.mock_gender_op.create.gender.type_, _GENDER_TYPE_MALE)
        # Positive criteria don't set .negative=True, so it's either False or not set
        # Depending on how Mock handles attribute access vs explicit setting,
        # we can check it's not True, or that it's explicitly False if the script sets it.
        # The script does NOT set gender_ad_group_criterion.negative.
        # A default Mock attribute will raise AttributeError if not set, unless spec'd.
        # For now, let's assume if it's not set, it's effectively false for the API.
        # We can also check it wasn't set to True:
        self.assertNotEqual(self.mock_gender_op.create.negative, True)


        # Verify age range criterion operation
        self.assertEqual(self.mock_age_range_op.create.ad_group, _DUMMY_AD_GROUP_RESOURCE_NAME)
        self.assertEqual(self.mock_age_range_op.create.negative, True)
        self.assertEqual(self.mock_age_range_op.create.age_range.type_, _AGE_RANGE_TYPE_18_24)

        # Verify mutate_ad_group_criteria call
        self.mock_ad_group_criterion_service.mutate_ad_group_criteria.assert_called_once_with(
            customer_id=_TEST_CUSTOMER_ID,
            operations=[self.mock_gender_op, self.mock_age_range_op],
        )

        # Verify print output
        # The script prints "Created keyword {}." for each result.
        # self.mock_mutate_response.results has two items.
        expected_print_calls = [
            call("Created keyword gender_result_rn."),
            call("Created keyword age_range_result_rn."),
        ]
        mock_print.assert_has_calls(expected_print_calls, any_order=False) # Order matters here

    @patch("examples.targeting.add_demographic_targeting_criteria.argparse.ArgumentParser")
    @patch("examples.targeting.add_demographic_targeting_criteria.GoogleAdsClient.load_from_storage")
    @patch("examples.targeting.add_demographic_targeting_criteria.main")
    def test_main_execution_path(
        self, mock_main_function, mock_load_from_storage, mock_argument_parser
    ):
        """Tests the script's entry point (__name__ == '__main__')."""
        mock_parser_instance = Mock()
        mock_parser_instance.parse_args.return_value = argparse.Namespace(
            customer_id=_TEST_CUSTOMER_ID,
            ad_group_id=_TEST_AD_GROUP_ID,
            google_ads_config_path=None
        )
        mock_argument_parser.return_value = mock_parser_instance

        mock_client_instance_main = Mock()
        mock_load_from_storage.return_value = mock_client_instance_main

        # Configure mock_client_instance_main like self.mock_google_ads_client in setUp
        # to allow the real 'main' to run without TypeErrors if runpy executes it.
        mock_main_ad_group_service = Mock()
        mock_main_ad_group_criterion_service = Mock()

        def main_get_service_side_effect(service_name, version=None):
            if service_name == "AdGroupService":
                return mock_main_ad_group_service
            elif service_name == "AdGroupCriterionService":
                return mock_main_ad_group_criterion_service
            return Mock()
        mock_client_instance_main.get_service.side_effect = main_get_service_side_effect

        mock_main_ad_group_service.ad_group_path.return_value = _DUMMY_AD_GROUP_RESOURCE_NAME

        mock_main_gender_type_enum = Mock()
        mock_main_gender_type_enum.MALE = _GENDER_TYPE_MALE
        mock_client_instance_main.enums.GenderTypeEnum = mock_main_gender_type_enum

        mock_main_age_range_type_enum = Mock()
        mock_main_age_range_type_enum.AGE_RANGE_18_24 = _AGE_RANGE_TYPE_18_24
        mock_client_instance_main.enums.AgeRangeTypeEnum = mock_main_age_range_type_enum

        mock_main_gender_op = Mock(spec=["create"])
        mock_main_age_range_op = Mock(spec=["create"])
        main_get_type_side_effects = [mock_main_gender_op, mock_main_age_range_op]
        mock_client_instance_main.get_type.side_effect = lambda type_name: (
            main_get_type_side_effects.pop(0) if type_name == "AdGroupCriterionOperation"
            and main_get_type_side_effects else Mock()
        )

        mock_main_mutate_response = Mock()
        mock_main_mutate_response.results = [Mock(), Mock()] # For len() and iteration
        mock_main_ad_group_criterion_service.mutate_ad_group_criteria.return_value = mock_main_mutate_response

        # Execute the script's __main__ block
        import runpy
        original_argv = list(sys.argv)
        try:
            sys.argv = [
                "add_demographic_targeting_criteria.py",
                "--customer_id", _TEST_CUSTOMER_ID,
                "--ad_group_id", _TEST_AD_GROUP_ID,
            ]
            runpy.run_module("examples.targeting.add_demographic_targeting_criteria", run_name="__main__")
        finally:
            sys.argv = original_argv

        mock_main_function.assert_called_once_with(
            mock_client_instance_main, _TEST_CUSTOMER_ID, _TEST_AD_GROUP_ID
        )
        mock_argument_parser.assert_called_once()
        mock_parser_instance.parse_args.assert_called_once()

if __name__ == "__main__":
    unittest.main()
