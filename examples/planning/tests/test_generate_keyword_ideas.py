import unittest
from unittest.mock import MagicMock, patch, call

from examples.planning import generate_keyword_ideas

class TestGenerateKeywordIdeas(unittest.TestCase):

    @patch('examples.planning.generate_keyword_ideas.GoogleAdsClient.load_from_storage')
    def test_main_generate_keyword_ideas_with_keywords_only(self, mock_load_from_storage):
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_keyword_plan_idea_service = MagicMock()
        mock_google_ads_service = MagicMock()
        mock_geo_target_constant_service = MagicMock()

        def get_service_side_effect(service_name, version=None):
            if service_name == "KeywordPlanIdeaService":
                return mock_keyword_plan_idea_service
            elif service_name == "GoogleAdsService":
                return mock_google_ads_service
            elif service_name == "GeoTargetConstantService":
                return mock_geo_target_constant_service
            return MagicMock()

        mock_google_ads_client.get_service.side_effect = get_service_side_effect

        # Mock responses
        mock_low_competition_enum = MagicMock()
        mock_low_competition_enum.name = "LOW"
        mock_medium_competition_enum = MagicMock()
        mock_medium_competition_enum.name = "MEDIUM"
        mock_keyword_ideas_response_iter = iter([
            MagicMock(text="keyword idea 1", keyword_idea_metrics=MagicMock(avg_monthly_searches=100, competition=mock_low_competition_enum)),
            MagicMock(text="keyword idea 2", keyword_idea_metrics=MagicMock(avg_monthly_searches=200, competition=mock_medium_competition_enum))
        ])
        # generate_keyword_ideas returns an iterator
        mock_keyword_plan_idea_service.generate_keyword_ideas.return_value = mock_keyword_ideas_response_iter

        # Mock path methods
        mock_geo_target_constant_service.geo_target_constant_path.side_effect = lambda x: f"geoTargetConstants/{x}"
        mock_google_ads_service.language_constant_path.return_value = "languageConstants/1000"

        # Mock enums
        mock_enums = MagicMock()
        mock_enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH_AND_PARTNERS = "GOOGLE_SEARCH_AND_PARTNERS"
        mock_enums.KeywordPlanCompetitionLevelEnum.LOW = "LOW"
        mock_enums.KeywordPlanCompetitionLevelEnum.MEDIUM = "MEDIUM"
        mock_google_ads_client.enums = mock_enums

        # Mock types for request construction
        mock_google_ads_client.get_type.side_effect = lambda name: MagicMock(name=name)

        test_customer_id = "1234567890"
        test_location_ids = ["1023191"] # New York
        test_language_id = "1000" # English
        test_keyword_texts = ["mars cruise", "venus cruise"]

        with patch('sys.stdout', new_callable=MagicMock) as mock_stdout:
            generate_keyword_ideas.main(
                mock_google_ads_client,
                test_customer_id,
                test_location_ids,
                test_language_id,
                test_keyword_texts,
                None # page_url
            )

        # mock_load_from_storage.assert_called_once_with(version="v19") # This is removed as client is injected
        mock_google_ads_client.get_service.assert_any_call("KeywordPlanIdeaService")
        mock_google_ads_client.get_service.assert_any_call("GoogleAdsService")
        mock_google_ads_client.get_service.assert_any_call("GeoTargetConstantService")

        mock_keyword_plan_idea_service.generate_keyword_ideas.assert_called_once()
        # Check that map_locations_ids_to_resource_names was called correctly
        mock_geo_target_constant_service.geo_target_constant_path.assert_called_once_with(test_location_ids[0])
        # Check that language_constant_path was called correctly
        mock_google_ads_service.language_constant_path.assert_called_once_with(test_language_id)

        # Check request construction
        # The request object is local to generate_keyword_ideas, so we inspect the call to the service method
        called_request = mock_keyword_plan_idea_service.generate_keyword_ideas.call_args[1]['request']
        self.assertEqual(called_request.customer_id, test_customer_id)
        self.assertIn(f"geoTargetConstants/{test_location_ids[0]}", called_request.geo_target_constants)
        self.assertEqual(called_request.language, "languageConstants/1000")
        self.assertEqual(called_request.keyword_plan_network, "GOOGLE_SEARCH_AND_PARTNERS")
        self.assertTrue(called_request.keyword_seed.keywords) # Check if keyword_seed is used
        # self.assertEqual(len(called_request.keyword_seed.keywords), 2) # No longer direct check
        called_request.keyword_seed.keywords.extend.assert_called_once_with(test_keyword_texts)


        output = "".join(call_args[0][0] for call_args in mock_stdout.write.call_args_list if call_args[0])
        self.assertIn('Keyword idea text "keyword idea 1" has "100" average monthly searches and "LOW" competition.', output)
        self.assertIn('Keyword idea text "keyword idea 2" has "200" average monthly searches and "MEDIUM" competition.', output)

    @patch('examples.planning.generate_keyword_ideas.GoogleAdsClient.load_from_storage')
    def test_main_generate_keyword_ideas_with_url_only(self, mock_load_from_storage):
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_keyword_plan_idea_service = MagicMock()
        mock_google_ads_service = MagicMock()
        mock_geo_target_constant_service = MagicMock()

        def get_service_side_effect(service_name, version=None):
            if service_name == "KeywordPlanIdeaService":
                return mock_keyword_plan_idea_service
            elif service_name == "GoogleAdsService":
                return mock_google_ads_service
            elif service_name == "GeoTargetConstantService":
                return mock_geo_target_constant_service
            return MagicMock()

        mock_google_ads_client.get_service.side_effect = get_service_side_effect
        mock_keyword_plan_idea_service.generate_keyword_ideas.return_value = iter([]) # No ideas for simplicity
        mock_geo_target_constant_service.geo_target_constant_path.side_effect = lambda x: f"geoTargetConstants/{x}"
        mock_google_ads_service.language_constant_path.return_value = "languageConstants/1000"
        mock_google_ads_client.enums = MagicMock() # Basic mock for enums
        mock_google_ads_client.get_type.side_effect = lambda name: MagicMock(name=name)


        test_customer_id = "1234567890"
        test_location_ids = ["1023191"]
        test_language_id = "1000"
        test_page_url = "http://www.example.com"

        with patch('sys.stdout', new_callable=MagicMock): # Ignore output for this test
            generate_keyword_ideas.main(
                mock_google_ads_client,
                test_customer_id,
                test_location_ids,
                test_language_id,
                [], # No keywords
                test_page_url
            )

        called_request = mock_keyword_plan_idea_service.generate_keyword_ideas.call_args[1]['request']
        self.assertTrue(called_request.url_seed.url)
        self.assertEqual(called_request.url_seed.url, test_page_url)

    @patch('examples.planning.generate_keyword_ideas.GoogleAdsClient.load_from_storage')
    def test_main_generate_keyword_ideas_with_keywords_and_url(self, mock_load_from_storage):
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client
        mock_keyword_plan_idea_service = MagicMock()
        mock_google_ads_service = MagicMock()
        mock_geo_target_constant_service = MagicMock()

        def get_service_side_effect(service_name, version=None):
            if service_name == "KeywordPlanIdeaService":
                return mock_keyword_plan_idea_service
            elif service_name == "GoogleAdsService":
                return mock_google_ads_service
            elif service_name == "GeoTargetConstantService":
                return mock_geo_target_constant_service
            return MagicMock()

        mock_google_ads_client.get_service.side_effect = get_service_side_effect
        mock_keyword_plan_idea_service.generate_keyword_ideas.return_value = iter([]) # No ideas for simplicity
        mock_geo_target_constant_service.geo_target_constant_path.side_effect = lambda x: f"geoTargetConstants/{x}"
        mock_google_ads_service.language_constant_path.return_value = "languageConstants/1000"
        mock_google_ads_client.enums = MagicMock()
        mock_google_ads_client.get_type.side_effect = lambda name: MagicMock(name=name)

        test_customer_id = "1234567890"
        test_location_ids = ["1023191"]
        test_language_id = "1000"
        test_keyword_texts = ["space hotel"]
        test_page_url = "http://www.example.com/space"

        with patch('sys.stdout', new_callable=MagicMock): # Ignore output
            generate_keyword_ideas.main(
                mock_google_ads_client,
                test_customer_id,
                test_location_ids,
                test_language_id,
                test_keyword_texts,
                test_page_url
            )

        called_request = mock_keyword_plan_idea_service.generate_keyword_ideas.call_args[1]['request']
        self.assertTrue(called_request.keyword_and_url_seed.url)
        self.assertEqual(called_request.keyword_and_url_seed.url, test_page_url)
        self.assertTrue(called_request.keyword_and_url_seed.keywords) # Check if attribute exists
        called_request.keyword_and_url_seed.keywords.extend.assert_called_once_with(test_keyword_texts)

    def test_main_with_no_keywords_or_url_raises_value_error(self):
        mock_google_ads_client = MagicMock() # Not used directly but expected by main
        with self.assertRaises(ValueError):
            generate_keyword_ideas.main(
                mock_google_ads_client,
                "123", ["1023191"], "1000", [], None
            )

if __name__ == "__main__":
    unittest.main()
