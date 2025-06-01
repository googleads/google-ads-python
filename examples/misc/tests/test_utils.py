from unittest import mock
from google.ads.googleads.errors import GoogleAdsException

def create_mock_google_ads_exception(mock_client, request_id="test_request_id", message="Test GoogleAdsException message"):
    """
    Creates a mock GoogleAdsException instance.

    Args:
        mock_client: A mock GoogleAdsClient instance that has get_type method.
        request_id: The request ID for the exception.
        message: The error message for the failure.

    Returns:
        A mock GoogleAdsException instance.
    """
    mock_error_proto = mock.Mock() # Represents the main error structure in the gRPC sense
    # If the code being tested accesses error_proto.code().name, mock it:
    # mock_error_proto.code.return_value.name = "MOCK_GRPC_ERROR"

    mock_grpc_call = mock.Mock() # Represents the gRPC call object

    mock_failure = mock_client.get_type("GoogleAdsFailure")() # Instantiate

    error_info = mock_client.get_type("ErrorInfo")() # Instantiate
    error_info.message = message

    # If location details are needed by any error handler:
    # error_location = mock_client.get_type("ErrorLocation")()
    # field_path_element = error_location.field_path_elements.add()
    # field_path_element.field_name = "mock_field"
    # error_info.location = error_location

    mock_failure.errors = [error_info]

    return GoogleAdsException(
        error_pb=mock_error_proto,
        call=mock_grpc_call,
        request_id=request_id,
        failure_pb=mock_failure
    )
