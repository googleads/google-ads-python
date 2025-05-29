import unittest
from unittest.mock import patch, MagicMock, ANY
import sys
import os

from google.api_core.exceptions import DeadlineExceeded
from google.api_core import retry as api_core_retry

# Adjust sys.path to allow import of the script under test
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from examples.misc import set_custom_client_timeouts

# _EXPECTED_PAGE_SIZE is not used in the target script.

class TestSetCustomClientTimeouts(unittest.TestCase):

    def _create_mock_row_with_campaign_id(self, campaign_id="test_campaign_id_123"):
        row = MagicMock()
        row.campaign.id = campaign_id
        return row

    def _create_mock_ads_client(self):
        mock_ads_client = MagicMock()
        mock_ga_service = mock_ads_client.get_service.return_value
        
        # Mock for search_stream (streaming call)
        mock_batch = MagicMock()
        mock_batch.results = [self._create_mock_row_with_campaign_id()] 
        mock_ga_service.search_stream.return_value = [mock_batch]

        # Mock for search (unary call)
        mock_ga_service.search.return_value = [self._create_mock_row_with_campaign_id()]
        
        return mock_ads_client, mock_ga_service

    # --- Tests for make_server_streaming_call ---

    @patch('set_custom_client_timeouts._CLIENT_TIMEOUT_SECONDS', 60.0) # Patch script's constant
    @patch('builtins.print')
    def test_streaming_call_success(self, mock_print):
        mock_ads_client, mock_ga_service = self._create_mock_ads_client()
        customer_id = "1234567890"
        
        # Call the function without timeout arg, it uses the patched script constant
        set_custom_client_timeouts.make_server_streaming_call(
            mock_ads_client, customer_id
        )

        mock_ads_client.get_service.assert_called_once_with("GoogleAdsService") # Version not specified in script func
        mock_ga_service.search_stream.assert_called_once_with(request=ANY, timeout=60.0) # Check patched timeout
        
        # Verify print output for success
        mock_print.assert_any_call("The server streaming call completed before the timeout.")
        mock_print.assert_any_call("Total # of campaign IDs retrieved: 1")


    @patch('set_custom_client_timeouts._CLIENT_TIMEOUT_SECONDS', 0.01) # Very small timeout
    @patch('builtins.print')
    @patch('sys.exit')
    def test_streaming_call_deadline_exceeded(self, mock_sys_exit, mock_print):
        mock_ads_client, mock_ga_service = self._create_mock_ads_client()
        customer_id = "1234567890"

        mock_ga_service.search_stream.side_effect = DeadlineExceeded("Test DeadlineExceeded Streaming")

        set_custom_client_timeouts.make_server_streaming_call(
            mock_ads_client, customer_id
        )
        
        mock_ga_service.search_stream.assert_called_once_with(request=ANY, timeout=0.01)
        mock_print.assert_any_call("The server streaming call did not complete before the timeout.")
        mock_sys_exit.assert_called_once_with(1)

    # --- Tests for make_unary_call ---

    @patch('set_custom_client_timeouts._CLIENT_TIMEOUT_SECONDS', 120.0) # Patch script's constant for deadline
    @patch('builtins.print')
    def test_unary_call_success(self, mock_print):
        mock_ads_client, mock_ga_service = self._create_mock_ads_client()
        customer_id = "1234567890"
        
        # Patched _CLIENT_TIMEOUT_SECONDS will be used by the script function
        script_timeout = 120.0
        expected_initial = script_timeout / 10.0
        expected_maximum = script_timeout / 5.0
        expected_deadline = script_timeout

        set_custom_client_timeouts.make_unary_call(
            mock_ads_client, customer_id
        )

        mock_ads_client.get_service.assert_called_once_with("GoogleAdsService") # Version not specified in script func
        
        args, kwargs = mock_ga_service.search.call_args
        self.assertEqual(kwargs.get('request').customer_id, customer_id)
        self.assertIn("SELECT campaign.id FROM campaign", kwargs.get('request').query)
        
        actual_retry = kwargs.get('retry')
        self.assertIsNotNone(actual_retry)
        self.assertIsInstance(actual_retry, api_core_retry.Retry)
        self.assertEqual(actual_retry._initial, expected_initial)
        self.assertEqual(actual_retry._maximum, expected_maximum)
        self.assertEqual(actual_retry._deadline, expected_deadline)
        # Assert default multiplier and predicate if they are not set in script
        self.assertEqual(actual_retry._multiplier, 1.3) # google.api_core.retry.Retry._DEFAULT_MULTIPLIER
        self.assertTrue(callable(actual_retry._predicate)) # Check if it's a callable, like if_transient_error


        mock_print.assert_any_call("The unary call completed before the timeout.")
        mock_print.assert_any_call("Total # of campaign IDs retrieved: 1")


    @patch('set_custom_client_timeouts._CLIENT_TIMEOUT_SECONDS', 0.01) # Very small timeout for deadline
    @patch('builtins.print')
    @patch('sys.exit')
    def test_unary_call_deadline_exceeded(self, mock_sys_exit, mock_print):
        mock_ads_client, mock_ga_service = self._create_mock_ads_client()
        customer_id = "1234567890"

        mock_ga_service.search.side_effect = DeadlineExceeded("Test DeadlineExceeded Unary")

        set_custom_client_timeouts.make_unary_call(
            mock_ads_client, customer_id
        )
        
        args, kwargs = mock_ga_service.search.call_args
        self.assertIsNotNone(kwargs.get('retry'))
        self.assertEqual(kwargs.get('retry')._deadline, 0.01)


        mock_print.assert_any_call("The unary call did not complete before the timeout.")
        mock_sys_exit.assert_called_once_with(1)


if __name__ == "__main__":
    unittest.main()
