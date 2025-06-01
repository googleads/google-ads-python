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

# Helper classes for mocking Google Ads API response structures
class MockCampaign:
    def __init__(self, campaign_id):
        self.id = campaign_id

class MockRow:
    def __init__(self, campaign_id):
        self.campaign = MockCampaign(campaign_id)

class MockBatch:
    def __init__(self, rows): # rows is a list of MockRow instances
        self.results = rows

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
        mock_row_streaming = MockRow(campaign_id="streaming_cid_1")
        mock_batch_streaming = MockBatch(rows=[mock_row_streaming])

        self.mock_ga_service.search_stream.return_value = [mock_batch_streaming] # List of MockBatch
        self.mock_ga_service.search_stream.side_effect = None # Ensure no interfering side effect

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
        mock_row_unary = MockRow(campaign_id="unary_cid_1")

        self.mock_ga_service.search.return_value = [mock_row_unary] # List of MockRow
        self.mock_ga_service.search.side_effect = None # Ensure no interfering side effect

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

    @mock.patch("sys.exit")
    @mock.patch("examples.misc.set_custom_client_timeouts.argparse.ArgumentParser")
    @mock.patch("examples.misc.set_custom_client_timeouts.GoogleAdsClient")
    @mock.patch("examples.misc.set_custom_client_timeouts.main")
    def test_argument_parsing_and_script_execution(
        self, mock_script_main_function, mock_google_ads_client_class_in_script,
        mock_argument_parser_class, mock_sys_exit
    ):
        """Tests argument parsing and the script's main execution block."""

        # 1. Configure the mock for ArgumentParser CLASS to return a specific INSTANCE mock
        mock_parser_instance = mock.Mock(name="ArgumentParserInstance")
        mock_argument_parser_class.return_value = mock_parser_instance

        # 2. Configure the INSTANCE mock's parse_args method
        mock_args_obj = argparse.Namespace(customer_id="test_customer_id_arg")
        mock_parser_instance.parse_args.return_value = mock_args_obj

        # 3. Configure the mock for GoogleAdsClient CLASS's load_from_storage method
        mock_script_client_instance = mock.Mock(name="GoogleAdsClientInstance")
        mock_google_ads_client_class_in_script.load_from_storage.return_value = mock_script_client_instance

        # Re-insert sys.argv manipulation for runpy
        original_argv = sys.argv
        sys.argv = ["set_custom_client_timeouts.py", "-c", "test_customer_id_arg"]

        import runpy
        runpy.run_module("examples.misc.set_custom_client_timeouts", run_name="__main__")

        sys.argv = original_argv # Restore

        # --- Assertions ---
        # 1. Assert ArgumentParser class was called
        mock_argument_parser_class.assert_called_once_with(
            description="Demonstrates custom client timeouts in the context of server streaming and unary calls."
        )

        # 2. mock_parser_instance is the object returned by mock_argument_parser_class()
        mock_parser_instance.add_argument.assert_called_once_with(
            "-c",
            "--customer_id",
            type=str,
            required=True,
            help="The Google Ads customer ID.",
        )
        mock_parser_instance.parse_args.assert_called_once_with()

        # 3. Assert GoogleAdsClient.load_from_storage was called
        mock_google_ads_client_class_in_script.load_from_storage.assert_called_once_with(version="v19")

        # 4. Assert the script's main (which is mock_script_main_function) was called
        mock_script_main_function.assert_called_once_with(
            mock_script_client_instance, # This is the return_value of load_from_storage
            "test_customer_id_arg"     # This is from mock_args_obj.customer_id
        )

if __name__ == "__main__":
    unittest.main()
