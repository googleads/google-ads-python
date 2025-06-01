import unittest
from unittest import mock
import argparse
import sys

# Assuming the script to be tested is in the parent directory.
# Adjust the import path as necessary.
from examples.misc import set_custom_client_timeouts
from google.ads.googleads.errors import GoogleAdsException
from google.api_core.exceptions import DeadlineExceeded


class TestSetCustomClientTimeouts(unittest.TestCase):
    """Tests for the set_custom_client_timeouts script."""

    @mock.patch("examples.misc.set_custom_client_timeouts.GoogleAdsClient")
    def setUp(self, mock_google_ads_client_class):
        # Mock the class's load_from_storage method
        self.mock_client = mock_google_ads_client_class.load_from_storage.return_value
        self.mock_ga_service = self.mock_client.get_service("GoogleAdsService")

        # Mock types
        self.mock_search_stream_request = self.mock_client.get_type("SearchGoogleAdsStreamRequest")
        self.mock_search_request = self.mock_client.get_type("SearchGoogleAdsRequest")

        # Ensure the mock service methods are also mocks
        self.mock_ga_service.search_stream = mock.Mock()
        self.mock_ga_service.search = mock.Mock()

    @mock.patch("sys.exit") # To check if sys.exit is called
    def test_make_server_streaming_call(self, mock_sys_exit):
        """Tests the make_server_streaming_call function."""
        customer_id = "1234567890"
        mock_request_instance = self.mock_search_stream_request.return_value
        mock_request_instance.customer_id = customer_id
        mock_request_instance.query = set_custom_client_timeouts.QUERY

        # Test successful call
        self.mock_ga_service.search_stream.return_value = [mock.Mock()] # Simulate some response
        set_custom_client_timeouts.make_server_streaming_call(self.mock_client, customer_id)
        self.mock_ga_service.search_stream.assert_called_once_with(
            request=mock_request_instance,
            timeout=set_custom_client_timeouts.CLIENT_TIMEOUT_SECONDS,
        )
        self.mock_search_stream_request.assert_called_once_with()
        self.assertEqual(mock_request_instance.customer_id, customer_id)
        self.assertEqual(mock_request_instance.query, set_custom_client_timeouts.QUERY)

        # Test DeadlineExceeded
        self.mock_ga_service.search_stream.reset_mock()
        self.mock_ga_service.search_stream.side_effect = DeadlineExceeded("Timeout")
        set_custom_client_timeouts.make_server_streaming_call(self.mock_client, customer_id)
        mock_sys_exit.assert_called_with(1)

        # Test GoogleAdsException
        self.mock_ga_service.search_stream.reset_mock()
        mock_sys_exit.reset_mock()
        self.mock_ga_service.search_stream.side_effect = GoogleAdsException(None, None, None)
        # This function is expected to raise GoogleAdsException if not DeadlineExceeded
        with self.assertRaises(GoogleAdsException):
            set_custom_client_timeouts.make_server_streaming_call(self.mock_client, customer_id)
        mock_sys_exit.assert_not_called() # Should not exit for general GoogleAdsException

    @mock.patch("sys.exit")
    def test_make_unary_call(self, mock_sys_exit):
        """Tests the make_unary_call function."""
        customer_id = "1234567890"
        mock_request_instance = self.mock_search_request.return_value
        mock_request_instance.customer_id = customer_id
        mock_request_instance.query = set_custom_client_timeouts.QUERY


        # Test successful call
        self.mock_ga_service.search.return_value = mock.Mock() # Simulate some response
        set_custom_client_timeouts.make_unary_call(self.mock_client, customer_id)
        self.mock_ga_service.search.assert_called_once()
        call_args = self.mock_ga_service.search.call_args
        self.assertEqual(call_args[1]["request"], mock_request_instance)
        self.assertIsNotNone(call_args[1]["retry"]) # Check that retry is passed
        self.mock_search_request.assert_called_once_with()
        self.assertEqual(mock_request_instance.customer_id, customer_id)
        self.assertEqual(mock_request_instance.query, set_custom_client_timeouts.QUERY)


        # Test DeadlineExceeded
        self.mock_ga_service.search.reset_mock()
        self.mock_ga_service.search.side_effect = DeadlineExceeded("Timeout")
        set_custom_client_timeouts.make_unary_call(self.mock_client, customer_id)
        mock_sys_exit.assert_called_with(1)

        # Test GoogleAdsException
        self.mock_ga_service.search.reset_mock()
        mock_sys_exit.reset_mock()
        self.mock_ga_service.search.side_effect = GoogleAdsException(None, None, None)
        with self.assertRaises(GoogleAdsException):
            set_custom_client_timeouts.make_unary_call(self.mock_client, customer_id)
        mock_sys_exit.assert_not_called()


    @mock.patch("examples.misc.set_custom_client_timeouts.make_server_streaming_call")
    @mock.patch("examples.misc.set_custom_client_timeouts.make_unary_call")
    def test_main_function_calls(self, mock_make_unary_call, mock_make_server_streaming_call):
        """Tests that the main function calls the processing functions."""
        customer_id = "1234567890"
        set_custom_client_timeouts.main(self.mock_client, customer_id)
        mock_make_server_streaming_call.assert_called_once_with(self.mock_client, customer_id)
        mock_make_unary_call.assert_called_once_with(self.mock_client, customer_id)

    @mock.patch("examples.misc.set_custom_client_timeouts.argparse.ArgumentParser")
    @mock.patch("examples.misc.set_custom_client_timeouts.GoogleAdsClient")
    def test_argument_parsing_and_script_execution(
        self, mock_google_ads_client_class_in_script, mock_argument_parser_class
    ):
        """Tests argument parsing and the script's main execution block."""
        # Prepare mock for ArgumentParser instance
        mock_parser_instance = mock.Mock()
        mock_args = argparse.Namespace(customer_id="test_customer_id_arg")
        mock_parser_instance.parse_args.return_value = mock_args
        mock_argument_parser_class.return_value = mock_parser_instance

        # Prepare mock for GoogleAdsClient.load_from_storage
        # This mock_client is what the script's main() will receive
        mock_script_client_instance = mock_google_ads_client_class_in_script.load_from_storage.return_value

        # Store original sys.argv and set up mocked command line arguments
        original_argv = sys.argv
        sys.argv = ["set_custom_client_timeouts.py", "-c", "test_customer_id_arg"]

        # Use runpy to execute the script's __main__ block
        # Patch the 'main' function within the script to prevent it from actually running
        # its logic, but to check if it's called correctly by the __main__ block.
        import runpy
        with mock.patch.object(set_custom_client_timeouts, "main") as mock_script_main_function:
            runpy.run_module("examples.misc.set_custom_client_timeouts", run_name="__main__")

        # Assertions
        mock_argument_parser_class.assert_called_once_with(
            description="Shows how to set custom client timeouts for API calls."
        )
        mock_parser_instance.add_argument.assert_called_once_with(
            "-c",
            "--customer_id",
            type=str,
            required=True,
            help="The Google Ads customer ID.",
        )
        mock_parser_instance.parse_args.assert_called_once()

        # Check that GoogleAdsClient.load_from_storage was called with version "v19"
        # This check is for the GoogleAdsClient class used within the script's __main__
        mock_google_ads_client_class_in_script.load_from_storage.assert_called_once_with(
            version="v19" # As specified in the script
        )

        # Assert that the script's main function was called with the correct arguments
        mock_script_main_function.assert_called_once_with(
            mock_script_client_instance, "test_customer_id_arg"
        )

        # Restore original sys.argv
        sys.argv = original_argv


if __name__ == "__main__":
    unittest.main()
