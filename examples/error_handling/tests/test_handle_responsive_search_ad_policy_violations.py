import unittest
from unittest.mock import MagicMock, patch, call, ANY
import sys
import uuid # Import uuid

# Add the examples directory to the system path
sys.path.insert(0, '../../..')

from examples.error_handling.handle_responsive_search_ad_policy_violations import (
    main,
    create_responsive_search_ad,
    fetch_ignorable_policy_topics,
    request_exemption,
)
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


class TestHandleResponsiveSearchAdPolicyViolations(unittest.TestCase):
    @patch("examples.error_handling.handle_responsive_search_ad_policy_violations.create_responsive_search_ad")
    @patch("examples.error_handling.handle_responsive_search_ad_policy_violations.fetch_ignorable_policy_topics")
    @patch("examples.error_handling.handle_responsive_search_ad_policy_violations.request_exemption")
    def test_main_first_attempt_succeeds(
        self, mock_request_exemption, mock_fetch_topics, mock_create_ad
    ):
        mock_client = MagicMock(spec=GoogleAdsClient)
        mock_customer_id = "test_customer_id"
        mock_ad_group_id = "test_ad_group_id"

        mock_ad_group_ad_service = MagicMock()
        mock_client.get_service.return_value = mock_ad_group_ad_service
        mock_ad_operation = MagicMock()
        mock_create_ad.return_value = mock_ad_operation

        # Simulate first mutate_ad_group_ads call succeeding
        mock_ad_group_ad_service.mutate_ad_group_ads.return_value = MagicMock()

        main(mock_client, mock_customer_id, mock_ad_group_id)

        mock_client.get_service.assert_called_once_with("AdGroupAdService")
        mock_create_ad.assert_called_once_with(
            mock_client, mock_ad_group_ad_service, mock_customer_id, mock_ad_group_id
        )
        mock_ad_group_ad_service.mutate_ad_group_ads.assert_called_once_with(
            customer_id=mock_customer_id, operations=[mock_ad_operation]
        )
        mock_fetch_topics.assert_not_called() # Not called if first attempt succeeds
        # request_exemption IS called, but with an empty list of ignorable_policy_topics
        mock_request_exemption.assert_called_once_with(
            mock_customer_id,
            mock_ad_group_ad_service,
            mock_ad_operation,
            [], # No topics fetched
        )


    @patch("examples.error_handling.handle_responsive_search_ad_policy_violations.create_responsive_search_ad")
    @patch("examples.error_handling.handle_responsive_search_ad_policy_violations.fetch_ignorable_policy_topics")
    @patch("examples.error_handling.handle_responsive_search_ad_policy_violations.request_exemption")
    def test_main_first_attempt_fails_then_exempts(
        self, mock_request_exemption, mock_fetch_topics, mock_create_ad
    ):
        mock_client = MagicMock(spec=GoogleAdsClient)
        mock_customer_id = "test_customer_id"
        mock_ad_group_id = "test_ad_group_id"

        mock_ad_group_ad_service = MagicMock()
        mock_client.get_service.return_value = mock_ad_group_ad_service
        mock_ad_operation = MagicMock()
        mock_create_ad.return_value = mock_ad_operation

        mock_google_ads_exception = MagicMock(spec=GoogleAdsException)
        # Simulate first mutate_ad_group_ads call failing
        mock_ad_group_ad_service.mutate_ad_group_ads.side_effect = mock_google_ads_exception

        mock_ignorable_topics = ["topic1", "topic2"]
        mock_fetch_topics.return_value = mock_ignorable_topics

        main(mock_client, mock_customer_id, mock_ad_group_id)

        mock_client.get_service.assert_called_once_with("AdGroupAdService")
        mock_create_ad.assert_called_once_with(
            mock_client, mock_ad_group_ad_service, mock_customer_id, mock_ad_group_id
        )
        mock_ad_group_ad_service.mutate_ad_group_ads.assert_called_once_with(
            customer_id=mock_customer_id, operations=[mock_ad_operation]
        )
        mock_fetch_topics.assert_called_once_with(mock_client, mock_google_ads_exception)
        mock_request_exemption.assert_called_once_with(
            mock_customer_id,
            mock_ad_group_ad_service,
            mock_ad_operation,
            mock_ignorable_topics,
        )

    @patch("uuid.uuid4") # Patch uuid.uuid4 for predictable text
    def test_create_responsive_search_ad(self, mock_uuid4):
        mock_client = MagicMock(spec=GoogleAdsClient)
        mock_ad_group_ad_service = MagicMock() # Not used directly in this func but passed
        mock_customer_id = "test_customer_id"
        mock_ad_group_id = "test_ad_group_id"

        mock_uuid_str = "test-uuid-12345"
        mock_uuid4.return_value = mock_uuid_str


        mock_ad_group_service = MagicMock()
        mock_client.get_service.return_value = mock_ad_group_service
        mock_ad_group_service.ad_group_path.return_value = "ad_group_path_val"

        # Mock types
        mock_ad_group_ad_operation_type = MagicMock()
        mock_ad_text_asset_type = MagicMock

        created_ad_text_assets = []
        def get_type_side_effect(type_name):
            if type_name == "AdGroupAdOperation":
                return mock_ad_group_ad_operation_type
            elif type_name == "AdTextAsset":
                # Return a new MagicMock each time AdTextAsset is requested
                new_asset = MagicMock()
                created_ad_text_assets.append(new_asset)
                return new_asset
            raise ValueError(f"Unexpected type: {type_name}")

        mock_client.get_type = MagicMock(side_effect=get_type_side_effect)


        # Mock the .create attribute for the AdGroupAdOperation
        mock_ad_group_ad_instance = MagicMock()
        # Ensure ad and responsive_search_ad are also MagicMocks with lists for headlines, descriptions, final_urls
        mock_ad_group_ad_instance.ad.responsive_search_ad.headlines = []
        mock_ad_group_ad_instance.ad.responsive_search_ad.descriptions = []
        mock_ad_group_ad_instance.ad.final_urls = []
        mock_ad_group_ad_operation_type.create = mock_ad_group_ad_instance


        operation = create_responsive_search_ad(
            mock_client, mock_ad_group_ad_service, mock_customer_id, mock_ad_group_id
        )

        self.assertEqual(operation, mock_ad_group_ad_operation_type)
        mock_client.get_service.assert_called_once_with("AdGroupService")
        mock_ad_group_service.ad_group_path.assert_called_once_with(
            mock_customer_id, mock_ad_group_id
        )

        # 1 for AdGroupAdOperation, 3 for headlines, 2 for descriptions
        self.assertEqual(mock_client.get_type.call_count, 1 + 3 + 2)
        mock_client.get_type.assert_any_call("AdGroupAdOperation")
        mock_client.get_type.assert_any_call("AdTextAsset")


        self.assertEqual(mock_ad_group_ad_instance.ad_group, "ad_group_path_val")
        self.assertEqual(
            mock_ad_group_ad_instance.status,
            mock_client.enums.AdGroupAdStatusEnum.PAUSED,
        )

        # Check headlines
        self.assertEqual(len(created_ad_text_assets), 5) # 3 headlines + 2 descriptions
        self.assertEqual(len(mock_ad_group_ad_instance.ad.responsive_search_ad.headlines), 3)
        self.assertEqual(created_ad_text_assets[0].text, f"Cruise to Mars #{mock_uuid_str[0:13]}")
        self.assertEqual(created_ad_text_assets[1].text, "Best Space Cruise Line")
        self.assertEqual(created_ad_text_assets[2].text, "Experience the Stars")
        self.assertIn(created_ad_text_assets[0], mock_ad_group_ad_instance.ad.responsive_search_ad.headlines)

        # Check descriptions
        self.assertEqual(len(mock_ad_group_ad_instance.ad.responsive_search_ad.descriptions), 2)
        self.assertEqual(created_ad_text_assets[3].text, "Buy your tickets now!!!!!!!")
        self.assertEqual(created_ad_text_assets[4].text, "Visit the Red Planet")
        self.assertIn(created_ad_text_assets[3], mock_ad_group_ad_instance.ad.responsive_search_ad.descriptions)


        self.assertEqual(mock_ad_group_ad_instance.ad.final_urls, ["https://www.example.com"])


    def test_fetch_ignorable_policy_topics_success(self):
        mock_client = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_exception = MagicMock(spec=GoogleAdsException)

        # Mock PolicyFindingErrorEnum
        mock_policy_finding_error_enum = MagicMock()
        mock_policy_finding_error_enum.PolicyFindingError.POLICY_FINDING = "POLICY_FINDING_VAL"
        mock_client.get_type.return_value = mock_policy_finding_error_enum

        mock_error1 = MagicMock()
        mock_error1.error_code.policy_finding_error = "POLICY_FINDING_VAL"
        mock_error1.details.policy_finding_details.policy_topic_entries = [
            MagicMock(topic="topic1"),
            MagicMock(topic="topic2"),
        ]

        mock_error2 = MagicMock() # Another error, also a policy finding
        mock_error2.error_code.policy_finding_error = "POLICY_FINDING_VAL"
        mock_error2.details.policy_finding_details.policy_topic_entries = [
            MagicMock(topic="topic3"),
        ]

        mock_google_ads_exception.failure.errors = [mock_error1, mock_error2]

        topics = fetch_ignorable_policy_topics(mock_client, mock_google_ads_exception)

        self.assertEqual(topics, ["topic1", "topic2", "topic3"])
        mock_client.get_type.assert_called_with("PolicyFindingErrorEnum")


    def test_fetch_ignorable_policy_topics_non_policy_finding_error(self):
        mock_client = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_exception = MagicMock(spec=GoogleAdsException)

        mock_policy_finding_error_enum = MagicMock()
        mock_policy_finding_error_enum.PolicyFindingError.POLICY_FINDING = "POLICY_FINDING_VAL"
        mock_client.get_type.return_value = mock_policy_finding_error_enum

        mock_error = MagicMock()
        # This error is NOT a policy finding error
        mock_error.error_code.policy_finding_error = "OTHER_ERROR_TYPE"
        mock_google_ads_exception.failure.errors = [mock_error]

        with self.assertRaises(GoogleAdsException) as cm:
            fetch_ignorable_policy_topics(mock_client, mock_google_ads_exception)
        self.assertEqual(cm.exception, mock_google_ads_exception)


    def test_fetch_ignorable_policy_topics_no_details(self):
        mock_client = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_exception = MagicMock(spec=GoogleAdsException)

        mock_policy_finding_error_enum = MagicMock()
        mock_policy_finding_error_enum.PolicyFindingError.POLICY_FINDING = "POLICY_FINDING_VAL"
        mock_client.get_type.return_value = mock_policy_finding_error_enum

        mock_error = MagicMock()
        mock_error.error_code.policy_finding_error = "POLICY_FINDING_VAL"
        # Simulate no policy_finding_details
        mock_error.details.policy_finding_details = None
        mock_google_ads_exception.failure.errors = [mock_error]

        # Should still run but return an empty list as no topics are found
        topics = fetch_ignorable_policy_topics(mock_client, mock_google_ads_exception)
        self.assertEqual(topics, [])


    def test_request_exemption_success(self):
        mock_customer_id = "test_customer_id"
        mock_ad_group_ad_service = MagicMock()
        mock_ad_group_ad_operation = MagicMock()
        # Ensure the attribute exists and is a list-like object for extend
        mock_ad_group_ad_operation.policy_validation_parameter.ignorable_policy_topics = []
        mock_ignorable_policy_topics = ["topic1", "topic2"]

        mock_response = MagicMock()
        mock_response.results = [MagicMock(resource_name="test_resource_name")]
        mock_ad_group_ad_service.mutate_ad_group_ads.return_value = mock_response

        request_exemption(
            mock_customer_id,
            mock_ad_group_ad_service,
            mock_ad_group_ad_operation,
            mock_ignorable_policy_topics,
        )

        # Check that extend was called correctly
        self.assertEqual(
            mock_ad_group_ad_operation.policy_validation_parameter.ignorable_policy_topics,
            mock_ignorable_policy_topics
        )
        mock_ad_group_ad_service.mutate_ad_group_ads.assert_called_once_with(
            customer_id=mock_customer_id, operations=[mock_ad_group_ad_operation]
        )


if __name__ == "__main__":
    unittest.main()
