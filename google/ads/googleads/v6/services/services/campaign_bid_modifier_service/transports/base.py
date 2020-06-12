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
from google.auth import credentials  # type: ignore

from google.ads.googleads.v6.resources.types import campaign_bid_modifier
from google.ads.googleads.v6.services.types import campaign_bid_modifier_service


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-ads-googleads",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class CampaignBidModifierServiceTransport(metaclass=abc.ABCMeta):
    """Abstract transport class for CampaignBidModifierService."""

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
            host (Optional[str]): The hostname to connect to.
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
            self.get_campaign_bid_modifier: gapic_v1.method.wrap_method(
                self.get_campaign_bid_modifier,
                default_timeout=None,
                client_info=client_info,
            ),
            self.mutate_campaign_bid_modifiers: gapic_v1.method.wrap_method(
                self.mutate_campaign_bid_modifiers,
                default_timeout=None,
                client_info=client_info,
            ),
        }

    @property
    def get_campaign_bid_modifier(
        self,
    ) -> typing.Callable[
        [campaign_bid_modifier_service.GetCampaignBidModifierRequest],
        campaign_bid_modifier.CampaignBidModifier,
    ]:
        raise NotImplementedError

    @property
    def mutate_campaign_bid_modifiers(
        self,
    ) -> typing.Callable[
        [campaign_bid_modifier_service.MutateCampaignBidModifiersRequest],
        campaign_bid_modifier_service.MutateCampaignBidModifiersResponse,
    ]:
        raise NotImplementedError


__all__ = ("CampaignBidModifierServiceTransport",)
