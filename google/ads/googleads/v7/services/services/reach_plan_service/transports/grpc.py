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
from google import auth  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore

from google.ads.googleads.v7.services.types import reach_plan_service
from .base import ReachPlanServiceTransport, DEFAULT_CLIENT_INFO


class ReachPlanServiceGrpcTransport(ReachPlanServiceTransport):
    """gRPC backend transport for ReachPlanService.

    Reach Plan Service gives users information about audience
    size that can be reached through advertisement on YouTube. In
    particular, GenerateReachForecast provides estimated number of
    people of specified demographics that can be reached by an ad in
    a given market by a campaign of certain duration with a defined
    budget.

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
        credentials: credentials.Credentials = None,
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
                credentials, _ = auth.default(
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
                credentials, _ = auth.default(scopes=self.AUTH_SCOPES)

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
        credentials: credentials.Credentials = None,
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
    def list_plannable_locations(
        self,
    ) -> Callable[
        [reach_plan_service.ListPlannableLocationsRequest],
        reach_plan_service.ListPlannableLocationsResponse,
    ]:
        r"""Return a callable for the
        list plannable locations
          method over gRPC.

        Returns the list of plannable locations (for example, countries
        & DMAs).

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `HeaderError <>`__
        `InternalError <>`__ `QuotaError <>`__ `RequestError <>`__

        Returns:
            Callable[[~.ListPlannableLocationsRequest],
                    ~.ListPlannableLocationsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_plannable_locations" not in self._stubs:
            self._stubs[
                "list_plannable_locations"
            ] = self.grpc_channel.unary_unary(
                "/google.ads.googleads.v7.services.ReachPlanService/ListPlannableLocations",
                request_serializer=reach_plan_service.ListPlannableLocationsRequest.serialize,
                response_deserializer=reach_plan_service.ListPlannableLocationsResponse.deserialize,
            )
        return self._stubs["list_plannable_locations"]

    @property
    def list_plannable_products(
        self,
    ) -> Callable[
        [reach_plan_service.ListPlannableProductsRequest],
        reach_plan_service.ListPlannableProductsResponse,
    ]:
        r"""Return a callable for the
        list plannable products
          method over gRPC.

        Returns the list of per-location plannable YouTube ad formats
        with allowed targeting.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `HeaderError <>`__
        `InternalError <>`__ `QuotaError <>`__ `RequestError <>`__

        Returns:
            Callable[[~.ListPlannableProductsRequest],
                    ~.ListPlannableProductsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_plannable_products" not in self._stubs:
            self._stubs[
                "list_plannable_products"
            ] = self.grpc_channel.unary_unary(
                "/google.ads.googleads.v7.services.ReachPlanService/ListPlannableProducts",
                request_serializer=reach_plan_service.ListPlannableProductsRequest.serialize,
                response_deserializer=reach_plan_service.ListPlannableProductsResponse.deserialize,
            )
        return self._stubs["list_plannable_products"]

    @property
    def generate_product_mix_ideas(
        self,
    ) -> Callable[
        [reach_plan_service.GenerateProductMixIdeasRequest],
        reach_plan_service.GenerateProductMixIdeasResponse,
    ]:
        r"""Return a callable for the
        generate product mix ideas
          method over gRPC.

        Generates a product mix ideas given a set of preferences. This
        method helps the advertiser to obtain a good mix of ad formats
        and budget allocations based on its preferences.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `HeaderError <>`__
        `InternalError <>`__ `QuotaError <>`__ `ReachPlanError <>`__
        `RequestError <>`__

        Returns:
            Callable[[~.GenerateProductMixIdeasRequest],
                    ~.GenerateProductMixIdeasResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "generate_product_mix_ideas" not in self._stubs:
            self._stubs[
                "generate_product_mix_ideas"
            ] = self.grpc_channel.unary_unary(
                "/google.ads.googleads.v7.services.ReachPlanService/GenerateProductMixIdeas",
                request_serializer=reach_plan_service.GenerateProductMixIdeasRequest.serialize,
                response_deserializer=reach_plan_service.GenerateProductMixIdeasResponse.deserialize,
            )
        return self._stubs["generate_product_mix_ideas"]

    @property
    def generate_reach_forecast(
        self,
    ) -> Callable[
        [reach_plan_service.GenerateReachForecastRequest],
        reach_plan_service.GenerateReachForecastResponse,
    ]:
        r"""Return a callable for the
        generate reach forecast
          method over gRPC.

        Generates a reach forecast for a given targeting / product mix.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `FieldError <>`__ `HeaderError <>`__
        `InternalError <>`__ `QuotaError <>`__ `RangeError <>`__
        `ReachPlanError <>`__ `RequestError <>`__

        Returns:
            Callable[[~.GenerateReachForecastRequest],
                    ~.GenerateReachForecastResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "generate_reach_forecast" not in self._stubs:
            self._stubs[
                "generate_reach_forecast"
            ] = self.grpc_channel.unary_unary(
                "/google.ads.googleads.v7.services.ReachPlanService/GenerateReachForecast",
                request_serializer=reach_plan_service.GenerateReachForecastRequest.serialize,
                response_deserializer=reach_plan_service.GenerateReachForecastResponse.deserialize,
            )
        return self._stubs["generate_reach_forecast"]


__all__ = ("ReachPlanServiceGrpcTransport",)
