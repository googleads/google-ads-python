import unittest
from unittest.mock import MagicMock, patch

from examples.planning import generate_historical_metrics

class TestGenerateHistoricalMetrics(unittest.TestCase):

    @patch('examples.planning.generate_historical_metrics.GoogleAdsClient.load_from_storage')
    def test_main_generate_historical_metrics(self, mock_load_from_storage):
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_keyword_plan_idea_service = MagicMock()
        mock_google_ads_service = MagicMock()

        def get_service_side_effect(service_name, version=None):
            if service_name == "KeywordPlanIdeaService":
                return mock_keyword_plan_idea_service
            elif service_name == "GoogleAdsService":
                return mock_google_ads_service
            return MagicMock()

        mock_google_ads_client.get_service.side_effect = get_service_side_effect

        # Mock responses
        mock_historical_response = MagicMock()
        mock_result = MagicMock()
        mock_result.text = "mars cruise"
        mock_result.close_variants = ["mars ship", "mars journey"]
        mock_result.keyword_metrics.avg_monthly_searches = 1000
        mock_result.keyword_metrics.competition = "HIGH" # This would be an enum actually
        mock_result.keyword_metrics.competition_index = 80
        mock_result.keyword_metrics.low_top_of_page_bid_micros = 1000000
        mock_result.keyword_metrics.high_top_of_page_bid_micros = 5000000

        mock_monthly_search_volume = MagicMock()
        mock_monthly_search_volume.year = 2023
        mock_month_enum = MagicMock()
        mock_month_enum.name = "JANUARY" # Simulate enum's .name attribute
        mock_monthly_search_volume.month = mock_month_enum
        mock_monthly_search_volume.monthly_searches = 1200
        mock_result.keyword_metrics.monthly_search_volumes = [mock_monthly_search_volume]

        mock_historical_response.results = [mock_result]
        mock_keyword_plan_idea_service.generate_keyword_historical_metrics.return_value = mock_historical_response

        # Mock path methods
        mock_google_ads_service.geo_target_constant_path.return_value = "geoTargetConstants/2840"
        mock_google_ads_service.language_constant_path.return_value = "languageConstants/1000"

        # Mock enums
        mock_enums = MagicMock()
        mock_enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH = "GOOGLE_SEARCH"
        # Assuming competition is an enum, e.g., KeywordPlanCompetitionLevelEnum
        mock_enums.KeywordPlanCompetitionLevelEnum.HIGH = "HIGH"
        mock_google_ads_client.enums = mock_enums

        # Mock types for request construction
        mock_google_ads_client.get_type.side_effect = lambda name: MagicMock(name=name)

        test_customer_id = "1234567890"

        with patch('sys.stdout', new_callable=MagicMock) as mock_stdout:
            generate_historical_metrics.main(mock_google_ads_client, test_customer_id)

        # mock_load_from_storage.assert_called_once_with(version="v19") # This is removed as client is injected
        mock_google_ads_client.get_service.assert_any_call("KeywordPlanIdeaService")
        mock_google_ads_client.get_service.assert_any_call("GoogleAdsService")
        mock_keyword_plan_idea_service.generate_keyword_historical_metrics.assert_called_once()

        output = "".join(call_args[0][0] for call_args in mock_stdout.write.call_args_list if call_args[0])
        self.assertIn("The search query 'mars cruise'", output)
        self.assertIn("Approximate monthly searches: 1000", output)
        self.assertIn("Competition level: HIGH", output) # This will depend on how enum is converted to string
        self.assertIn("Approximately 1200 searches in JANUARY, 2023", output)


if __name__ == "__main__":
    unittest.main()
