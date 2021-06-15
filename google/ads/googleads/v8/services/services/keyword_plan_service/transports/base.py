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
import abc
import typing
import pkg_resources

import google.auth  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore

from google.ads.googleads.v8.resources.types import keyword_plan
from google.ads.googleads.v8.services.types import keyword_plan_service

try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-ads-googleads",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class KeywordPlanServiceTransport(metaclass=abc.ABCMeta):
    """Abstract transport class for KeywordPlanService."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/adwords",)

    def __init__(
        self,
        *,
        host: str = "googleads.googleapis.com",
        credentials: ga_credentials.Credentials = None,
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
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials is None:
            credentials, _ = google.auth.default(scopes=self.AUTH_SCOPES)

        # Save the credentials.
        self._credentials = credentials

        # Lifted into its own function so it can be stubbed out during tests.
        self._prep_wrapped_messages(client_info)

    def _prep_wrapped_messages(self, client_info):
        # Precomputed wrapped methods
        self._wrapped_methods = {
            self.get_keyword_plan: gapic_v1.method.wrap_method(
                self.get_keyword_plan,
                default_timeout=None,
                client_info=client_info,
            ),
            self.mutate_keyword_plans: gapic_v1.method.wrap_method(
                self.mutate_keyword_plans,
                default_timeout=None,
                client_info=client_info,
            ),
            self.generate_forecast_curve: gapic_v1.method.wrap_method(
                self.generate_forecast_curve,
                default_timeout=None,
                client_info=client_info,
            ),
            self.generate_forecast_time_series: gapic_v1.method.wrap_method(
                self.generate_forecast_time_series,
                default_timeout=None,
                client_info=client_info,
            ),
            self.generate_forecast_metrics: gapic_v1.method.wrap_method(
                self.generate_forecast_metrics,
                default_timeout=None,
                client_info=client_info,
            ),
            self.generate_historical_metrics: gapic_v1.method.wrap_method(
                self.generate_historical_metrics,
                default_timeout=None,
                client_info=client_info,
            ),
        }

    @property
    def get_keyword_plan(
        self,
    ) -> typing.Callable[
        [keyword_plan_service.GetKeywordPlanRequest], keyword_plan.KeywordPlan
    ]:
        raise NotImplementedError

    @property
    def mutate_keyword_plans(
        self,
    ) -> typing.Callable[
        [keyword_plan_service.MutateKeywordPlansRequest],
        keyword_plan_service.MutateKeywordPlansResponse,
    ]:
        raise NotImplementedError

    @property
    def generate_forecast_curve(
        self,
    ) -> typing.Callable[
        [keyword_plan_service.GenerateForecastCurveRequest],
        keyword_plan_service.GenerateForecastCurveResponse,
    ]:
        raise NotImplementedError

    @property
    def generate_forecast_time_series(
        self,
    ) -> typing.Callable[
        [keyword_plan_service.GenerateForecastTimeSeriesRequest],
        keyword_plan_service.GenerateForecastTimeSeriesResponse,
    ]:
        raise NotImplementedError

    @property
    def generate_forecast_metrics(
        self,
    ) -> typing.Callable[
        [keyword_plan_service.GenerateForecastMetricsRequest],
        keyword_plan_service.GenerateForecastMetricsResponse,
    ]:
        raise NotImplementedError

    @property
    def generate_historical_metrics(
        self,
    ) -> typing.Callable[
        [keyword_plan_service.GenerateHistoricalMetricsRequest],
        keyword_plan_service.GenerateHistoricalMetricsResponse,
    ]:
        raise NotImplementedError


__all__ = ("KeywordPlanServiceTransport",)
