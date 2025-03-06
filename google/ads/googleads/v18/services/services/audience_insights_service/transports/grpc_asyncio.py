# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
import inspect
import pickle
import logging as std_logging
import warnings
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union

from google.api_core import gapic_v1
from google.api_core import grpc_helpers_async
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.protobuf.json_format import MessageToJson
import google.protobuf.message

import grpc  # type: ignore
import proto  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.ads.googleads.v18.services.types import audience_insights_service
from .base import AudienceInsightsServiceTransport, DEFAULT_CLIENT_INFO

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = std_logging.getLogger(__name__)


class _LoggingClientAIOInterceptor(
    grpc.aio.UnaryUnaryClientInterceptor
):  # pragma: NO COVER
    async def intercept_unary_unary(
        self, continuation, client_call_details, request
    ):
        logging_enabled = CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
            std_logging.DEBUG
        )
        if logging_enabled:  # pragma: NO COVER
            request_metadata = client_call_details.metadata
            if isinstance(request, proto.Message):
                request_payload = type(request).to_json(request)
            elif isinstance(request, google.protobuf.message.Message):
                request_payload = MessageToJson(request)
            else:
                request_payload = (
                    f"{type(request).__name__}: {pickle.dumps(request)}"
                )

            request_metadata = {
                key: (
                    value.decode("utf-8") if isinstance(value, bytes) else value
                )
                for key, value in request_metadata
            }
            grpc_request = {
                "payload": request_payload,
                "requestMethod": "grpc",
                "metadata": dict(request_metadata),
            }
            _LOGGER.debug(
                f"Sending request for {client_call_details.method}",
                extra={
                    "serviceName": "google.ads.googleads.v18.services.AudienceInsightsService",
                    "rpcName": str(client_call_details.method),
                    "request": grpc_request,
                    "metadata": grpc_request["metadata"],
                },
            )
        response = await continuation(client_call_details, request)
        if logging_enabled:  # pragma: NO COVER
            response_metadata = await response.trailing_metadata()
            # Convert gRPC metadata `<class 'grpc.aio._metadata.Metadata'>` to list of tuples
            metadata = (
                dict([(k, str(v)) for k, v in response_metadata])
                if response_metadata
                else None
            )
            result = await response
            if isinstance(result, proto.Message):
                response_payload = type(result).to_json(result)
            elif isinstance(result, google.protobuf.message.Message):
                response_payload = MessageToJson(result)
            else:
                response_payload = (
                    f"{type(result).__name__}: {pickle.dumps(result)}"
                )
            grpc_response = {
                "payload": response_payload,
                "metadata": metadata,
                "status": "OK",
            }
            _LOGGER.debug(
                f"Received response to rpc {client_call_details.method}.",
                extra={
                    "serviceName": "google.ads.googleads.v18.services.AudienceInsightsService",
                    "rpcName": str(client_call_details.method),
                    "response": grpc_response,
                    "metadata": grpc_response["metadata"],
                },
            )
        return response


class AudienceInsightsServiceGrpcAsyncIOTransport(
    AudienceInsightsServiceTransport
):
    """gRPC AsyncIO backend transport for AudienceInsightsService.

    Audience Insights Service helps users find information about
    groups of people and how they can be reached with Google Ads.
    Accessible to allowlisted customers only.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _grpc_channel: aio.Channel
    _stubs: Dict[str, Callable] = {}

    @classmethod
    def create_channel(
        cls,
        host: str = "googleads.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> aio.Channel:
        """Create and return a gRPC AsyncIO channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            aio.Channel: A gRPC AsyncIO channel object.
        """

        return grpc_helpers_async.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    def __init__(
        self,
        *,
        host: str = "googleads.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[
            Union[aio.Channel, Callable[..., aio.Channel]]
        ] = None,
        api_mtls_endpoint: Optional[str] = None,
        client_cert_source: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        ssl_channel_credentials: Optional[grpc.ChannelCredentials] = None,
        client_cert_source_for_mtls: Optional[
            Callable[[], Tuple[bytes, bytes]]
        ] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'googleads.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if a ``channel`` instance is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if a ``channel`` instance is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[Union[aio.Channel, Callable[..., aio.Channel]]]):
                A ``Channel`` instance through which to make calls, or a Callable
                that constructs and returns one. If set to None, ``self.create_channel``
                is used to create the channel. If a Callable is given, it will be called
                with the same arguments as used in ``self.create_channel``.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for the grpc channel. It is ignored if a ``channel`` instance is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure a mutual TLS channel. It is
                ignored if a ``channel`` instance or ``ssl_channel_credentials`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn(
                "client_cert_source is deprecated", DeprecationWarning
            )

        if isinstance(channel, aio.Channel):
            # Ignore credentials if a channel was passed.
            credentials = None
            self._ignore_credentials = True
            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None
        else:
            if api_mtls_endpoint:
                host = api_mtls_endpoint

                # Create SSL credentials with client_cert_source or application
                # default SSL credentials.
                if client_cert_source:
                    cert, key = client_cert_source()
                    self._ssl_channel_credentials = (
                        grpc.ssl_channel_credentials(
                            certificate_chain=cert, private_key=key
                        )
                    )
                else:
                    self._ssl_channel_credentials = (
                        SslCredentials().ssl_credentials
                    )

            else:
                if client_cert_source_for_mtls and not ssl_channel_credentials:
                    cert, key = client_cert_source_for_mtls()
                    self._ssl_channel_credentials = (
                        grpc.ssl_channel_credentials(
                            certificate_chain=cert, private_key=key
                        )
                    )

        # The base transport sets the host, credentials and scopes
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )

        if not self._grpc_channel:
            # initialize with the provided callable or the default channel
            channel_init = channel or type(self).create_channel
            self._grpc_channel = channel_init(
                self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                # Set ``credentials_file`` to ``None`` here as
                # the credentials that we saved earlier should be used.
                credentials_file=None,
                scopes=self._scopes,
                ssl_credentials=self._ssl_channel_credentials,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        self._interceptor = _LoggingClientAIOInterceptor()
        self._grpc_channel._unary_unary_interceptors.append(self._interceptor)
        self._logged_channel = self._grpc_channel
        self._wrap_with_kind = (
            "kind"
            in inspect.signature(gapic_v1.method_async.wrap_method).parameters
        )
        # Wrap messages. This must be done after self._logged_channel exists
        self._prep_wrapped_messages(client_info)

    @property
    def grpc_channel(self) -> aio.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Return the channel from cache.
        return self._grpc_channel

    @property
    def generate_insights_finder_report(
        self,
    ) -> Callable[
        [audience_insights_service.GenerateInsightsFinderReportRequest],
        Awaitable[
            audience_insights_service.GenerateInsightsFinderReportResponse
        ],
    ]:
        r"""Return a callable for the generate insights finder
        report method over gRPC.

        Creates a saved report that can be viewed in the Insights Finder
        tool.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `FieldError <>`__ `HeaderError <>`__
        `InternalError <>`__ `QuotaError <>`__ `RangeError <>`__
        `RequestError <>`__

        Returns:
            Callable[[~.GenerateInsightsFinderReportRequest],
                    Awaitable[~.GenerateInsightsFinderReportResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "generate_insights_finder_report" not in self._stubs:
            self._stubs["generate_insights_finder_report"] = (
                self._logged_channel.unary_unary(
                    "/google.ads.googleads.v18.services.AudienceInsightsService/GenerateInsightsFinderReport",
                    request_serializer=audience_insights_service.GenerateInsightsFinderReportRequest.serialize,
                    response_deserializer=audience_insights_service.GenerateInsightsFinderReportResponse.deserialize,
                )
            )
        return self._stubs["generate_insights_finder_report"]

    @property
    def list_audience_insights_attributes(
        self,
    ) -> Callable[
        [audience_insights_service.ListAudienceInsightsAttributesRequest],
        Awaitable[
            audience_insights_service.ListAudienceInsightsAttributesResponse
        ],
    ]:
        r"""Return a callable for the list audience insights
        attributes method over gRPC.

        Searches for audience attributes that can be used to generate
        insights.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `FieldError <>`__ `HeaderError <>`__
        `InternalError <>`__ `QuotaError <>`__ `RangeError <>`__
        `RequestError <>`__

        Returns:
            Callable[[~.ListAudienceInsightsAttributesRequest],
                    Awaitable[~.ListAudienceInsightsAttributesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_audience_insights_attributes" not in self._stubs:
            self._stubs["list_audience_insights_attributes"] = (
                self._logged_channel.unary_unary(
                    "/google.ads.googleads.v18.services.AudienceInsightsService/ListAudienceInsightsAttributes",
                    request_serializer=audience_insights_service.ListAudienceInsightsAttributesRequest.serialize,
                    response_deserializer=audience_insights_service.ListAudienceInsightsAttributesResponse.deserialize,
                )
            )
        return self._stubs["list_audience_insights_attributes"]

    @property
    def list_insights_eligible_dates(
        self,
    ) -> Callable[
        [audience_insights_service.ListInsightsEligibleDatesRequest],
        Awaitable[audience_insights_service.ListInsightsEligibleDatesResponse],
    ]:
        r"""Return a callable for the list insights eligible dates method over gRPC.

        Lists date ranges for which audience insights data can be
        requested.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `FieldError <>`__ `HeaderError <>`__
        `InternalError <>`__ `QuotaError <>`__ `RangeError <>`__
        `RequestError <>`__

        Returns:
            Callable[[~.ListInsightsEligibleDatesRequest],
                    Awaitable[~.ListInsightsEligibleDatesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_insights_eligible_dates" not in self._stubs:
            self._stubs["list_insights_eligible_dates"] = (
                self._logged_channel.unary_unary(
                    "/google.ads.googleads.v18.services.AudienceInsightsService/ListInsightsEligibleDates",
                    request_serializer=audience_insights_service.ListInsightsEligibleDatesRequest.serialize,
                    response_deserializer=audience_insights_service.ListInsightsEligibleDatesResponse.deserialize,
                )
            )
        return self._stubs["list_insights_eligible_dates"]

    @property
    def generate_audience_composition_insights(
        self,
    ) -> Callable[
        [audience_insights_service.GenerateAudienceCompositionInsightsRequest],
        Awaitable[
            audience_insights_service.GenerateAudienceCompositionInsightsResponse
        ],
    ]:
        r"""Return a callable for the generate audience composition
        insights method over gRPC.

        Returns a collection of attributes that are represented in an
        audience of interest, with metrics that compare each attribute's
        share of the audience with its share of a baseline audience.

        List of thrown errors: `AudienceInsightsError <>`__
        `AuthenticationError <>`__ `AuthorizationError <>`__
        `FieldError <>`__ `HeaderError <>`__ `InternalError <>`__
        `QuotaError <>`__ `RangeError <>`__ `RequestError <>`__

        Returns:
            Callable[[~.GenerateAudienceCompositionInsightsRequest],
                    Awaitable[~.GenerateAudienceCompositionInsightsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "generate_audience_composition_insights" not in self._stubs:
            self._stubs["generate_audience_composition_insights"] = (
                self._logged_channel.unary_unary(
                    "/google.ads.googleads.v18.services.AudienceInsightsService/GenerateAudienceCompositionInsights",
                    request_serializer=audience_insights_service.GenerateAudienceCompositionInsightsRequest.serialize,
                    response_deserializer=audience_insights_service.GenerateAudienceCompositionInsightsResponse.deserialize,
                )
            )
        return self._stubs["generate_audience_composition_insights"]

    @property
    def generate_suggested_targeting_insights(
        self,
    ) -> Callable[
        [audience_insights_service.GenerateSuggestedTargetingInsightsRequest],
        Awaitable[
            audience_insights_service.GenerateSuggestedTargetingInsightsResponse
        ],
    ]:
        r"""Return a callable for the generate suggested targeting
        insights method over gRPC.

        Returns a collection of targeting insights (e.g. targetable
        audiences) that are relevant to the requested audience.

        List of thrown errors: `AudienceInsightsError <>`__
        `AuthenticationError <>`__ `AuthorizationError <>`__
        `FieldError <>`__ `HeaderError <>`__ `InternalError <>`__
        `QuotaError <>`__ `RangeError <>`__ `RequestError <>`__

        Returns:
            Callable[[~.GenerateSuggestedTargetingInsightsRequest],
                    Awaitable[~.GenerateSuggestedTargetingInsightsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "generate_suggested_targeting_insights" not in self._stubs:
            self._stubs["generate_suggested_targeting_insights"] = (
                self._logged_channel.unary_unary(
                    "/google.ads.googleads.v18.services.AudienceInsightsService/GenerateSuggestedTargetingInsights",
                    request_serializer=audience_insights_service.GenerateSuggestedTargetingInsightsRequest.serialize,
                    response_deserializer=audience_insights_service.GenerateSuggestedTargetingInsightsResponse.deserialize,
                )
            )
        return self._stubs["generate_suggested_targeting_insights"]

    @property
    def generate_audience_overlap_insights(
        self,
    ) -> Callable[
        [audience_insights_service.GenerateAudienceOverlapInsightsRequest],
        Awaitable[
            audience_insights_service.GenerateAudienceOverlapInsightsResponse
        ],
    ]:
        r"""Return a callable for the generate audience overlap
        insights method over gRPC.

        Returns a collection of audience attributes along with estimates
        of the overlap between their potential YouTube reach and that of
        a given input attribute.

        List of thrown errors: `AudienceInsightsError <>`__
        `AuthenticationError <>`__ `AuthorizationError <>`__
        `FieldError <>`__ `HeaderError <>`__ `InternalError <>`__
        `QuotaError <>`__ `RangeError <>`__ `RequestError <>`__

        Returns:
            Callable[[~.GenerateAudienceOverlapInsightsRequest],
                    Awaitable[~.GenerateAudienceOverlapInsightsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "generate_audience_overlap_insights" not in self._stubs:
            self._stubs["generate_audience_overlap_insights"] = (
                self._logged_channel.unary_unary(
                    "/google.ads.googleads.v18.services.AudienceInsightsService/GenerateAudienceOverlapInsights",
                    request_serializer=audience_insights_service.GenerateAudienceOverlapInsightsRequest.serialize,
                    response_deserializer=audience_insights_service.GenerateAudienceOverlapInsightsResponse.deserialize,
                )
            )
        return self._stubs["generate_audience_overlap_insights"]

    @property
    def generate_targeting_suggestion_metrics(
        self,
    ) -> Callable[
        [audience_insights_service.GenerateTargetingSuggestionMetricsRequest],
        Awaitable[
            audience_insights_service.GenerateTargetingSuggestionMetricsResponse
        ],
    ]:
        r"""Return a callable for the generate targeting suggestion
        metrics method over gRPC.

        Returns potential reach metrics for targetable audiences.

        This method helps answer questions like "How many Men aged 18+
        interested in Camping can be reached on YouTube?"

        List of thrown errors: `AudienceInsightsError <>`__
        `AuthenticationError <>`__ `AuthorizationError <>`__
        `FieldError <>`__ `HeaderError <>`__ `InternalError <>`__
        `QuotaError <>`__ `RangeError <>`__ `RequestError <>`__

        Returns:
            Callable[[~.GenerateTargetingSuggestionMetricsRequest],
                    Awaitable[~.GenerateTargetingSuggestionMetricsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "generate_targeting_suggestion_metrics" not in self._stubs:
            self._stubs["generate_targeting_suggestion_metrics"] = (
                self._logged_channel.unary_unary(
                    "/google.ads.googleads.v18.services.AudienceInsightsService/GenerateTargetingSuggestionMetrics",
                    request_serializer=audience_insights_service.GenerateTargetingSuggestionMetricsRequest.serialize,
                    response_deserializer=audience_insights_service.GenerateTargetingSuggestionMetricsResponse.deserialize,
                )
            )
        return self._stubs["generate_targeting_suggestion_metrics"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.generate_insights_finder_report: self._wrap_method(
                self.generate_insights_finder_report,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_audience_insights_attributes: self._wrap_method(
                self.list_audience_insights_attributes,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_insights_eligible_dates: self._wrap_method(
                self.list_insights_eligible_dates,
                default_timeout=None,
                client_info=client_info,
            ),
            self.generate_audience_composition_insights: self._wrap_method(
                self.generate_audience_composition_insights,
                default_timeout=None,
                client_info=client_info,
            ),
            self.generate_suggested_targeting_insights: self._wrap_method(
                self.generate_suggested_targeting_insights,
                default_timeout=None,
                client_info=client_info,
            ),
            self.generate_audience_overlap_insights: self._wrap_method(
                self.generate_audience_overlap_insights,
                default_timeout=None,
                client_info=client_info,
            ),
            self.generate_targeting_suggestion_metrics: self._wrap_method(
                self.generate_targeting_suggestion_metrics,
                default_timeout=None,
                client_info=client_info,
            ),
        }

    def _wrap_method(self, func, *args, **kwargs):
        if self._wrap_with_kind:  # pragma: NO COVER
            kwargs["kind"] = self.kind
        return gapic_v1.method_async.wrap_method(func, *args, **kwargs)

    def close(self):
        return self._logged_channel.close()

    @property
    def kind(self) -> str:
        return "grpc_asyncio"


__all__ = ("AudienceInsightsServiceGrpcAsyncIOTransport",)
