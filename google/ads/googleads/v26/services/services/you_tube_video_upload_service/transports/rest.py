# -*- coding: utf-8 -*-
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import logging
import json  # type: ignore

from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.api_core import rest_helpers
from google.api_core import gapic_v1
import urllib.parse
from google.api_core import resumable_transfer
from google.ads.googleads.v26._compat import transcode_request
import google.protobuf

from google.protobuf import json_format

from requests import __version__ as requests_version
import dataclasses
from typing import Any, Callable, Dict, Optional, Sequence, Tuple, Union


from google.ads.googleads.v26.services.types import youtube_video_upload_service


from .rest_base import _BaseYouTubeVideoUploadServiceRestTransport
from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = logging.getLogger(__name__)

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)

DEFAULT_CLIENT_INFO.protobuf_runtime_version = google.protobuf.__version__


class YouTubeVideoUploadServiceRestInterceptor:
    """Interceptor for YouTubeVideoUploadService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the YouTubeVideoUploadServiceRestTransport.

    .. code-block:: python
        class MyCustomYouTubeVideoUploadServiceInterceptor(YouTubeVideoUploadServiceRestInterceptor):
            def pre_create_you_tube_video_upload(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_remove_you_tube_video_upload(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_remove_you_tube_video_upload(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_you_tube_video_upload(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_you_tube_video_upload(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = YouTubeVideoUploadServiceRestTransport(interceptor=MyCustomYouTubeVideoUploadServiceInterceptor())
        client = YouTubeVideoUploadServiceClient(transport=transport)


    """

    def pre_create_you_tube_video_upload(
        self,
        request: youtube_video_upload_service.CreateYouTubeVideoUploadRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        youtube_video_upload_service.CreateYouTubeVideoUploadRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for create_you_tube_video_upload

        Override in a subclass to manipulate the request or metadata
        before they are sent to the YouTubeVideoUploadService server.
        """
        return request, metadata

    def pre_remove_you_tube_video_upload(
        self,
        request: youtube_video_upload_service.RemoveYouTubeVideoUploadRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        youtube_video_upload_service.RemoveYouTubeVideoUploadRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for remove_you_tube_video_upload

        Override in a subclass to manipulate the request or metadata
        before they are sent to the YouTubeVideoUploadService server.
        """
        return request, metadata

    def post_remove_you_tube_video_upload(
        self,
        response: youtube_video_upload_service.RemoveYouTubeVideoUploadResponse,
    ) -> youtube_video_upload_service.RemoveYouTubeVideoUploadResponse:
        """Post-rpc interceptor for remove_you_tube_video_upload

        DEPRECATED. Please use the `post_remove_you_tube_video_upload_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the YouTubeVideoUploadService server but before
        it is returned to user code. This `post_remove_you_tube_video_upload` interceptor runs
        before the `post_remove_you_tube_video_upload_with_metadata` interceptor.
        """
        return response

    def post_remove_you_tube_video_upload_with_metadata(
        self,
        response: youtube_video_upload_service.RemoveYouTubeVideoUploadResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        youtube_video_upload_service.RemoveYouTubeVideoUploadResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for remove_you_tube_video_upload

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the YouTubeVideoUploadService server but before it is returned to user code.

        We recommend only using this `post_remove_you_tube_video_upload_with_metadata`
        interceptor in new development instead of the `post_remove_you_tube_video_upload` interceptor.
        When both interceptors are used, this `post_remove_you_tube_video_upload_with_metadata` interceptor runs after the
        `post_remove_you_tube_video_upload` interceptor. The (possibly modified) response returned by
        `post_remove_you_tube_video_upload` will be passed to
        `post_remove_you_tube_video_upload_with_metadata`.
        """
        return response, metadata

    def pre_update_you_tube_video_upload(
        self,
        request: youtube_video_upload_service.UpdateYouTubeVideoUploadRequest,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        youtube_video_upload_service.UpdateYouTubeVideoUploadRequest,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Pre-rpc interceptor for update_you_tube_video_upload

        Override in a subclass to manipulate the request or metadata
        before they are sent to the YouTubeVideoUploadService server.
        """
        return request, metadata

    def post_update_you_tube_video_upload(
        self,
        response: youtube_video_upload_service.UpdateYouTubeVideoUploadResponse,
    ) -> youtube_video_upload_service.UpdateYouTubeVideoUploadResponse:
        """Post-rpc interceptor for update_you_tube_video_upload

        DEPRECATED. Please use the `post_update_you_tube_video_upload_with_metadata`
        interceptor instead.

        Override in a subclass to read or manipulate the response
        after it is returned by the YouTubeVideoUploadService server but before
        it is returned to user code. This `post_update_you_tube_video_upload` interceptor runs
        before the `post_update_you_tube_video_upload_with_metadata` interceptor.
        """
        return response

    def post_update_you_tube_video_upload_with_metadata(
        self,
        response: youtube_video_upload_service.UpdateYouTubeVideoUploadResponse,
        metadata: Sequence[Tuple[str, Union[str, bytes]]],
    ) -> Tuple[
        youtube_video_upload_service.UpdateYouTubeVideoUploadResponse,
        Sequence[Tuple[str, Union[str, bytes]]],
    ]:
        """Post-rpc interceptor for update_you_tube_video_upload

        Override in a subclass to read or manipulate the response or metadata after it
        is returned by the YouTubeVideoUploadService server but before it is returned to user code.

        We recommend only using this `post_update_you_tube_video_upload_with_metadata`
        interceptor in new development instead of the `post_update_you_tube_video_upload` interceptor.
        When both interceptors are used, this `post_update_you_tube_video_upload_with_metadata` interceptor runs after the
        `post_update_you_tube_video_upload` interceptor. The (possibly modified) response returned by
        `post_update_you_tube_video_upload` will be passed to
        `post_update_you_tube_video_upload_with_metadata`.
        """
        return response, metadata


@dataclasses.dataclass
class YouTubeVideoUploadServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: YouTubeVideoUploadServiceRestInterceptor


class YouTubeVideoUploadServiceRestTransport(
    _BaseYouTubeVideoUploadServiceRestTransport
):
    """REST backend synchronous transport for YouTubeVideoUploadService.

    Service to manage YouTube video uploads.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "googleads.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[
            Callable[[], Tuple[bytes, bytes]]
        ] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[YouTubeVideoUploadServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        NOTE: This REST transport functionality is currently in a beta
        state (preview). We welcome your feedback via a GitHub issue in
        this library's repository. Thank you!

         Args:
             host (Optional[str]):
                  The hostname to connect to (default: 'googleads.googleapis.com').
             credentials (Optional[google.auth.credentials.Credentials]): The
                 authorization credentials to attach to requests. These
                 credentials identify the application to the service; if none
                 are specified, the client will attempt to ascertain the
                 credentials from the environment.

             credentials_file (Optional[str]): Deprecated. A file with credentials that can
                 be loaded with :func:`google.auth.load_credentials_from_file`.
                 This argument is ignored if ``channel`` is provided. This argument will be
                 removed in the next major version of this library.
             scopes (Optional(Sequence[str])): A list of scopes. This argument is
                 ignored if ``channel`` is provided.
             client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                 certificate to configure mutual TLS HTTP channel. It is ignored
                 if ``channel`` is provided.
             quota_project_id (Optional[str]): An optional project to use for billing
                 and quota.
             client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                 The client info used to send a user-agent string along with
                 API requests. If ``None``, then default info will be used.
                 Generally, you only need to set this if you are developing
                 your own client library.
             always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                 be used for service account credentials.
             url_scheme: the protocol scheme for the API endpoint.  Normally
                 "https", but for testing or local servers,
                 "http" can be specified.
             interceptor (Optional[YouTubeVideoUploadServiceRestInterceptor]): Interceptor used
                 to manipulate requests, request metadata, and responses.
             api_audience (Optional[str]): The intended audience for the API calls
                 to the service that will be set when using certain 3rd party
                 authentication flows. Audience is typically a resource identifier.
                 If not set, the host value will be used as a default.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            url_scheme=url_scheme,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = (
            interceptor or YouTubeVideoUploadServiceRestInterceptor()
        )
        self._prep_wrapped_messages(client_info)

    class _CreateYouTubeVideoUpload(
        _BaseYouTubeVideoUploadServiceRestTransport._BaseCreateYouTubeVideoUpload,
        YouTubeVideoUploadServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "YouTubeVideoUploadServiceRestTransport.CreateYouTubeVideoUpload"
            )

        def __call__(
            self,
            request: youtube_video_upload_service.CreateYouTubeVideoUploadRequest,
            *,
            config: Optional[resumable_transfer.ResumableUploadConfig] = None,
            start_retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> resumable_transfer.ResumableUploadSession:
            r"""Call the create you tube video
            upload method over HTTP.

                Args:
                    request (~.youtube_video_upload_service.CreateYouTubeVideoUploadRequest):
                        The request object. Request message for
                    [YouTubeVideoUploadService.CreateYouTubeVideoUpload][google.ads.googleads.v26.services.YouTubeVideoUploadService.CreateYouTubeVideoUpload].
                    config (Optional[google.api_core.resumable_transfer.ResumableUploadConfig]):
                        Optional configuration for the resumable upload session.
                    start_retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried when initiating the resumable upload session.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.resumable_transfer.ResumableUploadSession:
                        An object representing a resumable
                    upload session.

            """
            http_options = (
                _BaseYouTubeVideoUploadServiceRestTransport._BaseCreateYouTubeVideoUpload._get_http_options()
            )
            request, metadata = (
                self._interceptor.pre_create_you_tube_video_upload(
                    request, metadata
                )
            )
            transcoded_request, body, query_params = transcode_request(
                http_options,
                request,
                required_fields_default_values=getattr(
                    _BaseYouTubeVideoUploadServiceRestTransport._BaseCreateYouTubeVideoUpload,
                    "_BaseCreateYouTubeVideoUpload__REQUIRED_FIELDS_DEFAULT_VALUES",
                    None,
                ),
                rest_numeric_enums=False,
            )

            uri = transcoded_request["uri"]
            params = rest_helpers.flatten_query_params(
                query_params, strict=True
            )
            query_string = (
                f"?{urllib.parse.urlencode(params)}" if params else ""
            )
            upload_url = f"{self._host}{uri}{query_string}"
            headers: Dict[str, Any] = {
                **dict(metadata),
                **dict((config.headers or {}) if config else {}),
            }
            headers["Content-Type"] = "application/json"
            if config is None:
                config = resumable_transfer.ResumableUploadConfig(
                    headers=headers
                )
            else:
                config = dataclasses.replace(config, headers=headers)

            session_kwargs: Dict[str, Any] = (
                {"start_timeout": timeout}
                if isinstance(timeout, (int, float))
                else {}
            )
            # ``start_retry`` is used instead of ``retry`` because ``_GapicCallable``
            # consumes the ``retry`` argument before invoking the transport callable
            # and only forwards extra keyword arguments such as ``start_retry``.
            return resumable_transfer.ResumableUploadSession(
                upload_url=upload_url,
                config=config,
                transport=self._session,
                response_type=youtube_video_upload_service.CreateYouTubeVideoUploadResponse,
                start_retry=(
                    start_retry
                    if isinstance(start_retry, retries.Retry)
                    else None
                ),
                request_body=body,
                **session_kwargs,
            )

    class _RemoveYouTubeVideoUpload(
        _BaseYouTubeVideoUploadServiceRestTransport._BaseRemoveYouTubeVideoUpload,
        YouTubeVideoUploadServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "YouTubeVideoUploadServiceRestTransport.RemoveYouTubeVideoUpload"
            )

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(
                    query_params, strict=True
                ),
                data=body,
            )
            return response

        def __call__(
            self,
            request: youtube_video_upload_service.RemoveYouTubeVideoUploadRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> youtube_video_upload_service.RemoveYouTubeVideoUploadResponse:
            r"""Call the remove you tube video
            upload method over HTTP.

                Args:
                    request (~.youtube_video_upload_service.RemoveYouTubeVideoUploadRequest):
                        The request object. Request message for
                    [YouTubeVideoUploadService.RemoveYouTubeVideoUpload][google.ads.googleads.v26.services.YouTubeVideoUploadService.RemoveYouTubeVideoUpload].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.youtube_video_upload_service.RemoveYouTubeVideoUploadResponse:
                        Response message for
                    [YouTubeVideoUploadService.RemoveYouTubeVideoUpload][google.ads.googleads.v26.services.YouTubeVideoUploadService.RemoveYouTubeVideoUpload].

            """

            http_options = (
                _BaseYouTubeVideoUploadServiceRestTransport._BaseRemoveYouTubeVideoUpload._get_http_options()
            )
            request, metadata = (
                self._interceptor.pre_remove_you_tube_video_upload(
                    request, metadata
                )
            )
            transcoded_request, body, query_params = transcode_request(
                http_options,
                request,
                required_fields_default_values=getattr(
                    _BaseYouTubeVideoUploadServiceRestTransport._BaseRemoveYouTubeVideoUpload,
                    "_BaseRemoveYouTubeVideoUpload__REQUIRED_FIELDS_DEFAULT_VALUES",
                    None,
                ),
                rest_numeric_enums=False,
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.ads.googleads.v26.services.YouTubeVideoUploadServiceClient.RemoveYouTubeVideoUpload",
                    extra={
                        "serviceName": "google.ads.googleads.v26.services.YouTubeVideoUploadService",
                        "rpcName": "RemoveYouTubeVideoUpload",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = YouTubeVideoUploadServiceRestTransport._RemoveYouTubeVideoUpload._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = (
                youtube_video_upload_service.RemoveYouTubeVideoUploadResponse()
            )
            pb_resp = youtube_video_upload_service.RemoveYouTubeVideoUploadResponse.pb(
                resp
            )

            json_format.Parse(
                response.content, pb_resp, ignore_unknown_fields=True
            )

            resp = self._interceptor.post_remove_you_tube_video_upload(resp)
            response_metadata = [
                (k, str(v)) for k, v in response.headers.items()
            ]
            resp, _ = (
                self._interceptor.post_remove_you_tube_video_upload_with_metadata(
                    resp, response_metadata
                )
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = youtube_video_upload_service.RemoveYouTubeVideoUploadResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.ads.googleads.v26.services.YouTubeVideoUploadServiceClient.remove_you_tube_video_upload",
                    extra={
                        "serviceName": "google.ads.googleads.v26.services.YouTubeVideoUploadService",
                        "rpcName": "RemoveYouTubeVideoUpload",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    class _UpdateYouTubeVideoUpload(
        _BaseYouTubeVideoUploadServiceRestTransport._BaseUpdateYouTubeVideoUpload,
        YouTubeVideoUploadServiceRestStub,
    ):
        def __hash__(self):
            return hash(
                "YouTubeVideoUploadServiceRestTransport.UpdateYouTubeVideoUpload"
            )

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(
                    query_params, strict=True
                ),
                data=body,
            )
            return response

        def __call__(
            self,
            request: youtube_video_upload_service.UpdateYouTubeVideoUploadRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
        ) -> youtube_video_upload_service.UpdateYouTubeVideoUploadResponse:
            r"""Call the update you tube video
            upload method over HTTP.

                Args:
                    request (~.youtube_video_upload_service.UpdateYouTubeVideoUploadRequest):
                        The request object. Request message for
                    [YouTubeVideoUploadService.UpdateYouTubeVideoUpload][google.ads.googleads.v26.services.YouTubeVideoUploadService.UpdateYouTubeVideoUpload].
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                        sent along with the request as metadata. Normally, each value must be of type `str`,
                        but for metadata keys ending with the suffix `-bin`, the corresponding values must
                        be of type `bytes`.

                Returns:
                    ~.youtube_video_upload_service.UpdateYouTubeVideoUploadResponse:
                        Response message for
                    [YouTubeVideoUploadService.UpdateYouTubeVideoUpload][google.ads.googleads.v26.services.YouTubeVideoUploadService.UpdateYouTubeVideoUpload].

            """

            http_options = (
                _BaseYouTubeVideoUploadServiceRestTransport._BaseUpdateYouTubeVideoUpload._get_http_options()
            )
            request, metadata = (
                self._interceptor.pre_update_you_tube_video_upload(
                    request, metadata
                )
            )
            transcoded_request, body, query_params = transcode_request(
                http_options,
                request,
                required_fields_default_values=getattr(
                    _BaseYouTubeVideoUploadServiceRestTransport._BaseUpdateYouTubeVideoUpload,
                    "_BaseUpdateYouTubeVideoUpload__REQUIRED_FIELDS_DEFAULT_VALUES",
                    None,
                ),
                rest_numeric_enums=False,
            )

            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                request_url = "{host}{uri}".format(
                    host=self._host, uri=transcoded_request["uri"]
                )
                method = transcoded_request["method"]
                try:
                    request_payload = type(request).to_json(request)
                except:
                    request_payload = None
                http_request = {
                    "payload": request_payload,
                    "requestMethod": method,
                    "requestUrl": request_url,
                    "headers": dict(metadata),
                }
                _LOGGER.debug(
                    f"Sending request for google.ads.googleads.v26.services.YouTubeVideoUploadServiceClient.UpdateYouTubeVideoUpload",
                    extra={
                        "serviceName": "google.ads.googleads.v26.services.YouTubeVideoUploadService",
                        "rpcName": "UpdateYouTubeVideoUpload",
                        "httpRequest": http_request,
                        "metadata": http_request["headers"],
                    },
                )

            # Send the request
            response = YouTubeVideoUploadServiceRestTransport._UpdateYouTubeVideoUpload._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = (
                youtube_video_upload_service.UpdateYouTubeVideoUploadResponse()
            )
            pb_resp = youtube_video_upload_service.UpdateYouTubeVideoUploadResponse.pb(
                resp
            )

            json_format.Parse(
                response.content, pb_resp, ignore_unknown_fields=True
            )

            resp = self._interceptor.post_update_you_tube_video_upload(resp)
            response_metadata = [
                (k, str(v)) for k, v in response.headers.items()
            ]
            resp, _ = (
                self._interceptor.post_update_you_tube_video_upload_with_metadata(
                    resp, response_metadata
                )
            )
            if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
                logging.DEBUG
            ):  # pragma: NO COVER
                try:
                    response_payload = youtube_video_upload_service.UpdateYouTubeVideoUploadResponse.to_json(
                        response
                    )
                except:
                    response_payload = None
                http_response = {
                    "payload": response_payload,
                    "headers": dict(response.headers),
                    "status": response.status_code,
                }
                _LOGGER.debug(
                    "Received response for google.ads.googleads.v26.services.YouTubeVideoUploadServiceClient.update_you_tube_video_upload",
                    extra={
                        "serviceName": "google.ads.googleads.v26.services.YouTubeVideoUploadService",
                        "rpcName": "UpdateYouTubeVideoUpload",
                        "metadata": http_response["headers"],
                        "httpResponse": http_response,
                    },
                )
            return resp

    @property
    def create_you_tube_video_upload(
        self,
    ) -> Callable[
        [youtube_video_upload_service.CreateYouTubeVideoUploadRequest],
        resumable_transfer.ResumableUploadSession,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateYouTubeVideoUpload(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def remove_you_tube_video_upload(
        self,
    ) -> Callable[
        [youtube_video_upload_service.RemoveYouTubeVideoUploadRequest],
        youtube_video_upload_service.RemoveYouTubeVideoUploadResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._RemoveYouTubeVideoUpload(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_you_tube_video_upload(
        self,
    ) -> Callable[
        [youtube_video_upload_service.UpdateYouTubeVideoUploadRequest],
        youtube_video_upload_service.UpdateYouTubeVideoUploadResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateYouTubeVideoUpload(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("YouTubeVideoUploadServiceRestTransport",)
