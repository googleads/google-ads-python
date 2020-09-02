# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
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

from google.ads.google_ads.v5.proto.services import keyword_plan_service_pb2_grpc


class KeywordPlanServiceGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.ads.googleads.v5.services KeywordPlanService API.

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
                options={
                    'grpc.max_send_message_length': -1,
                    'grpc.max_receive_message_length': -1,
                }.items(),
            )

        self._channel = channel

        # gRPC uses objects called "stubs" that are bound to the
        # channel and provide a basic method for each RPC.
        self._stubs = {
            'keyword_plan_service_stub': keyword_plan_service_pb2_grpc.KeywordPlanServiceStub(channel),
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
    def get_keyword_plan(self):
        """Return the gRPC stub for :meth:`KeywordPlanServiceClient.get_keyword_plan`.

        Returns the requested plan in full detail.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['keyword_plan_service_stub'].GetKeywordPlan

    @property
    def mutate_keyword_plans(self):
        """Return the gRPC stub for :meth:`KeywordPlanServiceClient.mutate_keyword_plans`.

        Creates, updates, or removes keyword plans. Operation statuses are
        returned.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['keyword_plan_service_stub'].MutateKeywordPlans

    @property
    def generate_forecast_curve(self):
        """Return the gRPC stub for :meth:`KeywordPlanServiceClient.generate_forecast_curve`.

        Returns the requested Keyword Plan forecast curve.
        Only the bidding strategy is considered for generating forecast curve.
        The bidding strategy value specified in the plan is ignored.

        To generate a forecast at a value specified in the plan, use
        KeywordPlanService.GenerateForecastMetrics.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['keyword_plan_service_stub'].GenerateForecastCurve

    @property
    def generate_forecast_time_series(self):
        """Return the gRPC stub for :meth:`KeywordPlanServiceClient.generate_forecast_time_series`.

        Returns a forecast in the form of a time series for the Keyword Plan over
        the next 52 weeks.
        (1) Forecasts closer to the current date are generally more accurate than
        further out.

        (2) The forecast reflects seasonal trends using current and
        prior traffic patterns. The forecast period of the plan is ignored.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['keyword_plan_service_stub'].GenerateForecastTimeSeries

    @property
    def generate_forecast_metrics(self):
        """Return the gRPC stub for :meth:`KeywordPlanServiceClient.generate_forecast_metrics`.

        Returns the requested Keyword Plan forecasts.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['keyword_plan_service_stub'].GenerateForecastMetrics

    @property
    def generate_historical_metrics(self):
        """Return the gRPC stub for :meth:`KeywordPlanServiceClient.generate_historical_metrics`.

        Returns the requested Keyword Plan historical metrics.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs['keyword_plan_service_stub'].GenerateHistoricalMetrics