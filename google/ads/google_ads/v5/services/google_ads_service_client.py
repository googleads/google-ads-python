# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
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

"""Accesses the google.ads.googleads.v5.services GoogleAdsService API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.client_options
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.page_iterator

from google.ads.google_ads.v5.services import google_ads_service_client_config
from google.ads.google_ads.v5.services.transports import google_ads_service_grpc_transport
from google.ads.google_ads.v5.proto.services import google_ads_service_pb2



_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'google-ads',
).version


class GoogleAdsServiceClient(object):
    """Service to fetch data and metrics across resources."""

    SERVICE_ADDRESS = 'googleads.googleapis.com:443'
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = 'google.ads.googleads.v5.services.GoogleAdsService'


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
            client_config=None, client_info=None, client_options=None):
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
            client_options (Union[dict, google.api_core.client_options.ClientOptions]):
                Client options used to set user options on the client. API Endpoint
                should be set through client_options.
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

        api_endpoint = self.SERVICE_ADDRESS
        if client_options:
            if type(client_options) == dict:
                client_options = google.api_core.client_options.from_dict(client_options)
            if client_options.api_endpoint:
                api_endpoint = client_options.api_endpoint

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=google_ads_service_grpc_transport.GoogleAdsServiceGrpcTransport,
                    address=api_endpoint,
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
                address=api_endpoint,
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
            return_total_results_count=None,
            summary_row_setting=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Returns all rows that match the search query.

        Args:
            customer_id (str): Required. The ID of the customer being queried.
            query (str): Required. The query string.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            validate_only (bool): If true, the request is validated but not executed.
            return_total_results_count (bool): If true, the total number of results that match the query ignoring the
                LIMIT clause will be included in the response.
                Default is false.
            summary_row_setting (~google.ads.googleads_v5.types.SummaryRowSetting): Determines whether a summary row will be returned. By default, summary row
                is not returned. If requested, the summary row will be sent in a response
                by itself after all other query results are returned.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.ads.googleads_v5.types.GoogleAdsRow` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

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
            return_total_results_count=return_total_results_count,
            summary_row_setting=summary_row_setting,
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

    def search_stream(
            self,
            customer_id,
            query,
            summary_row_setting=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Returns all rows that match the search stream query.

        Args:
            customer_id (str): Required. The ID of the customer being queried.
            query (str): Required. The query string.
            summary_row_setting (~google.ads.googleads_v5.types.SummaryRowSetting): Determines whether a summary row will be returned. By default, summary row
                is not returned. If requested, the summary row will be sent in a response
                by itself after all other query results are returned.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            Iterable[~google.ads.googleads_v5.types.SearchGoogleAdsStreamResponse].

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'search_stream' not in self._inner_api_calls:
            self._inner_api_calls['search_stream'] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.search_stream,
                default_retry=self._method_configs['SearchStream'].retry,
                default_timeout=self._method_configs['SearchStream'].timeout,
                client_info=self._client_info,
            )

        request = google_ads_service_pb2.SearchGoogleAdsStreamRequest(
            customer_id=customer_id,
            query=query,
            summary_row_setting=summary_row_setting,
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

        return self._inner_api_calls['search_stream'](request, retry=retry, timeout=timeout, metadata=metadata)

    def mutate(
            self,
            customer_id,
            mutate_operations,
            partial_failure=None,
            validate_only=None,
            response_content_type=None,
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
            customer_id (str): Required. The ID of the customer whose resources are being modified.
            mutate_operations (list[Union[dict, ~google.ads.googleads_v5.types.MutateOperation]]): Required. The list of operations to perform on individual resources.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.ads.googleads_v5.types.MutateOperation`
            partial_failure (bool): If true, successful operations will be carried out and invalid
                operations will return errors. If false, all operations will be carried
                out in one transaction if and only if they are all valid.
                Default is false.
            validate_only (bool): If true, the request is validated but not executed. Only errors are
                returned, not results.
            response_content_type (~google.ads.googleads_v5.types.ResponseContentType): The response content type setting. Determines whether the mutable resource
                or just the resource name should be returned post mutation. The mutable
                resource will only be returned if the resource has the appropriate response
                field. E.g. MutateCampaignResult.campaign.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.ads.googleads_v5.types.MutateGoogleAdsResponse` instance.

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
            response_content_type=response_content_type,
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
