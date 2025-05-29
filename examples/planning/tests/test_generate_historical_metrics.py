import unittest
from unittest.mock import patch, MagicMock

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.v19.enums.types import keyword_plan_network as keyword_plan_network_enum

# Assuming generate_historical_metrics is importable
from examples.planning import generate_historical_metrics

# Constants from the script (generate_historical_metrics.py) for verification
# These would ideally be imported if they were true constants,
# but for testing, we can redefine them or ensure they match.
_KEYWORDS = ["mars cruise", "cheap cruise", "jupiter cruise"]
_GEO_TARGET_CONSTANT_US = "geoTargetConstants/2840"
_LANGUAGE_CONSTANT_EN = "languageConstants/1000"
_KEYWORD_PLAN_NETWORK = (
    keyword_plan_network_enum.KeywordPlanNetworkEnum.KeywordPlanNetwork.GOOGLE_SEARCH
)


class TestGenerateHistoricalMetrics(unittest.TestCase):

    MOCK_CUSTOMER_ID = "9876543210"

    @patch("examples.planning.generate_historical_metrics.GoogleAdsClient.load_from_storage")
    def test_main_execution(self, mock_load_client):
        # Mock GoogleAdsClient and its services
        mock_google_ads_client = MagicMock(spec=GoogleAdsClient)
        mock_keyword_plan_idea_service = MagicMock()
        # The script also gets GoogleAdsService, so we should mock it too.
        mock_google_ads_service = MagicMock()

        # Configure get_service mock to return the correct service mock based on name
        def get_service_side_effect(service_name, version="v19"):
            if service_name == "KeywordPlanIdeaService":
                return mock_keyword_plan_idea_service
            elif service_name == "GoogleAdsService":
                return mock_google_ads_service
            return MagicMock() # Default mock for any other service

        mock_google_ads_client.get_service.side_effect = get_service_side_effect
        mock_load_client.return_value = mock_google_ads_client

        # Call the main function from the script
        generate_historical_metrics.main(mock_google_ads_client, self.MOCK_CUSTOMER_ID)

        # 1. Assert GoogleAdsClient.load_from_storage was called
        mock_load_client.assert_called_once_with(version="v19")

        # 2. Assert client.get_service was called for KeywordPlanIdeaService and GoogleAdsService
        mock_google_ads_client.get_service.assert_any_call("KeywordPlanIdeaService", version="v19")
        # The script generate_historical_metrics.py's main function also calls:
        # client.get_service("GoogleAdsService", version=_땔감_VERSION)
        # so we should check for that call as well.
        mock_google_ads_client.get_service.assert_any_call("GoogleAdsService", version="v19")


        # 3. Verify the call to keyword_plan_idea_service.generate_keyword_historical_metrics()
        # This is called by the helper function `generate_historical_metrics` within main.
        mock_keyword_plan_idea_service.generate_keyword_historical_metrics.assert_called_once()
        
        # Get the actual request passed to generate_keyword_historical_metrics
        call_args = mock_keyword_plan_idea_service.generate_keyword_historical_metrics.call_args
        # The request is the first positional argument to the method in the generated client code.
        # Or, if the script uses keyword arguments like client.generate_keyword_historical_metrics(request=...)
        # then it would be call_args[1]['request'].
        # Looking at the library, it's likely positional.
        # Let's assume it's `generate_keyword_historical_metrics(request=request_object)`
        # If not, this will need to be `call_args[0][0]`.
        # The `generate_keyword_historical_metrics.py` script does:
        # response = keyword_plan_idea_service.generate_keyword_historical_metrics(request=request)
        # So, call_args[1]['request'] is correct.
        request = call_args.kwargs['request']


        # Verify customer_id in the request
        self.assertEqual(request.customer_id, self.MOCK_CUSTOMER_ID)

        # Verify keywords
        self.assertListEqual(list(request.keywords), _KEYWORDS)

        # Verify geo_target_constants
        # The script allows for multiple, but the example uses one.
        self.assertEqual(len(request.geo_target_constants), 1)
        self.assertEqual(request.geo_target_constants[0], _GEO_TARGET_CONSTANT_US)
        
        # Verify language
        self.assertEqual(request.language, _LANGUAGE_CONSTANT_EN)

        # Verify keyword_plan_network
        self.assertEqual(request.keyword_plan_network, _KEYWORD_PLAN_NETWORK)
        
        # Note: The generate_historical_metrics.py script does not set aggregate_metrics
        # on the request, so we do not assert it here.

if __name__ == "__main__":
    unittest.main()
