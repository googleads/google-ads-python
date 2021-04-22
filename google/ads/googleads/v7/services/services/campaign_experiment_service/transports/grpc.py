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
from google.api_core import operations_v1  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google import auth  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore

from google.ads.googleads.v7.resources.types import campaign_experiment
from google.ads.googleads.v7.services.types import campaign_experiment_service
from google.longrunning import operations_pb2 as operations  # type: ignore
from google.protobuf import empty_pb2 as empty  # type: ignore
from .base import CampaignExperimentServiceTransport, DEFAULT_CLIENT_INFO


class CampaignExperimentServiceGrpcTransport(
    CampaignExperimentServiceTransport
):
    """gRPC backend transport for CampaignExperimentService.

    CampaignExperimentService manages the life cycle of campaign
    experiments. It is used to create new experiments from drafts,
    modify experiment properties, promote changes in an experiment
    back to its base campaign, graduate experiments into new stand-
    alone campaigns, and to remove an experiment.

    An experiment consists of two variants or arms - the base
    campaign and the experiment campaign, directing a fixed share of
    traffic to each arm. A campaign experiment is created from a
    draft of changes to the base campaign and will be a snapshot of
    changes in the draft at the time of creation.

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
    def operations_client(self) -> operations_v1.OperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Sanity check: Only create a new client if we do not already have one.
        if "operations_client" not in self.__dict__:
            self.__dict__["operations_client"] = operations_v1.OperationsClient(
                self.grpc_channel
            )

        # Return the client from cache.
        return self.__dict__["operations_client"]

    @property
    def get_campaign_experiment(
        self,
    ) -> Callable[
        [campaign_experiment_service.GetCampaignExperimentRequest],
        campaign_experiment.CampaignExperiment,
    ]:
        r"""Return a callable for the
        get campaign experiment
          method over gRPC.

        Returns the requested campaign experiment in full detail.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `HeaderError <>`__
        `InternalError <>`__ `QuotaError <>`__ `RequestError <>`__

        Returns:
            Callable[[~.GetCampaignExperimentRequest],
                    ~.CampaignExperiment]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_campaign_experiment" not in self._stubs:
            self._stubs[
                "get_campaign_experiment"
            ] = self.grpc_channel.unary_unary(
                "/google.ads.googleads.v7.services.CampaignExperimentService/GetCampaignExperiment",
                request_serializer=campaign_experiment_service.GetCampaignExperimentRequest.serialize,
                response_deserializer=campaign_experiment.CampaignExperiment.deserialize,
            )
        return self._stubs["get_campaign_experiment"]

    @property
    def create_campaign_experiment(
        self,
    ) -> Callable[
        [campaign_experiment_service.CreateCampaignExperimentRequest],
        operations.Operation,
    ]:
        r"""Return a callable for the
        create campaign experiment
          method over gRPC.

        Creates a campaign experiment based on a campaign draft. The
        draft campaign will be forked into a real campaign (called the
        experiment campaign) that will begin serving ads if successfully
        created.

        The campaign experiment is created immediately with status
        INITIALIZING. This method return a long running operation that
        tracks the forking of the draft campaign. If the forking fails,
        a list of errors can be retrieved using the
        ListCampaignExperimentAsyncErrors method. The operation's
        metadata will be a StringValue containing the resource name of
        the created campaign experiment.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `CampaignExperimentError <>`__
        `DatabaseError <>`__ `DateError <>`__ `DateRangeError <>`__
        `FieldError <>`__ `HeaderError <>`__ `InternalError <>`__
        `QuotaError <>`__ `RangeError <>`__ `RequestError <>`__

        Returns:
            Callable[[~.CreateCampaignExperimentRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_campaign_experiment" not in self._stubs:
            self._stubs[
                "create_campaign_experiment"
            ] = self.grpc_channel.unary_unary(
                "/google.ads.googleads.v7.services.CampaignExperimentService/CreateCampaignExperiment",
                request_serializer=campaign_experiment_service.CreateCampaignExperimentRequest.serialize,
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["create_campaign_experiment"]

    @property
    def mutate_campaign_experiments(
        self,
    ) -> Callable[
        [campaign_experiment_service.MutateCampaignExperimentsRequest],
        campaign_experiment_service.MutateCampaignExperimentsResponse,
    ]:
        r"""Return a callable for the
        mutate campaign experiments
          method over gRPC.

        Updates campaign experiments. Operation statuses are returned.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `CampaignExperimentError <>`__
        `HeaderError <>`__ `InternalError <>`__ `QuotaError <>`__
        `RequestError <>`__

        Returns:
            Callable[[~.MutateCampaignExperimentsRequest],
                    ~.MutateCampaignExperimentsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "mutate_campaign_experiments" not in self._stubs:
            self._stubs[
                "mutate_campaign_experiments"
            ] = self.grpc_channel.unary_unary(
                "/google.ads.googleads.v7.services.CampaignExperimentService/MutateCampaignExperiments",
                request_serializer=campaign_experiment_service.MutateCampaignExperimentsRequest.serialize,
                response_deserializer=campaign_experiment_service.MutateCampaignExperimentsResponse.deserialize,
            )
        return self._stubs["mutate_campaign_experiments"]

    @property
    def graduate_campaign_experiment(
        self,
    ) -> Callable[
        [campaign_experiment_service.GraduateCampaignExperimentRequest],
        campaign_experiment_service.GraduateCampaignExperimentResponse,
    ]:
        r"""Return a callable for the
        graduate campaign experiment
          method over gRPC.

        Graduates a campaign experiment to a full campaign. The base and
        experiment campaigns will start running independently with their
        own budgets.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `CampaignExperimentError <>`__
        `HeaderError <>`__ `InternalError <>`__ `MutateError <>`__
        `QuotaError <>`__ `RequestError <>`__

        Returns:
            Callable[[~.GraduateCampaignExperimentRequest],
                    ~.GraduateCampaignExperimentResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "graduate_campaign_experiment" not in self._stubs:
            self._stubs[
                "graduate_campaign_experiment"
            ] = self.grpc_channel.unary_unary(
                "/google.ads.googleads.v7.services.CampaignExperimentService/GraduateCampaignExperiment",
                request_serializer=campaign_experiment_service.GraduateCampaignExperimentRequest.serialize,
                response_deserializer=campaign_experiment_service.GraduateCampaignExperimentResponse.deserialize,
            )
        return self._stubs["graduate_campaign_experiment"]

    @property
    def promote_campaign_experiment(
        self,
    ) -> Callable[
        [campaign_experiment_service.PromoteCampaignExperimentRequest],
        operations.Operation,
    ]:
        r"""Return a callable for the
        promote campaign experiment
          method over gRPC.

        Promotes the changes in a experiment campaign back to the base
        campaign.

        The campaign experiment is updated immediately with status
        PROMOTING. This method return a long running operation that
        tracks the promoting of the experiment campaign. If the
        promoting fails, a list of errors can be retrieved using the
        ListCampaignExperimentAsyncErrors method.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `HeaderError <>`__
        `InternalError <>`__ `QuotaError <>`__ `RequestError <>`__

        Returns:
            Callable[[~.PromoteCampaignExperimentRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "promote_campaign_experiment" not in self._stubs:
            self._stubs[
                "promote_campaign_experiment"
            ] = self.grpc_channel.unary_unary(
                "/google.ads.googleads.v7.services.CampaignExperimentService/PromoteCampaignExperiment",
                request_serializer=campaign_experiment_service.PromoteCampaignExperimentRequest.serialize,
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["promote_campaign_experiment"]

    @property
    def end_campaign_experiment(
        self,
    ) -> Callable[
        [campaign_experiment_service.EndCampaignExperimentRequest], empty.Empty
    ]:
        r"""Return a callable for the
        end campaign experiment
          method over gRPC.

        Immediately ends a campaign experiment, changing the
        experiment's scheduled end date and without waiting for end of
        day. End date is updated to be the time of the request.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `CampaignExperimentError <>`__
        `HeaderError <>`__ `InternalError <>`__ `QuotaError <>`__
        `RequestError <>`__

        Returns:
            Callable[[~.EndCampaignExperimentRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "end_campaign_experiment" not in self._stubs:
            self._stubs[
                "end_campaign_experiment"
            ] = self.grpc_channel.unary_unary(
                "/google.ads.googleads.v7.services.CampaignExperimentService/EndCampaignExperiment",
                request_serializer=campaign_experiment_service.EndCampaignExperimentRequest.serialize,
                response_deserializer=empty.Empty.FromString,
            )
        return self._stubs["end_campaign_experiment"]

    @property
    def list_campaign_experiment_async_errors(
        self,
    ) -> Callable[
        [campaign_experiment_service.ListCampaignExperimentAsyncErrorsRequest],
        campaign_experiment_service.ListCampaignExperimentAsyncErrorsResponse,
    ]:
        r"""Return a callable for the
        list campaign experiment async
        errors
          method over gRPC.

        Returns all errors that occurred during CampaignExperiment
        create or promote (whichever occurred last). Supports standard
        list paging.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `HeaderError <>`__
        `InternalError <>`__ `QuotaError <>`__ `RequestError <>`__

        Returns:
            Callable[[~.ListCampaignExperimentAsyncErrorsRequest],
                    ~.ListCampaignExperimentAsyncErrorsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_campaign_experiment_async_errors" not in self._stubs:
            self._stubs[
                "list_campaign_experiment_async_errors"
            ] = self.grpc_channel.unary_unary(
                "/google.ads.googleads.v7.services.CampaignExperimentService/ListCampaignExperimentAsyncErrors",
                request_serializer=campaign_experiment_service.ListCampaignExperimentAsyncErrorsRequest.serialize,
                response_deserializer=campaign_experiment_service.ListCampaignExperimentAsyncErrorsResponse.deserialize,
            )
        return self._stubs["list_campaign_experiment_async_errors"]


__all__ = ("CampaignExperimentServiceGrpcTransport",)
