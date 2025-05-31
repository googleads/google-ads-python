import pytest
import time
from unittest.mock import MagicMock, patch

# Local application imports (these trigger the problematic import if not mocked above)
from examples.custom_logging_interceptor.cloud_logging_interceptor import CloudLoggingInterceptor
from google.ads.googleads.interceptors import LoggingInterceptor # This is fine


# Mock a GRPC Call/Future object.
class MockFuture:
    def __init__(self, result=None, exception=None):
        self._result = result
        self._exception = exception
        self._callbacks = []

    def result(self):
        if self._exception:
            raise self._exception
        return self._result

    def exception(self):
        return self._exception

    def add_done_callback(self, fn):
        self._callbacks.append(fn)

    def run_callbacks(self):
        for callback in self._callbacks:
            callback(self)

    # Add a dummy cancel method
    def cancel(self):
        pass

    # Add a dummy cancelled method
    def cancelled(self):
        return False

    # Add a dummy running method
    def running(self):
        return False

    # Add a dummy done method
    def done(self):
        return True

    # Add a dummy set_result method
    def set_result(self, result):
        self._result = result

    # Add a dummy set_exception method
    def set_exception(self, exception):
        self._exception = exception

    # Add dummy methods to mimic grpc.Call attributes/methods if needed by the interceptor
    def initial_metadata(self):
        return (('request-id', 'test-request-id'),)

    def trailing_metadata(self):
        return (('foo', 'bar'),)

    def code(self):
        # This part might need adjustment if grpc.StatusCode is not available
        # For now, let's assume it might be available or this mock won't be hit
        # in a way that breaks tests if grpc is not installed directly in test env
        try:
            import grpc
            return grpc.StatusCode.OK if not self._exception else grpc.StatusCode.INTERNAL
        except ImportError:
            # Fallback if grpc is not importable
            return 0 if not self._exception else 14 # 0 for OK, 14 for INTERNAL

    def details(self):
        return "OK" if not self._exception else "Internal error"


@pytest.fixture
def mock_cloud_logging_components(): # Renamed for clarity
    with patch("google.cloud.logging.Client") as mock_client_constructor:
        # This is the mock for the google.cloud.logging.Client() instance
        mock_logging_client_instance = MagicMock(name="mock_logging_client_instance")
        mock_client_constructor.return_value = mock_logging_client_instance

        # This is the mock for the logger object that interceptor.logger will hold
        mock_interceptor_logger = MagicMock(name="mock_interceptor_logger")

        # This is the mock for the .logger() method on the client instance
        # When mock_logging_client_instance.logger("cloud_logging") is called,
        # it will return mock_interceptor_logger.
        mock_logger_method_on_client = MagicMock(name="mock_logger_method_on_client", return_value=mock_interceptor_logger)
        mock_logging_client_instance.logger = mock_logger_method_on_client

        yield {
            "mock_client_constructor": mock_client_constructor, # The class mock
            "mock_logging_client_instance": mock_logging_client_instance, # The instance of logging.Client()
            "mock_logger_method_on_client": mock_logger_method_on_client, # The method called on the instance
            "mock_interceptor_logger": mock_interceptor_logger # The logger returned and used by the interceptor
        }

@pytest.fixture
def interceptor(mock_cloud_logging_components): # Use the new fixture
    # CloudLoggingInterceptor will call google.cloud.logging.Client(),
    # which is mock_client_constructor. It returns mock_logging_client_instance.
    # Then it calls .logger("cloud_logging") on that, which is mock_logger_method_on_client.
    # This returns mock_interceptor_logger, which is assigned to self.logger.
    return CloudLoggingInterceptor(api_version="v19")

def test_interceptor_init(interceptor, mock_cloud_logging_components):
    assert interceptor._api_version == "v19"
    # interceptor.logger should be the mock_interceptor_logger
    assert interceptor.logger == mock_cloud_logging_components["mock_interceptor_logger"]
    # The method mock_logging_client_instance.logger() should have been called
    mock_cloud_logging_components["mock_logger_method_on_client"].assert_called_once_with("cloud_logging")


def test_log_successful_request(interceptor, mock_cloud_logging_components):
    mock_interceptor_logger = mock_cloud_logging_components["mock_interceptor_logger"]
    method = "/google.ads.googleads.v19.services.GoogleAdsService/SearchStream"
    customer_id = "1234567890"
    metadata_json = (('host', 'googleads.googleapis.com'),) # simplified metadata
    request_id = "test_request_id_success"
    request = MagicMock()
    request.__str__ = MagicMock(return_value="request_str")
    trailing_metadata_json = (('trailing', 'data'),) # simplified metadata

    # Mock response and its result method
    mock_response_message = MagicMock()
    mock_response_message.__str__ = MagicMock(return_value="response_str")

    response_future = MockFuture(result=mock_response_message)

    # Mock retrieve_and_mask_result
    interceptor.retrieve_and_mask_result = MagicMock(return_value=mock_response_message)

    # Simulate rpc_start and rpc_end as they are set in intercept_unary_* methods
    interceptor.rpc_start = time.perf_counter()
    time.sleep(0.001) # Simulate some work
    interceptor.rpc_end = time.perf_counter()

    interceptor.log_successful_request(
        method,
        customer_id,
        metadata_json,
        request_id,
        request,
        trailing_metadata_json,
        response_future,
    )

    assert mock_interceptor_logger.log_struct.call_count == 2

    debug_log_call = mock_interceptor_logger.log_struct.call_args_list[0]
    info_log_call = mock_interceptor_logger.log_struct.call_args_list[1]

    expected_debug_log = {
        "method": method,
        "host": metadata_json,
        "request_id": request_id,
        "request": "request_str",
        "headers": trailing_metadata_json,
        "response": "response_str", # Based on mocked retrieve_and_mask_result
        "is_fault": False,
        "elapsed_ms": pytest.approx((interceptor.rpc_end - interceptor.rpc_start) * 1000, rel=1e-1),
    }
    assert debug_log_call[0][0] == expected_debug_log
    assert debug_log_call[1]["severity"] == "DEBUG"

    expected_info_log = {
        "customer_id": customer_id,
        "method": method,
        "request_id": request_id,
        "is_fault": False,
        "api_version": "v19",
    }
    assert info_log_call[0][0] == expected_info_log
    assert info_log_call[1]["severity"] == "INFO"
    interceptor.retrieve_and_mask_result.assert_called_once_with(response_future)


def test_log_failed_request(interceptor, mock_cloud_logging_components):
    mock_interceptor_logger = mock_cloud_logging_components["mock_interceptor_logger"]
    method = "/google.ads.googleads.v19.services.GoogleAdsService/Mutate"
    customer_id = "1234567890"
    metadata_json = (('host', 'googleads.googleapis.com'),)
    request_id = "test_request_id_failure"
    request = MagicMock()
    request.__str__ = MagicMock(return_value="failed_request_str")
    trailing_metadata_json = (('trailing', 'data_failure'),)

    # Mock a GoogleAdsException style error
    mock_exception = MagicMock()
    mock_exception.trailing_metadata = MagicMock(return_value=trailing_metadata_json)
    # Mock the methods called by _get_error_from_response, _parse_exception_to_str, _get_fault_message
    interceptor._get_error_from_response = MagicMock(return_value=mock_exception)
    interceptor._parse_exception_to_str = MagicMock(return_value="exception_details_str")
    interceptor._get_fault_message = MagicMock(return_value="fault_message_str")

    response_future = MockFuture(exception=mock_exception)
    interceptor.endpoint = "googleads.googleapis.com" # Set as it's used in log_failed_request

    interceptor.log_failed_request(
        method,
        customer_id,
        metadata_json,
        request_id,
        request,
        trailing_metadata_json, # This is passed directly, but also on exception in real scenario
        response_future, # The response_future itself is passed
    )

    assert mock_interceptor_logger.log_struct.call_count == 2
    info_log_call = mock_interceptor_logger.log_struct.call_args_list[0]
    error_log_call = mock_interceptor_logger.log_struct.call_args_list[1]

    expected_info_log = {
        "method": method,
        "endpoint": "googleads.googleapis.com",
        "host": metadata_json,
        "request_id": request_id,
        "request": "failed_request_str",
        "headers": trailing_metadata_json,
        "exception": "exception_details_str",
        "is_fault": True,
    }
    assert info_log_call[0][0] == expected_info_log
    assert info_log_call[1]["severity"] == "INFO"

    expected_error_log = {
        "method": method,
        "endpoint": "googleads.googleapis.com",
        "request_id": request_id,
        "customer_id": customer_id,
        "is_fault": True,
        "fault_message": "fault_message_str",
    }
    assert error_log_call[0][0] == expected_error_log
    assert error_log_call[1]["severity"] == "ERROR"
    interceptor._get_error_from_response.assert_called_once_with(response_future)
    interceptor._parse_exception_to_str.assert_called_once_with(mock_exception)
    interceptor._get_fault_message.assert_called_once_with(mock_exception)


@patch.object(CloudLoggingInterceptor, 'log_request') # Patching the instance method
def test_intercept_unary_unary(mock_log_request, interceptor):
    mock_continuation = MagicMock()
    mock_client_call_details = MagicMock()
    mock_request = MagicMock()

    # Mock the continuation to return a MockFuture
    mock_response_future = MockFuture(result="unary_response")
    mock_continuation.return_value = mock_response_future

    response = interceptor.intercept_unary_unary(
        mock_continuation, mock_client_call_details, mock_request
    )

    assert response == mock_response_future
    mock_continuation.assert_called_once_with(mock_client_call_details, mock_request)

    # Simulate the callback being run
    assert hasattr(response, '_callbacks'), "MockFuture should have _callbacks list"
    assert len(response._callbacks) > 0, "A callback should have been added"

    # Check that rpc_start was set
    assert hasattr(interceptor, 'rpc_start')
    start_time = interceptor.rpc_start
    assert isinstance(start_time, float)

    # Run callbacks to simulate completion
    response.run_callbacks()

    # Check that rpc_end was set after callback
    assert hasattr(interceptor, 'rpc_end')
    end_time = interceptor.rpc_end
    assert isinstance(end_time, float)
    assert end_time >= start_time

    mock_log_request.assert_called_once_with(
        mock_client_call_details, mock_request, response
    )

@patch.object(CloudLoggingInterceptor, 'log_request') # Patching the instance method
def test_intercept_unary_stream(mock_log_request, interceptor):
    mock_continuation = MagicMock()
    mock_client_call_details = MagicMock()
    mock_request = MagicMock()

    # Mock the continuation to return a mock response wrapper that has get_cache and add_done_callback
    mock_response_wrapper = MagicMock()
    mock_response_wrapper.get_cache = MagicMock(return_value="stream_cache")

    # We need add_done_callback on the wrapper itself for unary-stream
    # Let's make it behave like our MockFuture for callback handling for simplicity here
    callback_list = []
    def add_cb(cb):
        callback_list.append(cb)
    def run_cbs():
        # Simulate a future-like object being passed to the callback
        future_like = MockFuture()
        for cb in callback_list:
            cb(future_like)

    mock_response_wrapper.add_done_callback = add_cb
    mock_continuation.return_value = mock_response_wrapper

    response = interceptor.intercept_unary_stream(
        mock_continuation, mock_client_call_details, mock_request
    )

    assert response == mock_response_wrapper
    mock_continuation.assert_called_once_with(mock_client_call_details, mock_request)
    assert interceptor._cache == "stream_cache"

    # Check that rpc_start was set
    assert hasattr(interceptor, 'rpc_start')
    start_time = interceptor.rpc_start
    assert isinstance(start_time, float)

    # Simulate the callback being run by manually calling our run_cbs
    run_cbs()

    # Check that rpc_end was set after callback
    assert hasattr(interceptor, 'rpc_end')
    end_time = interceptor.rpc_end
    assert isinstance(end_time, float)
    assert end_time >= start_time

    # The callback for unary-stream passes the response_future (which is the argument to the callback)
    # to log_request.
    # We need to ensure log_request was called with the object passed to the callback.
    # In our run_cbs, we used a new MockFuture() instance.
    assert mock_log_request.call_count == 1
    args, _ = mock_log_request.call_args
    assert args[0] == mock_client_call_details
    assert args[1] == mock_request
    assert isinstance(args[2], MockFuture) # It was called with the future-like object from callback
