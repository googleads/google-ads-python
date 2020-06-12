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

from google.ads.googleads.v6.services.services.google_ads_service import pagers
from google.ads.googleads.v6.services.types import google_ads_service
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
    def account_budget_path(customer_id: str, account_budget_id: str,) -> str:
        """Return a fully-qualified account_budget string."""
        return "customers/{customer_id}/accountBudgets/{account_budget_id}".format(
            customer_id=customer_id, account_budget_id=account_budget_id,
        )

    @staticmethod
    def parse_account_budget_path(path: str) -> Dict[str, str]:
        """Parse a account_budget path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/accountBudgets/(?P<account_budget_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def account_budget_proposal_path(
        customer_id: str, account_budget_proposal_id: str,
    ) -> str:
        """Return a fully-qualified account_budget_proposal string."""
        return "customers/{customer_id}/accountBudgetProposals/{account_budget_proposal_id}".format(
            customer_id=customer_id,
            account_budget_proposal_id=account_budget_proposal_id,
        )

    @staticmethod
    def parse_account_budget_proposal_path(path: str) -> Dict[str, str]:
        """Parse a account_budget_proposal path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/accountBudgetProposals/(?P<account_budget_proposal_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def account_link_path(customer_id: str, account_link_id: str,) -> str:
        """Return a fully-qualified account_link string."""
        return "customers/{customer_id}/accountLinks/{account_link_id}".format(
            customer_id=customer_id, account_link_id=account_link_id,
        )

    @staticmethod
    def parse_account_link_path(path: str) -> Dict[str, str]:
        """Parse a account_link path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/accountLinks/(?P<account_link_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def ad_path(customer_id: str, ad_id: str,) -> str:
        """Return a fully-qualified ad string."""
        return "customers/{customer_id}/ads/{ad_id}".format(
            customer_id=customer_id, ad_id=ad_id,
        )

    @staticmethod
    def parse_ad_path(path: str) -> Dict[str, str]:
        """Parse a ad path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/ads/(?P<ad_id>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_path(customer_id: str, ad_group_id: str,) -> str:
        """Return a fully-qualified ad_group string."""
        return "customers/{customer_id}/adGroups/{ad_group_id}".format(
            customer_id=customer_id, ad_group_id=ad_group_id,
        )

    @staticmethod
    def parse_ad_group_path(path: str) -> Dict[str, str]:
        """Parse a ad_group path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/adGroups/(?P<ad_group_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_ad_path(
        customer_id: str, ad_group_id: str, ad_id: str,
    ) -> str:
        """Return a fully-qualified ad_group_ad string."""
        return "customers/{customer_id}/adGroupAds/{ad_group_id}~{ad_id}".format(
            customer_id=customer_id, ad_group_id=ad_group_id, ad_id=ad_id,
        )

    @staticmethod
    def parse_ad_group_ad_path(path: str) -> Dict[str, str]:
        """Parse a ad_group_ad path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/adGroupAds/(?P<ad_group_id>.+?)~(?P<ad_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_ad_asset_view_path(
        customer_id: str,
        ad_group_id: str,
        ad_id: str,
        asset_id: str,
        field_type: str,
    ) -> str:
        """Return a fully-qualified ad_group_ad_asset_view string."""
        return "customers/{customer_id}/adGroupAdAssetViews/{ad_group_id}~{ad_id}~{asset_id}~{field_type}".format(
            customer_id=customer_id,
            ad_group_id=ad_group_id,
            ad_id=ad_id,
            asset_id=asset_id,
            field_type=field_type,
        )

    @staticmethod
    def parse_ad_group_ad_asset_view_path(path: str) -> Dict[str, str]:
        """Parse a ad_group_ad_asset_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/adGroupAdAssetViews/(?P<ad_group_id>.+?)~(?P<ad_id>.+?)~(?P<asset_id>.+?)~(?P<field_type>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_ad_label_path(
        customer_id: str, ad_group_id: str, ad_id: str, label_id: str,
    ) -> str:
        """Return a fully-qualified ad_group_ad_label string."""
        return "customers/{customer_id}/adGroupAdLabels/{ad_group_id}~{ad_id}~{label_id}".format(
            customer_id=customer_id,
            ad_group_id=ad_group_id,
            ad_id=ad_id,
            label_id=label_id,
        )

    @staticmethod
    def parse_ad_group_ad_label_path(path: str) -> Dict[str, str]:
        """Parse a ad_group_ad_label path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/adGroupAdLabels/(?P<ad_group_id>.+?)~(?P<ad_id>.+?)~(?P<label_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_audience_view_path(
        customer_id: str, ad_group_id: str, criterion_id: str,
    ) -> str:
        """Return a fully-qualified ad_group_audience_view string."""
        return "customers/{customer_id}/adGroupAudienceViews/{ad_group_id}~{criterion_id}".format(
            customer_id=customer_id,
            ad_group_id=ad_group_id,
            criterion_id=criterion_id,
        )

    @staticmethod
    def parse_ad_group_audience_view_path(path: str) -> Dict[str, str]:
        """Parse a ad_group_audience_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/adGroupAudienceViews/(?P<ad_group_id>.+?)~(?P<criterion_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_bid_modifier_path(
        customer_id: str, ad_group_id: str, criterion_id: str,
    ) -> str:
        """Return a fully-qualified ad_group_bid_modifier string."""
        return "customers/{customer_id}/adGroupBidModifiers/{ad_group_id}~{criterion_id}".format(
            customer_id=customer_id,
            ad_group_id=ad_group_id,
            criterion_id=criterion_id,
        )

    @staticmethod
    def parse_ad_group_bid_modifier_path(path: str) -> Dict[str, str]:
        """Parse a ad_group_bid_modifier path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/adGroupBidModifiers/(?P<ad_group_id>.+?)~(?P<criterion_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_criterion_path(
        customer_id: str, ad_group_id: str, criterion_id: str,
    ) -> str:
        """Return a fully-qualified ad_group_criterion string."""
        return "customers/{customer_id}/adGroupCriteria/{ad_group_id}~{criterion_id}".format(
            customer_id=customer_id,
            ad_group_id=ad_group_id,
            criterion_id=criterion_id,
        )

    @staticmethod
    def parse_ad_group_criterion_path(path: str) -> Dict[str, str]:
        """Parse a ad_group_criterion path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/adGroupCriteria/(?P<ad_group_id>.+?)~(?P<criterion_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_criterion_label_path(
        customer_id: str, ad_group_id: str, criterion_id: str, label_id: str,
    ) -> str:
        """Return a fully-qualified ad_group_criterion_label string."""
        return "customers/{customer_id}/adGroupCriterionLabels/{ad_group_id}~{criterion_id}~{label_id}".format(
            customer_id=customer_id,
            ad_group_id=ad_group_id,
            criterion_id=criterion_id,
            label_id=label_id,
        )

    @staticmethod
    def parse_ad_group_criterion_label_path(path: str) -> Dict[str, str]:
        """Parse a ad_group_criterion_label path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/adGroupCriterionLabels/(?P<ad_group_id>.+?)~(?P<criterion_id>.+?)~(?P<label_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_criterion_simulation_path(
        customer_id: str,
        ad_group_id: str,
        criterion_id: str,
        type: str,
        modification_method: str,
        start_date: str,
        end_date: str,
    ) -> str:
        """Return a fully-qualified ad_group_criterion_simulation string."""
        return "customers/{customer_id}/adGroupCriterionSimulations/{ad_group_id}~{criterion_id}~{type}~{modification_method}~{start_date}~{end_date}".format(
            customer_id=customer_id,
            ad_group_id=ad_group_id,
            criterion_id=criterion_id,
            type=type,
            modification_method=modification_method,
            start_date=start_date,
            end_date=end_date,
        )

    @staticmethod
    def parse_ad_group_criterion_simulation_path(path: str) -> Dict[str, str]:
        """Parse a ad_group_criterion_simulation path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/adGroupCriterionSimulations/(?P<ad_group_id>.+?)~(?P<criterion_id>.+?)~(?P<type>.+?)~(?P<modification_method>.+?)~(?P<start_date>.+?)~(?P<end_date>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_extension_setting_path(
        customer_id: str, ad_group_id: str, extension_type: str,
    ) -> str:
        """Return a fully-qualified ad_group_extension_setting string."""
        return "customers/{customer_id}/adGroupExtensionSettings/{ad_group_id}~{extension_type}".format(
            customer_id=customer_id,
            ad_group_id=ad_group_id,
            extension_type=extension_type,
        )

    @staticmethod
    def parse_ad_group_extension_setting_path(path: str) -> Dict[str, str]:
        """Parse a ad_group_extension_setting path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/adGroupExtensionSettings/(?P<ad_group_id>.+?)~(?P<extension_type>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_feed_path(
        customer_id: str, ad_group_id: str, feed_id: str,
    ) -> str:
        """Return a fully-qualified ad_group_feed string."""
        return "customers/{customer_id}/adGroupFeeds/{ad_group_id}~{feed_id}".format(
            customer_id=customer_id, ad_group_id=ad_group_id, feed_id=feed_id,
        )

    @staticmethod
    def parse_ad_group_feed_path(path: str) -> Dict[str, str]:
        """Parse a ad_group_feed path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/adGroupFeeds/(?P<ad_group_id>.+?)~(?P<feed_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_label_path(
        customer_id: str, ad_group_id: str, label_id: str,
    ) -> str:
        """Return a fully-qualified ad_group_label string."""
        return "customers/{customer_id}/adGroupLabels/{ad_group_id}~{label_id}".format(
            customer_id=customer_id, ad_group_id=ad_group_id, label_id=label_id,
        )

    @staticmethod
    def parse_ad_group_label_path(path: str) -> Dict[str, str]:
        """Parse a ad_group_label path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/adGroupLabels/(?P<ad_group_id>.+?)~(?P<label_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_simulation_path(
        customer_id: str,
        ad_group_id: str,
        type: str,
        modification_method: str,
        start_date: str,
        end_date: str,
    ) -> str:
        """Return a fully-qualified ad_group_simulation string."""
        return "customers/{customer_id}/adGroupSimulations/{ad_group_id}~{type}~{modification_method}~{start_date}~{end_date}".format(
            customer_id=customer_id,
            ad_group_id=ad_group_id,
            type=type,
            modification_method=modification_method,
            start_date=start_date,
            end_date=end_date,
        )

    @staticmethod
    def parse_ad_group_simulation_path(path: str) -> Dict[str, str]:
        """Parse a ad_group_simulation path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/adGroupSimulations/(?P<ad_group_id>.+?)~(?P<type>.+?)~(?P<modification_method>.+?)~(?P<start_date>.+?)~(?P<end_date>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def ad_parameter_path(
        customer_id: str,
        ad_group_id: str,
        criterion_id: str,
        parameter_index: str,
    ) -> str:
        """Return a fully-qualified ad_parameter string."""
        return "customers/{customer_id}/adParameters/{ad_group_id}~{criterion_id}~{parameter_index}".format(
            customer_id=customer_id,
            ad_group_id=ad_group_id,
            criterion_id=criterion_id,
            parameter_index=parameter_index,
        )

    @staticmethod
    def parse_ad_parameter_path(path: str) -> Dict[str, str]:
        """Parse a ad_parameter path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/adParameters/(?P<ad_group_id>.+?)~(?P<criterion_id>.+?)~(?P<parameter_index>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def ad_schedule_view_path(
        customer_id: str, campaign_id: str, criterion_id: str,
    ) -> str:
        """Return a fully-qualified ad_schedule_view string."""
        return "customers/{customer_id}/adScheduleViews/{campaign_id}~{criterion_id}".format(
            customer_id=customer_id,
            campaign_id=campaign_id,
            criterion_id=criterion_id,
        )

    @staticmethod
    def parse_ad_schedule_view_path(path: str) -> Dict[str, str]:
        """Parse a ad_schedule_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/adScheduleViews/(?P<campaign_id>.+?)~(?P<criterion_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def age_range_view_path(
        customer_id: str, ad_group_id: str, criterion_id: str,
    ) -> str:
        """Return a fully-qualified age_range_view string."""
        return "customers/{customer_id}/ageRangeViews/{ad_group_id}~{criterion_id}".format(
            customer_id=customer_id,
            ad_group_id=ad_group_id,
            criterion_id=criterion_id,
        )

    @staticmethod
    def parse_age_range_view_path(path: str) -> Dict[str, str]:
        """Parse a age_range_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/ageRangeViews/(?P<ad_group_id>.+?)~(?P<criterion_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def asset_path(customer_id: str, asset_id: str,) -> str:
        """Return a fully-qualified asset string."""
        return "customers/{customer_id}/assets/{asset_id}".format(
            customer_id=customer_id, asset_id=asset_id,
        )

    @staticmethod
    def parse_asset_path(path: str) -> Dict[str, str]:
        """Parse a asset path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/assets/(?P<asset_id>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def batch_job_path(customer_id: str, batch_job_id: str,) -> str:
        """Return a fully-qualified batch_job string."""
        return "customers/{customer_id}/batchJobs/{batch_job_id}".format(
            customer_id=customer_id, batch_job_id=batch_job_id,
        )

    @staticmethod
    def parse_batch_job_path(path: str) -> Dict[str, str]:
        """Parse a batch_job path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/batchJobs/(?P<batch_job_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def bidding_strategy_path(
        customer_id: str, bidding_strategy_id: str,
    ) -> str:
        """Return a fully-qualified bidding_strategy string."""
        return "customers/{customer_id}/biddingStrategies/{bidding_strategy_id}".format(
            customer_id=customer_id, bidding_strategy_id=bidding_strategy_id,
        )

    @staticmethod
    def parse_bidding_strategy_path(path: str) -> Dict[str, str]:
        """Parse a bidding_strategy path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/biddingStrategies/(?P<bidding_strategy_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def billing_setup_path(customer_id: str, billing_setup_id: str,) -> str:
        """Return a fully-qualified billing_setup string."""
        return "customers/{customer_id}/billingSetups/{billing_setup_id}".format(
            customer_id=customer_id, billing_setup_id=billing_setup_id,
        )

    @staticmethod
    def parse_billing_setup_path(path: str) -> Dict[str, str]:
        """Parse a billing_setup path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/billingSetups/(?P<billing_setup_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def call_view_path(customer_id: str, call_detail_id: str,) -> str:
        """Return a fully-qualified call_view string."""
        return "customers/{customer_id}/callViews/{call_detail_id}".format(
            customer_id=customer_id, call_detail_id=call_detail_id,
        )

    @staticmethod
    def parse_call_view_path(path: str) -> Dict[str, str]:
        """Parse a call_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/callViews/(?P<call_detail_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_path(customer_id: str, campaign_id: str,) -> str:
        """Return a fully-qualified campaign string."""
        return "customers/{customer_id}/campaigns/{campaign_id}".format(
            customer_id=customer_id, campaign_id=campaign_id,
        )

    @staticmethod
    def parse_campaign_path(path: str) -> Dict[str, str]:
        """Parse a campaign path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/campaigns/(?P<campaign_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_asset_path(
        customer_id: str, campaign_id: str, asset_id: str, field_type: str,
    ) -> str:
        """Return a fully-qualified campaign_asset string."""
        return "customers/{customer_id}/campaignAssets/{campaign_id}~{asset_id}~{field_type}".format(
            customer_id=customer_id,
            campaign_id=campaign_id,
            asset_id=asset_id,
            field_type=field_type,
        )

    @staticmethod
    def parse_campaign_asset_path(path: str) -> Dict[str, str]:
        """Parse a campaign_asset path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/campaignAssets/(?P<campaign_id>.+?)~(?P<asset_id>.+?)~(?P<field_type>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_audience_view_path(
        customer_id: str, campaign_id: str, criterion_id: str,
    ) -> str:
        """Return a fully-qualified campaign_audience_view string."""
        return "customers/{customer_id}/campaignAudienceViews/{campaign_id}~{criterion_id}".format(
            customer_id=customer_id,
            campaign_id=campaign_id,
            criterion_id=criterion_id,
        )

    @staticmethod
    def parse_campaign_audience_view_path(path: str) -> Dict[str, str]:
        """Parse a campaign_audience_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/campaignAudienceViews/(?P<campaign_id>.+?)~(?P<criterion_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_bid_modifier_path(
        customer_id: str, campaign_id: str, criterion_id: str,
    ) -> str:
        """Return a fully-qualified campaign_bid_modifier string."""
        return "customers/{customer_id}/campaignBidModifiers/{campaign_id}~{criterion_id}".format(
            customer_id=customer_id,
            campaign_id=campaign_id,
            criterion_id=criterion_id,
        )

    @staticmethod
    def parse_campaign_bid_modifier_path(path: str) -> Dict[str, str]:
        """Parse a campaign_bid_modifier path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/campaignBidModifiers/(?P<campaign_id>.+?)~(?P<criterion_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_budget_path(customer_id: str, campaign_budget_id: str,) -> str:
        """Return a fully-qualified campaign_budget string."""
        return "customers/{customer_id}/campaignBudgets/{campaign_budget_id}".format(
            customer_id=customer_id, campaign_budget_id=campaign_budget_id,
        )

    @staticmethod
    def parse_campaign_budget_path(path: str) -> Dict[str, str]:
        """Parse a campaign_budget path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/campaignBudgets/(?P<campaign_budget_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_criterion_path(
        customer_id: str, campaign_id: str, criterion_id: str,
    ) -> str:
        """Return a fully-qualified campaign_criterion string."""
        return "customers/{customer_id}/campaignCriteria/{campaign_id}~{criterion_id}".format(
            customer_id=customer_id,
            campaign_id=campaign_id,
            criterion_id=criterion_id,
        )

    @staticmethod
    def parse_campaign_criterion_path(path: str) -> Dict[str, str]:
        """Parse a campaign_criterion path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/campaignCriteria/(?P<campaign_id>.+?)~(?P<criterion_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_criterion_simulation_path(
        customer_id: str,
        campaign_id: str,
        criterion_id: str,
        type: str,
        modification_method: str,
        start_date: str,
        end_date: str,
    ) -> str:
        """Return a fully-qualified campaign_criterion_simulation string."""
        return "customers/{customer_id}/campaignCriterionSimulations/{campaign_id}~{criterion_id}~{type}~{modification_method}~{start_date}~{end_date}".format(
            customer_id=customer_id,
            campaign_id=campaign_id,
            criterion_id=criterion_id,
            type=type,
            modification_method=modification_method,
            start_date=start_date,
            end_date=end_date,
        )

    @staticmethod
    def parse_campaign_criterion_simulation_path(path: str) -> Dict[str, str]:
        """Parse a campaign_criterion_simulation path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/campaignCriterionSimulations/(?P<campaign_id>.+?)~(?P<criterion_id>.+?)~(?P<type>.+?)~(?P<modification_method>.+?)~(?P<start_date>.+?)~(?P<end_date>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_draft_path(
        customer_id: str, base_campaign_id: str, draft_id: str,
    ) -> str:
        """Return a fully-qualified campaign_draft string."""
        return "customers/{customer_id}/campaignDrafts/{base_campaign_id}~{draft_id}".format(
            customer_id=customer_id,
            base_campaign_id=base_campaign_id,
            draft_id=draft_id,
        )

    @staticmethod
    def parse_campaign_draft_path(path: str) -> Dict[str, str]:
        """Parse a campaign_draft path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/campaignDrafts/(?P<base_campaign_id>.+?)~(?P<draft_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_experiment_path(
        customer_id: str, campaign_experiment_id: str,
    ) -> str:
        """Return a fully-qualified campaign_experiment string."""
        return "customers/{customer_id}/campaignExperiments/{campaign_experiment_id}".format(
            customer_id=customer_id,
            campaign_experiment_id=campaign_experiment_id,
        )

    @staticmethod
    def parse_campaign_experiment_path(path: str) -> Dict[str, str]:
        """Parse a campaign_experiment path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/campaignExperiments/(?P<campaign_experiment_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_extension_setting_path(
        customer_id: str, campaign_id: str, extension_type: str,
    ) -> str:
        """Return a fully-qualified campaign_extension_setting string."""
        return "customers/{customer_id}/campaignExtensionSettings/{campaign_id}~{extension_type}".format(
            customer_id=customer_id,
            campaign_id=campaign_id,
            extension_type=extension_type,
        )

    @staticmethod
    def parse_campaign_extension_setting_path(path: str) -> Dict[str, str]:
        """Parse a campaign_extension_setting path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/campaignExtensionSettings/(?P<campaign_id>.+?)~(?P<extension_type>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_feed_path(
        customer_id: str, campaign_id: str, feed_id: str,
    ) -> str:
        """Return a fully-qualified campaign_feed string."""
        return "customers/{customer_id}/campaignFeeds/{campaign_id}~{feed_id}".format(
            customer_id=customer_id, campaign_id=campaign_id, feed_id=feed_id,
        )

    @staticmethod
    def parse_campaign_feed_path(path: str) -> Dict[str, str]:
        """Parse a campaign_feed path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/campaignFeeds/(?P<campaign_id>.+?)~(?P<feed_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_label_path(
        customer_id: str, campaign_id: str, label_id: str,
    ) -> str:
        """Return a fully-qualified campaign_label string."""
        return "customers/{customer_id}/campaignLabels/{campaign_id}~{label_id}".format(
            customer_id=customer_id, campaign_id=campaign_id, label_id=label_id,
        )

    @staticmethod
    def parse_campaign_label_path(path: str) -> Dict[str, str]:
        """Parse a campaign_label path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/campaignLabels/(?P<campaign_id>.+?)~(?P<label_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_shared_set_path(
        customer_id: str, campaign_id: str, shared_set_id: str,
    ) -> str:
        """Return a fully-qualified campaign_shared_set string."""
        return "customers/{customer_id}/campaignSharedSets/{campaign_id}~{shared_set_id}".format(
            customer_id=customer_id,
            campaign_id=campaign_id,
            shared_set_id=shared_set_id,
        )

    @staticmethod
    def parse_campaign_shared_set_path(path: str) -> Dict[str, str]:
        """Parse a campaign_shared_set path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/campaignSharedSets/(?P<campaign_id>.+?)~(?P<shared_set_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def carrier_constant_path(criterion_id: str,) -> str:
        """Return a fully-qualified carrier_constant string."""
        return "carrierConstants/{criterion_id}".format(
            criterion_id=criterion_id,
        )

    @staticmethod
    def parse_carrier_constant_path(path: str) -> Dict[str, str]:
        """Parse a carrier_constant path into its component segments."""
        m = re.match(r"^carrierConstants/(?P<criterion_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def change_event_path(
        customer_id: str,
        timestamp_micros: str,
        command_index: str,
        mutate_index: str,
    ) -> str:
        """Return a fully-qualified change_event string."""
        return "customers/{customer_id}/changeEvents/{timestamp_micros}~{command_index}~{mutate_index}".format(
            customer_id=customer_id,
            timestamp_micros=timestamp_micros,
            command_index=command_index,
            mutate_index=mutate_index,
        )

    @staticmethod
    def parse_change_event_path(path: str) -> Dict[str, str]:
        """Parse a change_event path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/changeEvents/(?P<timestamp_micros>.+?)~(?P<command_index>.+?)~(?P<mutate_index>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def change_status_path(customer_id: str, change_status_id: str,) -> str:
        """Return a fully-qualified change_status string."""
        return "customers/{customer_id}/changeStatus/{change_status_id}".format(
            customer_id=customer_id, change_status_id=change_status_id,
        )

    @staticmethod
    def parse_change_status_path(path: str) -> Dict[str, str]:
        """Parse a change_status path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/changeStatus/(?P<change_status_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def click_view_path(customer_id: str, date: str, gclid: str,) -> str:
        """Return a fully-qualified click_view string."""
        return "customers/{customer_id}/clickViews/{date}~{gclid}".format(
            customer_id=customer_id, date=date, gclid=gclid,
        )

    @staticmethod
    def parse_click_view_path(path: str) -> Dict[str, str]:
        """Parse a click_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/clickViews/(?P<date>.+?)~(?P<gclid>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def combined_audience_path(
        customer_id: str, combined_audience_id: str,
    ) -> str:
        """Return a fully-qualified combined_audience string."""
        return "customers/{customer_id}/combinedAudiences/{combined_audience_id}".format(
            customer_id=customer_id, combined_audience_id=combined_audience_id,
        )

    @staticmethod
    def parse_combined_audience_path(path: str) -> Dict[str, str]:
        """Parse a combined_audience path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/combinedAudiences/(?P<combined_audience_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def conversion_action_path(
        customer_id: str, conversion_action_id: str,
    ) -> str:
        """Return a fully-qualified conversion_action string."""
        return "customers/{customer_id}/conversionActions/{conversion_action_id}".format(
            customer_id=customer_id, conversion_action_id=conversion_action_id,
        )

    @staticmethod
    def parse_conversion_action_path(path: str) -> Dict[str, str]:
        """Parse a conversion_action path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/conversionActions/(?P<conversion_action_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def currency_constant_path(code: str,) -> str:
        """Return a fully-qualified currency_constant string."""
        return "currencyConstants/{code}".format(code=code,)

    @staticmethod
    def parse_currency_constant_path(path: str) -> Dict[str, str]:
        """Parse a currency_constant path into its component segments."""
        m = re.match(r"^currencyConstants/(?P<code>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def custom_audience_path(customer_id: str, custom_audience_id: str,) -> str:
        """Return a fully-qualified custom_audience string."""
        return "customers/{customer_id}/customAudiences/{custom_audience_id}".format(
            customer_id=customer_id, custom_audience_id=custom_audience_id,
        )

    @staticmethod
    def parse_custom_audience_path(path: str) -> Dict[str, str]:
        """Parse a custom_audience path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/customAudiences/(?P<custom_audience_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def customer_path(customer_id: str,) -> str:
        """Return a fully-qualified customer string."""
        return "customers/{customer_id}".format(customer_id=customer_id,)

    @staticmethod
    def parse_customer_path(path: str) -> Dict[str, str]:
        """Parse a customer path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def customer_client_path(customer_id: str, client_customer_id: str,) -> str:
        """Return a fully-qualified customer_client string."""
        return "customers/{customer_id}/customerClients/{client_customer_id}".format(
            customer_id=customer_id, client_customer_id=client_customer_id,
        )

    @staticmethod
    def parse_customer_client_path(path: str) -> Dict[str, str]:
        """Parse a customer_client path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/customerClients/(?P<client_customer_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def customer_client_link_path(
        customer_id: str, client_customer_id: str, manager_link_id: str,
    ) -> str:
        """Return a fully-qualified customer_client_link string."""
        return "customers/{customer_id}/customerClientLinks/{client_customer_id}~{manager_link_id}".format(
            customer_id=customer_id,
            client_customer_id=client_customer_id,
            manager_link_id=manager_link_id,
        )

    @staticmethod
    def parse_customer_client_link_path(path: str) -> Dict[str, str]:
        """Parse a customer_client_link path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/customerClientLinks/(?P<client_customer_id>.+?)~(?P<manager_link_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def customer_extension_setting_path(
        customer_id: str, extension_type: str,
    ) -> str:
        """Return a fully-qualified customer_extension_setting string."""
        return "customers/{customer_id}/customerExtensionSettings/{extension_type}".format(
            customer_id=customer_id, extension_type=extension_type,
        )

    @staticmethod
    def parse_customer_extension_setting_path(path: str) -> Dict[str, str]:
        """Parse a customer_extension_setting path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/customerExtensionSettings/(?P<extension_type>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def customer_feed_path(customer_id: str, feed_id: str,) -> str:
        """Return a fully-qualified customer_feed string."""
        return "customers/{customer_id}/customerFeeds/{feed_id}".format(
            customer_id=customer_id, feed_id=feed_id,
        )

    @staticmethod
    def parse_customer_feed_path(path: str) -> Dict[str, str]:
        """Parse a customer_feed path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/customerFeeds/(?P<feed_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def customer_label_path(customer_id: str, label_id: str,) -> str:
        """Return a fully-qualified customer_label string."""
        return "customers/{customer_id}/customerLabels/{label_id}".format(
            customer_id=customer_id, label_id=label_id,
        )

    @staticmethod
    def parse_customer_label_path(path: str) -> Dict[str, str]:
        """Parse a customer_label path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/customerLabels/(?P<label_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def customer_manager_link_path(
        customer_id: str, manager_customer_id: str, manager_link_id: str,
    ) -> str:
        """Return a fully-qualified customer_manager_link string."""
        return "customers/{customer_id}/customerManagerLinks/{manager_customer_id}~{manager_link_id}".format(
            customer_id=customer_id,
            manager_customer_id=manager_customer_id,
            manager_link_id=manager_link_id,
        )

    @staticmethod
    def parse_customer_manager_link_path(path: str) -> Dict[str, str]:
        """Parse a customer_manager_link path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/customerManagerLinks/(?P<manager_customer_id>.+?)~(?P<manager_link_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def customer_negative_criterion_path(
        customer_id: str, criterion_id: str,
    ) -> str:
        """Return a fully-qualified customer_negative_criterion string."""
        return "customers/{customer_id}/customerNegativeCriteria/{criterion_id}".format(
            customer_id=customer_id, criterion_id=criterion_id,
        )

    @staticmethod
    def parse_customer_negative_criterion_path(path: str) -> Dict[str, str]:
        """Parse a customer_negative_criterion path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/customerNegativeCriteria/(?P<criterion_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def customer_user_access_path(customer_id: str, user_id: str,) -> str:
        """Return a fully-qualified customer_user_access string."""
        return "customers/{customer_id}/customerUserAccesses/{user_id}".format(
            customer_id=customer_id, user_id=user_id,
        )

    @staticmethod
    def parse_customer_user_access_path(path: str) -> Dict[str, str]:
        """Parse a customer_user_access path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/customerUserAccesses/(?P<user_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def customer_user_access_invitation_path(
        customer_id: str, invitation_id: str,
    ) -> str:
        """Return a fully-qualified customer_user_access_invitation string."""
        return "customers/{customer_id}/customerUserAccessInvitations/{invitation_id}".format(
            customer_id=customer_id, invitation_id=invitation_id,
        )

    @staticmethod
    def parse_customer_user_access_invitation_path(path: str) -> Dict[str, str]:
        """Parse a customer_user_access_invitation path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/customerUserAccessInvitations/(?P<invitation_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def custom_interest_path(customer_id: str, custom_interest_id: str,) -> str:
        """Return a fully-qualified custom_interest string."""
        return "customers/{customer_id}/customInterests/{custom_interest_id}".format(
            customer_id=customer_id, custom_interest_id=custom_interest_id,
        )

    @staticmethod
    def parse_custom_interest_path(path: str) -> Dict[str, str]:
        """Parse a custom_interest path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/customInterests/(?P<custom_interest_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def detail_placement_view_path(
        customer_id: str, ad_group_id: str, base64_placement: str,
    ) -> str:
        """Return a fully-qualified detail_placement_view string."""
        return "customers/{customer_id}/detailPlacementViews/{ad_group_id}~{base64_placement}".format(
            customer_id=customer_id,
            ad_group_id=ad_group_id,
            base64_placement=base64_placement,
        )

    @staticmethod
    def parse_detail_placement_view_path(path: str) -> Dict[str, str]:
        """Parse a detail_placement_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/detailPlacementViews/(?P<ad_group_id>.+?)~(?P<base64_placement>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def display_keyword_view_path(
        customer_id: str, ad_group_id: str, criterion_id: str,
    ) -> str:
        """Return a fully-qualified display_keyword_view string."""
        return "customers/{customer_id}/displayKeywordViews/{ad_group_id}~{criterion_id}".format(
            customer_id=customer_id,
            ad_group_id=ad_group_id,
            criterion_id=criterion_id,
        )

    @staticmethod
    def parse_display_keyword_view_path(path: str) -> Dict[str, str]:
        """Parse a display_keyword_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/displayKeywordViews/(?P<ad_group_id>.+?)~(?P<criterion_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def distance_view_path(
        customer_id: str, placeholder_chain_id: str, distance_bucket: str,
    ) -> str:
        """Return a fully-qualified distance_view string."""
        return "customers/{customer_id}/distanceViews/{placeholder_chain_id}~{distance_bucket}".format(
            customer_id=customer_id,
            placeholder_chain_id=placeholder_chain_id,
            distance_bucket=distance_bucket,
        )

    @staticmethod
    def parse_distance_view_path(path: str) -> Dict[str, str]:
        """Parse a distance_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/distanceViews/(?P<placeholder_chain_id>.+?)~(?P<distance_bucket>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def domain_category_path(
        customer_id: str,
        campaign_id: str,
        base64_category: str,
        language_code: str,
    ) -> str:
        """Return a fully-qualified domain_category string."""
        return "customers/{customer_id}/domainCategories/{campaign_id}~{base64_category}~{language_code}".format(
            customer_id=customer_id,
            campaign_id=campaign_id,
            base64_category=base64_category,
            language_code=language_code,
        )

    @staticmethod
    def parse_domain_category_path(path: str) -> Dict[str, str]:
        """Parse a domain_category path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/domainCategories/(?P<campaign_id>.+?)~(?P<base64_category>.+?)~(?P<language_code>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def dynamic_search_ads_search_term_view_path(
        customer_id: str,
        ad_group_id: str,
        search_term_fingerprint: str,
        headline_fingerprint: str,
        landing_page_fingerprint: str,
        page_url_fingerprint: str,
    ) -> str:
        """Return a fully-qualified dynamic_search_ads_search_term_view string."""
        return "customers/{customer_id}/dynamicSearchAdsSearchTermViews/{ad_group_id}~{search_term_fingerprint}~{headline_fingerprint}~{landing_page_fingerprint}~{page_url_fingerprint}".format(
            customer_id=customer_id,
            ad_group_id=ad_group_id,
            search_term_fingerprint=search_term_fingerprint,
            headline_fingerprint=headline_fingerprint,
            landing_page_fingerprint=landing_page_fingerprint,
            page_url_fingerprint=page_url_fingerprint,
        )

    @staticmethod
    def parse_dynamic_search_ads_search_term_view_path(
        path: str,
    ) -> Dict[str, str]:
        """Parse a dynamic_search_ads_search_term_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/dynamicSearchAdsSearchTermViews/(?P<ad_group_id>.+?)~(?P<search_term_fingerprint>.+?)~(?P<headline_fingerprint>.+?)~(?P<landing_page_fingerprint>.+?)~(?P<page_url_fingerprint>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def expanded_landing_page_view_path(
        customer_id: str, expanded_final_url_fingerprint: str,
    ) -> str:
        """Return a fully-qualified expanded_landing_page_view string."""
        return "customers/{customer_id}/expandedLandingPageViews/{expanded_final_url_fingerprint}".format(
            customer_id=customer_id,
            expanded_final_url_fingerprint=expanded_final_url_fingerprint,
        )

    @staticmethod
    def parse_expanded_landing_page_view_path(path: str) -> Dict[str, str]:
        """Parse a expanded_landing_page_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/expandedLandingPageViews/(?P<expanded_final_url_fingerprint>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def extension_feed_item_path(customer_id: str, feed_item_id: str,) -> str:
        """Return a fully-qualified extension_feed_item string."""
        return "customers/{customer_id}/extensionFeedItems/{feed_item_id}".format(
            customer_id=customer_id, feed_item_id=feed_item_id,
        )

    @staticmethod
    def parse_extension_feed_item_path(path: str) -> Dict[str, str]:
        """Parse a extension_feed_item path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/extensionFeedItems/(?P<feed_item_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def feed_path(customer_id: str, feed_id: str,) -> str:
        """Return a fully-qualified feed string."""
        return "customers/{customer_id}/feeds/{feed_id}".format(
            customer_id=customer_id, feed_id=feed_id,
        )

    @staticmethod
    def parse_feed_path(path: str) -> Dict[str, str]:
        """Parse a feed path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/feeds/(?P<feed_id>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def feed_item_path(
        customer_id: str, feed_id: str, feed_item_id: str,
    ) -> str:
        """Return a fully-qualified feed_item string."""
        return "customers/{customer_id}/feedItems/{feed_id}~{feed_item_id}".format(
            customer_id=customer_id, feed_id=feed_id, feed_item_id=feed_item_id,
        )

    @staticmethod
    def parse_feed_item_path(path: str) -> Dict[str, str]:
        """Parse a feed_item path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/feedItems/(?P<feed_id>.+?)~(?P<feed_item_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def feed_item_set_path(
        customer_id: str, feed_id: str, feed_item_set_id: str,
    ) -> str:
        """Return a fully-qualified feed_item_set string."""
        return "customers/{customer_id}/feedItemSets/{feed_id}~{feed_item_set_id}".format(
            customer_id=customer_id,
            feed_id=feed_id,
            feed_item_set_id=feed_item_set_id,
        )

    @staticmethod
    def parse_feed_item_set_path(path: str) -> Dict[str, str]:
        """Parse a feed_item_set path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/feedItemSets/(?P<feed_id>.+?)~(?P<feed_item_set_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def feed_item_set_link_path(
        customer_id: str,
        feed_id: str,
        feed_item_set_id: str,
        feed_item_id: str,
    ) -> str:
        """Return a fully-qualified feed_item_set_link string."""
        return "customers/{customer_id}/feedItemSetLinks/{feed_id}~{feed_item_set_id}~{feed_item_id}".format(
            customer_id=customer_id,
            feed_id=feed_id,
            feed_item_set_id=feed_item_set_id,
            feed_item_id=feed_item_id,
        )

    @staticmethod
    def parse_feed_item_set_link_path(path: str) -> Dict[str, str]:
        """Parse a feed_item_set_link path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/feedItemSetLinks/(?P<feed_id>.+?)~(?P<feed_item_set_id>.+?)~(?P<feed_item_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def feed_item_target_path(
        customer_id: str,
        feed_id: str,
        feed_item_id: str,
        feed_item_target_type: str,
        feed_item_target_id: str,
    ) -> str:
        """Return a fully-qualified feed_item_target string."""
        return "customers/{customer_id}/feedItemTargets/{feed_id}~{feed_item_id}~{feed_item_target_type}~{feed_item_target_id}".format(
            customer_id=customer_id,
            feed_id=feed_id,
            feed_item_id=feed_item_id,
            feed_item_target_type=feed_item_target_type,
            feed_item_target_id=feed_item_target_id,
        )

    @staticmethod
    def parse_feed_item_target_path(path: str) -> Dict[str, str]:
        """Parse a feed_item_target path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/feedItemTargets/(?P<feed_id>.+?)~(?P<feed_item_id>.+?)~(?P<feed_item_target_type>.+?)~(?P<feed_item_target_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def feed_mapping_path(
        customer_id: str, feed_id: str, feed_mapping_id: str,
    ) -> str:
        """Return a fully-qualified feed_mapping string."""
        return "customers/{customer_id}/feedMappings/{feed_id}~{feed_mapping_id}".format(
            customer_id=customer_id,
            feed_id=feed_id,
            feed_mapping_id=feed_mapping_id,
        )

    @staticmethod
    def parse_feed_mapping_path(path: str) -> Dict[str, str]:
        """Parse a feed_mapping path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/feedMappings/(?P<feed_id>.+?)~(?P<feed_mapping_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def feed_placeholder_view_path(
        customer_id: str, placeholder_type: str,
    ) -> str:
        """Return a fully-qualified feed_placeholder_view string."""
        return "customers/{customer_id}/feedPlaceholderViews/{placeholder_type}".format(
            customer_id=customer_id, placeholder_type=placeholder_type,
        )

    @staticmethod
    def parse_feed_placeholder_view_path(path: str) -> Dict[str, str]:
        """Parse a feed_placeholder_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/feedPlaceholderViews/(?P<placeholder_type>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def gender_view_path(
        customer_id: str, ad_group_id: str, criterion_id: str,
    ) -> str:
        """Return a fully-qualified gender_view string."""
        return "customers/{customer_id}/genderViews/{ad_group_id}~{criterion_id}".format(
            customer_id=customer_id,
            ad_group_id=ad_group_id,
            criterion_id=criterion_id,
        )

    @staticmethod
    def parse_gender_view_path(path: str) -> Dict[str, str]:
        """Parse a gender_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/genderViews/(?P<ad_group_id>.+?)~(?P<criterion_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def geographic_view_path(
        customer_id: str, country_criterion_id: str, location_type: str,
    ) -> str:
        """Return a fully-qualified geographic_view string."""
        return "customers/{customer_id}/geographicViews/{country_criterion_id}~{location_type}".format(
            customer_id=customer_id,
            country_criterion_id=country_criterion_id,
            location_type=location_type,
        )

    @staticmethod
    def parse_geographic_view_path(path: str) -> Dict[str, str]:
        """Parse a geographic_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/geographicViews/(?P<country_criterion_id>.+?)~(?P<location_type>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def geo_target_constant_path(criterion_id: str,) -> str:
        """Return a fully-qualified geo_target_constant string."""
        return "geoTargetConstants/{criterion_id}".format(
            criterion_id=criterion_id,
        )

    @staticmethod
    def parse_geo_target_constant_path(path: str) -> Dict[str, str]:
        """Parse a geo_target_constant path into its component segments."""
        m = re.match(r"^geoTargetConstants/(?P<criterion_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def group_placement_view_path(
        customer_id: str, ad_group_id: str, base64_placement: str,
    ) -> str:
        """Return a fully-qualified group_placement_view string."""
        return "customers/{customer_id}/groupPlacementViews/{ad_group_id}~{base64_placement}".format(
            customer_id=customer_id,
            ad_group_id=ad_group_id,
            base64_placement=base64_placement,
        )

    @staticmethod
    def parse_group_placement_view_path(path: str) -> Dict[str, str]:
        """Parse a group_placement_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/groupPlacementViews/(?P<ad_group_id>.+?)~(?P<base64_placement>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def hotel_group_view_path(
        customer_id: str, ad_group_id: str, criterion_id: str,
    ) -> str:
        """Return a fully-qualified hotel_group_view string."""
        return "customers/{customer_id}/hotelGroupViews/{ad_group_id}~{criterion_id}".format(
            customer_id=customer_id,
            ad_group_id=ad_group_id,
            criterion_id=criterion_id,
        )

    @staticmethod
    def parse_hotel_group_view_path(path: str) -> Dict[str, str]:
        """Parse a hotel_group_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/hotelGroupViews/(?P<ad_group_id>.+?)~(?P<criterion_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def hotel_performance_view_path(customer_id: str,) -> str:
        """Return a fully-qualified hotel_performance_view string."""
        return "customers/{customer_id}/hotelPerformanceView".format(
            customer_id=customer_id,
        )

    @staticmethod
    def parse_hotel_performance_view_path(path: str) -> Dict[str, str]:
        """Parse a hotel_performance_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/hotelPerformanceView$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def income_range_view_path(
        customer_id: str, ad_group_id: str, criterion_id: str,
    ) -> str:
        """Return a fully-qualified income_range_view string."""
        return "customers/{customer_id}/incomeRangeViews/{ad_group_id}~{criterion_id}".format(
            customer_id=customer_id,
            ad_group_id=ad_group_id,
            criterion_id=criterion_id,
        )

    @staticmethod
    def parse_income_range_view_path(path: str) -> Dict[str, str]:
        """Parse a income_range_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/incomeRangeViews/(?P<ad_group_id>.+?)~(?P<criterion_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def keyword_plan_path(customer_id: str, keyword_plan_id: str,) -> str:
        """Return a fully-qualified keyword_plan string."""
        return "customers/{customer_id}/keywordPlans/{keyword_plan_id}".format(
            customer_id=customer_id, keyword_plan_id=keyword_plan_id,
        )

    @staticmethod
    def parse_keyword_plan_path(path: str) -> Dict[str, str]:
        """Parse a keyword_plan path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/keywordPlans/(?P<keyword_plan_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def keyword_plan_ad_group_path(
        customer_id: str, keyword_plan_ad_group_id: str,
    ) -> str:
        """Return a fully-qualified keyword_plan_ad_group string."""
        return "customers/{customer_id}/keywordPlanAdGroups/{keyword_plan_ad_group_id}".format(
            customer_id=customer_id,
            keyword_plan_ad_group_id=keyword_plan_ad_group_id,
        )

    @staticmethod
    def parse_keyword_plan_ad_group_path(path: str) -> Dict[str, str]:
        """Parse a keyword_plan_ad_group path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/keywordPlanAdGroups/(?P<keyword_plan_ad_group_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def keyword_plan_ad_group_keyword_path(
        customer_id: str, keyword_plan_ad_group_keyword_id: str,
    ) -> str:
        """Return a fully-qualified keyword_plan_ad_group_keyword string."""
        return "customers/{customer_id}/keywordPlanAdGroupKeywords/{keyword_plan_ad_group_keyword_id}".format(
            customer_id=customer_id,
            keyword_plan_ad_group_keyword_id=keyword_plan_ad_group_keyword_id,
        )

    @staticmethod
    def parse_keyword_plan_ad_group_keyword_path(path: str) -> Dict[str, str]:
        """Parse a keyword_plan_ad_group_keyword path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/keywordPlanAdGroupKeywords/(?P<keyword_plan_ad_group_keyword_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def keyword_plan_campaign_path(
        customer_id: str, keyword_plan_campaign_id: str,
    ) -> str:
        """Return a fully-qualified keyword_plan_campaign string."""
        return "customers/{customer_id}/keywordPlanCampaigns/{keyword_plan_campaign_id}".format(
            customer_id=customer_id,
            keyword_plan_campaign_id=keyword_plan_campaign_id,
        )

    @staticmethod
    def parse_keyword_plan_campaign_path(path: str) -> Dict[str, str]:
        """Parse a keyword_plan_campaign path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/keywordPlanCampaigns/(?P<keyword_plan_campaign_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def keyword_plan_campaign_keyword_path(
        customer_id: str, keyword_plan_campaign_keyword_id: str,
    ) -> str:
        """Return a fully-qualified keyword_plan_campaign_keyword string."""
        return "customers/{customer_id}/keywordPlanCampaignKeywords/{keyword_plan_campaign_keyword_id}".format(
            customer_id=customer_id,
            keyword_plan_campaign_keyword_id=keyword_plan_campaign_keyword_id,
        )

    @staticmethod
    def parse_keyword_plan_campaign_keyword_path(path: str) -> Dict[str, str]:
        """Parse a keyword_plan_campaign_keyword path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/keywordPlanCampaignKeywords/(?P<keyword_plan_campaign_keyword_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def keyword_view_path(
        customer_id: str, ad_group_id: str, criterion_id: str,
    ) -> str:
        """Return a fully-qualified keyword_view string."""
        return "customers/{customer_id}/keywordViews/{ad_group_id}~{criterion_id}".format(
            customer_id=customer_id,
            ad_group_id=ad_group_id,
            criterion_id=criterion_id,
        )

    @staticmethod
    def parse_keyword_view_path(path: str) -> Dict[str, str]:
        """Parse a keyword_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/keywordViews/(?P<ad_group_id>.+?)~(?P<criterion_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def label_path(customer_id: str, label_id: str,) -> str:
        """Return a fully-qualified label string."""
        return "customers/{customer_id}/labels/{label_id}".format(
            customer_id=customer_id, label_id=label_id,
        )

    @staticmethod
    def parse_label_path(path: str) -> Dict[str, str]:
        """Parse a label path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/labels/(?P<label_id>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def landing_page_view_path(
        customer_id: str, unexpanded_final_url_fingerprint: str,
    ) -> str:
        """Return a fully-qualified landing_page_view string."""
        return "customers/{customer_id}/landingPageViews/{unexpanded_final_url_fingerprint}".format(
            customer_id=customer_id,
            unexpanded_final_url_fingerprint=unexpanded_final_url_fingerprint,
        )

    @staticmethod
    def parse_landing_page_view_path(path: str) -> Dict[str, str]:
        """Parse a landing_page_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/landingPageViews/(?P<unexpanded_final_url_fingerprint>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def language_constant_path(criterion_id: str,) -> str:
        """Return a fully-qualified language_constant string."""
        return "languageConstants/{criterion_id}".format(
            criterion_id=criterion_id,
        )

    @staticmethod
    def parse_language_constant_path(path: str) -> Dict[str, str]:
        """Parse a language_constant path into its component segments."""
        m = re.match(r"^languageConstants/(?P<criterion_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def location_view_path(
        customer_id: str, campaign_id: str, criterion_id: str,
    ) -> str:
        """Return a fully-qualified location_view string."""
        return "customers/{customer_id}/locationViews/{campaign_id}~{criterion_id}".format(
            customer_id=customer_id,
            campaign_id=campaign_id,
            criterion_id=criterion_id,
        )

    @staticmethod
    def parse_location_view_path(path: str) -> Dict[str, str]:
        """Parse a location_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/locationViews/(?P<campaign_id>.+?)~(?P<criterion_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def managed_placement_view_path(
        customer_id: str, ad_group_id: str, criterion_id: str,
    ) -> str:
        """Return a fully-qualified managed_placement_view string."""
        return "customers/{customer_id}/managedPlacementViews/{ad_group_id}~{criterion_id}".format(
            customer_id=customer_id,
            ad_group_id=ad_group_id,
            criterion_id=criterion_id,
        )

    @staticmethod
    def parse_managed_placement_view_path(path: str) -> Dict[str, str]:
        """Parse a managed_placement_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/managedPlacementViews/(?P<ad_group_id>.+?)~(?P<criterion_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def media_file_path(customer_id: str, media_file_id: str,) -> str:
        """Return a fully-qualified media_file string."""
        return "customers/{customer_id}/mediaFiles/{media_file_id}".format(
            customer_id=customer_id, media_file_id=media_file_id,
        )

    @staticmethod
    def parse_media_file_path(path: str) -> Dict[str, str]:
        """Parse a media_file path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/mediaFiles/(?P<media_file_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def mobile_app_category_constant_path(mobile_app_category_id: str,) -> str:
        """Return a fully-qualified mobile_app_category_constant string."""
        return "mobileAppCategoryConstants/{mobile_app_category_id}".format(
            mobile_app_category_id=mobile_app_category_id,
        )

    @staticmethod
    def parse_mobile_app_category_constant_path(path: str) -> Dict[str, str]:
        """Parse a mobile_app_category_constant path into its component segments."""
        m = re.match(
            r"^mobileAppCategoryConstants/(?P<mobile_app_category_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def mobile_device_constant_path(criterion_id: str,) -> str:
        """Return a fully-qualified mobile_device_constant string."""
        return "mobileDeviceConstants/{criterion_id}".format(
            criterion_id=criterion_id,
        )

    @staticmethod
    def parse_mobile_device_constant_path(path: str) -> Dict[str, str]:
        """Parse a mobile_device_constant path into its component segments."""
        m = re.match(r"^mobileDeviceConstants/(?P<criterion_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def offline_user_data_job_path(
        customer_id: str, offline_user_data_update_id: str,
    ) -> str:
        """Return a fully-qualified offline_user_data_job string."""
        return "customers/{customer_id}/offlineUserDataJobs/{offline_user_data_update_id}".format(
            customer_id=customer_id,
            offline_user_data_update_id=offline_user_data_update_id,
        )

    @staticmethod
    def parse_offline_user_data_job_path(path: str) -> Dict[str, str]:
        """Parse a offline_user_data_job path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/offlineUserDataJobs/(?P<offline_user_data_update_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def operating_system_version_constant_path(criterion_id: str,) -> str:
        """Return a fully-qualified operating_system_version_constant string."""
        return "operatingSystemVersionConstants/{criterion_id}".format(
            criterion_id=criterion_id,
        )

    @staticmethod
    def parse_operating_system_version_constant_path(
        path: str,
    ) -> Dict[str, str]:
        """Parse a operating_system_version_constant path into its component segments."""
        m = re.match(
            r"^operatingSystemVersionConstants/(?P<criterion_id>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def paid_organic_search_term_view_path(
        customer_id: str,
        campaign_id: str,
        ad_group_id: str,
        base64_search_term: str,
    ) -> str:
        """Return a fully-qualified paid_organic_search_term_view string."""
        return "customers/{customer_id}/paidOrganicSearchTermViews/{campaign_id}~{ad_group_id}~{base64_search_term}".format(
            customer_id=customer_id,
            campaign_id=campaign_id,
            ad_group_id=ad_group_id,
            base64_search_term=base64_search_term,
        )

    @staticmethod
    def parse_paid_organic_search_term_view_path(path: str) -> Dict[str, str]:
        """Parse a paid_organic_search_term_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/paidOrganicSearchTermViews/(?P<campaign_id>.+?)~(?P<ad_group_id>.+?)~(?P<base64_search_term>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def parental_status_view_path(
        customer_id: str, ad_group_id: str, criterion_id: str,
    ) -> str:
        """Return a fully-qualified parental_status_view string."""
        return "customers/{customer_id}/parentalStatusViews/{ad_group_id}~{criterion_id}".format(
            customer_id=customer_id,
            ad_group_id=ad_group_id,
            criterion_id=criterion_id,
        )

    @staticmethod
    def parse_parental_status_view_path(path: str) -> Dict[str, str]:
        """Parse a parental_status_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/parentalStatusViews/(?P<ad_group_id>.+?)~(?P<criterion_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def payments_account_path(
        customer_id: str, payments_account_id: str,
    ) -> str:
        """Return a fully-qualified payments_account string."""
        return "customers/{customer_id}/paymentsAccounts/{payments_account_id}".format(
            customer_id=customer_id, payments_account_id=payments_account_id,
        )

    @staticmethod
    def parse_payments_account_path(path: str) -> Dict[str, str]:
        """Parse a payments_account path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/paymentsAccounts/(?P<payments_account_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def product_bidding_category_constant_path(
        country_code: str, level: str, id: str,
    ) -> str:
        """Return a fully-qualified product_bidding_category_constant string."""
        return "productBiddingCategoryConstants/{country_code}~{level}~{id}".format(
            country_code=country_code, level=level, id=id,
        )

    @staticmethod
    def parse_product_bidding_category_constant_path(
        path: str,
    ) -> Dict[str, str]:
        """Parse a product_bidding_category_constant path into its component segments."""
        m = re.match(
            r"^productBiddingCategoryConstants/(?P<country_code>.+?)~(?P<level>.+?)~(?P<id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def product_group_view_path(
        customer_id: str, adgroup_id: str, criterion_id: str,
    ) -> str:
        """Return a fully-qualified product_group_view string."""
        return "customers/{customer_id}/productGroupViews/{adgroup_id}~{criterion_id}".format(
            customer_id=customer_id,
            adgroup_id=adgroup_id,
            criterion_id=criterion_id,
        )

    @staticmethod
    def parse_product_group_view_path(path: str) -> Dict[str, str]:
        """Parse a product_group_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/productGroupViews/(?P<adgroup_id>.+?)~(?P<criterion_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def recommendation_path(customer_id: str, recommendation_id: str,) -> str:
        """Return a fully-qualified recommendation string."""
        return "customers/{customer_id}/recommendations/{recommendation_id}".format(
            customer_id=customer_id, recommendation_id=recommendation_id,
        )

    @staticmethod
    def parse_recommendation_path(path: str) -> Dict[str, str]:
        """Parse a recommendation path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/recommendations/(?P<recommendation_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def remarketing_action_path(
        customer_id: str, remarketing_action_id: str,
    ) -> str:
        """Return a fully-qualified remarketing_action string."""
        return "customers/{customer_id}/remarketingActions/{remarketing_action_id}".format(
            customer_id=customer_id,
            remarketing_action_id=remarketing_action_id,
        )

    @staticmethod
    def parse_remarketing_action_path(path: str) -> Dict[str, str]:
        """Parse a remarketing_action path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/remarketingActions/(?P<remarketing_action_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def search_term_view_path(
        customer_id: str, campaign_id: str, ad_group_id: str, query: str,
    ) -> str:
        """Return a fully-qualified search_term_view string."""
        return "customers/{customer_id}/searchTermViews/{campaign_id}~{ad_group_id}~{query}".format(
            customer_id=customer_id,
            campaign_id=campaign_id,
            ad_group_id=ad_group_id,
            query=query,
        )

    @staticmethod
    def parse_search_term_view_path(path: str) -> Dict[str, str]:
        """Parse a search_term_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/searchTermViews/(?P<campaign_id>.+?)~(?P<ad_group_id>.+?)~(?P<query>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def shared_criterion_path(
        customer_id: str, shared_set_id: str, criterion_id: str,
    ) -> str:
        """Return a fully-qualified shared_criterion string."""
        return "customers/{customer_id}/sharedCriteria/{shared_set_id}~{criterion_id}".format(
            customer_id=customer_id,
            shared_set_id=shared_set_id,
            criterion_id=criterion_id,
        )

    @staticmethod
    def parse_shared_criterion_path(path: str) -> Dict[str, str]:
        """Parse a shared_criterion path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/sharedCriteria/(?P<shared_set_id>.+?)~(?P<criterion_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def shared_set_path(customer_id: str, shared_set_id: str,) -> str:
        """Return a fully-qualified shared_set string."""
        return "customers/{customer_id}/sharedSets/{shared_set_id}".format(
            customer_id=customer_id, shared_set_id=shared_set_id,
        )

    @staticmethod
    def parse_shared_set_path(path: str) -> Dict[str, str]:
        """Parse a shared_set path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/sharedSets/(?P<shared_set_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def shopping_performance_view_path(customer_id: str,) -> str:
        """Return a fully-qualified shopping_performance_view string."""
        return "customers/{customer_id}/shoppingPerformanceView".format(
            customer_id=customer_id,
        )

    @staticmethod
    def parse_shopping_performance_view_path(path: str) -> Dict[str, str]:
        """Parse a shopping_performance_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/shoppingPerformanceView$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def third_party_app_analytics_link_path(
        customer_id: str, customer_link_id: str,
    ) -> str:
        """Return a fully-qualified third_party_app_analytics_link string."""
        return "customers/{customer_id}/thirdPartyAppAnalyticsLinks/{customer_link_id}".format(
            customer_id=customer_id, customer_link_id=customer_link_id,
        )

    @staticmethod
    def parse_third_party_app_analytics_link_path(path: str) -> Dict[str, str]:
        """Parse a third_party_app_analytics_link path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/thirdPartyAppAnalyticsLinks/(?P<customer_link_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def topic_constant_path(topic_id: str,) -> str:
        """Return a fully-qualified topic_constant string."""
        return "topicConstants/{topic_id}".format(topic_id=topic_id,)

    @staticmethod
    def parse_topic_constant_path(path: str) -> Dict[str, str]:
        """Parse a topic_constant path into its component segments."""
        m = re.match(r"^topicConstants/(?P<topic_id>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def topic_view_path(
        customer_id: str, ad_group_id: str, criterion_id: str,
    ) -> str:
        """Return a fully-qualified topic_view string."""
        return "customers/{customer_id}/topicViews/{ad_group_id}~{criterion_id}".format(
            customer_id=customer_id,
            ad_group_id=ad_group_id,
            criterion_id=criterion_id,
        )

    @staticmethod
    def parse_topic_view_path(path: str) -> Dict[str, str]:
        """Parse a topic_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/topicViews/(?P<ad_group_id>.+?)~(?P<criterion_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def user_interest_path(customer_id: str, user_interest_id: str,) -> str:
        """Return a fully-qualified user_interest string."""
        return "customers/{customer_id}/userInterests/{user_interest_id}".format(
            customer_id=customer_id, user_interest_id=user_interest_id,
        )

    @staticmethod
    def parse_user_interest_path(path: str) -> Dict[str, str]:
        """Parse a user_interest path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/userInterests/(?P<user_interest_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def user_list_path(customer_id: str, user_list_id: str,) -> str:
        """Return a fully-qualified user_list string."""
        return "customers/{customer_id}/userLists/{user_list_id}".format(
            customer_id=customer_id, user_list_id=user_list_id,
        )

    @staticmethod
    def parse_user_list_path(path: str) -> Dict[str, str]:
        """Parse a user_list path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/userLists/(?P<user_list_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def user_location_view_path(
        customer_id: str, country_criterion_id: str, is_targeting_location: str,
    ) -> str:
        """Return a fully-qualified user_location_view string."""
        return "customers/{customer_id}/userLocationViews/{country_criterion_id}~{is_targeting_location}".format(
            customer_id=customer_id,
            country_criterion_id=country_criterion_id,
            is_targeting_location=is_targeting_location,
        )

    @staticmethod
    def parse_user_location_view_path(path: str) -> Dict[str, str]:
        """Parse a user_location_view path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/userLocationViews/(?P<country_criterion_id>.+?)~(?P<is_targeting_location>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def video_path(customer_id: str, video_id: str,) -> str:
        """Return a fully-qualified video string."""
        return "customers/{customer_id}/videos/{video_id}".format(
            customer_id=customer_id, video_id=video_id,
        )

    @staticmethod
    def parse_video_path(path: str) -> Dict[str, str]:
        """Parse a video path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/videos/(?P<video_id>.+?)$", path
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
            request (:class:`google.ads.googleads.v6.services.types.SearchGoogleAdsRequest`):
                The request object. Request message for
                [GoogleAdsService.Search][google.ads.googleads.v6.services.GoogleAdsService.Search].
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
            google.ads.googleads.v6.services.services.google_ads_service.pagers.SearchPager:
                Response message for
                [GoogleAdsService.Search][google.ads.googleads.v6.services.GoogleAdsService.Search].

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
            request (:class:`google.ads.googleads.v6.services.types.SearchGoogleAdsStreamRequest`):
                The request object. Request message for
                [GoogleAdsService.SearchStream][google.ads.googleads.v6.services.GoogleAdsService.SearchStream].
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
            Iterable[google.ads.googleads.v6.services.types.SearchGoogleAdsStreamResponse]:
                Response message for
                [GoogleAdsService.SearchStream][google.ads.googleads.v6.services.GoogleAdsService.SearchStream].

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
            request (:class:`google.ads.googleads.v6.services.types.MutateGoogleAdsRequest`):
                The request object. Request message for
                [GoogleAdsService.Mutate][google.ads.googleads.v6.services.GoogleAdsService.Mutate].
            customer_id (:class:`str`):
                Required. The ID of the customer
                whose resources are being modified.

                This corresponds to the ``customer_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            mutate_operations (:class:`Sequence[google.ads.googleads.v6.services.types.MutateOperation]`):
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
            google.ads.googleads.v6.services.types.MutateGoogleAdsResponse:
                Response message for
                [GoogleAdsService.Mutate][google.ads.googleads.v6.services.GoogleAdsService.Mutate].

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
