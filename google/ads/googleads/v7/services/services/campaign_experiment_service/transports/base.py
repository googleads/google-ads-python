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

from google import auth
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.api_core import operations_v1  # type: ignore
from google.auth import credentials  # type: ignore

from google.ads.googleads.v7.resources.types import campaign_experiment
from google.ads.googleads.v7.services.types import campaign_experiment_service
from google.longrunning import operations_pb2 as operations  # type: ignore
from google.protobuf import empty_pb2 as empty  # type: ignore

try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-ads",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class CampaignExperimentServiceTransport(metaclass=abc.ABCMeta):
    """Abstract transport class for CampaignExperimentService."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/adwords",)

    def __init__(
        self,
        *,
        host: str = "googleads.googleapis.com",
        credentials: credentials.Credentials = None,
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
            credentials, _ = auth.default(scopes=self.AUTH_SCOPES)

        # Save the credentials.
        self._credentials = credentials

        # Lifted into its own function so it can be stubbed out during tests.
        self._prep_wrapped_messages(client_info)

    def _prep_wrapped_messages(self, client_info):
        # Precomputed wrapped methods
        self._wrapped_methods = {
            self.get_campaign_experiment: gapic_v1.method.wrap_method(
                self.get_campaign_experiment,
                default_timeout=None,
                client_info=client_info,
            ),
            self.create_campaign_experiment: gapic_v1.method.wrap_method(
                self.create_campaign_experiment,
                default_timeout=None,
                client_info=client_info,
            ),
            self.mutate_campaign_experiments: gapic_v1.method.wrap_method(
                self.mutate_campaign_experiments,
                default_timeout=None,
                client_info=client_info,
            ),
            self.graduate_campaign_experiment: gapic_v1.method.wrap_method(
                self.graduate_campaign_experiment,
                default_timeout=None,
                client_info=client_info,
            ),
            self.promote_campaign_experiment: gapic_v1.method.wrap_method(
                self.promote_campaign_experiment,
                default_timeout=None,
                client_info=client_info,
            ),
            self.end_campaign_experiment: gapic_v1.method.wrap_method(
                self.end_campaign_experiment,
                default_timeout=None,
                client_info=client_info,
            ),
            self.list_campaign_experiment_async_errors: gapic_v1.method.wrap_method(
                self.list_campaign_experiment_async_errors,
                default_timeout=None,
                client_info=client_info,
            ),
        }

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Return the client designed to process long-running operations."""
        raise NotImplementedError

    @property
    def get_campaign_experiment(
        self,
    ) -> typing.Callable[
        [campaign_experiment_service.GetCampaignExperimentRequest],
        campaign_experiment.CampaignExperiment,
    ]:
        raise NotImplementedError

    @property
    def create_campaign_experiment(
        self,
    ) -> typing.Callable[
        [campaign_experiment_service.CreateCampaignExperimentRequest],
        operations.Operation,
    ]:
        raise NotImplementedError

    @property
    def mutate_campaign_experiments(
        self,
    ) -> typing.Callable[
        [campaign_experiment_service.MutateCampaignExperimentsRequest],
        campaign_experiment_service.MutateCampaignExperimentsResponse,
    ]:
        raise NotImplementedError

    @property
    def graduate_campaign_experiment(
        self,
    ) -> typing.Callable[
        [campaign_experiment_service.GraduateCampaignExperimentRequest],
        campaign_experiment_service.GraduateCampaignExperimentResponse,
    ]:
        raise NotImplementedError

    @property
    def promote_campaign_experiment(
        self,
    ) -> typing.Callable[
        [campaign_experiment_service.PromoteCampaignExperimentRequest],
        operations.Operation,
    ]:
        raise NotImplementedError

    @property
    def end_campaign_experiment(
        self,
    ) -> typing.Callable[
        [campaign_experiment_service.EndCampaignExperimentRequest], empty.Empty
    ]:
        raise NotImplementedError

    @property
    def list_campaign_experiment_async_errors(
        self,
    ) -> typing.Callable[
        [campaign_experiment_service.ListCampaignExperimentAsyncErrorsRequest],
        campaign_experiment_service.ListCampaignExperimentAsyncErrorsResponse,
    ]:
        raise NotImplementedError


__all__ = ("CampaignExperimentServiceTransport",)
