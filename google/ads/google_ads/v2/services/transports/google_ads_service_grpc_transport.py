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

from google.ads.google_ads.v2.proto.services import google_ads_service_pb2_grpc


class GoogleAdsServiceGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.ads.googleads.v2.services GoogleAdsService API.

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
            'google_ads_service_stub': google_ads_service_pb2_grpc.GoogleAdsServiceStub(channel),
        }


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
    def search(self):
        """Return the gRPC stub for :meth:`GoogleAdsServiceClient.search`.

        Returns all rows that match the search query.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['google_ads_service_stub'].Search

    @property
    def mutate(self):
        """Return the gRPC stub for :meth:`GoogleAdsServiceClient.mutate`.

        Creates, updates, or removes resources. This method supports atomic
        transactions with multiple types of resources. For example, you can
        atomically create a campaign and a campaign budget, or perform up to
        thousands of mutates atomically.

        This method is essentially a wrapper around a series of mutate methods.
        The only features it offers over calling those methods directly are:

        -  Atomic transactions
        -  Temp resource names (described below)
        -  Somewhat reduced latency over making a series of mutate calls

        Note: Only resources that support atomic transactions are included, so
        this method can't replace all calls to individual services.

        ## Atomic Transaction Benefits

        Atomicity makes error handling much easier. If you're making a series of
        changes and one fails, it can leave your account in an inconsistent
        state. With atomicity, you either reach the desired state directly, or
        the request fails and you can retry.

        ## Temp Resource Names

        Temp resource names are a special type of resource name used to create a
        resource and reference that resource in the same request. For example,
        if a campaign budget is created with ``resource_name`` equal to
        ``customers/123/campaignBudgets/-1``, that resource name can be reused
        in the ``Campaign.budget`` field in the same request. That way, the two
        resources are created and linked atomically.

        To create a temp resource name, put a negative number in the part of the
        name that the server would normally allocate.

        Note:

        -  Resources must be created with a temp name before the name can be
           reused. For example, the previous CampaignBudget+Campaign example
           would fail if the mutate order was reversed.
        -  Temp names are not remembered across requests.
        -  There's no limit to the number of temp names in a request.
        -  Each temp name must use a unique negative number, even if the
           resource types differ.

        ## Latency

        It's important to group mutates by resource type or the request may time
        out and fail. Latency is roughly equal to a series of calls to
        individual mutate methods, where each change in resource type is a new
        call. For example, mutating 10 campaigns then 10 ad groups is like 2
        calls, while mutating 1 campaign, 1 ad group, 1 campaign, 1 ad group is
        like 4 calls.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['google_ads_service_stub'].Mutate