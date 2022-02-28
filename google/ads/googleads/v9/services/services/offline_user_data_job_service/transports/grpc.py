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
from google.api_core import operations_v1
from google.api_core import gapic_v1
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore

from google.ads.googleads.v9.resources.types import offline_user_data_job
from google.ads.googleads.v9.services.types import offline_user_data_job_service
from google.longrunning import operations_pb2  # type: ignore
from .base import OfflineUserDataJobServiceTransport, DEFAULT_CLIENT_INFO


class OfflineUserDataJobServiceGrpcTransport(
    OfflineUserDataJobServiceTransport
):
    """gRPC backend transport for OfflineUserDataJobService.

    Service to manage offline user data jobs.

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
    def create_offline_user_data_job(
        self,
    ) -> Callable[
        [offline_user_data_job_service.CreateOfflineUserDataJobRequest],
        offline_user_data_job_service.CreateOfflineUserDataJobResponse,
    ]:
        r"""Return a callable for the create offline user data job method over gRPC.

        Creates an offline user data job.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `DatabaseError <>`__ `FieldError <>`__
        `HeaderError <>`__ `InternalError <>`__
        `NotAllowlistedError <>`__ `OfflineUserDataJobError <>`__
        `QuotaError <>`__ `RequestError <>`__

        Returns:
            Callable[[~.CreateOfflineUserDataJobRequest],
                    ~.CreateOfflineUserDataJobResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_offline_user_data_job" not in self._stubs:
            self._stubs[
                "create_offline_user_data_job"
            ] = self.grpc_channel.unary_unary(
                "/google.ads.googleads.v9.services.OfflineUserDataJobService/CreateOfflineUserDataJob",
                request_serializer=offline_user_data_job_service.CreateOfflineUserDataJobRequest.serialize,
                response_deserializer=offline_user_data_job_service.CreateOfflineUserDataJobResponse.deserialize,
            )
        return self._stubs["create_offline_user_data_job"]

    @property
    def get_offline_user_data_job(
        self,
    ) -> Callable[
        [offline_user_data_job_service.GetOfflineUserDataJobRequest],
        offline_user_data_job.OfflineUserDataJob,
    ]:
        r"""Return a callable for the get offline user data job method over gRPC.

        Returns the offline user data job.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `HeaderError <>`__
        `InternalError <>`__ `QuotaError <>`__ `RequestError <>`__

        Returns:
            Callable[[~.GetOfflineUserDataJobRequest],
                    ~.OfflineUserDataJob]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_offline_user_data_job" not in self._stubs:
            self._stubs[
                "get_offline_user_data_job"
            ] = self.grpc_channel.unary_unary(
                "/google.ads.googleads.v9.services.OfflineUserDataJobService/GetOfflineUserDataJob",
                request_serializer=offline_user_data_job_service.GetOfflineUserDataJobRequest.serialize,
                response_deserializer=offline_user_data_job.OfflineUserDataJob.deserialize,
            )
        return self._stubs["get_offline_user_data_job"]

    @property
    def add_offline_user_data_job_operations(
        self,
    ) -> Callable[
        [offline_user_data_job_service.AddOfflineUserDataJobOperationsRequest],
        offline_user_data_job_service.AddOfflineUserDataJobOperationsResponse,
    ]:
        r"""Return a callable for the add offline user data job
        operations method over gRPC.

        Adds operations to the offline user data job.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `DatabaseError <>`__ `FieldError <>`__
        `HeaderError <>`__ `InternalError <>`__ `MutateError <>`__
        `OfflineUserDataJobError <>`__ `QuotaError <>`__
        `RequestError <>`__

        Returns:
            Callable[[~.AddOfflineUserDataJobOperationsRequest],
                    ~.AddOfflineUserDataJobOperationsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "add_offline_user_data_job_operations" not in self._stubs:
            self._stubs[
                "add_offline_user_data_job_operations"
            ] = self.grpc_channel.unary_unary(
                "/google.ads.googleads.v9.services.OfflineUserDataJobService/AddOfflineUserDataJobOperations",
                request_serializer=offline_user_data_job_service.AddOfflineUserDataJobOperationsRequest.serialize,
                response_deserializer=offline_user_data_job_service.AddOfflineUserDataJobOperationsResponse.deserialize,
            )
        return self._stubs["add_offline_user_data_job_operations"]

    @property
    def run_offline_user_data_job(
        self,
    ) -> Callable[
        [offline_user_data_job_service.RunOfflineUserDataJobRequest],
        operations_pb2.Operation,
    ]:
        r"""Return a callable for the run offline user data job method over gRPC.

        Runs the offline user data job.

        When finished, the long running operation will contain the
        processing result or failure information, if any.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `DatabaseError <>`__
        `HeaderError <>`__ `InternalError <>`__
        `OfflineUserDataJobError <>`__ `QuotaError <>`__
        `RequestError <>`__

        Returns:
            Callable[[~.RunOfflineUserDataJobRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "run_offline_user_data_job" not in self._stubs:
            self._stubs[
                "run_offline_user_data_job"
            ] = self.grpc_channel.unary_unary(
                "/google.ads.googleads.v9.services.OfflineUserDataJobService/RunOfflineUserDataJob",
                request_serializer=offline_user_data_job_service.RunOfflineUserDataJobRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["run_offline_user_data_job"]


__all__ = ("OfflineUserDataJobServiceGrpcTransport",)
