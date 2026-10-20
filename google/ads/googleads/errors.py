# Copyright 2018 Google LLC
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
"""Errors used by the Google Ads API library."""

import importlib
import inspect
import re
from typing import Any, Optional

import grpc
import requests
from google.api_core import exceptions as core_exceptions
from proto import Message as ProtobufMessageType

_VERSION_PREFIX = "google.ads.googleads.v"
_VERSION_REGEX = re.compile(r"^google\.ads\.googleads\.(v\d+(?:_\d+)?)(?:\.|$)")


def _get_caller_version() -> str:
    """Determines the Google Ads API version from the call stack.

    Walks the call stack looking for a frame originating from a versioned
    ``google.ads.googleads.<version>`` module. Falls back to
    ``_DEFAULT_VERSION`` if no versioned module is found.

    Returns:
        The detected API version string (e.g., "v25") or ``_DEFAULT_VERSION``.
    """
    frame = inspect.currentframe()
    try:
        if frame is not None:
            frame = frame.f_back
        while frame is not None:
            module_name = frame.f_globals.get("__name__", "")
            if module_name.startswith(_VERSION_PREFIX):
                match = _VERSION_REGEX.match(module_name)
                if match:
                    return match.group(1)
            frame = frame.f_back
    finally:
        del frame
    from google.ads.googleads.client import _DEFAULT_VERSION

    return _DEFAULT_VERSION


class GoogleAdsException(Exception):
    """Exception thrown in response to an API error from GoogleAds servers."""

    def __init__(
        self,
        error: grpc.RpcError,
        call: grpc.Call,
        failure: ProtobufMessageType,
        request_id: str,
    ) -> None:
        """Initializer.

        Args:
            error: the grpc.RpcError raised by an rpc call.
            call: the grpc.Call object containing the details of the rpc call.
            failure: the GoogleAdsFailure instance describing how the
                GoogleAds API call failed.
            request_id: a str request ID associated with the GoogleAds API call.
        """
        self.error: grpc.RpcError = error
        self.call: grpc.Call = call
        self.failure: ProtobufMessageType = failure
        self.request_id: str = request_id


class ResumableUploadErrorAdapter(grpc.RpcError, grpc.Call):
    """
    A concrete implementation of gRPC abstract classes.
    Wraps a requests.Response to mimic a gRPC call for GoogleAdsException.
    """

    def __init__(
        self,
        response: requests.Response,
        mapped_grpc_code: grpc.StatusCode,
        version: str,
    ):
        self._response = response
        self._mapped_code = mapped_grpc_code
        self.version = version

        import importlib

        error_module_path = f"google.ads.googleads.{version}.errors.types.errors"
        error_module = importlib.import_module(error_module_path)

        self._GoogleAdsError = error_module.GoogleAdsError
        self._GoogleAdsFailure = error_module.GoogleAdsFailure
        self._ErrorCode = error_module.ErrorCode

    # --- grpc.Call & grpc.RpcContext Required Methods ---
    def code(self) -> grpc.StatusCode:
        return self._mapped_code

    def details(self) -> str:
        # RUP specifies error details are in the response body
        return self._response.text

    def initial_metadata(self) -> Any:
        return None

    def trailing_metadata(self) -> Any:
        # HTTP headers serve as trailing metadata in RUP
        return tuple(self._response.headers.items())

    def is_active(self) -> bool:
        return False

    def time_remaining(self) -> Optional[float]:
        return None

    def cancel(self) -> None:
        pass

    def add_callback(self, callback: Any) -> None:
        pass


def raise_formatted_ads_exception(
    response: requests.Response, version: Optional[str] = None
):
    """Converts a RUP HTTP response into a rich GoogleAdsException.

    Args:
        response (requests.Response):
            The HTTP response containing error details.
        version (Optional[str]):
            The API version (e.g., "v23") used to import error classes. If not
            provided, it is inferred from the calling service module or falls
            back to the default API version.

    Raises:
        GoogleAdsException:
            A rich exception containing the mapped gRPC status, failure details,
            and request ID.
    """
    if not version:
        version = _get_caller_version()

    # 1. Map HTTP status (e.g., 400) to gRPC status (e.g., INVALID_ARGUMENT)
    core_error = core_exceptions.from_http_response(response)
    grpc_code = core_error.grpc_status_code or grpc.StatusCode.INTERNAL

    # 2. Instantiate the adapter
    adapter = ResumableUploadErrorAdapter(response, grpc_code, version)

    # 3. Build the ErrorCode using the specific oneof member 'request_error'
    e_code = adapter._ErrorCode(request_error=1)

    # 4. Build the GoogleAdsError
    g_error = adapter._GoogleAdsError(message=core_error.message, error_code=e_code)

    # 5. Build the GoogleAdsFailure container
    request_id = response.headers.get("X-Goog-Upload-Status", "unknown")
    failure = adapter._GoogleAdsFailure(errors=[g_error], request_id=request_id)

    # 6. Raise the final exception
    raise GoogleAdsException(
        error=adapter, call=adapter, failure=failure, request_id=request_id
    )


def raise_formatted_for_status(
    response: requests.Response, version: Optional[str] = None
):
    """Replacement for response.raise_for_status() that raises GoogleAdsException.

    Args:
        response (requests.Response):
            The HTTP response to check for errors.
        version (Optional[str]):
            The API version (e.g., "v23"). If not provided, it is inferred from
            the calling service module or falls back to the default API version.

    Raises:
        GoogleAdsException:
            If the response status code indicates an error.
    """
    if not response.ok:
        raise_formatted_ads_exception(response, version)
