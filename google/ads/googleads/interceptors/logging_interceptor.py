# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""A gRPC Interceptor that is responsible for logging requests and responses.

This class is initialized in the GoogleAdsClient and passed into a grpc
intercept_channel whenever a new service is initialized. It intercepts requests
and responses, parses them into a human readable structure and logs them using
the passed in logger instance.
"""

from copy import deepcopy
import json
import logging

from grpc import UnaryUnaryClientInterceptor, UnaryStreamClientInterceptor

from .interceptor import Interceptor
from ..util import set_nested_message_field, get_nested_attr

# The keys in this dict represent messages that have fields that may contain
# sensitive information, such as PII like an email address, that shouldn't
# be logged. The values are a list of dot-delimited field paths on the message
# where the sensitive information may exist. Messages listed here will have
# their sensitive fields redacted in logs when transmitted in the following
# scenarios:
#     1. They are returned as part of a Search or SearchStream request.
#     2. They are returned individually in a Get request.
#     3. They are sent to the API as part of a Mutate request.
_MESSAGES_WITH_SENSITIVE_FIELDS = {
    "CustomerUserAccess": ["email_address", "inviter_user_email_address"],
    "CustomerUserAccessInvitation": ["email_address"],
    "MutateCustomerUserAccessRequest": [
        "operation.update.email_address",
        "operation.update.inviter_user_email_address",
    ],
    "ChangeEvent": ["user_email"],
    "CreateCustomerClientRequest": ["email_address"],
    "Feed": ["places_location_feed_data.email_address"],
}

# This is a list of the names of messages that return search results from the
# API. These messages contain other messages that may contain sensitive
# information that needs to be masked before being logged.
_SEARCH_RESPONSE_MESSAGE_NAMES = [
    "SearchGoogleAdsResponse",
    "SearchGoogleAdsStreamResponse",
]


class LoggingInterceptor(
    Interceptor, UnaryUnaryClientInterceptor, UnaryStreamClientInterceptor
):
    """An interceptor that logs rpc requests and responses."""

    _FULL_REQUEST_LOG_LINE = (
        "Request\n-------\nMethod: {}\nHost: {}\n"
        "Headers: {}\nRequest: {}\n\nResponse\n-------\n"
        "Headers: {}\nResponse: {}\n"
    )
    _FULL_FAULT_LOG_LINE = (
        "Request\n-------\nMethod: {}\nHost: {}\n"
        "Headers: {}\nRequest: {}\n\nResponse\n-------\n"
        "Headers: {}\nFault: {}\n"
    )
    _SUMMARY_LOG_LINE = (
        "Request made: ClientCustomerId: {}, Host: {}, "
        "Method: {}, RequestId: {}, IsFault: {}, "
        "FaultMessage: {}"
    )

    def __init__(self, logger, api_version, endpoint=None):
        """Initializer for the LoggingInterceptor.

        Args:
            logger: An instance of logging.Logger.
            api_version: a str of the API version of the request.
            endpoint: a str specifying the endpoint for requests.
        """
        super().__init__(api_version)
        self.endpoint = endpoint
        self.logger = logger

    def _get_trailing_metadata(self, response):
        """Retrieves trailing metadata from a response object.

        If the exception is a GoogleAdsException the trailing metadata will be
        on its error object, otherwise it will be on the response object.

        Returns:
            A tuple of metadatum representing response header key value pairs.

        Args:
            response: A grpc.Call/grpc.Future instance.
        """
        try:
            trailing_metadata = response.trailing_metadata()

            if not trailing_metadata:
                return self.get_trailing_metadata_from_interceptor_exception(
                    response.exception()
                )

            return trailing_metadata
        except AttributeError:
            return self.get_trailing_metadata_from_interceptor_exception(
                response.exception()
            )

    def _get_initial_metadata(self, client_call_details):
        """Retrieves the initial metadata from client_call_details.

        Returns an empty tuple if metadata isn't present on the
        client_call_details object.

        Returns:
            A tuple of metadatum representing request header key value pairs.

        Args:
            client_call_details: An instance of grpc.ClientCallDetails.
        """
        return getattr(client_call_details, "metadata", tuple())

    def _get_call_method(self, client_call_details):
        """Retrieves the call method from client_call_details.

        Returns None if the method is not present on the client_call_details
        object.

        Returns:
            A str with the call method or None if it isn't present.

        Args:
            client_call_details: An instance of grpc.ClientCallDetails.
        """
        return getattr(client_call_details, "method", None)

    def _get_customer_id(self, request):
        """Retrieves the customer_id from the grpc request.

        Returns None if a customer_id is not present on the request object.

        Returns:
            A str with the customer id from the request or None if it isn't
            present.

        Args:
            request: An instance of a request proto message.
        """
        if hasattr(request, "customer_id"):
            return getattr(request, "customer_id")
        elif hasattr(request, "resource_name"):
            resource_name = getattr(request, "resource_name")
            segments = resource_name.split("/")
            if segments[0] == "customers":
                return segments[1]
        else:
            return None

    def _parse_exception_to_str(self, exception):
        """Parses response exception object to str for logging.

        Returns:
            A str representing a exception from the API.

        Args:
            exception: A grpc.Call instance.
        """
        try:
            # If the exception is from the Google Ads API then the failure
            # attribute will be an instance of GoogleAdsFailure and can be
            # concatenated into a log string.
            return exception.failure
        except AttributeError:
            try:
                # if exception.failure isn't present then it's likely this is a
                # transport error with a .debug_error_string method and the
                # returned JSON string will need to be formatted.
                return self.format_json_object(
                    json.loads(exception.debug_error_string())
                )
            except (AttributeError, ValueError):
                # if both attempts to retrieve serializable error data fail
                # then simply return an empty JSON string
                return "{}"

    def _get_fault_message(self, exception):
        """Retrieves a fault/error message from an exception object.

        Returns None if no error message can be found on the exception.

        Returns:
            A str with an error message or None if one cannot be found.

        Args:
            response: A grpc.Call/grpc.Future instance.
            exception: A grpc.Call instance.
        """
        try:
            return exception.failure.errors[0].message
        except AttributeError:
            try:
                return exception.details()
            except AttributeError:
                return None

    def _log_successful_request(
        self,
        method,
        customer_id,
        metadata_json,
        request_id,
        request,
        trailing_metadata_json,
        response,
    ):
        """Handles logging of a successful request.

        Args:
            method: The method of the request.
            customer_id: The customer ID associated with the request.
            metadata_json: A JSON str of initial_metadata.
            request_id: A unique ID for the request provided in the response.
            request: An instance of a request proto message.
            trailing_metadata_json: A JSON str of trailing_metadata.
            response: A grpc.Call/grpc.Future instance.
        """
        result = _mask_message(response.result(), self._SENSITIVE_INFO_MASK)

        self.logger.debug(
            self._FULL_REQUEST_LOG_LINE.format(
                method,
                self.endpoint,
                metadata_json,
                request,
                trailing_metadata_json,
                result,
            )
        )

        self.logger.info(
            self._SUMMARY_LOG_LINE.format(
                customer_id, self.endpoint, method, request_id, False, None
            )
        )

    def _log_failed_request(
        self,
        method,
        customer_id,
        metadata_json,
        request_id,
        request,
        trailing_metadata_json,
        response,
    ):
        """Handles logging of a failed request.

        Args:
            method: The method of the request.
            customer_id: The customer ID associated with the request.
            metadata_json: A JSON str of initial_metadata.
            request_id: A unique ID for the request provided in the response.
            request: An instance of a request proto message.
            trailing_metadata_json: A JSON str of trailing_metadata.
            response: A JSON str of the response message.
        """
        exception = self._get_error_from_response(response)
        exception_str = self._parse_exception_to_str(exception)
        fault_message = self._get_fault_message(exception)

        self.logger.info(
            self._FULL_FAULT_LOG_LINE.format(
                method,
                self.endpoint,
                metadata_json,
                request,
                trailing_metadata_json,
                exception_str,
            )
        )

        self.logger.warning(
            self._SUMMARY_LOG_LINE.format(
                customer_id,
                self.endpoint,
                method,
                request_id,
                True,
                fault_message,
            )
        )

    def _log_request(self, client_call_details, request, response):
        """Handles logging all requests.

        Args:
            client_call_details: An instance of grpc.ClientCallDetails.
            request: An instance of a request proto message.
            response: A grpc.Call/grpc.Future instance.
        """
        method = self._get_call_method(client_call_details)
        customer_id = self._get_customer_id(request)
        initial_metadata = self._get_initial_metadata(client_call_details)
        initial_metadata_json = self.parse_metadata_to_json(initial_metadata)
        trailing_metadata = self._get_trailing_metadata(response)
        request_id = self.get_request_id_from_metadata(trailing_metadata)
        trailing_metadata_json = self.parse_metadata_to_json(trailing_metadata)
        request = _mask_message(request, self._SENSITIVE_INFO_MASK)

        if response.exception():
            self._log_failed_request(
                method,
                customer_id,
                initial_metadata_json,
                request_id,
                request,
                trailing_metadata_json,
                response,
            )
        else:
            self._log_successful_request(
                method,
                customer_id,
                initial_metadata_json,
                request_id,
                request,
                trailing_metadata_json,
                response,
            )

    def intercept_unary_unary(self, continuation, client_call_details, request):
        """Intercepts and logs API interactions.

        Overrides abstract method defined in grpc.UnaryUnaryClientInterceptor.

        Args:
            continuation: a function to continue the request process.
            client_call_details: a grpc._interceptor._ClientCallDetails
                instance containing request metadata.
            request: a SearchGoogleAdsRequest or SearchGoogleAdsStreamRequest
                message class instance.

        Returns:
            A grpc.Call/grpc.Future instance representing a service response.
        """
        response = continuation(client_call_details, request)

        if self.logger.isEnabledFor(logging.WARNING):
            self._log_request(client_call_details, request, response)

        return response

    def intercept_unary_stream(
        self, continuation, client_call_details, request
    ):
        """Intercepts and logs API interactions for Unary-Stream requests.

        Overrides abstract method defined in grpc.UnaryStreamClientInterceptor.

        Args:
            continuation: a function to continue the request process.
            client_call_details: a grpc._interceptor._ClientCallDetails
                instance containing request metadata.
            request: a SearchGoogleAdsRequest or SearchGoogleAdsStreamRequest
                message class instance.

        Returns:
            A grpc.Call/grpc.Future instance representing a service response.
        """

        def on_rpc_complete(response_future):
            if self.logger.isEnabledFor(logging.WARNING):
                self._log_request(client_call_details, request, response_future)

        response = continuation(client_call_details, request)

        response.add_done_callback(on_rpc_complete)

        return response


def _copy_message(message):
    """Returns a copy of the given message.

    Args:
        message: An object containing information from an API request
            or response.

    Returns:
        A copy of the given message.
    """
    return deepcopy(message)


def _mask_message_fields(field_list, message, mask):
    """Copies the given message and masks sensitive fields.

    Sensitive fields are given as a list of strings and are overridden
    with the word "REDACTED" to protect PII from being logged.

    Args:
        field_list: A list of strings specifying the fields on the message
            that should be masked.
        message: An object containing information from an API request
            or response.
        mask: A str that should replace the sensitive information in the
            message.

    Returns:
        A new instance of the message object with fields copied and masked
            where necessary.
    """
    copy = _copy_message(message)

    for field_path in field_list:
        try:
            # Only mask the field if it's been set on the message.
            if get_nested_attr(copy, field_path):
                set_nested_message_field(copy, field_path, mask)
        except AttributeError:
            # AttributeError is raised when the field is not defined on the
            # message. In this case there's nothing to mask and the field
            # should be skipped.
            break

    return copy


def _mask_google_ads_search_response(message, mask):
    """Copies and masks sensitive data in a Search response

    Response messages include instances of GoogleAdsSearchResponse and
    GoogleAdsSearchStreamResponse.

    Args:
        message: A SearchGoogleAdsResponse or SearchGoogleAdsStreamResponse
            instance.
        mask: A str that should replace the sensitive information in the
            message.

    Returns:
        A copy of the message with sensitive fields masked.
    """
    copy = _copy_message(message)

    for row in copy.results:
        # Each row is an instance of GoogleAdsRow. The ListFields method
        # returns a list of (FieldDescriptor, value) tuples for all fields in
        # the message which are not empty
        row_fields = row._pb.ListFields()
        for field in row_fields:
            field_descriptor = field[0]
            # field_name is the name of the field on the GoogleAdsRow instance,
            # for example "campaign" or "customer_user_access"
            field_name = field_descriptor.name
            # message_name is the name of the message, similar to the class
            # name, for example "Campaign" or "CustomerUserAccess"
            message_name = field_descriptor.message_type.name
            if message_name in _MESSAGES_WITH_SENSITIVE_FIELDS.keys():
                nested_message = getattr(row, field_name)
                masked_message = _mask_message_fields(
                    _MESSAGES_WITH_SENSITIVE_FIELDS[message_name],
                    nested_message,
                    mask,
                )
                # Overwrites the nested message with an exact copy of itself,
                # where sensitive fields have been masked.
                setattr(row, field_name, masked_message)

    return copy


def _mask_message(message, mask):
    """Copies and returns a message with sensitive fields masked.

    Args:
        message: An object containing information from an API request
            or response.
        mask: A str that should replace the sensitive information in the
            message.

    Returns:
        A copy of the message instance with sensitive fields masked.
    """
    class_name = message.__class__.__name__

    if class_name in _SEARCH_RESPONSE_MESSAGE_NAMES:
        return _mask_google_ads_search_response(message, mask)
    elif class_name in _MESSAGES_WITH_SENSITIVE_FIELDS.keys():
        sensitive_fields = _MESSAGES_WITH_SENSITIVE_FIELDS[class_name]
        return _mask_message_fields(sensitive_fields, message, mask)
    else:
        return message
