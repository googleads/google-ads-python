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

from collections import OrderedDict
from distutils import util
import os
import re
from typing import Dict, Iterable, Optional, Sequence, Tuple, Type, Union

from google.api_core import client_options as client_options_lib  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.ads.googleads.v5.services.services.google_ads_service import pagers
from google.ads.googleads.v5.services.types import google_ads_service
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.rpc import status_pb2 as status  # type: ignore

from .transports.base import GoogleAdsServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import GoogleAdsServiceGrpcTransport


class GoogleAdsServiceClientMeta(type):
    """Metaclass for the GoogleAdsService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[GoogleAdsServiceTransport]]
    _transport_registry["grpc"] = GoogleAdsServiceGrpcTransport

    def get_transport_class(
        cls, label: str = None,
    ) -> Type[GoogleAdsServiceTransport]:
        """Return an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class GoogleAdsServiceClient(metaclass=GoogleAdsServiceClientMeta):
    """Service to fetch data and metrics across resources."""

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Convert api endpoint to mTLS endpoint.
        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    DEFAULT_ENDPOINT = "googleads.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            GoogleAdsServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_info(
            info
        )
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            GoogleAdsServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(
            filename
        )
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> GoogleAdsServiceTransport:
        """Return the transport used by the client instance.

        Returns:
            GoogleAdsServiceTransport: The transport used by the client instance.
        """
        return self._transport

    @staticmethod
    def account_budget_path(customer: str, account_budget: str,) -> str:
        """Return a fully-qualified account_budget string."""
        return "customers/{customer}/accountBudgets/{account_budget}".format(
            customer=customer, account_budget=account_budget,
        )

    @staticmethod
    def parse_account_budget_path(path: str) -> Dict[str, str]:
        """Parse a account_budget path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/accountBudgets/(?P<account_budget>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def account_budget_proposal_path(
        customer: str, account_budget_proposal: str,
    ) -> str:
        """Return a fully-qualified account_budget_proposal string."""
        return "customers/{customer}/accountBudgetProposals/{account_budget_proposal}".format(
            customer=customer, account_budget_proposal=account_budget_proposal,
        )

    @staticmethod
    def parse_account_budget_proposal_path(path: str) -> Dict[str, str]:
        """Parse a account_budget_proposal path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/accountBudgetProposals/(?P<account_budget_proposal>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def account_link_path(customer: str, account_link: str,) -> str:
        """Return a fully-qualified account_link string."""
        return "customers/{customer}/accountLinks/{account_link}".format(
            customer=customer, account_link=account_link,
        )

    @staticmethod
    def parse_account_link_path(path: str) -> Dict[str, str]:
        """Parse a account_link path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/accountLinks/(?P<account_link>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def ad_path(customer: str, ad: str,) -> str:
        """Return a fully-qualified ad string."""
        return "customers/{customer}/ads/{ad}".format(customer=customer, ad=ad,)

    @staticmethod
    def parse_ad_path(path: str) -> Dict[str, str]:
        """Parse a ad path into its component segments."""
        m = re.match(r"^customers/(?P<customer>.+?)/ads/(?P<ad>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_path(customer: str, ad_group: str,) -> str:
        """Return a fully-qualified ad_group string."""
        return "customers/{customer}/adGroups/{ad_group}".format(
            customer=customer, ad_group=ad_group,
        )

    @staticmethod
    def parse_ad_group_path(path: str) -> Dict[str, str]:
        """Parse a ad_group path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/adGroups/(?P<ad_group>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_ad_path(customer: str, ad_group_ad: str,) -> str:
        """Return a fully-qualified ad_group_ad string."""
        return "customers/{customer}/adGroupAds/{ad_group_ad}".format(
            customer=customer, ad_group_ad=ad_group_ad,
        )

    @staticmethod
    def parse_ad_group_ad_path(path: str) -> Dict[str, str]:
        """Parse a ad_group_ad path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/adGroupAds/(?P<ad_group_ad>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_ad_asset_view_path(
        customer: str, ad_group_ad_asset_view: str,
    ) -> str:
        """Return a fully-qualified ad_group_ad_asset_view string."""
        return "customers/{customer}/adGroupAdAssetViews/{ad_group_ad_asset_view}".format(
            customer=customer, ad_group_ad_asset_view=ad_group_ad_asset_view,
        )

    @staticmethod
    def parse_ad_group_ad_asset_view_path(path: str) -> Dict[str, str]:
        """Parse a ad_group_ad_asset_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/adGroupAdAssetViews/(?P<ad_group_ad_asset_view>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_ad_label_path(customer: str, ad_group_ad_label: str,) -> str:
        """Return a fully-qualified ad_group_ad_label string."""
        return "customers/{customer}/adGroupAdLabels/{ad_group_ad_label}".format(
            customer=customer, ad_group_ad_label=ad_group_ad_label,
        )

    @staticmethod
    def parse_ad_group_ad_label_path(path: str) -> Dict[str, str]:
        """Parse a ad_group_ad_label path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/adGroupAdLabels/(?P<ad_group_ad_label>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_audience_view_path(
        customer: str, ad_group_audience_view: str,
    ) -> str:
        """Return a fully-qualified ad_group_audience_view string."""
        return "customers/{customer}/adGroupAudienceViews/{ad_group_audience_view}".format(
            customer=customer, ad_group_audience_view=ad_group_audience_view,
        )

    @staticmethod
    def parse_ad_group_audience_view_path(path: str) -> Dict[str, str]:
        """Parse a ad_group_audience_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/adGroupAudienceViews/(?P<ad_group_audience_view>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_bid_modifier_path(
        customer: str, ad_group_bid_modifier: str,
    ) -> str:
        """Return a fully-qualified ad_group_bid_modifier string."""
        return "customers/{customer}/adGroupBidModifiers/{ad_group_bid_modifier}".format(
            customer=customer, ad_group_bid_modifier=ad_group_bid_modifier,
        )

    @staticmethod
    def parse_ad_group_bid_modifier_path(path: str) -> Dict[str, str]:
        """Parse a ad_group_bid_modifier path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/adGroupBidModifiers/(?P<ad_group_bid_modifier>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_criterion_path(customer: str, ad_group_criterion: str,) -> str:
        """Return a fully-qualified ad_group_criterion string."""
        return "customers/{customer}/adGroupCriteria/{ad_group_criterion}".format(
            customer=customer, ad_group_criterion=ad_group_criterion,
        )

    @staticmethod
    def parse_ad_group_criterion_path(path: str) -> Dict[str, str]:
        """Parse a ad_group_criterion path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/adGroupCriteria/(?P<ad_group_criterion>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_criterion_label_path(
        customer: str, ad_group_criterion_label: str,
    ) -> str:
        """Return a fully-qualified ad_group_criterion_label string."""
        return "customers/{customer}/adGroupCriterionLabels/{ad_group_criterion_label}".format(
            customer=customer,
            ad_group_criterion_label=ad_group_criterion_label,
        )

    @staticmethod
    def parse_ad_group_criterion_label_path(path: str) -> Dict[str, str]:
        """Parse a ad_group_criterion_label path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/adGroupCriterionLabels/(?P<ad_group_criterion_label>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_criterion_simulation_path(
        customer: str, ad_group_criterion_simulation: str,
    ) -> str:
        """Return a fully-qualified ad_group_criterion_simulation string."""
        return "customers/{customer}/adGroupCriterionSimulations/{ad_group_criterion_simulation}".format(
            customer=customer,
            ad_group_criterion_simulation=ad_group_criterion_simulation,
        )

    @staticmethod
    def parse_ad_group_criterion_simulation_path(path: str) -> Dict[str, str]:
        """Parse a ad_group_criterion_simulation path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/adGroupCriterionSimulations/(?P<ad_group_criterion_simulation>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_extension_setting_path(
        customer: str, ad_group_extension_setting: str,
    ) -> str:
        """Return a fully-qualified ad_group_extension_setting string."""
        return "customers/{customer}/adGroupExtensionSettings/{ad_group_extension_setting}".format(
            customer=customer,
            ad_group_extension_setting=ad_group_extension_setting,
        )

    @staticmethod
    def parse_ad_group_extension_setting_path(path: str) -> Dict[str, str]:
        """Parse a ad_group_extension_setting path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/adGroupExtensionSettings/(?P<ad_group_extension_setting>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_feed_path(customer: str, ad_group_feed: str,) -> str:
        """Return a fully-qualified ad_group_feed string."""
        return "customers/{customer}/adGroupFeeds/{ad_group_feed}".format(
            customer=customer, ad_group_feed=ad_group_feed,
        )

    @staticmethod
    def parse_ad_group_feed_path(path: str) -> Dict[str, str]:
        """Parse a ad_group_feed path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/adGroupFeeds/(?P<ad_group_feed>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_label_path(customer: str, ad_group_label: str,) -> str:
        """Return a fully-qualified ad_group_label string."""
        return "customers/{customer}/adGroupLabels/{ad_group_label}".format(
            customer=customer, ad_group_label=ad_group_label,
        )

    @staticmethod
    def parse_ad_group_label_path(path: str) -> Dict[str, str]:
        """Parse a ad_group_label path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/adGroupLabels/(?P<ad_group_label>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_simulation_path(
        customer: str, ad_group_simulation: str,
    ) -> str:
        """Return a fully-qualified ad_group_simulation string."""
        return "customers/{customer}/adGroupSimulations/{ad_group_simulation}".format(
            customer=customer, ad_group_simulation=ad_group_simulation,
        )

    @staticmethod
    def parse_ad_group_simulation_path(path: str) -> Dict[str, str]:
        """Parse a ad_group_simulation path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/adGroupSimulations/(?P<ad_group_simulation>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def ad_parameter_path(customer: str, ad_parameter: str,) -> str:
        """Return a fully-qualified ad_parameter string."""
        return "customers/{customer}/adParameters/{ad_parameter}".format(
            customer=customer, ad_parameter=ad_parameter,
        )

    @staticmethod
    def parse_ad_parameter_path(path: str) -> Dict[str, str]:
        """Parse a ad_parameter path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/adParameters/(?P<ad_parameter>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def ad_schedule_view_path(customer: str, ad_schedule_view: str,) -> str:
        """Return a fully-qualified ad_schedule_view string."""
        return "customers/{customer}/adScheduleViews/{ad_schedule_view}".format(
            customer=customer, ad_schedule_view=ad_schedule_view,
        )

    @staticmethod
    def parse_ad_schedule_view_path(path: str) -> Dict[str, str]:
        """Parse a ad_schedule_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/adScheduleViews/(?P<ad_schedule_view>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def age_range_view_path(customer: str, age_range_view: str,) -> str:
        """Return a fully-qualified age_range_view string."""
        return "customers/{customer}/ageRangeViews/{age_range_view}".format(
            customer=customer, age_range_view=age_range_view,
        )

    @staticmethod
    def parse_age_range_view_path(path: str) -> Dict[str, str]:
        """Parse a age_range_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/ageRangeViews/(?P<age_range_view>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def asset_path(customer: str, asset: str,) -> str:
        """Return a fully-qualified asset string."""
        return "customers/{customer}/assets/{asset}".format(
            customer=customer, asset=asset,
        )

    @staticmethod
    def parse_asset_path(path: str) -> Dict[str, str]:
        """Parse a asset path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/assets/(?P<asset>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def batch_job_path(customer: str, batch_job: str,) -> str:
        """Return a fully-qualified batch_job string."""
        return "customers/{customer}/batchJobs/{batch_job}".format(
            customer=customer, batch_job=batch_job,
        )

    @staticmethod
    def parse_batch_job_path(path: str) -> Dict[str, str]:
        """Parse a batch_job path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/batchJobs/(?P<batch_job>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def bidding_strategy_path(customer: str, bidding_strategy: str,) -> str:
        """Return a fully-qualified bidding_strategy string."""
        return "customers/{customer}/biddingStrategies/{bidding_strategy}".format(
            customer=customer, bidding_strategy=bidding_strategy,
        )

    @staticmethod
    def parse_bidding_strategy_path(path: str) -> Dict[str, str]:
        """Parse a bidding_strategy path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/biddingStrategies/(?P<bidding_strategy>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def billing_setup_path(customer: str, billing_setup: str,) -> str:
        """Return a fully-qualified billing_setup string."""
        return "customers/{customer}/billingSetups/{billing_setup}".format(
            customer=customer, billing_setup=billing_setup,
        )

    @staticmethod
    def parse_billing_setup_path(path: str) -> Dict[str, str]:
        """Parse a billing_setup path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/billingSetups/(?P<billing_setup>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_path(customer: str, campaign: str,) -> str:
        """Return a fully-qualified campaign string."""
        return "customers/{customer}/campaigns/{campaign}".format(
            customer=customer, campaign=campaign,
        )

    @staticmethod
    def parse_campaign_path(path: str) -> Dict[str, str]:
        """Parse a campaign path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/campaigns/(?P<campaign>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_asset_path(customer: str, campaign_asset: str,) -> str:
        """Return a fully-qualified campaign_asset string."""
        return "customers/{customer}/campaignAssets/{campaign_asset}".format(
            customer=customer, campaign_asset=campaign_asset,
        )

    @staticmethod
    def parse_campaign_asset_path(path: str) -> Dict[str, str]:
        """Parse a campaign_asset path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/campaignAssets/(?P<campaign_asset>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_audience_view_path(
        customer: str, campaign_audience_view: str,
    ) -> str:
        """Return a fully-qualified campaign_audience_view string."""
        return "customers/{customer}/campaignAudienceViews/{campaign_audience_view}".format(
            customer=customer, campaign_audience_view=campaign_audience_view,
        )

    @staticmethod
    def parse_campaign_audience_view_path(path: str) -> Dict[str, str]:
        """Parse a campaign_audience_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/campaignAudienceViews/(?P<campaign_audience_view>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_bid_modifier_path(
        customer: str, campaign_bid_modifier: str,
    ) -> str:
        """Return a fully-qualified campaign_bid_modifier string."""
        return "customers/{customer}/campaignBidModifiers/{campaign_bid_modifier}".format(
            customer=customer, campaign_bid_modifier=campaign_bid_modifier,
        )

    @staticmethod
    def parse_campaign_bid_modifier_path(path: str) -> Dict[str, str]:
        """Parse a campaign_bid_modifier path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/campaignBidModifiers/(?P<campaign_bid_modifier>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_budget_path(customer: str, campaign_budget: str,) -> str:
        """Return a fully-qualified campaign_budget string."""
        return "customers/{customer}/campaignBudgets/{campaign_budget}".format(
            customer=customer, campaign_budget=campaign_budget,
        )

    @staticmethod
    def parse_campaign_budget_path(path: str) -> Dict[str, str]:
        """Parse a campaign_budget path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/campaignBudgets/(?P<campaign_budget>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_criterion_path(customer: str, campaign_criterion: str,) -> str:
        """Return a fully-qualified campaign_criterion string."""
        return "customers/{customer}/campaignCriteria/{campaign_criterion}".format(
            customer=customer, campaign_criterion=campaign_criterion,
        )

    @staticmethod
    def parse_campaign_criterion_path(path: str) -> Dict[str, str]:
        """Parse a campaign_criterion path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/campaignCriteria/(?P<campaign_criterion>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_criterion_simulation_path(
        customer: str, campaign_criterion_simulation: str,
    ) -> str:
        """Return a fully-qualified campaign_criterion_simulation string."""
        return "customers/{customer}/campaignCriterionSimulations/{campaign_criterion_simulation}".format(
            customer=customer,
            campaign_criterion_simulation=campaign_criterion_simulation,
        )

    @staticmethod
    def parse_campaign_criterion_simulation_path(path: str) -> Dict[str, str]:
        """Parse a campaign_criterion_simulation path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/campaignCriterionSimulations/(?P<campaign_criterion_simulation>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_draft_path(customer: str, campaign_draft: str,) -> str:
        """Return a fully-qualified campaign_draft string."""
        return "customers/{customer}/campaignDrafts/{campaign_draft}".format(
            customer=customer, campaign_draft=campaign_draft,
        )

    @staticmethod
    def parse_campaign_draft_path(path: str) -> Dict[str, str]:
        """Parse a campaign_draft path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/campaignDrafts/(?P<campaign_draft>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_experiment_path(
        customer: str, campaign_experiment: str,
    ) -> str:
        """Return a fully-qualified campaign_experiment string."""
        return "customers/{customer}/campaignExperiments/{campaign_experiment}".format(
            customer=customer, campaign_experiment=campaign_experiment,
        )

    @staticmethod
    def parse_campaign_experiment_path(path: str) -> Dict[str, str]:
        """Parse a campaign_experiment path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/campaignExperiments/(?P<campaign_experiment>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_extension_setting_path(
        customer: str, campaign_extension_setting: str,
    ) -> str:
        """Return a fully-qualified campaign_extension_setting string."""
        return "customers/{customer}/campaignExtensionSettings/{campaign_extension_setting}".format(
            customer=customer,
            campaign_extension_setting=campaign_extension_setting,
        )

    @staticmethod
    def parse_campaign_extension_setting_path(path: str) -> Dict[str, str]:
        """Parse a campaign_extension_setting path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/campaignExtensionSettings/(?P<campaign_extension_setting>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_feed_path(customer: str, campaign_feed: str,) -> str:
        """Return a fully-qualified campaign_feed string."""
        return "customers/{customer}/campaignFeeds/{campaign_feed}".format(
            customer=customer, campaign_feed=campaign_feed,
        )

    @staticmethod
    def parse_campaign_feed_path(path: str) -> Dict[str, str]:
        """Parse a campaign_feed path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/campaignFeeds/(?P<campaign_feed>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_label_path(customer: str, campaign_label: str,) -> str:
        """Return a fully-qualified campaign_label string."""
        return "customers/{customer}/campaignLabels/{campaign_label}".format(
            customer=customer, campaign_label=campaign_label,
        )

    @staticmethod
    def parse_campaign_label_path(path: str) -> Dict[str, str]:
        """Parse a campaign_label path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/campaignLabels/(?P<campaign_label>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_shared_set_path(
        customer: str, campaign_shared_set: str,
    ) -> str:
        """Return a fully-qualified campaign_shared_set string."""
        return "customers/{customer}/campaignSharedSets/{campaign_shared_set}".format(
            customer=customer, campaign_shared_set=campaign_shared_set,
        )

    @staticmethod
    def parse_campaign_shared_set_path(path: str) -> Dict[str, str]:
        """Parse a campaign_shared_set path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/campaignSharedSets/(?P<campaign_shared_set>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def carrier_constant_path(carrier_constant: str,) -> str:
        """Return a fully-qualified carrier_constant string."""
        return "carrierConstants/{carrier_constant}".format(
            carrier_constant=carrier_constant,
        )

    @staticmethod
    def parse_carrier_constant_path(path: str) -> Dict[str, str]:
        """Parse a carrier_constant path into its component segments."""
        m = re.match(r"^carrierConstants/(?P<carrier_constant>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def change_status_path(customer: str, change_status: str,) -> str:
        """Return a fully-qualified change_status string."""
        return "customers/{customer}/changeStatus/{change_status}".format(
            customer=customer, change_status=change_status,
        )

    @staticmethod
    def parse_change_status_path(path: str) -> Dict[str, str]:
        """Parse a change_status path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/changeStatus/(?P<change_status>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def click_view_path(customer: str, click_view: str,) -> str:
        """Return a fully-qualified click_view string."""
        return "customers/{customer}/clickViews/{click_view}".format(
            customer=customer, click_view=click_view,
        )

    @staticmethod
    def parse_click_view_path(path: str) -> Dict[str, str]:
        """Parse a click_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/clickViews/(?P<click_view>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def conversion_action_path(customer: str, conversion_action: str,) -> str:
        """Return a fully-qualified conversion_action string."""
        return "customers/{customer}/conversionActions/{conversion_action}".format(
            customer=customer, conversion_action=conversion_action,
        )

    @staticmethod
    def parse_conversion_action_path(path: str) -> Dict[str, str]:
        """Parse a conversion_action path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/conversionActions/(?P<conversion_action>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def currency_constant_path(currency_constant: str,) -> str:
        """Return a fully-qualified currency_constant string."""
        return "currencyConstants/{currency_constant}".format(
            currency_constant=currency_constant,
        )

    @staticmethod
    def parse_currency_constant_path(path: str) -> Dict[str, str]:
        """Parse a currency_constant path into its component segments."""
        m = re.match(r"^currencyConstants/(?P<currency_constant>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def customer_path(customer: str,) -> str:
        """Return a fully-qualified customer string."""
        return "customers/{customer}".format(customer=customer,)

    @staticmethod
    def parse_customer_path(path: str) -> Dict[str, str]:
        """Parse a customer path into its component segments."""
        m = re.match(r"^customers/(?P<customer>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def customer_client_path(customer: str, customer_client: str,) -> str:
        """Return a fully-qualified customer_client string."""
        return "customers/{customer}/customerClients/{customer_client}".format(
            customer=customer, customer_client=customer_client,
        )

    @staticmethod
    def parse_customer_client_path(path: str) -> Dict[str, str]:
        """Parse a customer_client path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/customerClients/(?P<customer_client>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def customer_client_link_path(
        customer: str, customer_client_link: str,
    ) -> str:
        """Return a fully-qualified customer_client_link string."""
        return "customers/{customer}/customerClientLinks/{customer_client_link}".format(
            customer=customer, customer_client_link=customer_client_link,
        )

    @staticmethod
    def parse_customer_client_link_path(path: str) -> Dict[str, str]:
        """Parse a customer_client_link path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/customerClientLinks/(?P<customer_client_link>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def customer_extension_setting_path(
        customer: str, customer_extension_setting: str,
    ) -> str:
        """Return a fully-qualified customer_extension_setting string."""
        return "customers/{customer}/customerExtensionSettings/{customer_extension_setting}".format(
            customer=customer,
            customer_extension_setting=customer_extension_setting,
        )

    @staticmethod
    def parse_customer_extension_setting_path(path: str) -> Dict[str, str]:
        """Parse a customer_extension_setting path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/customerExtensionSettings/(?P<customer_extension_setting>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def customer_feed_path(customer: str, customer_feed: str,) -> str:
        """Return a fully-qualified customer_feed string."""
        return "customers/{customer}/customerFeeds/{customer_feed}".format(
            customer=customer, customer_feed=customer_feed,
        )

    @staticmethod
    def parse_customer_feed_path(path: str) -> Dict[str, str]:
        """Parse a customer_feed path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/customerFeeds/(?P<customer_feed>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def customer_label_path(customer: str, customer_label: str,) -> str:
        """Return a fully-qualified customer_label string."""
        return "customers/{customer}/customerLabels/{customer_label}".format(
            customer=customer, customer_label=customer_label,
        )

    @staticmethod
    def parse_customer_label_path(path: str) -> Dict[str, str]:
        """Parse a customer_label path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/customerLabels/(?P<customer_label>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def customer_manager_link_path(
        customer: str, customer_manager_link: str,
    ) -> str:
        """Return a fully-qualified customer_manager_link string."""
        return "customers/{customer}/customerManagerLinks/{customer_manager_link}".format(
            customer=customer, customer_manager_link=customer_manager_link,
        )

    @staticmethod
    def parse_customer_manager_link_path(path: str) -> Dict[str, str]:
        """Parse a customer_manager_link path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/customerManagerLinks/(?P<customer_manager_link>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def customer_negative_criterion_path(
        customer: str, customer_negative_criterion: str,
    ) -> str:
        """Return a fully-qualified customer_negative_criterion string."""
        return "customers/{customer}/customerNegativeCriteria/{customer_negative_criterion}".format(
            customer=customer,
            customer_negative_criterion=customer_negative_criterion,
        )

    @staticmethod
    def parse_customer_negative_criterion_path(path: str) -> Dict[str, str]:
        """Parse a customer_negative_criterion path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/customerNegativeCriteria/(?P<customer_negative_criterion>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def custom_interest_path(customer: str, custom_interest: str,) -> str:
        """Return a fully-qualified custom_interest string."""
        return "customers/{customer}/customInterests/{custom_interest}".format(
            customer=customer, custom_interest=custom_interest,
        )

    @staticmethod
    def parse_custom_interest_path(path: str) -> Dict[str, str]:
        """Parse a custom_interest path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/customInterests/(?P<custom_interest>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def detail_placement_view_path(
        customer: str, detail_placement_view: str,
    ) -> str:
        """Return a fully-qualified detail_placement_view string."""
        return "customers/{customer}/detailPlacementViews/{detail_placement_view}".format(
            customer=customer, detail_placement_view=detail_placement_view,
        )

    @staticmethod
    def parse_detail_placement_view_path(path: str) -> Dict[str, str]:
        """Parse a detail_placement_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/detailPlacementViews/(?P<detail_placement_view>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def display_keyword_view_path(
        customer: str, display_keyword_view: str,
    ) -> str:
        """Return a fully-qualified display_keyword_view string."""
        return "customers/{customer}/displayKeywordViews/{display_keyword_view}".format(
            customer=customer, display_keyword_view=display_keyword_view,
        )

    @staticmethod
    def parse_display_keyword_view_path(path: str) -> Dict[str, str]:
        """Parse a display_keyword_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/displayKeywordViews/(?P<display_keyword_view>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def distance_view_path(customer: str, distance_view: str,) -> str:
        """Return a fully-qualified distance_view string."""
        return "customers/{customer}/distanceViews/{distance_view}".format(
            customer=customer, distance_view=distance_view,
        )

    @staticmethod
    def parse_distance_view_path(path: str) -> Dict[str, str]:
        """Parse a distance_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/distanceViews/(?P<distance_view>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def domain_category_path(customer: str, domain_category: str,) -> str:
        """Return a fully-qualified domain_category string."""
        return "customers/{customer}/domainCategories/{domain_category}".format(
            customer=customer, domain_category=domain_category,
        )

    @staticmethod
    def parse_domain_category_path(path: str) -> Dict[str, str]:
        """Parse a domain_category path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/domainCategories/(?P<domain_category>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def dynamic_search_ads_search_term_view_path(
        customer: str, dynamic_search_ads_search_term_view: str,
    ) -> str:
        """Return a fully-qualified dynamic_search_ads_search_term_view string."""
        return "customers/{customer}/dynamicSearchAdsSearchTermViews/{dynamic_search_ads_search_term_view}".format(
            customer=customer,
            dynamic_search_ads_search_term_view=dynamic_search_ads_search_term_view,
        )

    @staticmethod
    def parse_dynamic_search_ads_search_term_view_path(
        path: str,
    ) -> Dict[str, str]:
        """Parse a dynamic_search_ads_search_term_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/dynamicSearchAdsSearchTermViews/(?P<dynamic_search_ads_search_term_view>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def expanded_landing_page_view_path(
        customer: str, expanded_landing_page_view: str,
    ) -> str:
        """Return a fully-qualified expanded_landing_page_view string."""
        return "customers/{customer}/expandedLandingPageViews/{expanded_landing_page_view}".format(
            customer=customer,
            expanded_landing_page_view=expanded_landing_page_view,
        )

    @staticmethod
    def parse_expanded_landing_page_view_path(path: str) -> Dict[str, str]:
        """Parse a expanded_landing_page_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/expandedLandingPageViews/(?P<expanded_landing_page_view>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def extension_feed_item_path(
        customer: str, extension_feed_item: str,
    ) -> str:
        """Return a fully-qualified extension_feed_item string."""
        return "customers/{customer}/extensionFeedItems/{extension_feed_item}".format(
            customer=customer, extension_feed_item=extension_feed_item,
        )

    @staticmethod
    def parse_extension_feed_item_path(path: str) -> Dict[str, str]:
        """Parse a extension_feed_item path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/extensionFeedItems/(?P<extension_feed_item>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def feed_path(customer: str, feed: str,) -> str:
        """Return a fully-qualified feed string."""
        return "customers/{customer}/feeds/{feed}".format(
            customer=customer, feed=feed,
        )

    @staticmethod
    def parse_feed_path(path: str) -> Dict[str, str]:
        """Parse a feed path into its component segments."""
        m = re.match(r"^customers/(?P<customer>.+?)/feeds/(?P<feed>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def feed_item_path(customer: str, feed_item: str,) -> str:
        """Return a fully-qualified feed_item string."""
        return "customers/{customer}/feedItems/{feed_item}".format(
            customer=customer, feed_item=feed_item,
        )

    @staticmethod
    def parse_feed_item_path(path: str) -> Dict[str, str]:
        """Parse a feed_item path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/feedItems/(?P<feed_item>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def feed_item_target_path(customer: str, feed_item_target: str,) -> str:
        """Return a fully-qualified feed_item_target string."""
        return "customers/{customer}/feedItemTargets/{feed_item_target}".format(
            customer=customer, feed_item_target=feed_item_target,
        )

    @staticmethod
    def parse_feed_item_target_path(path: str) -> Dict[str, str]:
        """Parse a feed_item_target path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/feedItemTargets/(?P<feed_item_target>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def feed_mapping_path(customer: str, feed_mapping: str,) -> str:
        """Return a fully-qualified feed_mapping string."""
        return "customers/{customer}/feedMappings/{feed_mapping}".format(
            customer=customer, feed_mapping=feed_mapping,
        )

    @staticmethod
    def parse_feed_mapping_path(path: str) -> Dict[str, str]:
        """Parse a feed_mapping path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/feedMappings/(?P<feed_mapping>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def feed_placeholder_view_path(
        customer: str, feed_placeholder_view: str,
    ) -> str:
        """Return a fully-qualified feed_placeholder_view string."""
        return "customers/{customer}/feedPlaceholderViews/{feed_placeholder_view}".format(
            customer=customer, feed_placeholder_view=feed_placeholder_view,
        )

    @staticmethod
    def parse_feed_placeholder_view_path(path: str) -> Dict[str, str]:
        """Parse a feed_placeholder_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/feedPlaceholderViews/(?P<feed_placeholder_view>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def gender_view_path(customer: str, gender_view: str,) -> str:
        """Return a fully-qualified gender_view string."""
        return "customers/{customer}/genderViews/{gender_view}".format(
            customer=customer, gender_view=gender_view,
        )

    @staticmethod
    def parse_gender_view_path(path: str) -> Dict[str, str]:
        """Parse a gender_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/genderViews/(?P<gender_view>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def geographic_view_path(customer: str, geographic_view: str,) -> str:
        """Return a fully-qualified geographic_view string."""
        return "customers/{customer}/geographicViews/{geographic_view}".format(
            customer=customer, geographic_view=geographic_view,
        )

    @staticmethod
    def parse_geographic_view_path(path: str) -> Dict[str, str]:
        """Parse a geographic_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/geographicViews/(?P<geographic_view>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def geo_target_constant_path(geo_target_constant: str,) -> str:
        """Return a fully-qualified geo_target_constant string."""
        return "geoTargetConstants/{geo_target_constant}".format(
            geo_target_constant=geo_target_constant,
        )

    @staticmethod
    def parse_geo_target_constant_path(path: str) -> Dict[str, str]:
        """Parse a geo_target_constant path into its component segments."""
        m = re.match(r"^geoTargetConstants/(?P<geo_target_constant>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def group_placement_view_path(
        customer: str, group_placement_view: str,
    ) -> str:
        """Return a fully-qualified group_placement_view string."""
        return "customers/{customer}/groupPlacementViews/{group_placement_view}".format(
            customer=customer, group_placement_view=group_placement_view,
        )

    @staticmethod
    def parse_group_placement_view_path(path: str) -> Dict[str, str]:
        """Parse a group_placement_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/groupPlacementViews/(?P<group_placement_view>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def hotel_group_view_path(customer: str, hotel_group_view: str,) -> str:
        """Return a fully-qualified hotel_group_view string."""
        return "customers/{customer}/hotelGroupViews/{hotel_group_view}".format(
            customer=customer, hotel_group_view=hotel_group_view,
        )

    @staticmethod
    def parse_hotel_group_view_path(path: str) -> Dict[str, str]:
        """Parse a hotel_group_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/hotelGroupViews/(?P<hotel_group_view>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def hotel_performance_view_path(customer: str,) -> str:
        """Return a fully-qualified hotel_performance_view string."""
        return "customers/{customer}/hotelPerformanceView".format(
            customer=customer,
        )

    @staticmethod
    def parse_hotel_performance_view_path(path: str) -> Dict[str, str]:
        """Parse a hotel_performance_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/hotelPerformanceView$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def income_range_view_path(customer: str, income_range_view: str,) -> str:
        """Return a fully-qualified income_range_view string."""
        return "customers/{customer}/incomeRangeViews/{income_range_view}".format(
            customer=customer, income_range_view=income_range_view,
        )

    @staticmethod
    def parse_income_range_view_path(path: str) -> Dict[str, str]:
        """Parse a income_range_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/incomeRangeViews/(?P<income_range_view>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def keyword_plan_path(customer: str, keyword_plan: str,) -> str:
        """Return a fully-qualified keyword_plan string."""
        return "customers/{customer}/keywordPlans/{keyword_plan}".format(
            customer=customer, keyword_plan=keyword_plan,
        )

    @staticmethod
    def parse_keyword_plan_path(path: str) -> Dict[str, str]:
        """Parse a keyword_plan path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/keywordPlans/(?P<keyword_plan>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def keyword_plan_ad_group_path(
        customer: str, keyword_plan_ad_group: str,
    ) -> str:
        """Return a fully-qualified keyword_plan_ad_group string."""
        return "customers/{customer}/keywordPlanAdGroups/{keyword_plan_ad_group}".format(
            customer=customer, keyword_plan_ad_group=keyword_plan_ad_group,
        )

    @staticmethod
    def parse_keyword_plan_ad_group_path(path: str) -> Dict[str, str]:
        """Parse a keyword_plan_ad_group path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/keywordPlanAdGroups/(?P<keyword_plan_ad_group>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def keyword_plan_ad_group_keyword_path(
        customer: str, keyword_plan_ad_group_keyword: str,
    ) -> str:
        """Return a fully-qualified keyword_plan_ad_group_keyword string."""
        return "customers/{customer}/keywordPlanAdGroupKeywords/{keyword_plan_ad_group_keyword}".format(
            customer=customer,
            keyword_plan_ad_group_keyword=keyword_plan_ad_group_keyword,
        )

    @staticmethod
    def parse_keyword_plan_ad_group_keyword_path(path: str) -> Dict[str, str]:
        """Parse a keyword_plan_ad_group_keyword path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/keywordPlanAdGroupKeywords/(?P<keyword_plan_ad_group_keyword>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def keyword_plan_campaign_path(
        customer: str, keyword_plan_campaign: str,
    ) -> str:
        """Return a fully-qualified keyword_plan_campaign string."""
        return "customers/{customer}/keywordPlanCampaigns/{keyword_plan_campaign}".format(
            customer=customer, keyword_plan_campaign=keyword_plan_campaign,
        )

    @staticmethod
    def parse_keyword_plan_campaign_path(path: str) -> Dict[str, str]:
        """Parse a keyword_plan_campaign path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/keywordPlanCampaigns/(?P<keyword_plan_campaign>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def keyword_plan_campaign_keyword_path(
        customer: str, keyword_plan_campaign_keyword: str,
    ) -> str:
        """Return a fully-qualified keyword_plan_campaign_keyword string."""
        return "customers/{customer}/keywordPlanCampaignKeywords/{keyword_plan_campaign_keyword}".format(
            customer=customer,
            keyword_plan_campaign_keyword=keyword_plan_campaign_keyword,
        )

    @staticmethod
    def parse_keyword_plan_campaign_keyword_path(path: str) -> Dict[str, str]:
        """Parse a keyword_plan_campaign_keyword path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/keywordPlanCampaignKeywords/(?P<keyword_plan_campaign_keyword>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def keyword_view_path(customer: str, keyword_view: str,) -> str:
        """Return a fully-qualified keyword_view string."""
        return "customers/{customer}/keywordViews/{keyword_view}".format(
            customer=customer, keyword_view=keyword_view,
        )

    @staticmethod
    def parse_keyword_view_path(path: str) -> Dict[str, str]:
        """Parse a keyword_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/keywordViews/(?P<keyword_view>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def label_path(customer: str, label: str,) -> str:
        """Return a fully-qualified label string."""
        return "customers/{customer}/labels/{label}".format(
            customer=customer, label=label,
        )

    @staticmethod
    def parse_label_path(path: str) -> Dict[str, str]:
        """Parse a label path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/labels/(?P<label>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def landing_page_view_path(customer: str, landing_page_view: str,) -> str:
        """Return a fully-qualified landing_page_view string."""
        return "customers/{customer}/landingPageViews/{landing_page_view}".format(
            customer=customer, landing_page_view=landing_page_view,
        )

    @staticmethod
    def parse_landing_page_view_path(path: str) -> Dict[str, str]:
        """Parse a landing_page_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/landingPageViews/(?P<landing_page_view>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def language_constant_path(language_constant: str,) -> str:
        """Return a fully-qualified language_constant string."""
        return "languageConstants/{language_constant}".format(
            language_constant=language_constant,
        )

    @staticmethod
    def parse_language_constant_path(path: str) -> Dict[str, str]:
        """Parse a language_constant path into its component segments."""
        m = re.match(r"^languageConstants/(?P<language_constant>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def location_view_path(customer: str, location_view: str,) -> str:
        """Return a fully-qualified location_view string."""
        return "customers/{customer}/locationViews/{location_view}".format(
            customer=customer, location_view=location_view,
        )

    @staticmethod
    def parse_location_view_path(path: str) -> Dict[str, str]:
        """Parse a location_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/locationViews/(?P<location_view>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def managed_placement_view_path(
        customer: str, managed_placement_view: str,
    ) -> str:
        """Return a fully-qualified managed_placement_view string."""
        return "customers/{customer}/managedPlacementViews/{managed_placement_view}".format(
            customer=customer, managed_placement_view=managed_placement_view,
        )

    @staticmethod
    def parse_managed_placement_view_path(path: str) -> Dict[str, str]:
        """Parse a managed_placement_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/managedPlacementViews/(?P<managed_placement_view>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def media_file_path(customer: str, media_file: str,) -> str:
        """Return a fully-qualified media_file string."""
        return "customers/{customer}/mediaFiles/{media_file}".format(
            customer=customer, media_file=media_file,
        )

    @staticmethod
    def parse_media_file_path(path: str) -> Dict[str, str]:
        """Parse a media_file path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/mediaFiles/(?P<media_file>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def mobile_app_category_constant_path(
        mobile_app_category_constant: str,
    ) -> str:
        """Return a fully-qualified mobile_app_category_constant string."""
        return "mobileAppCategoryConstants/{mobile_app_category_constant}".format(
            mobile_app_category_constant=mobile_app_category_constant,
        )

    @staticmethod
    def parse_mobile_app_category_constant_path(path: str) -> Dict[str, str]:
        """Parse a mobile_app_category_constant path into its component segments."""
        m = re.match(
            r"^mobileAppCategoryConstants/(?P<mobile_app_category_constant>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def mobile_device_constant_path(mobile_device_constant: str,) -> str:
        """Return a fully-qualified mobile_device_constant string."""
        return "mobileDeviceConstants/{mobile_device_constant}".format(
            mobile_device_constant=mobile_device_constant,
        )

    @staticmethod
    def parse_mobile_device_constant_path(path: str) -> Dict[str, str]:
        """Parse a mobile_device_constant path into its component segments."""
        m = re.match(
            r"^mobileDeviceConstants/(?P<mobile_device_constant>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def offline_user_data_job_path(
        customer: str, offline_user_data_job: str,
    ) -> str:
        """Return a fully-qualified offline_user_data_job string."""
        return "customers/{customer}/offlineUserDataJobs/{offline_user_data_job}".format(
            customer=customer, offline_user_data_job=offline_user_data_job,
        )

    @staticmethod
    def parse_offline_user_data_job_path(path: str) -> Dict[str, str]:
        """Parse a offline_user_data_job path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/offlineUserDataJobs/(?P<offline_user_data_job>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def operating_system_version_constant_path(
        operating_system_version_constant: str,
    ) -> str:
        """Return a fully-qualified operating_system_version_constant string."""
        return "operatingSystemVersionConstants/{operating_system_version_constant}".format(
            operating_system_version_constant=operating_system_version_constant,
        )

    @staticmethod
    def parse_operating_system_version_constant_path(
        path: str,
    ) -> Dict[str, str]:
        """Parse a operating_system_version_constant path into its component segments."""
        m = re.match(
            r"^operatingSystemVersionConstants/(?P<operating_system_version_constant>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def paid_organic_search_term_view_path(
        customer: str, paid_organic_search_term_view: str,
    ) -> str:
        """Return a fully-qualified paid_organic_search_term_view string."""
        return "customers/{customer}/paidOrganicSearchTermViews/{paid_organic_search_term_view}".format(
            customer=customer,
            paid_organic_search_term_view=paid_organic_search_term_view,
        )

    @staticmethod
    def parse_paid_organic_search_term_view_path(path: str) -> Dict[str, str]:
        """Parse a paid_organic_search_term_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/paidOrganicSearchTermViews/(?P<paid_organic_search_term_view>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def parental_status_view_path(
        customer: str, parental_status_view: str,
    ) -> str:
        """Return a fully-qualified parental_status_view string."""
        return "customers/{customer}/parentalStatusViews/{parental_status_view}".format(
            customer=customer, parental_status_view=parental_status_view,
        )

    @staticmethod
    def parse_parental_status_view_path(path: str) -> Dict[str, str]:
        """Parse a parental_status_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/parentalStatusViews/(?P<parental_status_view>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def payments_account_path(customer: str, payments_account: str,) -> str:
        """Return a fully-qualified payments_account string."""
        return "customers/{customer}/paymentsAccounts/{payments_account}".format(
            customer=customer, payments_account=payments_account,
        )

    @staticmethod
    def parse_payments_account_path(path: str) -> Dict[str, str]:
        """Parse a payments_account path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/paymentsAccounts/(?P<payments_account>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def product_bidding_category_constant_path(
        product_bidding_category_constant: str,
    ) -> str:
        """Return a fully-qualified product_bidding_category_constant string."""
        return "productBiddingCategoryConstants/{product_bidding_category_constant}".format(
            product_bidding_category_constant=product_bidding_category_constant,
        )

    @staticmethod
    def parse_product_bidding_category_constant_path(
        path: str,
    ) -> Dict[str, str]:
        """Parse a product_bidding_category_constant path into its component segments."""
        m = re.match(
            r"^productBiddingCategoryConstants/(?P<product_bidding_category_constant>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def product_group_view_path(customer: str, product_group_view: str,) -> str:
        """Return a fully-qualified product_group_view string."""
        return "customers/{customer}/productGroupViews/{product_group_view}".format(
            customer=customer, product_group_view=product_group_view,
        )

    @staticmethod
    def parse_product_group_view_path(path: str) -> Dict[str, str]:
        """Parse a product_group_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/productGroupViews/(?P<product_group_view>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def recommendation_path(customer: str, recommendation: str,) -> str:
        """Return a fully-qualified recommendation string."""
        return "customers/{customer}/recommendations/{recommendation}".format(
            customer=customer, recommendation=recommendation,
        )

    @staticmethod
    def parse_recommendation_path(path: str) -> Dict[str, str]:
        """Parse a recommendation path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/recommendations/(?P<recommendation>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def remarketing_action_path(customer: str, remarketing_action: str,) -> str:
        """Return a fully-qualified remarketing_action string."""
        return "customers/{customer}/remarketingActions/{remarketing_action}".format(
            customer=customer, remarketing_action=remarketing_action,
        )

    @staticmethod
    def parse_remarketing_action_path(path: str) -> Dict[str, str]:
        """Parse a remarketing_action path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/remarketingActions/(?P<remarketing_action>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def search_term_view_path(customer: str, search_term_view: str,) -> str:
        """Return a fully-qualified search_term_view string."""
        return "customers/{customer}/searchTermViews/{search_term_view}".format(
            customer=customer, search_term_view=search_term_view,
        )

    @staticmethod
    def parse_search_term_view_path(path: str) -> Dict[str, str]:
        """Parse a search_term_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/searchTermViews/(?P<search_term_view>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def shared_criterion_path(customer: str, shared_criterion: str,) -> str:
        """Return a fully-qualified shared_criterion string."""
        return "customers/{customer}/sharedCriteria/{shared_criterion}".format(
            customer=customer, shared_criterion=shared_criterion,
        )

    @staticmethod
    def parse_shared_criterion_path(path: str) -> Dict[str, str]:
        """Parse a shared_criterion path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/sharedCriteria/(?P<shared_criterion>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def shared_set_path(customer: str, shared_set: str,) -> str:
        """Return a fully-qualified shared_set string."""
        return "customers/{customer}/sharedSets/{shared_set}".format(
            customer=customer, shared_set=shared_set,
        )

    @staticmethod
    def parse_shared_set_path(path: str) -> Dict[str, str]:
        """Parse a shared_set path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/sharedSets/(?P<shared_set>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def shopping_performance_view_path(customer: str,) -> str:
        """Return a fully-qualified shopping_performance_view string."""
        return "customers/{customer}/shoppingPerformanceView".format(
            customer=customer,
        )

    @staticmethod
    def parse_shopping_performance_view_path(path: str) -> Dict[str, str]:
        """Parse a shopping_performance_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/shoppingPerformanceView$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def third_party_app_analytics_link_path(
        customer: str, third_party_app_analytics_link: str,
    ) -> str:
        """Return a fully-qualified third_party_app_analytics_link string."""
        return "customers/{customer}/thirdPartyAppAnalyticsLinks/{third_party_app_analytics_link}".format(
            customer=customer,
            third_party_app_analytics_link=third_party_app_analytics_link,
        )

    @staticmethod
    def parse_third_party_app_analytics_link_path(path: str) -> Dict[str, str]:
        """Parse a third_party_app_analytics_link path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/thirdPartyAppAnalyticsLinks/(?P<third_party_app_analytics_link>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def topic_constant_path(topic_constant: str,) -> str:
        """Return a fully-qualified topic_constant string."""
        return "topicConstants/{topic_constant}".format(
            topic_constant=topic_constant,
        )

    @staticmethod
    def parse_topic_constant_path(path: str) -> Dict[str, str]:
        """Parse a topic_constant path into its component segments."""
        m = re.match(r"^topicConstants/(?P<topic_constant>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def topic_view_path(customer: str, topic_view: str,) -> str:
        """Return a fully-qualified topic_view string."""
        return "customers/{customer}/topicViews/{topic_view}".format(
            customer=customer, topic_view=topic_view,
        )

    @staticmethod
    def parse_topic_view_path(path: str) -> Dict[str, str]:
        """Parse a topic_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/topicViews/(?P<topic_view>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def user_interest_path(customer: str, user_interest: str,) -> str:
        """Return a fully-qualified user_interest string."""
        return "customers/{customer}/userInterests/{user_interest}".format(
            customer=customer, user_interest=user_interest,
        )

    @staticmethod
    def parse_user_interest_path(path: str) -> Dict[str, str]:
        """Parse a user_interest path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/userInterests/(?P<user_interest>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def user_list_path(customer: str, user_list: str,) -> str:
        """Return a fully-qualified user_list string."""
        return "customers/{customer}/userLists/{user_list}".format(
            customer=customer, user_list=user_list,
        )

    @staticmethod
    def parse_user_list_path(path: str) -> Dict[str, str]:
        """Parse a user_list path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/userLists/(?P<user_list>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def user_location_view_path(customer: str, user_location_view: str,) -> str:
        """Return a fully-qualified user_location_view string."""
        return "customers/{customer}/userLocationViews/{user_location_view}".format(
            customer=customer, user_location_view=user_location_view,
        )

    @staticmethod
    def parse_user_location_view_path(path: str) -> Dict[str, str]:
        """Parse a user_location_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/userLocationViews/(?P<user_location_view>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def video_path(customer: str, video: str,) -> str:
        """Return a fully-qualified video string."""
        return "customers/{customer}/videos/{video}".format(
            customer=customer, video=video,
        )

    @staticmethod
    def parse_video_path(path: str) -> Dict[str, str]:
        """Parse a video path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer>.+?)/videos/(?P<video>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(billing_account: str,) -> str:
        """Return a fully-qualified billing_account string."""
        return "billingAccounts/{billing_account}".format(
            billing_account=billing_account,
        )

    @staticmethod
    def parse_common_billing_account_path(path: str) -> Dict[str, str]:
        """Parse a billing_account path into its component segments."""
        m = re.match(r"^billingAccounts/(?P<billing_account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_folder_path(folder: str,) -> str:
        """Return a fully-qualified folder string."""
        return "folders/{folder}".format(folder=folder,)

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(organization: str,) -> str:
        """Return a fully-qualified organization string."""
        return "organizations/{organization}".format(organization=organization,)

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(project: str,) -> str:
        """Return a fully-qualified project string."""
        return "projects/{project}".format(project=project,)

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(project: str, location: str,) -> str:
        """Return a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(
            project=project, location=location,
        )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str, str]:
        """Parse a location path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path
        )
        return m.groupdict() if m else {}

    def __init__(
        self,
        *,
        credentials: Optional[credentials.Credentials] = None,
        transport: Union[str, GoogleAdsServiceTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the google ads service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.GoogleAdsServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. It won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = client_options_lib.from_dict(client_options)
        if client_options is None:
            client_options = client_options_lib.ClientOptions()

        # Create SSL credentials for mutual TLS if needed.
        use_client_cert = bool(
            util.strtobool(
                os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false")
            )
        )

        ssl_credentials = None
        is_mtls = False
        if use_client_cert:
            if client_options.client_cert_source:
                import grpc  # type: ignore

                cert, key = client_options.client_cert_source()
                ssl_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )
                is_mtls = True
            else:
                creds = SslCredentials()
                is_mtls = creds.is_mtls
                ssl_credentials = creds.ssl_credentials if is_mtls else None

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        else:
            use_mtls_env = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
            if use_mtls_env == "never":
                api_endpoint = self.DEFAULT_ENDPOINT
            elif use_mtls_env == "always":
                api_endpoint = self.DEFAULT_MTLS_ENDPOINT
            elif use_mtls_env == "auto":
                api_endpoint = (
                    self.DEFAULT_MTLS_ENDPOINT
                    if is_mtls
                    else self.DEFAULT_ENDPOINT
                )
            else:
                raise MutualTLSChannelError(
                    "Unsupported GOOGLE_API_USE_MTLS_ENDPOINT value. Accepted values: never, auto, always"
                )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, GoogleAdsServiceTransport):
            # transport is a GoogleAdsServiceTransport instance.
            if credentials:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            self._transport = transport
        elif isinstance(transport, str):
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials, host=self.DEFAULT_ENDPOINT
            )
        else:
            self._transport = GoogleAdsServiceGrpcTransport(
                credentials=credentials,
                host=api_endpoint,
                ssl_channel_credentials=ssl_credentials,
                client_info=client_info,
            )

    def search(
        self,
        request: google_ads_service.SearchGoogleAdsRequest = None,
        *,
        customer_id: str = None,
        query: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.SearchPager:
        r"""Returns all rows that match the search query.

        Args:
            request (:class:`google.ads.googleads.v5.services.types.SearchGoogleAdsRequest`):
                The request object. Request message for
                [GoogleAdsService.Search][google.ads.googleads.v5.services.GoogleAdsService.Search].
            customer_id (:class:`str`):
                Required. The ID of the customer
                being queried.

                This corresponds to the ``customer_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            query (:class:`str`):
                Required. The query string.
                This corresponds to the ``query`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.ads.googleads.v5.services.services.google_ads_service.pagers.SearchPager:
                Response message for
                [GoogleAdsService.Search][google.ads.googleads.v5.services.GoogleAdsService.Search].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([customer_id, query]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a google_ads_service.SearchGoogleAdsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, google_ads_service.SearchGoogleAdsRequest):
            request = google_ads_service.SearchGoogleAdsRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if customer_id is not None:
                request.customer_id = customer_id
            if query is not None:
                request.query = query

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.search]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("customer_id", request.customer_id),)
            ),
        )

        # Send the request.
        response = rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.SearchPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def search_stream(
        self,
        request: google_ads_service.SearchGoogleAdsStreamRequest = None,
        *,
        customer_id: str = None,
        query: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> Iterable[google_ads_service.SearchGoogleAdsStreamResponse]:
        r"""Returns all rows that match the search stream query.

        Args:
            request (:class:`google.ads.googleads.v5.services.types.SearchGoogleAdsStreamRequest`):
                The request object. Request message for
                [GoogleAdsService.SearchStream][google.ads.googleads.v5.services.GoogleAdsService.SearchStream].
            customer_id (:class:`str`):
                Required. The ID of the customer
                being queried.

                This corresponds to the ``customer_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            query (:class:`str`):
                Required. The query string.
                This corresponds to the ``query`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            Iterable[google.ads.googleads.v5.services.types.SearchGoogleAdsStreamResponse]:
                Response message for
                [GoogleAdsService.SearchStream][google.ads.googleads.v5.services.GoogleAdsService.SearchStream].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([customer_id, query]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a google_ads_service.SearchGoogleAdsStreamRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, google_ads_service.SearchGoogleAdsStreamRequest
        ):
            request = google_ads_service.SearchGoogleAdsStreamRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if customer_id is not None:
                request.customer_id = customer_id
            if query is not None:
                request.query = query

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.search_stream]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("customer_id", request.customer_id),)
            ),
        )

        # Send the request.
        response = rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

        # Done; return the response.
        return response

    def mutate(
        self,
        request: google_ads_service.MutateGoogleAdsRequest = None,
        *,
        customer_id: str = None,
        mutate_operations: Sequence[google_ads_service.MutateOperation] = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> google_ads_service.MutateGoogleAdsResponse:
        r"""Creates, updates, or removes resources. This method supports
        atomic transactions with multiple types of resources. For
        example, you can atomically create a campaign and a campaign
        budget, or perform up to thousands of mutates atomically.

        This method is essentially a wrapper around a series of mutate
        methods. The only features it offers over calling those methods
        directly are:

        -  Atomic transactions
        -  Temp resource names (described below)
        -  Somewhat reduced latency over making a series of mutate calls

        Note: Only resources that support atomic transactions are
        included, so this method can't replace all calls to individual
        services.

        Atomic Transaction Benefits
        ---------------------------

        Atomicity makes error handling much easier. If you're making a
        series of changes and one fails, it can leave your account in an
        inconsistent state. With atomicity, you either reach the desired
        state directly, or the request fails and you can retry.

        Temp Resource Names
        -------------------

        Temp resource names are a special type of resource name used to
        create a resource and reference that resource in the same
        request. For example, if a campaign budget is created with
        ``resource_name`` equal to ``customers/123/campaignBudgets/-1``,
        that resource name can be reused in the ``Campaign.budget``
        field in the same request. That way, the two resources are
        created and linked atomically.

        To create a temp resource name, put a negative number in the
        part of the name that the server would normally allocate.

        Note:

        -  Resources must be created with a temp name before the name
           can be reused. For example, the previous
           CampaignBudget+Campaign example would fail if the mutate
           order was reversed.
        -  Temp names are not remembered across requests.
        -  There's no limit to the number of temp names in a request.
        -  Each temp name must use a unique negative number, even if the
           resource types differ.

        Latency
        -------

        It's important to group mutates by resource type or the request
        may time out and fail. Latency is roughly equal to a series of
        calls to individual mutate methods, where each change in
        resource type is a new call. For example, mutating 10 campaigns
        then 10 ad groups is like 2 calls, while mutating 1 campaign, 1
        ad group, 1 campaign, 1 ad group is like 4 calls.

        Args:
            request (:class:`google.ads.googleads.v5.services.types.MutateGoogleAdsRequest`):
                The request object. Request message for
                [GoogleAdsService.Mutate][google.ads.googleads.v5.services.GoogleAdsService.Mutate].
            customer_id (:class:`str`):
                Required. The ID of the customer
                whose resources are being modified.

                This corresponds to the ``customer_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            mutate_operations (:class:`Sequence[google.ads.googleads.v5.services.types.MutateOperation]`):
                Required. The list of operations to
                perform on individual resources.

                This corresponds to the ``mutate_operations`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.ads.googleads.v5.services.types.MutateGoogleAdsResponse:
                Response message for
                [GoogleAdsService.Mutate][google.ads.googleads.v5.services.GoogleAdsService.Mutate].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([customer_id, mutate_operations]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a google_ads_service.MutateGoogleAdsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, google_ads_service.MutateGoogleAdsRequest):
            request = google_ads_service.MutateGoogleAdsRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if customer_id is not None:
                request.customer_id = customer_id
            if mutate_operations is not None:
                request.mutate_operations = mutate_operations

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.mutate]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("customer_id", request.customer_id),)
            ),
        )

        # Send the request.
        response = rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

        # Done; return the response.
        return response


__all__ = ("GoogleAdsServiceClient",)
