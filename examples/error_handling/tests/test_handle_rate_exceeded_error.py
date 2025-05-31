import unittest
from unittest.mock import MagicMock, patch, call, ANY
import sys
from time import sleep

# Add the examples directory to the system path
sys.path.insert(0, '../../..')

from examples.error_handling.handle_rate_exceeded_error import (
    main,
    create_ad_group_criterion_operations,
    request_mutate_and_display_result,
    NUM_REQUESTS, # Import constants for use in tests
    NUM_KEYWORDS,
    NUM_RETRIES,
    RETRY_SECONDS,
)
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


class TestHandleRateExceededError(unittest.TestCase):
    @patch("examples.error_handling.handle_rate_exceeded_error.create_ad_group_criterion_operations")
    @patch("examples.error_handling.handle_rate_exceeded_error.request_mutate_and_display_result")
    @patch("time.sleep") # Patch sleep
    def test_main_no_errors(
        self, mock_sleep, mock_request_mutate, mock_create_operations
    ):
        mock_client = MagicMock(spec=GoogleAdsClient)
        mock_customer_id = "test_customer_id"
        mock_ad_group_id = "test_ad_group_id"

        # Mock QuotaErrorEnum
        mock_quota_error_enum = MagicMock()
        mock_quota_error_enum.QuotaError.RESOURCE_EXHAUSTED = "RESOURCE_EXHAUSTED"
        mock_quota_error_enum.QuotaError.RESOURCE_TEMPORARILY_EXHAUSTED = "RESOURCE_TEMPORARILY_EXHAUSTED"
        mock_client.get_type.return_value = mock_quota_error_enum

        mock_operations = [MagicMock()]
        mock_create_operations.return_value = mock_operations

        main(mock_client, mock_customer_id, mock_ad_group_id)

        self.assertEqual(mock_create_operations.call_count, NUM_REQUESTS)
        self.assertEqual(mock_request_mutate.call_count, NUM_REQUESTS)
        mock_request_mutate.assert_called_with(
            mock_client, mock_customer_id, mock_operations
        )
        mock_sleep.assert_not_called() # No sleep if no errors

    @patch("examples.error_handling.handle_rate_exceeded_error.create_ad_group_criterion_operations")
    @patch("examples.error_handling.handle_rate_exceeded_error.request_mutate_and_display_result")
    @patch("time.sleep")
    def test_main_with_recoverable_rate_exceeded_error(
        self, mock_sleep, mock_request_mutate, mock_create_operations
    ):
        mock_client = MagicMock(spec=GoogleAdsClient)
        mock_customer_id = "test_customer_id"
        mock_ad_group_id = "test_ad_group_id"

        mock_quota_error_enum = MagicMock()
        mock_quota_error_enum.QuotaError.RESOURCE_EXHAUSTED = "RESOURCE_EXHAUSTED"
        mock_quota_error_enum.QuotaError.RESOURCE_TEMPORARILY_EXHAUSTED = "RESOURCE_TEMPORARILY_EXHAUSTED"
        mock_client.get_type.return_value = mock_quota_error_enum

        mock_operations = [MagicMock()]
        mock_create_operations.return_value = mock_operations

        # Simulate RateExceededError on the first attempt of the first request, then succeed
        mock_rate_exceeded_failure = MagicMock()
        mock_error = MagicMock()
        mock_error.error_code.quota_error = "RESOURCE_TEMPORARILY_EXHAUSTED"
        mock_rate_exceeded_failure.errors = [mock_error]
        rate_exceeded_exception = GoogleAdsException(
            error=MagicMock(),
            failure=mock_rate_exceeded_failure,
            request_id="test_req_id"
        )

        # Let the first call to the first request fail, then succeed
        # All other NUM_REQUESTS-1 requests will succeed on the first try
        side_effects = [rate_exceeded_exception, None] + [None] * (NUM_REQUESTS -1)
        mock_request_mutate.side_effect = side_effects

        main(mock_client, mock_customer_id, mock_ad_group_id)

        self.assertEqual(mock_create_operations.call_count, NUM_REQUESTS)
        # Total calls = 1 (failed) + 1 (success) + (NUM_REQUESTS - 1) (successes)
        self.assertEqual(mock_request_mutate.call_count, NUM_REQUESTS + 1)
        mock_sleep.assert_called_once_with(RETRY_SECONDS)


    @patch("examples.error_handling.handle_rate_exceeded_error.create_ad_group_criterion_operations")
    @patch("examples.error_handling.handle_rate_exceeded_error.request_mutate_and_display_result")
    @patch("time.sleep")
    def test_main_with_unrecoverable_rate_exceeded_error(
        self, mock_sleep, mock_request_mutate, mock_create_operations
    ):
        mock_client = MagicMock(spec=GoogleAdsClient)
        mock_customer_id = "test_customer_id"
        mock_ad_group_id = "test_ad_group_id"

        mock_quota_error_enum = MagicMock()
        mock_quota_error_enum.QuotaError.RESOURCE_EXHAUSTED = "RESOURCE_EXHAUSTED"
        mock_quota_error_enum.QuotaError.RESOURCE_TEMPORARILY_EXHAUSTED = "RESOURCE_TEMPORARILY_EXHAUSTED"
        mock_client.get_type.return_value = mock_quota_error_enum

        mock_operations = [MagicMock()]
        mock_create_operations.return_value = mock_operations

        # Simulate RateExceededError always
        mock_rate_exceeded_failure = MagicMock()
        mock_error = MagicMock()
        mock_error.error_code.quota_error = "RESOURCE_EXHAUSTED"
        mock_rate_exceeded_failure.errors = [mock_error]
        rate_exceeded_exception = GoogleAdsException(
            error=MagicMock(),
            failure=mock_rate_exceeded_failure,
            request_id="test_req_id"
        )
        mock_request_mutate.side_effect = rate_exceeded_exception

        with self.assertRaisesRegex(Exception, "Could not recover after making 3 attempts."):
            main(mock_client, mock_customer_id, mock_ad_group_id)

        self.assertEqual(mock_create_operations.call_count, 1) # Only for the first request
        self.assertEqual(mock_request_mutate.call_count, NUM_RETRIES) # Retries for the first request
        expected_sleep_calls = [
            call(RETRY_SECONDS),
            call(RETRY_SECONDS * 2),
            call(RETRY_SECONDS * 4), # This sleep happens before the final check raises exception
        ]
        # The loop for retries runs NUM_RETRIES times. Inside the loop, if a rate error occurs,
        # sleep is called, retry_count is incremented.
        # The exception is raised in the finally block of the inner try-except-finally
        # The check `retry_count == NUM_RETRIES` will be true after NUM_RETRIES failures.
        # So, sleep will be called NUM_RETRIES times.
        self.assertEqual(mock_sleep.call_count, NUM_RETRIES)
        mock_sleep.assert_has_calls(expected_sleep_calls)


    @patch("examples.error_handling.handle_rate_exceeded_error.create_ad_group_criterion_operations")
    @patch("examples.error_handling.handle_rate_exceeded_error.request_mutate_and_display_result")
    @patch("time.sleep")
    def test_main_with_non_rate_exceeded_error(
        self, mock_sleep, mock_request_mutate, mock_create_operations
    ):
        mock_client = MagicMock(spec=GoogleAdsClient)
        mock_customer_id = "test_customer_id"
        mock_ad_group_id = "test_ad_group_id"

        mock_quota_error_enum = MagicMock()
        # Ensure these are different from what the code checks for rate limits
        mock_quota_error_enum.QuotaError.RESOURCE_EXHAUSTED = "ACTUAL_RESOURCE_EXHAUSTED"
        mock_quota_error_enum.QuotaError.RESOURCE_TEMPORARILY_EXHAUSTED = "ACTUAL_RESOURCE_TEMPORARILY_EXHAUSTED"
        mock_client.get_type.return_value = mock_quota_error_enum


        mock_operations = [MagicMock()]
        mock_create_operations.return_value = mock_operations

        # Simulate a non-RateExceededError
        mock_other_failure = MagicMock()
        mock_error = MagicMock()
        mock_error.error_code.quota_error = "SOME_OTHER_ERROR" # Not a rate limit error
        mock_other_failure.errors = [mock_error]
        other_exception = GoogleAdsException(
            error=MagicMock(),
            failure=mock_other_failure,
            request_id="test_req_id"
        )
        mock_request_mutate.side_effect = other_exception

        with self.assertRaises(GoogleAdsException) as cm:
            main(mock_client, mock_customer_id, mock_ad_group_id)

        self.assertEqual(cm.exception, other_exception)
        self.assertEqual(mock_create_operations.call_count, 1)
        self.assertEqual(mock_request_mutate.call_count, 1)
        mock_sleep.assert_not_called()


    def test_create_ad_group_criterion_operations(self):
        mock_client = MagicMock(spec=GoogleAdsClient)
        mock_customer_id = "test_customer_id"
        mock_ad_group_id = "test_ad_group_id"
        request_index = 1

        mock_ad_group_service = MagicMock()
        mock_client.get_service.return_value = mock_ad_group_service
        mock_ad_group_service.ad_group_path.return_value = "ad_group_path"

        mock_ad_group_criterion_operation_type = MagicMock()
        mock_client.get_type.return_value = mock_ad_group_criterion_operation_type

        # Mock the .create attribute on the returned operation type
        mock_operation_instance = MagicMock()
        mock_ad_group_criterion_operation_type.create = mock_operation_instance
        # Ensure that when client.get_type("AdGroupCriterionOperation") is called,
        # it returns an object that, when .create is accessed, gives mock_operation_instance
        # This needs to happen for each of NUM_KEYWORDS iterations.
        # So, client.get_type should return a new mock each time that has a .create attribute
        created_operations = []
        def get_type_side_effect(type_name):
            if type_name == "AdGroupCriterionOperation":
                op_mock = MagicMock()
                op_mock.create = MagicMock() # Each operation has its own .create
                created_operations.append(op_mock)
                return op_mock
            return MagicMock() # Default for other types if any

        mock_client.get_type = MagicMock(side_effect=get_type_side_effect)


        operations = create_ad_group_criterion_operations(
            mock_client, mock_customer_id, mock_ad_group_id, request_index
        )

        self.assertEqual(len(operations), NUM_KEYWORDS)
        mock_client.get_service.assert_called_once_with("AdGroupService")
        self.assertEqual(mock_client.get_type.call_count, NUM_KEYWORDS)
        mock_client.get_type.assert_called_with("AdGroupCriterionOperation")

        for i, op_mock in enumerate(created_operations):
            self.assertEqual(op_mock.create.ad_group, "ad_group_path")
            self.assertEqual(
                op_mock.create.status, mock_client.enums.AdGroupCriterionStatusEnum.ENABLED
            )
            self.assertEqual(
                op_mock.create.keyword.text, f"mars cruise req {request_index} seed {i}"
            )
            self.assertEqual(
                op_mock.create.keyword.match_type,
                mock_client.enums.KeywordMatchTypeEnum.EXACT,
            )
            self.assertIn(op_mock, operations)


    @patch("builtins.print") # To capture print statements
    def test_request_mutate_and_display_result(self, mock_print):
        mock_client = MagicMock(spec=GoogleAdsClient)
        mock_customer_id = "test_customer_id"
        mock_operations = [MagicMock(), MagicMock()]

        mock_ad_group_criterion_service = MagicMock()
        mock_client.get_service.return_value = mock_ad_group_criterion_service

        mock_request_type = MagicMock()
        mock_client.get_type.return_value = mock_request_type
        mock_request_instance = MagicMock()
        # Instead of assigning to mock_request_type.return_value, assign directly to the instance
        # that will be manipulated in the function.
        mock_client.get_type.return_value = mock_request_instance


        mock_response = MagicMock()
        mock_result1 = MagicMock(resource_name="rn1")
        mock_result2 = MagicMock(resource_name="rn2")
        mock_response.results = [mock_result1, mock_result2]
        mock_ad_group_criterion_service.mutate_ad_group_criteria.return_value = (
            mock_response
        )

        request_mutate_and_display_result(
            mock_client, mock_customer_id, mock_operations
        )

        mock_client.get_service.assert_called_once_with("AdGroupCriterionService")
        mock_client.get_type.assert_called_once_with("MutateAdGroupCriteriaRequest")

        self.assertEqual(mock_request_instance.customer_id, mock_customer_id)
        self.assertEqual(mock_request_instance.operations, mock_operations)
        self.assertTrue(mock_request_instance.validate_only)

        mock_ad_group_criterion_service.mutate_ad_group_criteria.assert_called_once_with(
            request=mock_request_instance
        )

        mock_print.assert_any_call(f"Added {len(mock_response.results)} ad group criteria:")
        mock_print.assert_any_call("Resource name: 'rn1'")
        mock_print.assert_any_call("Resource name: 'rn2'")


if __name__ == "__main__":
    unittest.main()
