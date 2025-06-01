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

    mock_failure = mock.Mock(spec_set=["errors"]) # spec_set for stricter mocking

    error_info = mock.Mock()
    error_info.message = message

    # Explicitly create a mock for location
    error_info.location = mock.Mock(spec_set=["field_path_elements"])
    # Set field_path_elements to an empty list (iterable)
    error_info.location.field_path_elements = []

    mock_failure.errors = [error_info]

    return GoogleAdsException(
        error=mock_error_proto,
        call=mock_grpc_call,
        request_id=request_id,
        failure=mock_failure
    )
