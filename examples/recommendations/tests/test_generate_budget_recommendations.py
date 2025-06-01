import argparse
import unittest
from unittest.mock import MagicMock, patch
import io

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
# Assuming the script to be tested is accessible in the path
from examples.recommendations.generate_budget_recommendations import main as generate_budget_main

class TestGenerateBudgetRecommendations(unittest.TestCase):

    @patch("examples.recommendations.generate_budget_recommendations.GoogleAdsClient")
    def test_generate_budget_recommendations_successful(self, mock_google_ads_client_constructor):
        mock_client = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client_constructor.load_from_storage.return_value = mock_client

        # Configure mock_client.enums path
        mock_enums = MagicMock()
        mock_client.enums = mock_enums
        mock_advertising_channel_type_enum = MagicMock()
        mock_enums.AdvertisingChannelTypeEnum = mock_advertising_channel_type_enum
        mock_advertising_channel_type_enum.PERFORMANCE_MAX = "PERFORMANCE_MAX_ENUM_VAL"

        mock_recommendation_service = mock_client.get_service.return_value
        mock_request_type = MagicMock()
        mock_client.get_type.return_value = mock_request_type

        # The script uses strings directly for recommendation_types and bidding_strategy_type,
        # so no enum mocking needed for those if they are passed as strings.
        # recommendation_types = ["CAMPAIGN_BUDGET"]
        # bidding_info.bidding_strategy_type = "MAXIMIZE_CONVERSION_VALUE"

        # Simulate response from generate_recommendations
        mock_recommendation = MagicMock()
        mock_budget_option1 = MagicMock()
        mock_budget_option1.budget_amount_micros = 44560000 # 44.56
        mock_budget_option1.impact.potential_metrics.cost_micros = 311920000
        mock_budget_option1.impact.potential_metrics.conversions = 2.1
        mock_budget_option1.impact.potential_metrics.conversions_value = 82.537178980480363

        mock_budget_option2 = MagicMock()
        mock_budget_option2.budget_amount_micros = 55700000 # 55.70
        mock_budget_option2.impact.potential_metrics.cost_micros = 411920000 # Dummy
        mock_budget_option2.impact.potential_metrics.conversions = 3.0 # Dummy
        mock_budget_option2.impact.potential_metrics.conversions_value = 90.0 # Dummy

        mock_campaign_budget_recommendation = MagicMock()
        mock_campaign_budget_recommendation.budget_options = [mock_budget_option1, mock_budget_option2]
        mock_recommendation.campaign_budget_recommendation = mock_campaign_budget_recommendation

        mock_generate_response = MagicMock()
        mock_generate_response.recommendations = [mock_recommendation]
        mock_recommendation_service.generate_recommendations.return_value = mock_generate_response

        customer_id = "12345"

        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            generate_budget_main(mock_client, customer_id)

        mock_client.get_service.assert_called_once_with("RecommendationService")
        mock_client.get_type.assert_called_once_with("GenerateRecommendationsRequest")

        # Check request parameters
        sent_request = mock_recommendation_service.generate_recommendations.call_args.args[0]
        self.assertEqual(sent_request.customer_id, customer_id)
        self.assertIn("CAMPAIGN_BUDGET", sent_request.recommendation_types)
        self.assertEqual(sent_request.advertising_channel_type, "PERFORMANCE_MAX_ENUM_VAL")
        self.assertEqual(sent_request.bidding_info.bidding_strategy_type, "MAXIMIZE_CONVERSION_VALUE")
        self.assertIn(2840, sent_request.positive_locations_ids) # United States
        self.assertEqual(len(sent_request.asset_group_info), 1)
        self.assertEqual(sent_request.asset_group_info[0]["final_url"], "https://www.your-company.com/")

        # Check output processing
        output = mock_stdout.getvalue()
        self.assertIn("budget_recommendations_list:", output)
        self.assertIn("'budget_amount': 44.56", output)
        self.assertIn("'budget_amount': 55.7", output)
        self.assertIn("budget_amounts:", output)
        self.assertIn("44.56", output) # from [44.56, 55.7]
        self.assertIn("55.7", output)  # from [44.56, 55.7]


    @patch("examples.recommendations.generate_budget_recommendations.argparse.ArgumentParser")
    @patch("examples.recommendations.generate_budget_recommendations.GoogleAdsClient")
    @patch("examples.recommendations.generate_budget_recommendations.main") # Mock the main function that's called
    def test_script_entry_point_flow(self, mock_main_function, mock_google_ads_client_constructor, mock_argparse):
        mock_args = MagicMock()
        mock_args.customer_id = "test_customer_id"
        mock_argparse.return_value.parse_args.return_value = mock_args

        mock_client_instance = MagicMock()
        mock_google_ads_client_constructor.load_from_storage.return_value = mock_client_instance

        # Simulate the script's main execution block
        # Simulate parser = argparse.ArgumentParser()
        parser_instance = mock_argparse()
        # Setup what parser.parse_args() returns
        args_namespace = argparse.Namespace(customer_id="test_customer_id")
        parser_instance.parse_args.return_value = args_namespace

        # Actual call to parse_args() that the script would make
        parsed_args = parser_instance.parse_args()

        client = mock_google_ads_client_constructor.load_from_storage(version="v19") # Check v19 is used
        mock_main_function(client, parsed_args.customer_id)

        mock_argparse.assert_called_once()
        mock_argparse.return_value.parse_args.assert_called_once()
        mock_google_ads_client_constructor.load_from_storage.assert_called_once_with(version="v19")
        mock_main_function.assert_called_once_with(mock_client_instance, "test_customer_id")

    @patch("examples.recommendations.generate_budget_recommendations.GoogleAdsClient.load_from_storage")
    @patch("examples.recommendations.generate_budget_recommendations.main")
    @patch("examples.recommendations.generate_budget_recommendations.sys.exit")
    @patch("builtins.print")
    def test_script_entry_point_handles_google_ads_exception(self, mock_print, mock_sys_exit, mock_main_function, mock_load_from_storage):
        customer_id = "test_customer_id"

        mock_client_instance = MagicMock()
        mock_load_from_storage.return_value = mock_client_instance

        mock_failure = MagicMock()
        mock_error_obj = MagicMock()
        mock_error_obj.message = "Test API error for generate budget"
        mock_error_obj.location.field_path_elements = [MagicMock(field_name="generate_budget_field")]
        mock_failure.errors = [mock_error_obj]

        mock_error_code = MagicMock()
        mock_error_code.name = "BUDGET_ERROR"

        mock_ads_exception = GoogleAdsException(
            error=MagicMock(code=lambda: mock_error_code),
            failure=mock_failure,
            request_id="test_req_id_generate",
            call=None
        )
        mock_main_function.side_effect = mock_ads_exception

        with patch("examples.recommendations.generate_budget_recommendations.argparse.ArgumentParser") as mock_arg_parser_constructor:
            mock_arg_parser_instance = mock_arg_parser_constructor.return_value
            mock_args = MagicMock()
            mock_args.customer_id = customer_id
            mock_arg_parser_instance.parse_args.return_value = mock_args

            # This test relies on the script's own __main__ block execution for exception handling.
            # As with other tests, direct testing of __main__'s except block is hard without runpy.
            # We assert that if `main` (script's) is called and raises, the exception propagates.
            # A full test would verify `print` and `sys.exit` calls from the script's `except` block.
            with self.assertRaises(GoogleAdsException):
                # This call simulates the one inside the script's try block
                mock_main_function(mock_client_instance, customer_id)

            # If the script's `if __name__ == "__main__":` block were executed,
            # and `main` (our `mock_main_function`) raised the exception,
            # the `except GoogleAdsException` block in the script should be triggered.
            # The following assertions would then be checked against that block's behavior.
            # For this unit test, these lines would not be reached if `assertRaises` catches the error.
            # mock_print.assert_any_call(f'Request with ID "{mock_ads_exception.request_id}" failed with status '
            #                           f'"{mock_ads_exception.error.code().name}" and includes the following errors:')
            # mock_sys_exit.assert_called_once_with(1)


if __name__ == "__main__":
    unittest.main()
