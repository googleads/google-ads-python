import unittest
from unittest.mock import MagicMock, patch, call
import sys

# Add the examples directory to the system path
sys.path.insert(0, '../../..')

from examples.error_handling.handle_keyword_policy_violations import (
    main,
    create_keyword_criterion,
    fetch_exempt_policy_violation_keys,
    request_exemption,
)
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.client import GoogleAdsClient


class TestHandleKeywordPolicyViolations(unittest.TestCase):
    @patch("examples.error_handling.handle_keyword_policy_violations.GoogleAdsClient")
    def test_main_success_no_exception(self, mock_google_ads_client_constructor):
        mock_client = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client_constructor.load_from_storage.return_value = mock_client
        mock_ad_group_criterion_service = MagicMock()
        mock_client.get_service.return_value = mock_ad_group_criterion_service

        # Mock create_keyword_criterion to return no exception
        with patch("examples.error_handling.handle_keyword_policy_violations.create_keyword_criterion") as mock_create_keyword:
            mock_create_keyword.return_value = (None, MagicMock()) # No exception

            main(mock_client, "test_customer_id", "test_ad_group_id", "test_keyword")

            mock_create_keyword.assert_called_once_with(
                mock_client,
                mock_ad_group_criterion_service,
                "test_customer_id",
                "test_ad_group_id",
                "test_keyword",
            )
            # fetch_exempt_policy_violation_keys and request_exemption should not be called
            self.assertFalse(mock_client.fetch_exempt_policy_violation_keys.called)
            self.assertFalse(mock_client.request_exemption.called)


    @patch("examples.error_handling.handle_keyword_policy_violations.GoogleAdsClient")
    @patch("examples.error_handling.handle_keyword_policy_violations.fetch_exempt_policy_violation_keys")
    @patch("examples.error_handling.handle_keyword_policy_violations.request_exemption")
    def test_main_with_exception_and_exemption(
        self, mock_request_exemption, mock_fetch_keys, mock_google_ads_client_constructor
    ):
        mock_client = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client_constructor.load_from_storage.return_value = mock_client
        mock_ad_group_criterion_service = MagicMock()
        mock_client.get_service.return_value = mock_ad_group_criterion_service
        mock_google_ads_exception = MagicMock(spec=GoogleAdsException)
        mock_operation = MagicMock()
        mock_exempt_keys = [MagicMock()]

        # Mock create_keyword_criterion to return an exception
        with patch("examples.error_handling.handle_keyword_policy_violations.create_keyword_criterion") as mock_create_keyword:
            mock_create_keyword.return_value = (mock_google_ads_exception, mock_operation)
            mock_fetch_keys.return_value = mock_exempt_keys

            main(mock_client, "test_customer_id", "test_ad_group_id", "test_keyword")

            mock_create_keyword.assert_called_once_with(
                mock_client,
                mock_ad_group_criterion_service,
                "test_customer_id",
                "test_ad_group_id",
                "test_keyword",
            )
            mock_fetch_keys.assert_called_once_with(mock_google_ads_exception)
            mock_request_exemption.assert_called_once_with(
                "test_customer_id",
                mock_ad_group_criterion_service,
                mock_operation,
                mock_exempt_keys,
            )

    @patch("examples.error_handling.handle_keyword_policy_violations.GoogleAdsClient")
    @patch("examples.error_handling.handle_keyword_policy_violations.fetch_exempt_policy_violation_keys")
    @patch("examples.error_handling.handle_keyword_policy_violations.request_exemption")
    @patch("sys.exit") # Mock sys.exit to prevent test termination
    def test_main_with_exemption_failure(
        self, mock_sys_exit, mock_request_exemption, mock_fetch_keys, mock_google_ads_client_constructor
    ):
        mock_client = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client_constructor.load_from_storage.return_value = mock_client
        mock_ad_group_criterion_service = MagicMock()
        mock_client.get_service.return_value = mock_ad_group_criterion_service
        mock_google_ads_exception = MagicMock(spec=GoogleAdsException)
        mock_operation = MagicMock()
        mock_exempt_keys = [MagicMock()]

        # Mock create_keyword_criterion to return an exception
        with patch("examples.error_handling.handle_keyword_policy_violations.create_keyword_criterion") as mock_create_keyword:
            mock_create_keyword.return_value = (mock_google_ads_exception, mock_operation)
            mock_fetch_keys.return_value = mock_exempt_keys
            # Simulate GoogleAdsException during request_exemption
            mock_request_exemption.side_effect = GoogleAdsException(
                error=MagicMock(),
                failure=MagicMock(errors=[MagicMock(message=MagicMock())]),
                request_id="test_request_id"
            )


            main(mock_client, "test_customer_id", "test_ad_group_id", "test_keyword")

            mock_create_keyword.assert_called_once()
            mock_fetch_keys.assert_called_once()
            mock_request_exemption.assert_called_once()
            mock_sys_exit.assert_called_once_with(1)


    def test_create_keyword_criterion_success(self):
        mock_client = MagicMock(spec=GoogleAdsClient)
        mock_ad_group_criterion_service = MagicMock()
        mock_customer_id = "test_customer_id"
        mock_ad_group_id = "test_ad_group_id"
        mock_keyword_text = "test_keyword"

        mock_operation = MagicMock()
        mock_client.get_type.return_value = mock_operation
        mock_ad_group_service = MagicMock()
        mock_client.get_service.return_value = mock_ad_group_service
        mock_ad_group_service.ad_group_path.return_value = "ad_group_path"

        mock_response = MagicMock()
        mock_response.results = [MagicMock(resource_name="test_resource_name")]
        mock_ad_group_criterion_service.mutate_ad_group_criteria.return_value = mock_response

        exception, operation_out = create_keyword_criterion(
            mock_client,
            mock_ad_group_criterion_service,
            mock_customer_id,
            mock_ad_group_id,
            mock_keyword_text,
        )

        self.assertIsNone(exception)
        self.assertEqual(operation_out, mock_operation)
        mock_client.get_type.assert_called_once_with("AdGroupCriterionOperation")
        mock_client.get_service.assert_called_once_with("AdGroupService")
        mock_ad_group_service.ad_group_path.assert_called_once_with(
            mock_customer_id, mock_ad_group_id
        )
        mock_ad_group_criterion_service.mutate_ad_group_criteria.assert_called_once_with(
            customer_id=mock_customer_id, operations=[mock_operation]
        )

    def test_create_keyword_criterion_failure(self):
        mock_client = MagicMock(spec=GoogleAdsClient)
        mock_ad_group_criterion_service = MagicMock()
        mock_customer_id = "test_customer_id"
        mock_ad_group_id = "test_ad_group_id"
        mock_keyword_text = "test_keyword"

        mock_operation = MagicMock()
        mock_client.get_type.return_value = mock_operation
        mock_ad_group_service = MagicMock()
        mock_client.get_service.return_value = mock_ad_group_service
        mock_ad_group_service.ad_group_path.return_value = "ad_group_path"

        mock_google_ads_exception = MagicMock(spec=GoogleAdsException)
        mock_ad_group_criterion_service.mutate_ad_group_criteria.side_effect = (
            mock_google_ads_exception
        )

        exception, operation_out = create_keyword_criterion(
            mock_client,
            mock_ad_group_criterion_service,
            mock_customer_id,
            mock_ad_group_id,
            mock_keyword_text,
        )

        self.assertEqual(exception, mock_google_ads_exception)
        self.assertEqual(operation_out, mock_operation)


    def test_fetch_exempt_policy_violation_keys_success(self):
        mock_google_ads_exception = MagicMock(spec=GoogleAdsException)
        mock_error = MagicMock()
        mock_error.details.policy_violation_details.is_exemptible = True
        mock_error.details.policy_violation_details.key = "test_key"
        mock_google_ads_exception.failure.errors = [mock_error]

        keys = fetch_exempt_policy_violation_keys(mock_google_ads_exception)

        self.assertEqual(keys, ["test_key"])

    def test_fetch_exempt_policy_violation_keys_not_exemptible(self):
        mock_google_ads_exception = MagicMock(spec=GoogleAdsException)
        mock_error = MagicMock()
        mock_error.details.policy_violation_details.is_exemptible = False
        mock_google_ads_exception.failure.errors = [mock_error]

        with self.assertRaises(GoogleAdsException):
            fetch_exempt_policy_violation_keys(mock_google_ads_exception)

    def test_fetch_exempt_policy_violation_keys_no_details(self):
        mock_google_ads_exception = MagicMock(spec=GoogleAdsException)
        mock_error = MagicMock()
        mock_error.details.policy_violation_details = None # No policy violation details
        mock_google_ads_exception.failure.errors = [mock_error]

        with self.assertRaises(GoogleAdsException):
            fetch_exempt_policy_violation_keys(mock_google_ads_exception)

    def test_request_exemption_success(self):
        mock_customer_id = "test_customer_id"
        mock_ad_group_criterion_service = MagicMock()
        mock_ad_group_criterion_operation = MagicMock()
        mock_ad_group_criterion_operation.exempt_policy_violation_keys = [] # Initialize as list
        mock_exempt_policy_violation_keys = ["key1", "key2"]

        mock_response = MagicMock()
        mock_response.results = [MagicMock(resource_name="test_resource_name")]
        mock_ad_group_criterion_service.mutate_ad_group_criteria.return_value = (
            mock_response
        )

        request_exemption(
            mock_customer_id,
            mock_ad_group_criterion_service,
            mock_ad_group_criterion_operation,
            mock_exempt_policy_violation_keys,
        )

        mock_ad_group_criterion_operation.exempt_policy_violation_keys.extend.assert_called_once_with(
            mock_exempt_policy_violation_keys
        )
        mock_ad_group_criterion_service.mutate_ad_group_criteria.assert_called_once_with(
            customer_id=mock_customer_id,
            operations=[mock_ad_group_criterion_operation],
        )


if __name__ == "__main__":
    unittest.main()
