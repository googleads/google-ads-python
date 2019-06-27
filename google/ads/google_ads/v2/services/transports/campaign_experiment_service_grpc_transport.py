# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
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


import google.api_core.grpc_helpers
import google.api_core.operations_v1

from google.ads.google_ads.v2.proto.services import campaign_experiment_service_pb2_grpc


class CampaignExperimentServiceGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.ads.googleads.v2.services CampaignExperimentService API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """
    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = (
    )

    def __init__(self, channel=None, credentials=None,
                 address='googleads.googleapis.com:443'):
        """Instantiate the transport class.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            address (str): The address where the service is hosted.
        """
        # If both `channel` and `credentials` are specified, raise an
        # exception (channels come with credentials baked in already).
        if channel is not None and credentials is not None:
            raise ValueError(
                'The `channel` and `credentials` arguments are mutually '
                'exclusive.',
            )

        # Create the channel.
        if channel is None:
            channel = self.create_channel(
                address=address,
                credentials=credentials,
            )

        self._channel = channel

        # gRPC uses objects called "stubs" that are bound to the
        # channel and provide a basic method for each RPC.
        self._stubs = {
            'campaign_experiment_service_stub': campaign_experiment_service_pb2_grpc.CampaignExperimentServiceStub(channel),
        }

        # Because this API includes a method that returns a
        # long-running operation (proto: google.longrunning.Operation),
        # instantiate an LRO client.
        self._operations_client = google.api_core.operations_v1.OperationsClient(channel)

    @classmethod
    def create_channel(
                cls,
                address='googleads.googleapis.com:443',
                credentials=None,
                **kwargs):
        """Create and return a gRPC channel object.

        Args:
            address (str): The host for the channel to use.
            credentials (~.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            kwargs (dict): Keyword arguments, which are passed to the
                channel creation.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return google.api_core.grpc_helpers.create_channel(
            address,
            credentials=credentials,
            scopes=cls._OAUTH_SCOPES,
            **kwargs
        )

    @property
    def channel(self):
        """The gRPC channel used by the transport.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return self._channel

    @property
    def get_campaign_experiment(self):
        """Return the gRPC stub for :meth:`CampaignExperimentServiceClient.get_campaign_experiment`.

        Returns the requested campaign experiment in full detail.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['campaign_experiment_service_stub'].GetCampaignExperiment

    @property
    def create_campaign_experiment(self):
        """Return the gRPC stub for :meth:`CampaignExperimentServiceClient.create_campaign_experiment`.

        Creates a campaign experiment based on a campaign draft. The draft campaign
        will be forked into a real campaign (called the experiment campaign) that
        will begin serving ads if successfully created.

        The campaign experiment is created immediately with status INITIALIZING.
        This method return a long running operation that tracks the forking of the
        draft campaign. If the forking fails, a list of errors can be retrieved
        using the ListCampaignExperimentAsyncErrors method. The operation's
        metadata will be a StringValue containing the resource name of the created
        campaign experiment.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['campaign_experiment_service_stub'].CreateCampaignExperiment

    @property
    def mutate_campaign_experiments(self):
        """Return the gRPC stub for :meth:`CampaignExperimentServiceClient.mutate_campaign_experiments`.

        Updates campaign experiments. Operation statuses are returned.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['campaign_experiment_service_stub'].MutateCampaignExperiments

    @property
    def graduate_campaign_experiment(self):
        """Return the gRPC stub for :meth:`CampaignExperimentServiceClient.graduate_campaign_experiment`.

        Graduates a campaign experiment to a full campaign. The base and experiment
        campaigns will start running independently with their own budgets.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['campaign_experiment_service_stub'].GraduateCampaignExperiment

    @property
    def promote_campaign_experiment(self):
        """Return the gRPC stub for :meth:`CampaignExperimentServiceClient.promote_campaign_experiment`.

        Promotes the changes in a experiment campaign back to the base campaign.

        The campaign experiment is updated immediately with status PROMOTING.
        This method return a long running operation that tracks the promoting of
        the experiment campaign. If the promoting fails, a list of errors can be
        retrieved using the ListCampaignExperimentAsyncErrors method.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['campaign_experiment_service_stub'].PromoteCampaignExperiment

    @property
    def end_campaign_experiment(self):
        """Return the gRPC stub for :meth:`CampaignExperimentServiceClient.end_campaign_experiment`.

        Immediately ends a campaign experiment, changing the experiment's scheduled
        end date and without waiting for end of day. End date is updated to be the
        time of the request.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['campaign_experiment_service_stub'].EndCampaignExperiment

    @property
    def list_campaign_experiment_async_errors(self):
        """Return the gRPC stub for :meth:`CampaignExperimentServiceClient.list_campaign_experiment_async_errors`.

        Returns all errors that occurred during CampaignExperiment create or
        promote (whichever occurred last).
        Supports standard list paging.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['campaign_experiment_service_stub'].ListCampaignExperimentAsyncErrors