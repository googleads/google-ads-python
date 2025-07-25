# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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

from google.ads.googleads.v20.services.types import google_ads_service
from .base import GoogleAdsServiceTransport, DEFAULT_CLIENT_INFO

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
                    "serviceName": "google.ads.googleads.v20.services.GoogleAdsService",
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
                    "serviceName": "google.ads.googleads.v20.services.GoogleAdsService",
                    "rpcName": str(client_call_details.method),
                    "response": grpc_response,
                    "metadata": grpc_response["metadata"],
                },
            )
        return response


class GoogleAdsServiceGrpcAsyncIOTransport(GoogleAdsServiceTransport):
    """gRPC AsyncIO backend transport for GoogleAdsService.

    Service to fetch data and metrics across resources.

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
    def search(
        self,
    ) -> Callable[
        [google_ads_service.SearchGoogleAdsRequest],
        Awaitable[google_ads_service.SearchGoogleAdsResponse],
    ]:
        r"""Return a callable for the search method over gRPC.

        Returns all rows that match the search query.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `ChangeEventError <>`__
        `ChangeStatusError <>`__ `ClickViewError <>`__
        `HeaderError <>`__ `InternalError <>`__ `QueryError <>`__
        `QuotaError <>`__ `RequestError <>`__

        Returns:
            Callable[[~.SearchGoogleAdsRequest],
                    Awaitable[~.SearchGoogleAdsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "search" not in self._stubs:
            self._stubs["search"] = self._logged_channel.unary_unary(
                "/google.ads.googleads.v20.services.GoogleAdsService/Search",
                request_serializer=google_ads_service.SearchGoogleAdsRequest.serialize,
                response_deserializer=google_ads_service.SearchGoogleAdsResponse.deserialize,
            )
        return self._stubs["search"]

    @property
    def search_stream(
        self,
    ) -> Callable[
        [google_ads_service.SearchGoogleAdsStreamRequest],
        Awaitable[google_ads_service.SearchGoogleAdsStreamResponse],
    ]:
        r"""Return a callable for the search stream method over gRPC.

        Returns all rows that match the search stream query.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `ChangeEventError <>`__
        `ChangeStatusError <>`__ `ClickViewError <>`__
        `HeaderError <>`__ `InternalError <>`__ `QueryError <>`__
        `QuotaError <>`__ `RequestError <>`__

        Returns:
            Callable[[~.SearchGoogleAdsStreamRequest],
                    Awaitable[~.SearchGoogleAdsStreamResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "search_stream" not in self._stubs:
            self._stubs["search_stream"] = self._logged_channel.unary_stream(
                "/google.ads.googleads.v20.services.GoogleAdsService/SearchStream",
                request_serializer=google_ads_service.SearchGoogleAdsStreamRequest.serialize,
                response_deserializer=google_ads_service.SearchGoogleAdsStreamResponse.deserialize,
            )
        return self._stubs["search_stream"]

    @property
    def mutate(
        self,
    ) -> Callable[
        [google_ads_service.MutateGoogleAdsRequest],
        Awaitable[google_ads_service.MutateGoogleAdsResponse],
    ]:
        r"""Return a callable for the mutate method over gRPC.

        Creates, updates, or removes resources. This method supports
        atomic transactions with multiple types of resources. For
        example, you can atomically create a campaign and a campaign
        budget, or perform up to thousands of mutates atomically.

        This method is essentially a wrapper around a series of mutate
        methods. The only features it offers over calling those methods
        directly are:

        -  Atomic transactions
        -  Temp resource names (described below)
        -  Somewhat reduced latency over making a series of mutate calls

        Note: Only resources that support atomic transactions are
        included, so this method can't replace all calls to individual
        services.

        Atomic Transaction Benefits
        ---------------------------

        Atomicity makes error handling much easier. If you're making a
        series of changes and one fails, it can leave your account in an
        inconsistent state. With atomicity, you either reach the chosen
        state directly, or the request fails and you can retry.

        Temp Resource Names
        -------------------

        Temp resource names are a special type of resource name used to
        create a resource and reference that resource in the same
        request. For example, if a campaign budget is created with
        ``resource_name`` equal to ``customers/123/campaignBudgets/-1``,
        that resource name can be reused in the ``Campaign.budget``
        field in the same request. That way, the two resources are
        created and linked atomically.

        To create a temp resource name, put a negative number in the
        part of the name that the server would normally allocate.

        Note:

        -  Resources must be created with a temp name before the name
           can be reused. For example, the previous
           CampaignBudget+Campaign example would fail if the mutate
           order was reversed.
        -  Temp names are not remembered across requests.
        -  There's no limit to the number of temp names in a request.
        -  Each temp name must use a unique negative number, even if the
           resource types differ.

        Latency
        -------

        It's important to group mutates by resource type or the request
        may time out and fail. Latency is roughly equal to a series of
        calls to individual mutate methods, where each change in
        resource type is a new call. For example, mutating 10 campaigns
        then 10 ad groups is like 2 calls, while mutating 1 campaign, 1
        ad group, 1 campaign, 1 ad group is like 4 calls.

        List of thrown errors: `AdCustomizerError <>`__ `AdError <>`__
        `AdGroupAdError <>`__ `AdGroupCriterionError <>`__
        `AdGroupError <>`__ `AssetError <>`__ `AuthenticationError <>`__
        `AuthorizationError <>`__ `BiddingError <>`__
        `CampaignBudgetError <>`__ `CampaignCriterionError <>`__
        `CampaignError <>`__ `CampaignExperimentError <>`__
        `CampaignSharedSetError <>`__ `CollectionSizeError <>`__
        `ContextError <>`__ `ConversionActionError <>`__
        `CriterionError <>`__ `CustomerFeedError <>`__
        `DatabaseError <>`__ `DateError <>`__ `DateRangeError <>`__
        `DistinctError <>`__ `ExtensionFeedItemError <>`__
        `ExtensionSettingError <>`__ `FeedAttributeReferenceError <>`__
        `FeedError <>`__ `FeedItemError <>`__ `FeedItemSetError <>`__
        `FieldError <>`__ `FieldMaskError <>`__
        `FunctionParsingError <>`__ `HeaderError <>`__ `ImageError <>`__
        `InternalError <>`__ `KeywordPlanAdGroupKeywordError <>`__
        `KeywordPlanCampaignError <>`__ `KeywordPlanError <>`__
        `LabelError <>`__ `ListOperationError <>`__
        `MediaUploadError <>`__ `MutateError <>`__
        `NewResourceCreationError <>`__ `NullError <>`__
        `OperationAccessDeniedError <>`__ `PolicyFindingError <>`__
        `PolicyViolationError <>`__ `QuotaError <>`__ `RangeError <>`__
        `RequestError <>`__ `ResourceCountLimitExceededError <>`__
        `SettingError <>`__ `SharedSetError <>`__ `SizeLimitError <>`__
        `StringFormatError <>`__ `StringLengthError <>`__
        `UrlFieldError <>`__ `UserListError <>`__
        `YoutubeVideoRegistrationError <>`__

        Returns:
            Callable[[~.MutateGoogleAdsRequest],
                    Awaitable[~.MutateGoogleAdsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "mutate" not in self._stubs:
            self._stubs["mutate"] = self._logged_channel.unary_unary(
                "/google.ads.googleads.v20.services.GoogleAdsService/Mutate",
                request_serializer=google_ads_service.MutateGoogleAdsRequest.serialize,
                response_deserializer=google_ads_service.MutateGoogleAdsResponse.deserialize,
            )
        return self._stubs["mutate"]

    def _prep_wrapped_messages(self, client_info):
        """Precompute the wrapped methods, overriding the base class method to use async wrappers."""
        self._wrapped_methods = {
            self.search: self._wrap_method(
                self.search,
                default_timeout=None,
                client_info=client_info,
            ),
            self.search_stream: self._wrap_method(
                self.search_stream,
                default_timeout=None,
                client_info=client_info,
            ),
            self.mutate: self._wrap_method(
                self.mutate,
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


__all__ = ("GoogleAdsServiceGrpcAsyncIOTransport",)
