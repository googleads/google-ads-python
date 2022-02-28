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

from google.api_core import grpc_helpers
from google.api_core import gapic_v1
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore

from google.ads.googleads.v9.resources.types import keyword_plan
from google.ads.googleads.v9.services.types import keyword_plan_service
from .base import KeywordPlanServiceTransport, DEFAULT_CLIENT_INFO


class KeywordPlanServiceGrpcTransport(KeywordPlanServiceTransport):
    """gRPC backend transport for KeywordPlanService.

    Service to manage keyword plans.

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
                ``client_cert_source`` or application default SSL credentials.
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

    def close(self):
        self.grpc_channel.close()

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Return the channel designed to connect to this service.
        """
        return self._grpc_channel

    @property
    def get_keyword_plan(
        self,
    ) -> Callable[
        [keyword_plan_service.GetKeywordPlanRequest], keyword_plan.KeywordPlan
    ]:
        r"""Return a callable for the get keyword plan method over gRPC.

        Returns the requested plan in full detail.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `HeaderError <>`__
        `InternalError <>`__ `QuotaError <>`__ `RequestError <>`__

        Returns:
            Callable[[~.GetKeywordPlanRequest],
                    ~.KeywordPlan]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_keyword_plan" not in self._stubs:
            self._stubs["get_keyword_plan"] = self.grpc_channel.unary_unary(
                "/google.ads.googleads.v9.services.KeywordPlanService/GetKeywordPlan",
                request_serializer=keyword_plan_service.GetKeywordPlanRequest.serialize,
                response_deserializer=keyword_plan.KeywordPlan.deserialize,
            )
        return self._stubs["get_keyword_plan"]

    @property
    def mutate_keyword_plans(
        self,
    ) -> Callable[
        [keyword_plan_service.MutateKeywordPlansRequest],
        keyword_plan_service.MutateKeywordPlansResponse,
    ]:
        r"""Return a callable for the mutate keyword plans method over gRPC.

        Creates, updates, or removes keyword plans. Operation statuses
        are returned.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `DatabaseError <>`__ `FieldError <>`__
        `HeaderError <>`__ `InternalError <>`__ `KeywordPlanError <>`__
        `MutateError <>`__ `NewResourceCreationError <>`__
        `QuotaError <>`__ `RequestError <>`__
        `ResourceCountLimitExceededError <>`__ `StringLengthError <>`__

        Returns:
            Callable[[~.MutateKeywordPlansRequest],
                    ~.MutateKeywordPlansResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "mutate_keyword_plans" not in self._stubs:
            self._stubs["mutate_keyword_plans"] = self.grpc_channel.unary_unary(
                "/google.ads.googleads.v9.services.KeywordPlanService/MutateKeywordPlans",
                request_serializer=keyword_plan_service.MutateKeywordPlansRequest.serialize,
                response_deserializer=keyword_plan_service.MutateKeywordPlansResponse.deserialize,
            )
        return self._stubs["mutate_keyword_plans"]

    @property
    def generate_forecast_curve(
        self,
    ) -> Callable[
        [keyword_plan_service.GenerateForecastCurveRequest],
        keyword_plan_service.GenerateForecastCurveResponse,
    ]:
        r"""Return a callable for the generate forecast curve method over gRPC.

        Returns the requested Keyword Plan forecast curve. Only the
        bidding strategy is considered for generating forecast curve.
        The bidding strategy value specified in the plan is ignored.

        To generate a forecast at a value specified in the plan, use
        KeywordPlanService.GenerateForecastMetrics.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `HeaderError <>`__
        `InternalError <>`__ `KeywordPlanError <>`__ `QuotaError <>`__
        `RequestError <>`__

        Returns:
            Callable[[~.GenerateForecastCurveRequest],
                    ~.GenerateForecastCurveResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "generate_forecast_curve" not in self._stubs:
            self._stubs[
                "generate_forecast_curve"
            ] = self.grpc_channel.unary_unary(
                "/google.ads.googleads.v9.services.KeywordPlanService/GenerateForecastCurve",
                request_serializer=keyword_plan_service.GenerateForecastCurveRequest.serialize,
                response_deserializer=keyword_plan_service.GenerateForecastCurveResponse.deserialize,
            )
        return self._stubs["generate_forecast_curve"]

    @property
    def generate_forecast_time_series(
        self,
    ) -> Callable[
        [keyword_plan_service.GenerateForecastTimeSeriesRequest],
        keyword_plan_service.GenerateForecastTimeSeriesResponse,
    ]:
        r"""Return a callable for the generate forecast time series method over gRPC.

        Returns a forecast in the form of a time series for the Keyword
        Plan over the next 52 weeks. (1) Forecasts closer to the current
        date are generally more accurate than further out.

        (2) The forecast reflects seasonal trends using current and
        prior traffic patterns. The forecast period of the plan is
        ignored.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `HeaderError <>`__
        `InternalError <>`__ `KeywordPlanError <>`__ `QuotaError <>`__
        `RequestError <>`__

        Returns:
            Callable[[~.GenerateForecastTimeSeriesRequest],
                    ~.GenerateForecastTimeSeriesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "generate_forecast_time_series" not in self._stubs:
            self._stubs[
                "generate_forecast_time_series"
            ] = self.grpc_channel.unary_unary(
                "/google.ads.googleads.v9.services.KeywordPlanService/GenerateForecastTimeSeries",
                request_serializer=keyword_plan_service.GenerateForecastTimeSeriesRequest.serialize,
                response_deserializer=keyword_plan_service.GenerateForecastTimeSeriesResponse.deserialize,
            )
        return self._stubs["generate_forecast_time_series"]

    @property
    def generate_forecast_metrics(
        self,
    ) -> Callable[
        [keyword_plan_service.GenerateForecastMetricsRequest],
        keyword_plan_service.GenerateForecastMetricsResponse,
    ]:
        r"""Return a callable for the generate forecast metrics method over gRPC.

        Returns the requested Keyword Plan forecasts.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `HeaderError <>`__
        `InternalError <>`__ `KeywordPlanError <>`__ `QuotaError <>`__
        `RequestError <>`__

        Returns:
            Callable[[~.GenerateForecastMetricsRequest],
                    ~.GenerateForecastMetricsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "generate_forecast_metrics" not in self._stubs:
            self._stubs[
                "generate_forecast_metrics"
            ] = self.grpc_channel.unary_unary(
                "/google.ads.googleads.v9.services.KeywordPlanService/GenerateForecastMetrics",
                request_serializer=keyword_plan_service.GenerateForecastMetricsRequest.serialize,
                response_deserializer=keyword_plan_service.GenerateForecastMetricsResponse.deserialize,
            )
        return self._stubs["generate_forecast_metrics"]

    @property
    def generate_historical_metrics(
        self,
    ) -> Callable[
        [keyword_plan_service.GenerateHistoricalMetricsRequest],
        keyword_plan_service.GenerateHistoricalMetricsResponse,
    ]:
        r"""Return a callable for the generate historical metrics method over gRPC.

        Returns the requested Keyword Plan historical metrics.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `HeaderError <>`__
        `InternalError <>`__ `KeywordPlanError <>`__ `QuotaError <>`__
        `RequestError <>`__

        Returns:
            Callable[[~.GenerateHistoricalMetricsRequest],
                    ~.GenerateHistoricalMetricsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "generate_historical_metrics" not in self._stubs:
            self._stubs[
                "generate_historical_metrics"
            ] = self.grpc_channel.unary_unary(
                "/google.ads.googleads.v9.services.KeywordPlanService/GenerateHistoricalMetrics",
                request_serializer=keyword_plan_service.GenerateHistoricalMetricsRequest.serialize,
                response_deserializer=keyword_plan_service.GenerateHistoricalMetricsResponse.deserialize,
            )
        return self._stubs["generate_historical_metrics"]


__all__ = ("KeywordPlanServiceGrpcTransport",)
