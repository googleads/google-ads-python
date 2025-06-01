import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta

from examples.planning import generate_forecast_metrics

class TestGenerateForecastMetrics(unittest.TestCase):

    @patch('examples.planning.generate_forecast_metrics.GoogleAdsClient.load_from_storage')
    def test_main_generate_forecast_metrics(self, mock_load_from_storage):
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_keyword_plan_idea_service = MagicMock()
        mock_google_ads_service = MagicMock()

        # Configure get_service to return the correct mock based on the service name
        def get_service_side_effect(service_name, version=None):
            if service_name == "KeywordPlanIdeaService":
                return mock_keyword_plan_idea_service
            elif service_name == "GoogleAdsService":
                return mock_google_ads_service
            return MagicMock() # Default mock for other services if any

        mock_google_ads_client.get_service.side_effect = get_service_side_effect

        # Mock responses
        mock_forecast_response = MagicMock()
        mock_forecast_response.campaign_forecast_metrics.clicks = 100.0
        mock_forecast_response.campaign_forecast_metrics.impressions = 1000.0
        mock_forecast_response.campaign_forecast_metrics.average_cpc_micros = 1230000
        mock_keyword_plan_idea_service.generate_keyword_forecast_metrics.return_value = mock_forecast_response

        # Mock path methods
        mock_google_ads_service.geo_target_constant_path.return_value = "geoTargetConstants/2840"
        mock_google_ads_service.language_constant_path.return_value = "languageConstants/1000"

        # Mock enums (adjust as per actual usage in the script)
        mock_enums = MagicMock()
        mock_enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH = "GOOGLE_SEARCH"
        mock_enums.KeywordMatchTypeEnum.BROAD = "BROAD"
        mock_enums.KeywordMatchTypeEnum.PHRASE = "PHRASE"
        mock_enums.KeywordMatchTypeEnum.EXACT = "EXACT"
        mock_google_ads_client.enums = mock_enums

        # Mock types for request construction
        mock_google_ads_client.get_type.side_effect = lambda name: MagicMock(name=name)


        test_customer_id = "1234567890"

        with patch('sys.stdout', new_callable=MagicMock) as mock_stdout:
            generate_forecast_metrics.main(mock_google_ads_client, test_customer_id)

        # mock_load_from_storage.assert_called_once_with(version="v19") # This is removed as client is injected
        mock_google_ads_client.get_service.assert_any_call("KeywordPlanIdeaService")
        mock_google_ads_client.get_service.assert_any_call("GoogleAdsService")
        mock_keyword_plan_idea_service.generate_keyword_forecast_metrics.assert_called_once()

        # Check if the output contains expected metrics
        output = "".join(call_args[0][0] for call_args in mock_stdout.write.call_args_list if call_args[0])
        self.assertIn("Estimated daily clicks: 100.0", output)
        self.assertIn("Estimated daily impressions: 1000.0", output)
        self.assertIn("Estimated daily average CPC: 1230000", output)

if __name__ == "__main__":
    unittest.main()
