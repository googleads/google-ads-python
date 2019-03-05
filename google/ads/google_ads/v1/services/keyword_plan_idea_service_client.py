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
"""Accesses the google.ads.googleads.v1.services KeywordPlanIdeaService API."""

import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.protobuf_helpers

from google.ads.google_ads.v1.services import keyword_plan_idea_service_client_config
from google.ads.google_ads.v1.services.transports import keyword_plan_idea_service_grpc_transport
from google.ads.google_ads.v1.proto.services import keyword_plan_idea_service_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'google-ads', ).version


class KeywordPlanIdeaServiceClient(object):
    """Service to generate keyword ideas."""

    SERVICE_ADDRESS = 'googleads.googleapis.com:443'
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = 'google.ads.googleads.v1.services.KeywordPlanIdeaService'

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
            KeywordPlanIdeaServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(
            filename)
        kwargs['credentials'] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    def __init__(self,
                 transport=None,
                 channel=None,
                 credentials=None,
                 client_config=None,
                 client_info=None):
        """Constructor.

        Args:
            transport (Union[~.KeywordPlanIdeaServiceGrpcTransport,
                    Callable[[~.Credentials, type], ~.KeywordPlanIdeaServiceGrpcTransport]): A transport
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
            warnings.warn(
                'The `client_config` argument is deprecated.',
                PendingDeprecationWarning,
                stacklevel=2)
        else:
            client_config = keyword_plan_idea_service_client_config.config

        if channel:
            warnings.warn(
                'The `channel` argument is deprecated; use '
                '`transport` instead.',
                PendingDeprecationWarning,
                stacklevel=2)

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=keyword_plan_idea_service_grpc_transport.
                    KeywordPlanIdeaServiceGrpcTransport,
                )
            else:
                if credentials:
                    raise ValueError(
                        'Received both a transport instance and '
                        'credentials; these are mutually exclusive.')
                self.transport = transport
        else:
            self.transport = keyword_plan_idea_service_grpc_transport.KeywordPlanIdeaServiceGrpcTransport(
                address=self.SERVICE_ADDRESS,
                channel=channel,
                credentials=credentials,
            )

        if client_info is None:
            client_info = google.api_core.gapic_v1.client_info.ClientInfo(
                gapic_version=_GAPIC_LIBRARY_VERSION, )
        else:
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
    def generate_keyword_ideas(self,
                               customer_id,
                               language,
                               geo_target_constants,
                               keyword_plan_network,
                               keyword_and_url_seed=None,
                               keyword_seed=None,
                               url_seed=None,
                               retry=google.api_core.gapic_v1.method.DEFAULT,
                               timeout=google.api_core.gapic_v1.method.DEFAULT,
                               metadata=None):
        """
        Returns a list of keyword ideas.

        Args:
            customer_id (str): The ID of the customer with the recommendation.
            language (Union[dict, ~google.ads.googleads_v1.types.StringValue]): The resource name of the language to target.
                Required

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.ads.googleads_v1.types.StringValue`
            geo_target_constants (list[Union[dict, ~google.ads.googleads_v1.types.StringValue]]): The resource names of the location to target.
                Max 10

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.ads.googleads_v1.types.StringValue`
            keyword_plan_network (~google.ads.googleads_v1.types.KeywordPlanNetwork): Targeting network.
            keyword_and_url_seed (Union[dict, ~google.ads.googleads_v1.types.KeywordAndUrlSeed]): A Keyword and a specific Url to generate ideas from
                e.g. cars, www.example.com/cars.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.ads.googleads_v1.types.KeywordAndUrlSeed`
            keyword_seed (Union[dict, ~google.ads.googleads_v1.types.KeywordSeed]): A Keyword or phrase to generate ideas from, e.g. cars.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.ads.googleads_v1.types.KeywordSeed`
            url_seed (Union[dict, ~google.ads.googleads_v1.types.UrlSeed]): A specific url to generate ideas from, e.g. www.example.com/cars.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.ads.googleads_v1.types.UrlSeed`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.ads.googleads_v1.types.GenerateKeywordIdeaResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'generate_keyword_ideas' not in self._inner_api_calls:
            self._inner_api_calls[
                'generate_keyword_ideas'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.generate_keyword_ideas,
                    default_retry=self._method_configs['GenerateKeywordIdeas'].
                    retry,
                    default_timeout=self.
                    _method_configs['GenerateKeywordIdeas'].timeout,
                    client_info=self._client_info,
                )

        # Sanity check: We have some fields which are mutually exclusive;
        # raise ValueError if more than one is sent.
        google.api_core.protobuf_helpers.check_oneof(
            keyword_and_url_seed=keyword_and_url_seed,
            keyword_seed=keyword_seed,
            url_seed=url_seed,
        )

        request = keyword_plan_idea_service_pb2.GenerateKeywordIdeasRequest(
            customer_id=customer_id,
            language=language,
            geo_target_constants=geo_target_constants,
            keyword_plan_network=keyword_plan_network,
            keyword_and_url_seed=keyword_and_url_seed,
            keyword_seed=keyword_seed,
            url_seed=url_seed,
        )
        return self._inner_api_calls['generate_keyword_ideas'](
            request, retry=retry, timeout=timeout, metadata=metadata)
