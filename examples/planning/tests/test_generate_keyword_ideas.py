import unittest
from unittest.mock import patch, MagicMock, call

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.v19.enums.types import keyword_plan_network as keyword_plan_network_enum

# Assuming generate_keyword_ideas is importable
from examples.planning import generate_keyword_ideas

# Constants from generate_keyword_ideas.py or derived for testing
DEFAULT_LOCATION_IDS = ["1023191", "2840"]  # New York, USA
DEFAULT_LANGUAGE_ID = "1000"  # English
MOCK_CUSTOMER_ID = "1112223333"

# Expected resource names
EXPECTED_LANGUAGE_RN = f"languageConstants/{DEFAULT_LANGUAGE_ID}"
EXPECTED_LOCATION_RNS = [f"geoTargetConstants/{loc_id}" for loc_id in DEFAULT_LOCATION_IDS]


class TestGenerateKeywordIdeas(unittest.TestCase):

    def setUp(self):
        # Mock GoogleAdsClient and its services
        self.mock_google_ads_client = MagicMock(spec=GoogleAdsClient)
        self.mock_keyword_plan_idea_service = MagicMock()
        self.mock_geo_target_constant_service = MagicMock()

        # Configure get_service mock
        self.mock_google_ads_client.get_service.side_effect = lambda service_name, version="v19": {
            "KeywordPlanIdeaService": self.mock_keyword_plan_idea_service,
            "GeoTargetConstantService": self.mock_geo_target_constant_service,
        }.get(service_name, MagicMock())
        
        # Mock the load_from_storage method that will be patched at the class/method level for main tests
        self.mock_load_client_patcher = patch("examples.planning.generate_keyword_ideas.GoogleAdsClient.load_from_storage")
        self.mock_load_client = self.mock_load_client_patcher.start()
        self.mock_load_client.return_value = self.mock_google_ads_client

        # Mock for map_locations_ids_to_resource_names's internal call
        # It constructs resource names like "geoTargetConstants/123"
        self.mock_geo_target_constant_service.geo_target_constant_path = MagicMock(
            side_effect=lambda location_id: f"geoTargetConstants/{location_id}"
        )

    def tearDown(self):
        self.mock_load_client_patcher.stop()

    def test_map_locations_ids_to_resource_names(self):
        """Tests the map_locations_ids_to_resource_names helper function."""
        sample_location_ids = ["100", "200"]
        expected_rns = ["geoTargetConstants/100", "geoTargetConstants/200"]
        
        actual_rns = generate_keyword_ideas.map_locations_ids_to_resource_names(
            self.mock_google_ads_client, sample_location_ids
        )
        self.assertEqual(actual_rns, expected_rns)
        self.mock_geo_target_constant_service.geo_target_constant_path.assert_has_calls([
            call("100"), call("200")
        ])

    @patch("examples.planning.generate_keyword_ideas.map_locations_ids_to_resource_names")
    def test_main_with_keywords_only(self, mock_map_locations):
        mock_map_locations.return_value = EXPECTED_LOCATION_RNS
        keyword_texts = ["cat food", "dog toys"]
        
        generate_keyword_ideas.main(
            self.mock_google_ads_client, MOCK_CUSTOMER_ID,
            DEFAULT_LOCATION_IDS, DEFAULT_LANGUAGE_ID,
            keyword_texts, None  # No page_url
        )

        self.mock_load_client.assert_called_once_with(version="v19")
        self.mock_keyword_plan_idea_service.generate_keyword_ideas.assert_called_once()
        
        request = self.mock_keyword_plan_idea_service.generate_keyword_ideas.call_args[1]['request']
        
        self.assertEqual(request.customer_id, MOCK_CUSTOMER_ID)
        self.assertEqual(request.language, EXPECTED_LANGUAGE_RN)
        self.assertListEqual(list(request.geo_target_constants), EXPECTED_LOCATION_RNS)
        self.assertFalse(request.include_adult_keywords)
        self.assertEqual(
            request.keyword_plan_network,
            keyword_plan_network_enum.KeywordPlanNetworkEnum.KeywordPlanNetwork.GOOGLE_SEARCH_AND_PARTNERS
        )
        
        self.assertTrue(request.keyword_seed)
        self.assertListEqual(list(request.keyword_seed.keywords), keyword_texts)
        self.assertFalse(request.url_seed)
        self.assertFalse(request.keyword_and_url_seed)
        mock_map_locations.assert_called_once_with(self.mock_google_ads_client, DEFAULT_LOCATION_IDS)

    @patch("examples.planning.generate_keyword_ideas.map_locations_ids_to_resource_names")
    def test_main_with_url_only(self, mock_map_locations):
        mock_map_locations.return_value = EXPECTED_LOCATION_RNS
        page_url = "http://www.example.com/pets"

        generate_keyword_ideas.main(
            self.mock_google_ads_client, MOCK_CUSTOMER_ID,
            DEFAULT_LOCATION_IDS, DEFAULT_LANGUAGE_ID,
            [], page_url  # No keywords
        )

        self.mock_load_client.assert_called_once_with(version="v19")
        self.mock_keyword_plan_idea_service.generate_keyword_ideas.assert_called_once()
        
        request = self.mock_keyword_plan_idea_service.generate_keyword_ideas.call_args[1]['request']

        self.assertEqual(request.customer_id, MOCK_CUSTOMER_ID)
        self.assertEqual(request.language, EXPECTED_LANGUAGE_RN)
        self.assertListEqual(list(request.geo_target_constants), EXPECTED_LOCATION_RNS)
        self.assertFalse(request.include_adult_keywords)
        self.assertEqual(
            request.keyword_plan_network,
            keyword_plan_network_enum.KeywordPlanNetworkEnum.KeywordPlanNetwork.GOOGLE_SEARCH_AND_PARTNERS
        )

        self.assertTrue(request.url_seed)
        self.assertEqual(request.url_seed.url, page_url)
        self.assertFalse(request.keyword_seed)
        self.assertFalse(request.keyword_and_url_seed)
        mock_map_locations.assert_called_once_with(self.mock_google_ads_client, DEFAULT_LOCATION_IDS)

    @patch("examples.planning.generate_keyword_ideas.map_locations_ids_to_resource_names")
    def test_main_with_keywords_and_url(self, mock_map_locations):
        mock_map_locations.return_value = EXPECTED_LOCATION_RNS
        keyword_texts = ["cat food", "dog toys"]
        page_url = "http://www.example.com/pets"

        generate_keyword_ideas.main(
            self.mock_google_ads_client, MOCK_CUSTOMER_ID,
            DEFAULT_LOCATION_IDS, DEFAULT_LANGUAGE_ID,
            keyword_texts, page_url
        )
        
        self.mock_load_client.assert_called_once_with(version="v19")
        self.mock_keyword_plan_idea_service.generate_keyword_ideas.assert_called_once()

        request = self.mock_keyword_plan_idea_service.generate_keyword_ideas.call_args[1]['request']

        self.assertEqual(request.customer_id, MOCK_CUSTOMER_ID)
        self.assertEqual(request.language, EXPECTED_LANGUAGE_RN)
        self.assertListEqual(list(request.geo_target_constants), EXPECTED_LOCATION_RNS)
        self.assertFalse(request.include_adult_keywords)
        self.assertEqual(
            request.keyword_plan_network,
            keyword_plan_network_enum.KeywordPlanNetworkEnum.KeywordPlanNetwork.GOOGLE_SEARCH_AND_PARTNERS
        )

        self.assertTrue(request.keyword_and_url_seed)
        self.assertEqual(request.keyword_and_url_seed.url, page_url)
        self.assertListEqual(list(request.keyword_and_url_seed.keywords), keyword_texts)
        self.assertFalse(request.keyword_seed)
        self.assertFalse(request.url_seed)
        mock_map_locations.assert_called_once_with(self.mock_google_ads_client, DEFAULT_LOCATION_IDS)

    def test_main_with_no_keywords_or_url(self):
        with self.assertRaisesRegex(ValueError, "At least one of keywords or page URL is required."):
            generate_keyword_ideas.main(
                self.mock_google_ads_client, MOCK_CUSTOMER_ID,
                DEFAULT_LOCATION_IDS, DEFAULT_LANGUAGE_ID,
                [], None  # No keywords, no page_url
            )
        # Ensure no call to generate_keyword_ideas happened
        self.mock_keyword_plan_idea_service.generate_keyword_ideas.assert_not_called()


if __name__ == "__main__":
    unittest.main()
