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

"""Accesses the google.ads.googleads.v2.services GoogleAdsService API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.page_iterator
import grpc

from google.ads.google_ads.v2.services import enums
from google.ads.google_ads.v2.services import google_ads_service_client_config
from google.ads.google_ads.v2.services.transports import google_ads_service_grpc_transport
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
from google.ads.google_ads.v2.proto.resources import geographic_view_pb2
from google.ads.google_ads.v2.proto.resources import google_ads_field_pb2
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
from google.ads.google_ads.v2.proto.services import geographic_view_service_pb2
from google.ads.google_ads.v2.proto.services import geographic_view_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import google_ads_field_service_pb2
from google.ads.google_ads.v2.proto.services import google_ads_field_service_pb2_grpc
from google.ads.google_ads.v2.proto.services import google_ads_service_pb2
from google.ads.google_ads.v2.proto.services import google_ads_service_pb2_grpc
from google.longrunning import operations_pb2
from google.protobuf import empty_pb2
from google.protobuf import wrappers_pb2



_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'google-ads',
).version


class GoogleAdsServiceClient(object):
    """Service to fetch data and metrics across resources."""

    SERVICE_ADDRESS = 'googleads.googleapis.com:443'
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = 'google.ads.googleads.v2.services.GoogleAdsService'


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
            GoogleAdsServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(
            filename)
        kwargs['credentials'] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    def __init__(self, transport=None, channel=None, credentials=None,
            client_config=None, client_info=None):
        """Constructor.

        Args:
            transport (Union[~.GoogleAdsServiceGrpcTransport,
                    Callable[[~.Credentials, type], ~.GoogleAdsServiceGrpcTransport]): A transport
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
            client_config = google_ads_service_client_config.config

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
                    default_class=google_ads_service_grpc_transport.GoogleAdsServiceGrpcTransport,
                )
            else:
                if credentials:
                    raise ValueError(
                        'Received both a transport instance and '
                        'credentials; these are mutually exclusive.'
                    )
                self.transport = transport
        else:
            self.transport = google_ads_service_grpc_transport.GoogleAdsServiceGrpcTransport(
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
    def search(
            self,
            customer_id,
            query,
            page_size=None,
            validate_only=None,
            return_summary_row=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Returns all rows that match the search query.

        Args:
            customer_id (str): The ID of the customer being queried.
            query (str): The query string.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            validate_only (bool): If true, the request is validated but not executed.
            return_summary_row (bool): If true, summary row will be included in the response.
                Otherwise(false or not specified) summary row will not be returned.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`~google.ads.googleads_v2.types.GoogleAdsRow` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'search' not in self._inner_api_calls:
            self._inner_api_calls['search'] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.search,
                default_retry=self._method_configs['Search'].retry,
                default_timeout=self._method_configs['Search'].timeout,
                client_info=self._client_info,
            )

        request = google_ads_service_pb2.SearchGoogleAdsRequest(
            customer_id=customer_id,
            query=query,
            page_size=page_size,
            validate_only=validate_only,
            return_summary_row=return_summary_row,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [('customer_id', customer_id)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(routing_header)
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(self._inner_api_calls['search'], retry=retry, timeout=timeout, metadata=metadata),
            request=request,
            items_field='results',
            request_token_field='page_token',
            response_token_field='next_page_token',
        )
        return iterator

    def mutate(
            self,
            customer_id,
            mutate_operations,
            partial_failure=None,
            validate_only=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
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

        Args:
            customer_id (str): The ID of the customer whose resources are being modified.
            mutate_operations (list[Union[dict, ~google.ads.googleads_v2.types.MutateOperation]]): The list of operations to perform on individual resources.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.ads.googleads_v2.types.MutateOperation`
            partial_failure (bool): If true, successful operations will be carried out and invalid
                operations will return errors. If false, all operations will be carried
                out in one transaction if and only if they are all valid.
                Default is false.
            validate_only (bool): If true, the request is validated but not executed. Only errors are
                returned, not results.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.ads.googleads_v2.types.MutateGoogleAdsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'mutate' not in self._inner_api_calls:
            self._inner_api_calls['mutate'] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.mutate,
                default_retry=self._method_configs['Mutate'].retry,
                default_timeout=self._method_configs['Mutate'].timeout,
                client_info=self._client_info,
            )

        request = google_ads_service_pb2.MutateGoogleAdsRequest(
            customer_id=customer_id,
            mutate_operations=mutate_operations,
            partial_failure=partial_failure,
            validate_only=validate_only,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [('customer_id', customer_id)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(routing_header)
            metadata.append(routing_metadata)

        return self._inner_api_calls['mutate'](request, retry=retry, timeout=timeout, metadata=metadata)
