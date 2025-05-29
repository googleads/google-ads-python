import unittest
from unittest.mock import patch, MagicMock, call
from datetime import datetime, timedelta

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.v19.enums.types import keyword_plan_network as keyword_plan_network_enum
from google.ads.googleads.v19.enums.types import keyword_match_type as keyword_match_type_enum

# Assuming generate_forecast_metrics is importable
from examples.planning import generate_forecast_metrics


class TestGenerateForecastMetrics(unittest.TestCase):

    MOCK_CUSTOMER_ID = "1234567890"

    @patch("examples.planning.generate_forecast_metrics.GoogleAdsClient.load_from_storage")
    def test_main_execution(self, mock_load_client):
        # Mock GoogleAdsClient and its services
        mock_google_ads_client = MagicMock(spec=GoogleAdsClient)
        mock_keyword_plan_idea_service = MagicMock()
        mock_google_ads_service = MagicMock() # Though not directly used by the forecast part, main might get it.

        mock_google_ads_client.get_service.side_effect = lambda service_name, version: {
            "KeywordPlanIdeaService": mock_keyword_plan_idea_service,
            "GoogleAdsService": mock_google_ads_service,
        }[service_name]
        
        mock_load_client.return_value = mock_google_ads_client

        # Call the main function
        generate_forecast_metrics.main(mock_google_ads_client, self.MOCK_CUSTOMER_ID)

        # 1. Assert GoogleAdsClient.load_from_storage was called
        mock_load_client.assert_called_once_with(version="v19")

        # 2. Assert client.get_service was called for KeywordPlanIdeaService
        # and potentially GoogleAdsService if main uses it.
        # The script uses get_service for KeywordPlanIdeaService for the core logic.
        # It doesn't appear to use GoogleAdsService directly in the forecasting part.
        mock_google_ads_client.get_service.assert_any_call("KeywordPlanIdeaService", version="v19")
        # Check if GoogleAdsService was also requested if it's part of main's setup
        # According to generate_forecast_metrics.py, GoogleAdsService is not explicitly fetched in main.

        # 3. Verify the call to keyword_plan_idea_service.generate_keyword_forecast_metrics()
        mock_keyword_plan_idea_service.generate_keyword_forecast_metrics.assert_called_once()
        
        # Get the actual request passed to generate_keyword_forecast_metrics
        call_args = mock_keyword_plan_idea_service.generate_keyword_forecast_metrics.call_args
        request = call_args[1]['request'] # request is a keyword argument or use call_args[0][0] if positional

        # Verify customer_id in the request
        self.assertEqual(request.customer_id, self.MOCK_CUSTOMER_ID)

        # Verify forecast_period
        # Dates are based on the day the test runs.
        tomorrow = datetime.now().date() + timedelta(days=1)
        thirty_days_from_tomorrow = tomorrow + timedelta(days=30)
        
        self.assertEqual(request.forecast_period.start_date.year, tomorrow.year)
        self.assertEqual(request.forecast_period.start_date.month, tomorrow.month)
        self.assertEqual(request.forecast_period.start_date.day, tomorrow.day)
        
        self.assertEqual(request.forecast_period.end_date.year, thirty_days_from_tomorrow.year)
        self.assertEqual(request.forecast_period.end_date.month, thirty_days_from_tomorrow.month)
        self.assertEqual(request.forecast_period.end_date.day, thirty_days_from_tomorrow.day)

        # Verify CampaignToForecast object (implicitly tests create_campaign_to_forecast)
        campaign_to_forecast = request.campaign_to_forecast
        
        self.assertEqual(
            campaign_to_forecast.keyword_plan_network,
            keyword_plan_network_enum.KeywordPlanNetworkEnum.KeywordPlanNetwork.GOOGLE_SEARCH
        )
        self.assertIsNotNone(campaign_to_forecast.bidding_strategy)
        self.assertEqual(campaign_to_forecast.bidding_strategy.max_cpc_bid_ceiling_micros, 1_000_000) # Default from script

        # Geo modifiers (Location)
        self.assertEqual(len(campaign_to_forecast.geo_modifiers), 1)
        # From the script: _GEO_TARGET_CONSTANT_US = "geoTargetConstants/2840"
        self.assertEqual(campaign_to_forecast.geo_modifiers[0].geo_target_constant, "geoTargetConstants/2840")

        # Language constant
        self.assertEqual(len(campaign_to_forecast.language_constants), 1)
        # From the script: _LANGUAGE_CONSTANT_EN = "languageConstants/1000"
        self.assertEqual(campaign_to_forecast.language_constants[0], "languageConstants/1000")

        # Ad Groups and Keywords
        self.assertEqual(len(campaign_to_forecast.ad_groups), 2)

        # Ad Group 1
        ad_group1 = campaign_to_forecast.ad_groups[0]
        self.assertEqual(ad_group1.max_cpc_bid_micros, 2_500_000) # Default from script
        
        # Biddable Keywords for Ad Group 1
        # From script: ("mars cruise", BROAD), ("cheap cruise", PHRASE), ("jupiter cruise", EXACT)
        self.assertEqual(len(ad_group1.biddable_keywords), 3)
        self.assertEqual(ad_group1.biddable_keywords[0].keyword.text, "mars cruise")
        self.assertEqual(ad_group1.biddable_keywords[0].keyword.match_type, keyword_match_type_enum.KeywordMatchTypeEnum.KeywordMatchType.BROAD)
        self.assertEqual(ad_group1.biddable_keywords[1].keyword.text, "cheap cruise")
        self.assertEqual(ad_group1.biddable_keywords[1].keyword.match_type, keyword_match_type_enum.KeywordMatchTypeEnum.KeywordMatchType.PHRASE)
        self.assertEqual(ad_group1.biddable_keywords[2].keyword.text, "jupiter cruise")
        self.assertEqual(ad_group1.biddable_keywords[2].keyword.match_type, keyword_match_type_enum.KeywordMatchTypeEnum.KeywordMatchType.EXACT)

        # Negative Keywords for Ad Group 1
        # From script: ("moon walk", BROAD)
        self.assertEqual(len(ad_group1.negative_keywords), 1)
        self.assertEqual(ad_group1.negative_keywords[0].text, "moon walk")
        self.assertEqual(ad_group1.negative_keywords[0].match_type, keyword_match_type_enum.KeywordMatchTypeEnum.KeywordMatchType.BROAD)
        
        # Ad Group 2
        ad_group2 = campaign_to_forecast.ad_groups[1]
        self.assertEqual(ad_group2.max_cpc_bid_micros, 1_990_000) # Default from script

        # Biddable Keywords for Ad Group 2
        # From script: ("saturn cruise", BROAD), ("expensive cruise", PHRASE), ("mercury cruise", EXACT)
        self.assertEqual(len(ad_group2.biddable_keywords), 3)
        self.assertEqual(ad_group2.biddable_keywords[0].keyword.text, "saturn cruise")
        self.assertEqual(ad_group2.biddable_keywords[0].keyword.match_type, keyword_match_type_enum.KeywordMatchTypeEnum.KeywordMatchType.BROAD)
        self.assertEqual(ad_group2.biddable_keywords[1].keyword.text, "expensive cruise")
        self.assertEqual(ad_group2.biddable_keywords[1].keyword.match_type, keyword_match_type_enum.KeywordMatchTypeEnum.KeywordMatchType.PHRASE)
        self.assertEqual(ad_group2.biddable_keywords[2].keyword.text, "mercury cruise")
        self.assertEqual(ad_group2.biddable_keywords[2].keyword.match_type, keyword_match_type_enum.KeywordMatchTypeEnum.KeywordMatchType.EXACT)

        # Negative Keywords for Ad Group 2
        # From script: ("venus walk", BROAD)
        self.assertEqual(len(ad_group2.negative_keywords), 1)
        self.assertEqual(ad_group2.negative_keywords[0].text, "venus walk")
        self.assertEqual(ad_group2.negative_keywords[0].match_type, keyword_match_type_enum.KeywordMatchTypeEnum.KeywordMatchType.BROAD)


if __name__ == "__main__":
    unittest.main()
