# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
import warnings
from typing import Callable, Dict, Optional, Sequence, Tuple

from google.api_core import grpc_helpers  # type: ignore
from google.api_core import gapic_v1  # type: ignore
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore

from google.ads.googleads.v8.services.types import google_ads_service
from .base import GoogleAdsServiceTransport, DEFAULT_CLIENT_INFO


class GoogleAdsServiceGrpcTransport(GoogleAdsServiceTransport):
    """gRPC backend transport for GoogleAdsService.

    Service to fetch data and metrics across resources.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    def __init__(
        self,
        *,
        host: str = "googleads.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Sequence[str] = None,
        channel: grpc.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        ssl_channel_credentials: grpc.ChannelCredentials = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            channel (Optional[grpc.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or applicatin default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for grpc channel. It is ignored if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
          google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
              creation failed for any reason.
        """
        self._ssl_channel_credentials = ssl_channel_credentials

        if channel:
            # Sanity check: Ensure that channel and credentials are not both
            # provided.
            credentials = False

            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None
        elif api_mtls_endpoint:
            warnings.warn(
                "api_mtls_endpoint and client_cert_source are deprecated",
                DeprecationWarning,
            )

            host = (
                api_mtls_endpoint
                if ":" in api_mtls_endpoint
                else api_mtls_endpoint + ":443"
            )

            if credentials is None:
                credentials, _ = google.auth.default(
                    scopes=self.AUTH_SCOPES, quota_project_id=quota_project_id
                )

            # Create SSL credentials with client_cert_source or application
            # default SSL credentials.
            if client_cert_source:
                cert, key = client_cert_source()
                ssl_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )
            else:
                ssl_credentials = SslCredentials().ssl_credentials

            # create a new channel. The provided one is ignored.
            self._grpc_channel = type(self).create_channel(
                host,
                credentials=credentials,
                credentials_file=credentials_file,
                ssl_credentials=ssl_credentials,
                scopes=scopes or self.AUTH_SCOPES,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            self._ssl_channel_credentials = ssl_credentials
        else:
            host = host if ":" in host else host + ":443"

            if credentials is None:
                credentials, _ = google.auth.default(scopes=self.AUTH_SCOPES)

            # create a new channel. The provided one is ignored.
            self._grpc_channel = type(self).create_channel(
                host,
                credentials=credentials,
                ssl_credentials=ssl_channel_credentials,
                scopes=self.AUTH_SCOPES,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        self._stubs = {}  # type: Dict[str, Callable]

        # Run the base constructor.
        super().__init__(
            host=host, credentials=credentials, client_info=client_info,
        )

    @classmethod
    def create_channel(
        cls,
        host: str = "googleads.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        scopes: Optional[Sequence[str]] = None,
        **kwargs,
    ) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            address (Optionsl[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return grpc_helpers.create_channel(
            host,
            credentials=credentials,
            scopes=scopes or cls.AUTH_SCOPES,
            **kwargs,
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Return the channel designed to connect to this service.
        """
        return self._grpc_channel

    @property
    def search(
        self,
    ) -> Callable[
        [google_ads_service.SearchGoogleAdsRequest],
        google_ads_service.SearchGoogleAdsResponse,
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
                    ~.SearchGoogleAdsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "search" not in self._stubs:
            self._stubs["search"] = self.grpc_channel.unary_unary(
                "/google.ads.googleads.v8.services.GoogleAdsService/Search",
                request_serializer=google_ads_service.SearchGoogleAdsRequest.serialize,
                response_deserializer=google_ads_service.SearchGoogleAdsResponse.deserialize,
            )
        return self._stubs["search"]

    @property
    def search_stream(
        self,
    ) -> Callable[
        [google_ads_service.SearchGoogleAdsStreamRequest],
        google_ads_service.SearchGoogleAdsStreamResponse,
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
                    ~.SearchGoogleAdsStreamResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "search_stream" not in self._stubs:
            self._stubs["search_stream"] = self.grpc_channel.unary_stream(
                "/google.ads.googleads.v8.services.GoogleAdsService/SearchStream",
                request_serializer=google_ads_service.SearchGoogleAdsStreamRequest.serialize,
                response_deserializer=google_ads_service.SearchGoogleAdsStreamResponse.deserialize,
            )
        return self._stubs["search_stream"]

    @property
    def mutate(
        self,
    ) -> Callable[
        [google_ads_service.MutateGoogleAdsRequest],
        google_ads_service.MutateGoogleAdsResponse,
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
        inconsistent state. With atomicity, you either reach the desired
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
                    ~.MutateGoogleAdsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "mutate" not in self._stubs:
            self._stubs["mutate"] = self.grpc_channel.unary_unary(
                "/google.ads.googleads.v8.services.GoogleAdsService/Mutate",
                request_serializer=google_ads_service.MutateGoogleAdsRequest.serialize,
                response_deserializer=google_ads_service.MutateGoogleAdsResponse.deserialize,
            )
        return self._stubs["mutate"]


__all__ = ("GoogleAdsServiceGrpcTransport",)
