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

from google.ads.google_ads.v2.proto.services import campaign_draft_service_pb2_grpc


class CampaignDraftServiceGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.ads.googleads.v2.services CampaignDraftService API.

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
            'campaign_draft_service_stub': campaign_draft_service_pb2_grpc.CampaignDraftServiceStub(channel),
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
    def get_campaign_draft(self):
        """Return the gRPC stub for :meth:`CampaignDraftServiceClient.get_campaign_draft`.

        Returns the requested campaign draft in full detail.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['campaign_draft_service_stub'].GetCampaignDraft

    @property
    def mutate_campaign_drafts(self):
        """Return the gRPC stub for :meth:`CampaignDraftServiceClient.mutate_campaign_drafts`.

        Creates, updates, or removes campaign drafts. Operation statuses are
        returned.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['campaign_draft_service_stub'].MutateCampaignDrafts

    @property
    def promote_campaign_draft(self):
        """Return the gRPC stub for :meth:`CampaignDraftServiceClient.promote_campaign_draft`.

        Promotes the changes in a draft back to the base campaign.

        This method returns a Long Running Operation (LRO) indicating if the
        Promote is done. Use [Operations.GetOperation] to poll the LRO until it
        is done. Only a done status is returned in the response. See the status
        in the Campaign Draft resource to determine if the promotion was
        successful. If the LRO failed, use
        ``CampaignDraftService.ListCampaignDraftAsyncErrors`` to view the list
        of error reasons.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['campaign_draft_service_stub'].PromoteCampaignDraft

    @property
    def list_campaign_draft_async_errors(self):
        """Return the gRPC stub for :meth:`CampaignDraftServiceClient.list_campaign_draft_async_errors`.

        Returns all errors that occurred during CampaignDraft promote. Throws an
        error if called before campaign draft is promoted.
        Supports standard list paging.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['campaign_draft_service_stub'].ListCampaignDraftAsyncErrors