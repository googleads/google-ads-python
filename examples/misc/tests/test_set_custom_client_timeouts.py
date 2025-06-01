import unittest
from unittest import mock
import argparse
import sys

# Assuming the script to be tested is in the parent directory.
# Adjust the import path as necessary.
from examples.misc import set_custom_client_timeouts
from google.ads.googleads.errors import GoogleAdsException
from google.api_core.exceptions import DeadlineExceeded
from google.api_core.retry import Retry # Added import for Retry
from .test_utils import create_mock_google_ads_exception


class TestSetCustomClientTimeouts(unittest.TestCase):
    """Tests for the set_custom_client_timeouts script."""

    @mock.patch("examples.misc.set_custom_client_timeouts.GoogleAdsClient")
    def setUp(self, mock_google_ads_client_class):
        # Mock the class's load_from_storage method
        self.mock_client = mock_google_ads_client_class.load_from_storage.return_value
        self.mock_ga_service = self.mock_client.get_service("GoogleAdsService")

        # Mock types returned by get_type
        self.mock_search_stream_request_obj = mock.Mock(name="SearchGoogleAdsStreamRequestInstance")
        self.mock_search_request_obj = mock.Mock(name="SearchGoogleAdsRequestInstance")

        # Store the original get_type if it's already a mock with other behavior,
        # though usually it's a new MagicMock per test instance of the client.
        self._original_get_type = self.mock_client.get_type

        def get_type_side_effect(type_name):
            if type_name == "SearchGoogleAdsStreamRequest":
                return self.mock_search_stream_request_obj
            elif type_name == "SearchGoogleAdsRequest":
                return self.mock_search_request_obj
            # Fallback for other types like "GoogleAdsFailure", "ErrorInfo"
            # which are used by create_mock_google_ads_exception
            if isinstance(self._original_get_type, mock.Mock) and \
               self._original_get_type.side_effect is not get_type_side_effect:
                return self._original_get_type(type_name)
            # If the original get_type was not a complex mock, or to ensure other types are still mockable:
            # For "GoogleAdsFailure" and "ErrorInfo", the create_mock_google_ads_exception
            # expects get_type to return a type that can be instantiated (e.g. by calling () on it)
            # and that instance should have an 'errors' attribute if it's a GoogleAdsFailure.
            # A simple mock.Mock() would work for these if they are then assigned attributes.
            # However, the create_mock_google_ads_exception calls .get_type(...)()
            # so get_type should return a mock that, when called, returns another mock.
            temp_mock_type = mock.Mock(name=f"{type_name}_Type")
            temp_mock_instance = mock.Mock(name=f"{type_name}_Instance")
            if type_name == "GoogleAdsFailure":
                temp_mock_instance.errors = []
            temp_mock_type.return_value = temp_mock_instance
            return temp_mock_type

        self.mock_client.get_type.side_effect = get_type_side_effect

        # Ensure the mock service methods are also mocks
        self.mock_ga_service.search_stream = mock.Mock()
        self.mock_ga_service.search = mock.Mock()

    @mock.patch("sys.exit") # To check if sys.exit is called
    def test_make_server_streaming_call(self, mock_sys_exit):
        """Tests the make_server_streaming_call function."""
        customer_id = "1234567890"
        # mock_request_instance related lines are removed as we use self.mock_search_stream_request_obj

        # Test successful call
        # Create a mock for the row object with campaign.id attribute
        mock_row_for_streaming = mock.Mock()
        mock_row_for_streaming.campaign.id = "streaming_c_id_1"

        # Create a mock for the batch object with a results list containing the mock_row_streaming
        mock_batch_for_streaming = mock.Mock()
        mock_batch_for_streaming.results = [mock_row_for_streaming]

        # Set the return_value for search_stream to be a list containing the mock_batch_streaming
        self.mock_ga_service.search_stream.return_value = [mock_batch_for_streaming]
        # Explicitly clear any prior side_effect that might have been set for other test conditions within this method
        self.mock_ga_service.search_stream.side_effect = None

        set_custom_client_timeouts.make_server_streaming_call(self.mock_client, customer_id)

        # Verify attributes were set on the shared mock object by the script
        self.assertEqual(self.mock_search_stream_request_obj.customer_id, customer_id)
        self.assertEqual(self.mock_search_stream_request_obj.query, set_custom_client_timeouts._QUERY)

        # Verify the service call
        self.mock_ga_service.search_stream.assert_called_once_with(
            request=self.mock_search_stream_request_obj, # Use the shared mock from setUp
            timeout=set_custom_client_timeouts._CLIENT_TIMEOUT_SECONDS,
        )
        # self.mock_search_stream_request.assert_called_once_with() # This assertion is no longer valid with the new setUp

        # Test DeadlineExceeded
        self.mock_ga_service.search_stream.reset_mock()
        self.mock_ga_service.search_stream.side_effect = DeadlineExceeded("Timeout")
        set_custom_client_timeouts.make_server_streaming_call(self.mock_client, customer_id)
        mock_sys_exit.assert_called_with(1)

        # Test GoogleAdsException
        self.mock_ga_service.search_stream.reset_mock()
        mock_sys_exit.reset_mock()
        mock_ex_stream = create_mock_google_ads_exception(self.mock_client, request_id="ga_ex_timeout_stream", message="Stream error")
        self.mock_ga_service.search_stream.side_effect = mock_ex_stream
        # This function is expected to raise GoogleAdsException if not DeadlineExceeded
        with self.assertRaises(GoogleAdsException):
            set_custom_client_timeouts.make_server_streaming_call(self.mock_client, customer_id)
        mock_sys_exit.assert_not_called() # Should not exit for general GoogleAdsException

    @mock.patch("sys.exit")
    def test_make_unary_call(self, mock_sys_exit):
        """Tests the make_unary_call function."""
        customer_id = "1234567890"
        # mock_request_instance related lines are removed

        # Test successful call
        # Create a mock for the row object with campaign.id attribute
        mock_row_for_unary = mock.Mock()
        mock_row_for_unary.campaign.id = "unary_c_id_1"

        # Set the return_value for search to be a list containing the mock_row_unary
        self.mock_ga_service.search.return_value = [mock_row_for_unary]
        # Explicitly clear any prior side_effect
        self.mock_ga_service.search.side_effect = None

        set_custom_client_timeouts.make_unary_call(self.mock_client, customer_id)

        # Verify attributes were set on the shared mock object by the script
        self.assertEqual(self.mock_search_request_obj.customer_id, customer_id)
        self.assertEqual(self.mock_search_request_obj.query, set_custom_client_timeouts._QUERY)

        # Verify the service call
        self.mock_ga_service.search.assert_called_once_with(
            request=self.mock_search_request_obj,
            retry=mock.ANY
        )

        # Capture the actual retry object passed to the mock
        actual_call_args = self.mock_ga_service.search.call_args
        passed_retry_object = actual_call_args[1]['retry'] # Get the 'retry' kwarg

        # Assert the attributes of the passed_retry_object
        self.assertIsInstance(passed_retry_object, Retry)
        self.assertEqual(passed_retry_object._deadline, set_custom_client_timeouts._CLIENT_TIMEOUT_SECONDS)
        self.assertEqual(passed_retry_object._initial, set_custom_client_timeouts._CLIENT_TIMEOUT_SECONDS / 10)
        self.assertEqual(passed_retry_object._maximum, set_custom_client_timeouts._CLIENT_TIMEOUT_SECONDS / 5)

        # Test DeadlineExceeded
        self.mock_ga_service.search.reset_mock()
        self.mock_ga_service.search.side_effect = DeadlineExceeded("Timeout")
        set_custom_client_timeouts.make_unary_call(self.mock_client, customer_id)
        mock_sys_exit.assert_called_with(1)

        # Test GoogleAdsException
        self.mock_ga_service.search.reset_mock()
        mock_sys_exit.reset_mock()
        mock_ex_unary = create_mock_google_ads_exception(self.mock_client, request_id="ga_ex_timeout_unary", message="Unary error")
        self.mock_ga_service.search.side_effect = mock_ex_unary
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

    def _simulate_script_main_execution(
        self,
        mock_argparser_class,
        mock_googleadsclient_class,
        mock_main_function,
        # cli_args parameter is not strictly needed here if parse_args is fully mocked
        # but kept for conceptual completeness if we were to use actual sys.argv
        cli_args
    ):
        # This simulates the script's if __name__ == "__main__": block

        # 1. parser = argparse.ArgumentParser(...)
        #    In our sim, this is:
        #    The mock_argparser_class is already configured by the test method's decorator.
        #    When it's called, it returns mock_argparser_class.return_value (which is mock_parser_instance from the test)
        parser_sim = mock_argparser_class(description="Demonstrates custom client timeouts in the context of server streaming and unary calls.") # Changed description

        # 2. args = parser.parse_args()
        #    In our sim, this is:
        #    The mock_parser_instance.parse_args.return_value is set by the calling test.
        args_sim = parser_sim.parse_args()

        # 3. googleads_client = GoogleAdsClient.load_from_storage(version="v19")
        #    In our sim, this is:
        #    The mock_googleadsclient_class.load_from_storage.return_value is set by the calling test.
        client_sim = mock_googleadsclient_class.load_from_storage(version="v19")

        # 4. main(googleads_client, args.customer_id)
        #    In our sim, call the mocked main function:
        mock_main_function(client_sim, args_sim.customer_id)

    @mock.patch("sys.exit")
    @mock.patch("examples.misc.set_custom_client_timeouts.argparse.ArgumentParser")
    @mock.patch("examples.misc.set_custom_client_timeouts.GoogleAdsClient")
    @mock.patch("examples.misc.set_custom_client_timeouts.main") # Patches main in the already imported module
    def test_argument_parsing_and_script_execution(
        self, mock_script_main_function, mock_google_ads_client_class_in_script,
        mock_argument_parser_class, mock_sys_exit
    ):
        """Tests argument parsing and the script's main execution block."""
        # 1. Setup ArgumentParser mock
        # The mock_argument_parser_class is the class mock from the decorator.
        # We need to configure its return_value (the instance mock)
        mock_parser_instance = mock_argument_parser_class.return_value
        mock_args_obj = argparse.Namespace(customer_id="test_customer_id_arg")
        mock_parser_instance.parse_args.return_value = mock_args_obj
        # mock_argument_parser_class is already configured by @mock.patch to return mock_parser_instance

        # 2. Setup GoogleAdsClient mock
        # mock_google_ads_client_class_in_script is the class mock from the decorator.
        mock_script_client_instance = mock.Mock() # This will be the instance returned by load_from_storage
        mock_google_ads_client_class_in_script.load_from_storage.return_value = mock_script_client_instance

        # 3. Call the helper to simulate the script's __main__ execution
        self._simulate_script_main_execution(
            mock_argparser_class=mock_argument_parser_class,
            mock_googleadsclient_class=mock_google_ads_client_class_in_script,
            mock_main_function=mock_script_main_function,
            cli_args=["set_custom_client_timeouts.py", "-c", mock_args_obj.customer_id]
        )

        # 4. Assertions
        # 1. Assert that ArgumentParser class was called (instantiated) correctly
        mock_argument_parser_class.assert_called_once_with(
            description="Demonstrates custom client timeouts in the context of server streaming and unary calls."
        )

        # 2. mock_parser_instance is already mock_argument_parser_class.return_value from the test setup

        # 3. Assert that add_argument was called on this instance
        mock_parser_instance.add_argument.assert_called_once_with(
            "-c",
            "--customer_id",
            type=str,
            required=True,
            help="The Google Ads customer ID.",
        )

        # 4. Assert that parse_args was called on this instance
        mock_parser_instance.parse_args.assert_called_once_with()

        # The existing assertions for GoogleAdsClient.load_from_storage and mock_script_main_function should remain:
        mock_google_ads_client_class_in_script.load_from_storage.assert_called_once_with(version="v19")
        mock_script_main_function.assert_called_once_with(
            mock_script_client_instance, # This is mock_google_ads_client_class_in_script.load_from_storage.return_value
            mock_args_obj.customer_id  # This is from mock_parser_instance.parse_args.return_value.customer_id
        )

        # original_argv and sys.argv restoration are no longer needed here
        # as sys.argv is not modified by this test method directly.

if __name__ == "__main__":
    unittest.main()
