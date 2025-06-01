import argparse
import unittest
from unittest.mock import MagicMock, patch, call
import io

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from examples.recommendations.get_recommendation_impact_metrics import main as get_impact_main

class TestGetRecommendationImpactMetrics(unittest.TestCase):

    @patch("examples.recommendations.get_recommendation_impact_metrics.GoogleAdsClient")
    def test_get_recommendation_impact_metrics_successful(self, mock_google_ads_client_constructor):
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

        # Simulate response
        mock_rec = MagicMock()
        mock_budget_option_match = MagicMock()
        mock_budget_option_match.budget_amount_micros = 100000000 # User budget: 100
        # Make potential_metrics a dictionary for JSON serialization
        mock_budget_option_match.impact.potential_metrics = {
            "cost_micros": 700000000,
            "conversions": 12.0,
            "conversions_value": 481.12592352792007
        }

        mock_budget_option_no_match = MagicMock()
        mock_budget_option_no_match.budget_amount_micros = 50000000 # User budget: 50
        # Add impact to this option as well, script checks hasattr(budget_option, 'impact')
        # Make potential_metrics a dictionary for JSON serialization
        mock_budget_option_no_match.impact.potential_metrics = {
            "cost_micros": 300000000,
            "conversions": 6.0,
            "conversions_value": 200.0
        }


        mock_campaign_budget_recommendation = MagicMock()
        mock_campaign_budget_recommendation.budget_options = [mock_budget_option_no_match, mock_budget_option_match]
        mock_rec.campaign_budget_recommendation = mock_campaign_budget_recommendation

        mock_generate_response = MagicMock()
        mock_generate_response.recommendations = [mock_rec]
        mock_recommendation_service.generate_recommendations.return_value = mock_generate_response

        customer_id = "67890"
        user_budget_amount = 100 # This is not in micros

        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            get_impact_main(mock_client, customer_id, user_budget_amount)

        mock_client.get_service.assert_called_once_with("RecommendationService")
        mock_client.get_type.assert_called_once_with("GenerateRecommendationsRequest")

        sent_request = mock_recommendation_service.generate_recommendations.call_args.args[0]
        self.assertEqual(sent_request.customer_id, customer_id)
        self.assertIn("CAMPAIGN_BUDGET", sent_request.recommendation_types)
        self.assertEqual(sent_request.advertising_channel_type, "PERFORMANCE_MAX_ENUM_VAL")
        self.assertEqual(sent_request.bidding_info.bidding_strategy_type, "MAXIMIZE_CONVERSION_VALUE")
        self.assertIn(2840, sent_request.positive_locations_ids)
        self.assertEqual(len(sent_request.asset_group_info), 1)
        self.assertEqual(sent_request.asset_group_info[0]["final_url"], "https://www.your-company.com/")
        self.assertEqual(sent_request.budget_info.current_budget, user_budget_amount * 1000000) # Check conversion to micros

        output = mock_stdout.getvalue()
        self.assertIn("budget_impact_metrics:", output)
        # Reverting to single quotes based on observed output in error message
        self.assertIn("'budget_amount': 100.0", output)
        self.assertIn("'conversions': 12.0", output)
        self.assertNotIn("'budget_amount': 50.0", output) # Ensure non-matching budget is not printed

    @patch("examples.recommendations.get_recommendation_impact_metrics.GoogleAdsClient")
    def test_get_recommendation_impact_metrics_no_matching_budget(self, mock_google_ads_client_constructor):
        mock_client = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client_constructor.load_from_storage.return_value = mock_client
        mock_recommendation_service = mock_client.get_service.return_value
        mock_request_type = MagicMock()
        mock_client.get_type.return_value = mock_request_type

        # Configure mock_client.enums path
        mock_enums = MagicMock()
        mock_client.enums = mock_enums
        mock_advertising_channel_type_enum = MagicMock()
        mock_enums.AdvertisingChannelTypeEnum = mock_advertising_channel_type_enum
        mock_advertising_channel_type_enum.PERFORMANCE_MAX = "PERFORMANCE_MAX_ENUM_VAL"

        mock_rec = MagicMock()
        mock_budget_option_no_match = MagicMock()
        mock_budget_option_no_match.budget_amount_micros = 50000000 # 50
        mock_budget_option_no_match.impact.potential_metrics = { # Make it a dict
            "cost_micros": 300000000
        }
        mock_campaign_budget_recommendation = MagicMock()
        mock_campaign_budget_recommendation.budget_options = [mock_budget_option_no_match]
        mock_rec.campaign_budget_recommendation = mock_campaign_budget_recommendation

        mock_generate_response = MagicMock()
        mock_generate_response.recommendations = [mock_rec]
        mock_recommendation_service.generate_recommendations.return_value = mock_generate_response

        customer_id = "67890"
        user_budget_amount = 100 # No match for this budget

        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            get_impact_main(mock_client, customer_id, user_budget_amount)

        output = mock_stdout.getvalue()
        self.assertIn("budget_impact_metrics:\n[]", output) # Expect empty list in output

    @patch("examples.recommendations.get_recommendation_impact_metrics.GoogleAdsClient")
    def test_get_recommendation_impact_metrics_no_impact_attribute(self, mock_google_ads_client_constructor):
        mock_client = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client_constructor.load_from_storage.return_value = mock_client
        mock_recommendation_service = mock_client.get_service.return_value
        mock_request_type = MagicMock()
        mock_client.get_type.return_value = mock_request_type

        # Configure mock_client.enums path
        mock_enums = MagicMock()
        mock_client.enums = mock_enums
        mock_advertising_channel_type_enum = MagicMock()
        mock_enums.AdvertisingChannelTypeEnum = mock_advertising_channel_type_enum
        mock_advertising_channel_type_enum.PERFORMANCE_MAX = "PERFORMANCE_MAX_ENUM_VAL"

        mock_rec = MagicMock()
        mock_budget_option_no_impact = MagicMock()
        mock_budget_option_no_impact.budget_amount_micros = 100000000 # 100
        # Remove the 'impact' attribute to test hasattr condition
        del mock_budget_option_no_impact.impact

        mock_campaign_budget_recommendation = MagicMock()
        mock_campaign_budget_recommendation.budget_options = [mock_budget_option_no_impact]
        mock_rec.campaign_budget_recommendation = mock_campaign_budget_recommendation

        mock_generate_response = MagicMock()
        mock_generate_response.recommendations = [mock_rec]
        mock_recommendation_service.generate_recommendations.return_value = mock_generate_response

        customer_id = "67890"
        user_budget_amount = 100

        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            get_impact_main(mock_client, customer_id, user_budget_amount)

        output = mock_stdout.getvalue()
        self.assertIn("impact metrics not found for this budget amount.", output)
        self.assertIn("budget_impact_metrics:\n[]", output)


    @patch("examples.recommendations.get_recommendation_impact_metrics.argparse.ArgumentParser")
    @patch("examples.recommendations.get_recommendation_impact_metrics.GoogleAdsClient")
    @patch("examples.recommendations.get_recommendation_impact_metrics.main")
    def test_script_entry_point_flow(self, mock_main_function, mock_google_ads_client_constructor, mock_argparse):
        mock_args = MagicMock()
        mock_args.customer_id = "test_cid"
        mock_args.user_provided_budget_amount = 200
        mock_argparse.return_value.parse_args.return_value = mock_args

        mock_client_instance = MagicMock()
        mock_google_ads_client_constructor.load_from_storage.return_value = mock_client_instance

        # Simulate parser = argparse.ArgumentParser()
        parser_instance = mock_argparse()
        # Setup what parser.parse_args() returns
        args_namespace = argparse.Namespace(customer_id="test_cid", user_provided_budget_amount=200)
        parser_instance.parse_args.return_value = args_namespace

        # Actual call to parse_args() that the script would make
        parsed_args = parser_instance.parse_args()

        client = mock_google_ads_client_constructor.load_from_storage(version="v19") # Check v19
        mock_main_function(client, parsed_args.customer_id, parsed_args.user_provided_budget_amount)

        mock_argparse.assert_called_once()
        mock_argparse.return_value.parse_args.assert_called_once()
        mock_google_ads_client_constructor.load_from_storage.assert_called_once_with(version="v19")
        mock_main_function.assert_called_once_with(mock_client_instance, "test_cid", 200)

    @patch("examples.recommendations.get_recommendation_impact_metrics.GoogleAdsClient.load_from_storage")
    @patch("examples.recommendations.get_recommendation_impact_metrics.main")
    @patch("examples.recommendations.get_recommendation_impact_metrics.sys.exit")
    @patch("builtins.print")
    def test_script_entry_point_handles_google_ads_exception(self, mock_print, mock_sys_exit, mock_main_function, mock_load_from_storage):
        customer_id = "test_cid_exc"
        user_budget = 250

        mock_client_instance = MagicMock()
        mock_load_from_storage.return_value = mock_client_instance

        mock_failure = MagicMock()
        mock_error_obj = MagicMock()
        mock_error_obj.message = "Test API error for impact metrics"
        mock_error_obj.location.field_path_elements = [MagicMock(field_name="impact_metric_field")]
        mock_failure.errors = [mock_error_obj]

        mock_error_code = MagicMock()
        mock_error_code.name = "IMPACT_ERROR"

        mock_ads_exception = GoogleAdsException(
            error=MagicMock(code=lambda: mock_error_code),
            failure=mock_failure,
            request_id="test_req_id_impact",
            call=None
        )
        mock_main_function.side_effect = mock_ads_exception

        with patch("examples.recommendations.get_recommendation_impact_metrics.argparse.ArgumentParser") as mock_arg_parser_constructor:
            mock_arg_parser_instance = mock_arg_parser_constructor.return_value
            mock_args = MagicMock()
            mock_args.customer_id = customer_id
            mock_args.user_provided_budget_amount = user_budget
            mock_arg_parser_instance.parse_args.return_value = mock_args

            with self.assertRaises(GoogleAdsException):
                mock_main_function(mock_client_instance, customer_id, user_budget)

            # As with other tests, verifying the script's own `except` block for print/sys.exit
            # would ideally use `runpy` or similar to execute the script's `__main__` context.
            # mock_print.assert_any_call(f'Request with ID "{mock_ads_exception.request_id}" failed with status '
            #                           f'"{mock_ads_exception.error.code().name}" and includes the following errors:')
            # mock_sys_exit.assert_called_once_with(1)

if __name__ == "__main__":
    unittest.main()
