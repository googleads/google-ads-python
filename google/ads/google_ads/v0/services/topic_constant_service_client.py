# Copyright 2018 Google LLC
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
"""Accesses the google.ads.googleads.v0.services TopicConstantService API."""

import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.path_template
import grpc

from google.ads.google_ads.v0.services import enums
from google.ads.google_ads.v0.services import topic_constant_service_client_config
from google.ads.google_ads.v0.services.transports import topic_constant_service_grpc_transport
from google.ads.google_ads.v0.proto.resources import account_budget_pb2
from google.ads.google_ads.v0.proto.resources import account_budget_proposal_pb2
from google.ads.google_ads.v0.proto.resources import ad_group_ad_pb2
from google.ads.google_ads.v0.proto.resources import ad_group_audience_view_pb2
from google.ads.google_ads.v0.proto.resources import ad_group_bid_modifier_pb2
from google.ads.google_ads.v0.proto.resources import ad_group_criterion_pb2
from google.ads.google_ads.v0.proto.resources import ad_group_pb2
from google.ads.google_ads.v0.proto.resources import age_range_view_pb2
from google.ads.google_ads.v0.proto.resources import bidding_strategy_pb2
from google.ads.google_ads.v0.proto.resources import billing_setup_pb2
from google.ads.google_ads.v0.proto.resources import campaign_bid_modifier_pb2
from google.ads.google_ads.v0.proto.resources import campaign_budget_pb2
from google.ads.google_ads.v0.proto.resources import campaign_criterion_pb2
from google.ads.google_ads.v0.proto.resources import campaign_group_pb2
from google.ads.google_ads.v0.proto.resources import campaign_pb2
from google.ads.google_ads.v0.proto.resources import campaign_shared_set_pb2
from google.ads.google_ads.v0.proto.resources import change_status_pb2
from google.ads.google_ads.v0.proto.resources import conversion_action_pb2
from google.ads.google_ads.v0.proto.resources import customer_client_link_pb2
from google.ads.google_ads.v0.proto.resources import customer_manager_link_pb2
from google.ads.google_ads.v0.proto.resources import customer_pb2
from google.ads.google_ads.v0.proto.resources import display_keyword_view_pb2
from google.ads.google_ads.v0.proto.resources import gender_view_pb2
from google.ads.google_ads.v0.proto.resources import geo_target_constant_pb2
from google.ads.google_ads.v0.proto.resources import google_ads_field_pb2
from google.ads.google_ads.v0.proto.resources import hotel_group_view_pb2
from google.ads.google_ads.v0.proto.resources import keyword_view_pb2
from google.ads.google_ads.v0.proto.resources import managed_placement_view_pb2
from google.ads.google_ads.v0.proto.resources import media_file_pb2
from google.ads.google_ads.v0.proto.resources import parental_status_view_pb2
from google.ads.google_ads.v0.proto.resources import product_group_view_pb2
from google.ads.google_ads.v0.proto.resources import recommendation_pb2
from google.ads.google_ads.v0.proto.resources import shared_criterion_pb2
from google.ads.google_ads.v0.proto.resources import shared_set_pb2
from google.ads.google_ads.v0.proto.resources import topic_constant_pb2
from google.ads.google_ads.v0.proto.services import account_budget_proposal_service_pb2
from google.ads.google_ads.v0.proto.services import account_budget_proposal_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import account_budget_service_pb2
from google.ads.google_ads.v0.proto.services import account_budget_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import ad_group_ad_service_pb2
from google.ads.google_ads.v0.proto.services import ad_group_ad_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import ad_group_audience_view_service_pb2
from google.ads.google_ads.v0.proto.services import ad_group_audience_view_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import ad_group_bid_modifier_service_pb2
from google.ads.google_ads.v0.proto.services import ad_group_bid_modifier_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import ad_group_criterion_service_pb2
from google.ads.google_ads.v0.proto.services import ad_group_criterion_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import ad_group_service_pb2
from google.ads.google_ads.v0.proto.services import ad_group_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import age_range_view_service_pb2
from google.ads.google_ads.v0.proto.services import age_range_view_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import bidding_strategy_service_pb2
from google.ads.google_ads.v0.proto.services import bidding_strategy_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import billing_setup_service_pb2
from google.ads.google_ads.v0.proto.services import billing_setup_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import campaign_bid_modifier_service_pb2
from google.ads.google_ads.v0.proto.services import campaign_bid_modifier_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import campaign_budget_service_pb2
from google.ads.google_ads.v0.proto.services import campaign_budget_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import campaign_criterion_service_pb2
from google.ads.google_ads.v0.proto.services import campaign_criterion_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import campaign_group_service_pb2
from google.ads.google_ads.v0.proto.services import campaign_group_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import campaign_service_pb2
from google.ads.google_ads.v0.proto.services import campaign_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import campaign_shared_set_service_pb2
from google.ads.google_ads.v0.proto.services import campaign_shared_set_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import change_status_service_pb2
from google.ads.google_ads.v0.proto.services import change_status_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import conversion_action_service_pb2
from google.ads.google_ads.v0.proto.services import conversion_action_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import customer_client_link_service_pb2
from google.ads.google_ads.v0.proto.services import customer_client_link_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import customer_manager_link_service_pb2
from google.ads.google_ads.v0.proto.services import customer_manager_link_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import customer_service_pb2
from google.ads.google_ads.v0.proto.services import customer_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import display_keyword_view_service_pb2
from google.ads.google_ads.v0.proto.services import display_keyword_view_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import gender_view_service_pb2
from google.ads.google_ads.v0.proto.services import gender_view_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import geo_target_constant_service_pb2
from google.ads.google_ads.v0.proto.services import geo_target_constant_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import google_ads_field_service_pb2
from google.ads.google_ads.v0.proto.services import google_ads_field_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import google_ads_service_pb2
from google.ads.google_ads.v0.proto.services import google_ads_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import hotel_group_view_service_pb2
from google.ads.google_ads.v0.proto.services import hotel_group_view_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import keyword_view_service_pb2
from google.ads.google_ads.v0.proto.services import keyword_view_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import managed_placement_view_service_pb2
from google.ads.google_ads.v0.proto.services import managed_placement_view_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import media_file_service_pb2
from google.ads.google_ads.v0.proto.services import media_file_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import parental_status_view_service_pb2
from google.ads.google_ads.v0.proto.services import parental_status_view_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import product_group_view_service_pb2
from google.ads.google_ads.v0.proto.services import product_group_view_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import recommendation_service_pb2
from google.ads.google_ads.v0.proto.services import recommendation_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import shared_criterion_service_pb2
from google.ads.google_ads.v0.proto.services import shared_criterion_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import shared_set_service_pb2
from google.ads.google_ads.v0.proto.services import shared_set_service_pb2_grpc
from google.ads.google_ads.v0.proto.services import topic_constant_service_pb2
from google.ads.google_ads.v0.proto.services import topic_constant_service_pb2_grpc
from google.protobuf import wrappers_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'google-ads', ).version


class TopicConstantServiceClient(object):
    """Service to fetch topic constants."""

    SERVICE_ADDRESS = 'googleads.googleapis.com:443'
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = 'google.ads.googleads.v0.services.TopicConstantService'

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
            TopicConstantServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(
            filename)
        kwargs['credentials'] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def topic_constant_path(cls, topic_constant):
        """Return a fully-qualified topic_constant string."""
        return google.api_core.path_template.expand(
            'topicConstants/{topic_constant}',
            topic_constant=topic_constant,
        )

    def __init__(self,
                 transport=None,
                 channel=None,
                 credentials=None,
                 client_config=topic_constant_service_client_config.config,
                 client_info=None):
        """Constructor.

        Args:
            transport (Union[~.TopicConstantServiceGrpcTransport,
                    Callable[[~.Credentials, type], ~.TopicConstantServiceGrpcTransport]): A transport
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
        if client_config:
            warnings.warn('The `client_config` argument is deprecated.',
                          PendingDeprecationWarning)
        if channel:
            warnings.warn(
                'The `channel` argument is deprecated; use '
                '`transport` instead.', PendingDeprecationWarning)

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=topic_constant_service_grpc_transport.
                    TopicConstantServiceGrpcTransport,
                )
            else:
                if credentials:
                    raise ValueError(
                        'Received both a transport instance and '
                        'credentials; these are mutually exclusive.')
                self.transport = transport
        else:
            self.transport = topic_constant_service_grpc_transport.TopicConstantServiceGrpcTransport(
                address=self.SERVICE_ADDRESS,
                channel=channel,
                credentials=credentials,
            )

        if client_info is None:
            client_info = (
                google.api_core.gapic_v1.client_info.DEFAULT_CLIENT_INFO)
        client_info.gapic_version = _GAPIC_LIBRARY_VERSION
        self._client_info = client_info

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        self._method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config['interfaces'][self._INTERFACE_NAME], )

        # Save a dictionary of cached API call functions.
        # These are the actual callables which invoke the proper
        # transport methods, wrapped with `wrap_method` to add retry,
        # timeout, and the like.
        self._inner_api_calls = {}

    # Service calls
    def get_topic_constant(self,
                           resource_name,
                           retry=google.api_core.gapic_v1.method.DEFAULT,
                           timeout=google.api_core.gapic_v1.method.DEFAULT,
                           metadata=None):
        """
        Returns the requested topic constant in full detail.

        Args:
            resource_name (str): Resource name of the Topic to fetch.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.ads.google_ads.v0.types.TopicConstant` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'get_topic_constant' not in self._inner_api_calls:
            self._inner_api_calls[
                'get_topic_constant'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.get_topic_constant,
                    default_retry=self._method_configs[
                        'GetTopicConstant'].retry,
                    default_timeout=self._method_configs['GetTopicConstant']
                    .timeout,
                    client_info=self._client_info,
                )

        request = topic_constant_service_pb2.GetTopicConstantRequest(
            resource_name=resource_name, )
        return self._inner_api_calls['get_topic_constant'](
            request, retry=retry, timeout=timeout, metadata=metadata)
