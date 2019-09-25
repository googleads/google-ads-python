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

"""Accesses the google.ads.googleads.v2.services GeoTargetConstantService API."""

import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.path_template
import google.api_core.protobuf_helpers
import grpc

from google.ads.google_ads.v2.services import enums
from google.ads.google_ads.v2.services import geo_target_constant_service_client_config
from google.ads.google_ads.v2.services.transports import geo_target_constant_service_grpc_transport
from google.ads.google_ads.v2.proto.resources import account_budget_pb2
from google.ads.google_ads.v2.proto.resources import account_budget_proposal_pb2
from google.ads.google_ads.v2.proto.resources import ad_group_ad_asset_view_pb2
from google.ads.google_ads.v2.proto.resources import ad_group_ad_label_pb2
from google.ads.google_ads.v2.proto.resources import ad_group_ad_pb2
from google.ads.google_ads.v2.proto.resources import ad_group_audience_view_pb2
from google.ads.google_ads.v2.proto.resources import ad_group_bid_modifier_pb2
from google.ads.google_ads.v2.proto.resources import ad_group_criterion_label_pb2
from google.ads.google_ads.v2.proto.resources import ad_group_criterion_pb2
from google.ads.google_ads.v2.proto.resources import ad_group_criterion_simulation_pb2
from google.ads.google_ads.v2.proto.resources import ad_group_extension_setting_pb2
from google.ads.google_ads.v2.proto.resources import ad_group_feed_pb2
from google.ads.google_ads.v2.proto.resources import ad_group_label_pb2
from google.ads.google_ads.v2.proto.resources import ad_group_pb2
from google.ads.google_ads.v2.proto.resources import ad_group_simulation_pb2
from google.ads.google_ads.v2.proto.resources import ad_parameter_pb2
from google.ads.google_ads.v2.proto.resources import ad_pb2
from google.ads.google_ads.v2.proto.resources import ad_schedule_view_pb2
from google.ads.google_ads.v2.proto.resources import age_range_view_pb2
from google.ads.google_ads.v2.proto.resources import asset_pb2
from google.ads.google_ads.v2.proto.resources import bidding_strategy_pb2
from google.ads.google_ads.v2.proto.resources import billing_setup_pb2
from google.ads.google_ads.v2.proto.resources import campaign_audience_view_pb2
from google.ads.google_ads.v2.proto.resources import campaign_bid_modifier_pb2
from google.ads.google_ads.v2.proto.resources import campaign_budget_pb2
from google.ads.google_ads.v2.proto.resources import campaign_criterion_pb2
from google.ads.google_ads.v2.proto.resources import campaign_criterion_simulation_pb2
from google.ads.google_ads.v2.proto.resources import campaign_draft_pb2
from google.ads.google_ads.v2.proto.resources import campaign_experiment_pb2
from google.ads.google_ads.v2.proto.resources import campaign_extension_setting_pb2
from google.ads.google_ads.v2.proto.resources import campaign_feed_pb2
from google.ads.google_ads.v2.proto.resources import campaign_label_pb2
from google.ads.google_ads.v2.proto.resources import campaign_pb2
from google.ads.google_ads.v2.proto.resources import campaign_shared_set_pb2
from google.ads.google_ads.v2.proto.resources import carrier_constant_pb2
from google.ads.google_ads.v2.proto.resources import change_status_pb2
from google.ads.google_ads.v2.proto.resources import click_view_pb2
from google.ads.google_ads.v2.proto.resources import conversion_action_pb2
from google.ads.google_ads.v2.proto.resources import custom_interest_pb2
from google.ads.google_ads.v2.proto.resources import customer_client_link_pb2
from google.ads.google_ads.v2.proto.resources import customer_client_pb2
from google.ads.google_ads.v2.proto.resources import customer_extension_setting_pb2
from google.ads.google_ads.v2.proto.resources import customer_feed_pb2
from google.ads.google_ads.v2.proto.resources import customer_label_pb2
from google.ads.google_ads.v2.proto.resources import customer_manager_link_pb2
from google.ads.google_ads.v2.proto.resources import customer_negative_criterion_pb2
from google.ads.google_ads.v2.proto.resources import customer_pb2
from google.ads.google_ads.v2.proto.resources import detail_placement_view_pb2
from google.ads.google_ads.v2.proto.resources import display_keyword_view_pb2
from google.ads.google_ads.v2.proto.resources import distance_view_pb2
from google.ads.google_ads.v2.proto.resources import domain_category_pb2
from google.ads.google_ads.v2.proto.resources import dynamic_search_ads_search_term_view_pb2
from google.ads.google_ads.v2.proto.resources import expanded_landing_page_view_pb2
from google.ads.google_ads.v2.proto.resources import extension_feed_item_pb2
from google.ads.google_ads.v2.proto.resources import feed_item_pb2
from google.ads.google_ads.v2.proto.resources import feed_item_target_pb2
from google.ads.google_ads.v2.proto.resources import feed_mapping_pb2
from google.ads.google_ads.v2.proto.resources import feed_pb2
from google.ads.google_ads.v2.proto.resources import feed_placeholder_view_pb2
from google.ads.google_ads.v2.proto.resources import gender_view_pb2
from google.ads.google_ads.v2.proto.resources import geo_target_constant_pb2
from google.ads.google_ads.v2.proto.services import account_budget_proposal_service_pb2
from google.ads.google_ads.v2.proto.services import account_budget_proposal_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import account_budget_service_pb2
from google.ads.google_ads.v2.proto.services import account_budget_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import ad_group_ad_asset_view_service_pb2
from google.ads.google_ads.v2.proto.services import ad_group_ad_asset_view_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import ad_group_ad_label_service_pb2
from google.ads.google_ads.v2.proto.services import ad_group_ad_label_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import ad_group_ad_service_pb2
from google.ads.google_ads.v2.proto.services import ad_group_ad_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import ad_group_audience_view_service_pb2
from google.ads.google_ads.v2.proto.services import ad_group_audience_view_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import ad_group_bid_modifier_service_pb2
from google.ads.google_ads.v2.proto.services import ad_group_bid_modifier_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import ad_group_criterion_label_service_pb2
from google.ads.google_ads.v2.proto.services import ad_group_criterion_label_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import ad_group_criterion_service_pb2
from google.ads.google_ads.v2.proto.services import ad_group_criterion_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import ad_group_criterion_simulation_service_pb2
from google.ads.google_ads.v2.proto.services import ad_group_criterion_simulation_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import ad_group_extension_setting_service_pb2
from google.ads.google_ads.v2.proto.services import ad_group_extension_setting_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import ad_group_feed_service_pb2
from google.ads.google_ads.v2.proto.services import ad_group_feed_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import ad_group_label_service_pb2
from google.ads.google_ads.v2.proto.services import ad_group_label_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import ad_group_service_pb2
from google.ads.google_ads.v2.proto.services import ad_group_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import ad_group_simulation_service_pb2
from google.ads.google_ads.v2.proto.services import ad_group_simulation_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import ad_parameter_service_pb2
from google.ads.google_ads.v2.proto.services import ad_parameter_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import ad_schedule_view_service_pb2
from google.ads.google_ads.v2.proto.services import ad_schedule_view_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import ad_service_pb2
from google.ads.google_ads.v2.proto.services import ad_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import age_range_view_service_pb2
from google.ads.google_ads.v2.proto.services import age_range_view_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import asset_service_pb2
from google.ads.google_ads.v2.proto.services import asset_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import bidding_strategy_service_pb2
from google.ads.google_ads.v2.proto.services import bidding_strategy_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import billing_setup_service_pb2
from google.ads.google_ads.v2.proto.services import billing_setup_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import campaign_audience_view_service_pb2
from google.ads.google_ads.v2.proto.services import campaign_audience_view_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import campaign_bid_modifier_service_pb2
from google.ads.google_ads.v2.proto.services import campaign_bid_modifier_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import campaign_budget_service_pb2
from google.ads.google_ads.v2.proto.services import campaign_budget_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import campaign_criterion_service_pb2
from google.ads.google_ads.v2.proto.services import campaign_criterion_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import campaign_criterion_simulation_service_pb2
from google.ads.google_ads.v2.proto.services import campaign_criterion_simulation_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import campaign_draft_service_pb2
from google.ads.google_ads.v2.proto.services import campaign_draft_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import campaign_experiment_service_pb2
from google.ads.google_ads.v2.proto.services import campaign_experiment_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import campaign_extension_setting_service_pb2
from google.ads.google_ads.v2.proto.services import campaign_extension_setting_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import campaign_feed_service_pb2
from google.ads.google_ads.v2.proto.services import campaign_feed_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import campaign_label_service_pb2
from google.ads.google_ads.v2.proto.services import campaign_label_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import campaign_service_pb2
from google.ads.google_ads.v2.proto.services import campaign_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import campaign_shared_set_service_pb2
from google.ads.google_ads.v2.proto.services import campaign_shared_set_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import carrier_constant_service_pb2
from google.ads.google_ads.v2.proto.services import carrier_constant_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import change_status_service_pb2
from google.ads.google_ads.v2.proto.services import change_status_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import click_view_service_pb2
from google.ads.google_ads.v2.proto.services import click_view_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import conversion_action_service_pb2
from google.ads.google_ads.v2.proto.services import conversion_action_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import conversion_adjustment_upload_service_pb2
from google.ads.google_ads.v2.proto.services import conversion_adjustment_upload_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import conversion_upload_service_pb2
from google.ads.google_ads.v2.proto.services import conversion_upload_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import custom_interest_service_pb2
from google.ads.google_ads.v2.proto.services import custom_interest_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import customer_client_link_service_pb2
from google.ads.google_ads.v2.proto.services import customer_client_link_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import customer_client_service_pb2
from google.ads.google_ads.v2.proto.services import customer_client_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import customer_extension_setting_service_pb2
from google.ads.google_ads.v2.proto.services import customer_extension_setting_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import customer_feed_service_pb2
from google.ads.google_ads.v2.proto.services import customer_feed_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import customer_label_service_pb2
from google.ads.google_ads.v2.proto.services import customer_label_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import customer_manager_link_service_pb2
from google.ads.google_ads.v2.proto.services import customer_manager_link_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import customer_negative_criterion_service_pb2
from google.ads.google_ads.v2.proto.services import customer_negative_criterion_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import customer_service_pb2
from google.ads.google_ads.v2.proto.services import customer_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import detail_placement_view_service_pb2
from google.ads.google_ads.v2.proto.services import detail_placement_view_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import display_keyword_view_service_pb2
from google.ads.google_ads.v2.proto.services import display_keyword_view_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import distance_view_service_pb2
from google.ads.google_ads.v2.proto.services import distance_view_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import domain_category_service_pb2
from google.ads.google_ads.v2.proto.services import domain_category_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import dynamic_search_ads_search_term_view_service_pb2
from google.ads.google_ads.v2.proto.services import dynamic_search_ads_search_term_view_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import expanded_landing_page_view_service_pb2
from google.ads.google_ads.v2.proto.services import expanded_landing_page_view_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import extension_feed_item_service_pb2
from google.ads.google_ads.v2.proto.services import extension_feed_item_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import feed_item_service_pb2
from google.ads.google_ads.v2.proto.services import feed_item_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import feed_item_target_service_pb2
from google.ads.google_ads.v2.proto.services import feed_item_target_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import feed_mapping_service_pb2
from google.ads.google_ads.v2.proto.services import feed_mapping_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import feed_placeholder_view_service_pb2
from google.ads.google_ads.v2.proto.services import feed_placeholder_view_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import feed_service_pb2
from google.ads.google_ads.v2.proto.services import feed_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import gender_view_service_pb2
from google.ads.google_ads.v2.proto.services import gender_view_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import geo_target_constant_service_pb2
from google.ads.google_ads.v2.proto.services import geo_target_constant_service_pb2_grpc
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2
from google.protobuf import wrappers_pb2



_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'google-ads',
).version


class GeoTargetConstantServiceClient(object):
    """Service to fetch geo target constants."""

    SERVICE_ADDRESS = 'googleads.googleapis.com:443'
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = 'google.ads.googleads.v2.services.GeoTargetConstantService'


    @classmethod
    def from_service_account_file(cls, filename, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            GeoTargetConstantServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(
            filename)
        kwargs['credentials'] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file


    @classmethod
    def geo_target_constant_path(cls, geo_target_constant):
        """Return a fully-qualified geo_target_constant string."""
        return google.api_core.path_template.expand(
            'geoTargetConstants/{geo_target_constant}',
            geo_target_constant=geo_target_constant,
        )

    def __init__(self, transport=None, channel=None, credentials=None,
            client_config=None, client_info=None):
        """Constructor.

        Args:
            transport (Union[~.GeoTargetConstantServiceGrpcTransport,
                    Callable[[~.Credentials, type], ~.GeoTargetConstantServiceGrpcTransport]): A transport
                instance, responsible for actually making the API calls.
                The default transport uses the gRPC protocol.
                This argument may also be a callable which returns a
                transport instance. Callables will be sent the credentials
                as the first argument and the default transport class as
                the second argument.
            channel (grpc.Channel): DEPRECATED. A ``Channel`` instance
                through which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is mutually exclusive with providing a
                transport instance to ``transport``; doing so will raise
                an exception.
            client_config (dict): DEPRECATED. A dictionary of call options for
                each method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        # Raise deprecation warnings for things we want to go away.
        if client_config is not None:
            warnings.warn('The `client_config` argument is deprecated.',
                          PendingDeprecationWarning, stacklevel=2)
        else:
            client_config = geo_target_constant_service_client_config.config

        if channel:
            warnings.warn('The `channel` argument is deprecated; use '
                          '`transport` instead.',
                          PendingDeprecationWarning, stacklevel=2)

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=geo_target_constant_service_grpc_transport.GeoTargetConstantServiceGrpcTransport,
                )
            else:
                if credentials:
                    raise ValueError(
                        'Received both a transport instance and '
                        'credentials; these are mutually exclusive.'
                    )
                self.transport = transport
        else:
            self.transport = geo_target_constant_service_grpc_transport.GeoTargetConstantServiceGrpcTransport(
                address=self.SERVICE_ADDRESS,
                channel=channel,
                credentials=credentials,
            )

        if client_info is None:
            client_info = google.api_core.gapic_v1.client_info.ClientInfo(
                gapic_version=_GAPIC_LIBRARY_VERSION,
            )
        else:
            client_info.gapic_version = _GAPIC_LIBRARY_VERSION
        self._client_info = client_info

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        self._method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config['interfaces'][self._INTERFACE_NAME],
        )

        # Save a dictionary of cached API call functions.
        # These are the actual callables which invoke the proper
        # transport methods, wrapped with `wrap_method` to add retry,
        # timeout, and the like.
        self._inner_api_calls = {}

    # Service calls
    def get_geo_target_constant(
            self,
            resource_name,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Returns the requested geo target constant in full detail.

        Args:
            resource_name (str): The resource name of the geo target constant to fetch.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.ads.googleads_v2.types.GeoTargetConstant` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'get_geo_target_constant' not in self._inner_api_calls:
            self._inner_api_calls['get_geo_target_constant'] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_geo_target_constant,
                default_retry=self._method_configs['GetGeoTargetConstant'].retry,
                default_timeout=self._method_configs['GetGeoTargetConstant'].timeout,
                client_info=self._client_info,
            )

        request = geo_target_constant_service_pb2.GetGeoTargetConstantRequest(
            resource_name=resource_name,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [('resource_name', resource_name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(routing_header)
            metadata.append(routing_metadata)

        return self._inner_api_calls['get_geo_target_constant'](request, retry=retry, timeout=timeout, metadata=metadata)

    def suggest_geo_target_constants(
            self,
            locale,
            country_code,
            location_names=None,
            geo_targets=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Returns GeoTargetConstant suggestions by location name or by resource name.

        Args:
            locale (Union[dict, ~google.ads.googleads_v2.types.StringValue]): If possible, returned geo targets are translated using this locale. If not,
                en is used by default. This is also used as a hint for returned geo
                targets.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.ads.googleads_v2.types.StringValue`
            country_code (Union[dict, ~google.ads.googleads_v2.types.StringValue]): Returned geo targets are restricted to this country code.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.ads.googleads_v2.types.StringValue`
            location_names (Union[dict, ~google.ads.googleads_v2.types.LocationNames]): The location names to search by. At most 25 names can be set.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.ads.googleads_v2.types.LocationNames`
            geo_targets (Union[dict, ~google.ads.googleads_v2.types.GeoTargets]): The geo target constant resource names to filter by.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.ads.googleads_v2.types.GeoTargets`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.ads.googleads_v2.types.SuggestGeoTargetConstantsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'suggest_geo_target_constants' not in self._inner_api_calls:
            self._inner_api_calls['suggest_geo_target_constants'] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.suggest_geo_target_constants,
                default_retry=self._method_configs['SuggestGeoTargetConstants'].retry,
                default_timeout=self._method_configs['SuggestGeoTargetConstants'].timeout,
                client_info=self._client_info,
            )

        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        google.api_core.protobuf_helpers.check_oneof(
            location_names=location_names,
            geo_targets=geo_targets,
        )

        request = geo_target_constant_service_pb2.SuggestGeoTargetConstantsRequest(
            locale=locale,
            country_code=country_code,
            location_names=location_names,
            geo_targets=geo_targets,
        )
        return self._inner_api_calls['suggest_geo_target_constants'](request, retry=retry, timeout=timeout, metadata=metadata)
