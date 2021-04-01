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
from typing import Dict, Optional, Sequence, Tuple, Type, Union

from google.api_core import client_options as client_options_lib  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.ads.googleads.v6.resources.types import batch_job
from google.ads.googleads.v6.services.services.batch_job_service import pagers
from google.ads.googleads.v6.services.types import batch_job_service
from google.ads.googleads.v6.services.types import google_ads_service
from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.protobuf import empty_pb2 as empty  # type: ignore

from .transports.base import BatchJobServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import BatchJobServiceGrpcTransport


class BatchJobServiceClientMeta(type):
    """Metaclass for the BatchJobService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[BatchJobServiceTransport]]
    _transport_registry["grpc"] = BatchJobServiceGrpcTransport

    def get_transport_class(
        cls, label: str = None,
    ) -> Type[BatchJobServiceTransport]:
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


class BatchJobServiceClient(metaclass=BatchJobServiceClientMeta):
    """Service to manage batch jobs."""

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
            BatchJobServiceClient: The constructed client.
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
            BatchJobServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(
            filename
        )
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> BatchJobServiceTransport:
        """Return the transport used by the client instance.

        Returns:
            BatchJobServiceTransport: The transport used by the client instance.
        """
        return self._transport

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
    def customer_path(customer_id: str,) -> str:
        """Return a fully-qualified customer string."""
        return "customers/{customer_id}".format(customer_id=customer_id,)

    @staticmethod
    def parse_customer_path(path: str) -> Dict[str, str]:
        """Parse a customer path into its component segments."""
        m = re.match(r"^customers/(?P<customer_id>.+?)$", path)
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
        transport: Union[str, BatchJobServiceTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the batch job service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.BatchJobServiceTransport]): The
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
        if isinstance(transport, BatchJobServiceTransport):
            # transport is a BatchJobServiceTransport instance.
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
            self._transport = BatchJobServiceGrpcTransport(
                credentials=credentials,
                host=api_endpoint,
                ssl_channel_credentials=ssl_credentials,
                client_info=client_info,
            )

    def mutate_batch_job(
        self,
        request: batch_job_service.MutateBatchJobRequest = None,
        *,
        customer_id: str = None,
        operation: batch_job_service.BatchJobOperation = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> batch_job_service.MutateBatchJobResponse:
        r"""Mutates a batch job.

        Args:
            request (:class:`google.ads.googleads.v6.services.types.MutateBatchJobRequest`):
                The request object. Request message for
                [BatchJobService.MutateBatchJob][google.ads.googleads.v6.services.BatchJobService.MutateBatchJob].
            customer_id (:class:`str`):
                Required. The ID of the customer for
                which to create a batch job.

                This corresponds to the ``customer_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            operation (:class:`google.ads.googleads.v6.services.types.BatchJobOperation`):
                Required. The operation to perform on
                an individual batch job.

                This corresponds to the ``operation`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.ads.googleads.v6.services.types.MutateBatchJobResponse:
                Response message for
                [BatchJobService.MutateBatchJob][google.ads.googleads.v6.services.BatchJobService.MutateBatchJob].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([customer_id, operation]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a batch_job_service.MutateBatchJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, batch_job_service.MutateBatchJobRequest):
            request = batch_job_service.MutateBatchJobRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if customer_id is not None:
                request.customer_id = customer_id
            if operation is not None:
                request.operation = operation

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.mutate_batch_job]

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

    def get_batch_job(
        self,
        request: batch_job_service.GetBatchJobRequest = None,
        *,
        resource_name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> batch_job.BatchJob:
        r"""Returns the batch job.

        Args:
            request (:class:`google.ads.googleads.v6.services.types.GetBatchJobRequest`):
                The request object. Request message for
                [BatchJobService.GetBatchJob][google.ads.googleads.v6.services.BatchJobService.GetBatchJob].
            resource_name (:class:`str`):
                Required. The resource name of the
                batch job to get.

                This corresponds to the ``resource_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.ads.googleads.v6.resources.types.BatchJob:
                A list of mutates being processed
                asynchronously. The mutates are uploaded
                by the user. The mutates themselves
                aren't readable and the results of the
                job can only be read using
                BatchJobService.ListBatchJobResults.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([resource_name]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a batch_job_service.GetBatchJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, batch_job_service.GetBatchJobRequest):
            request = batch_job_service.GetBatchJobRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if resource_name is not None:
                request.resource_name = resource_name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_batch_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("resource_name", request.resource_name),)
            ),
        )

        # Send the request.
        response = rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_batch_job_results(
        self,
        request: batch_job_service.ListBatchJobResultsRequest = None,
        *,
        resource_name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListBatchJobResultsPager:
        r"""Returns the results of the batch job. The job must be
        done. Supports standard list paging.

        Args:
            request (:class:`google.ads.googleads.v6.services.types.ListBatchJobResultsRequest`):
                The request object. Request message for
                [BatchJobService.ListBatchJobResults][google.ads.googleads.v6.services.BatchJobService.ListBatchJobResults].
            resource_name (:class:`str`):
                Required. The resource name of the
                batch job whose results are being
                listed.

                This corresponds to the ``resource_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.ads.googleads.v6.services.services.batch_job_service.pagers.ListBatchJobResultsPager:
                Response message for
                [BatchJobService.ListBatchJobResults][google.ads.googleads.v6.services.BatchJobService.ListBatchJobResults].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([resource_name]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a batch_job_service.ListBatchJobResultsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, batch_job_service.ListBatchJobResultsRequest
        ):
            request = batch_job_service.ListBatchJobResultsRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if resource_name is not None:
                request.resource_name = resource_name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_batch_job_results
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("resource_name", request.resource_name),)
            ),
        )

        # Send the request.
        response = rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListBatchJobResultsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def run_batch_job(
        self,
        request: batch_job_service.RunBatchJobRequest = None,
        *,
        resource_name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Runs the batch job.
        The Operation.metadata field type is BatchJobMetadata.
        When finished, the long running operation will not
        contain errors or a response. Instead, use
        ListBatchJobResults to get the results of the job.

        Args:
            request (:class:`google.ads.googleads.v6.services.types.RunBatchJobRequest`):
                The request object. Request message for
                [BatchJobService.RunBatchJob][google.ads.googleads.v6.services.BatchJobService.RunBatchJob].
            resource_name (:class:`str`):
                Required. The resource name of the
                BatchJob to run.

                This corresponds to the ``resource_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

                   The JSON representation for Empty is empty JSON
                   object {}.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([resource_name]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a batch_job_service.RunBatchJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, batch_job_service.RunBatchJobRequest):
            request = batch_job_service.RunBatchJobRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if resource_name is not None:
                request.resource_name = resource_name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.run_batch_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("resource_name", request.resource_name),)
            ),
        )

        # Send the request.
        response = rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            empty.Empty,
            metadata_type=batch_job.BatchJob.BatchJobMetadata,
        )

        # Done; return the response.
        return response

    def add_batch_job_operations(
        self,
        request: batch_job_service.AddBatchJobOperationsRequest = None,
        *,
        resource_name: str = None,
        sequence_token: str = None,
        mutate_operations: Sequence[google_ads_service.MutateOperation] = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> batch_job_service.AddBatchJobOperationsResponse:
        r"""Add operations to the batch job.

        Args:
            request (:class:`google.ads.googleads.v6.services.types.AddBatchJobOperationsRequest`):
                The request object. Request message for
                [BatchJobService.AddBatchJobOperations][google.ads.googleads.v6.services.BatchJobService.AddBatchJobOperations].
            resource_name (:class:`str`):
                Required. The resource name of the
                batch job.

                This corresponds to the ``resource_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            sequence_token (:class:`str`):
                A token used to enforce sequencing.

                The first AddBatchJobOperations request for a batch job
                should not set sequence_token. Subsequent requests must
                set sequence_token to the value of next_sequence_token
                received in the previous AddBatchJobOperations response.

                This corresponds to the ``sequence_token`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            mutate_operations (:class:`Sequence[google.ads.googleads.v6.services.types.MutateOperation]`):
                Required. The list of mutates being
                added.
                Operations can use negative integers as
                temp ids to signify dependencies between
                entities created in this batch job. For
                example, a customer with id = 1234 can
                create a campaign and an ad group in
                that same campaign by creating a
                campaign in the first operation with the
                resource name explicitly set to
                "customers/1234/campaigns/-1", and
                creating an ad group in the second
                operation with the campaign field also
                set to "customers/1234/campaigns/-1".

                This corresponds to the ``mutate_operations`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.ads.googleads.v6.services.types.AddBatchJobOperationsResponse:
                Response message for
                [BatchJobService.AddBatchJobOperations][google.ads.googleads.v6.services.BatchJobService.AddBatchJobOperations].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any(
            [resource_name, sequence_token, mutate_operations]
        ):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a batch_job_service.AddBatchJobOperationsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, batch_job_service.AddBatchJobOperationsRequest
        ):
            request = batch_job_service.AddBatchJobOperationsRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if resource_name is not None:
                request.resource_name = resource_name
            if sequence_token is not None:
                request.sequence_token = sequence_token
            if mutate_operations is not None:
                request.mutate_operations = mutate_operations

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.add_batch_job_operations
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("resource_name", request.resource_name),)
            ),
        )

        # Send the request.
        response = rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

        # Done; return the response.
        return response


__all__ = ("BatchJobServiceClient",)
