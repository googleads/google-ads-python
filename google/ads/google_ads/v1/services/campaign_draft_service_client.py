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
"""Accesses the google.ads.googleads.v1.services CampaignDraftService API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.operation
import google.api_core.operations_v1
import google.api_core.page_iterator
import google.api_core.path_template

from google.ads.google_ads.v1.services import campaign_draft_service_client_config
from google.ads.google_ads.v1.services.transports import campaign_draft_service_grpc_transport
from google.ads.google_ads.v1.proto.services import campaign_draft_service_pb2
from google.protobuf import empty_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'google-ads', ).version


class CampaignDraftServiceClient(object):
    """Service to manage campaign drafts."""

    SERVICE_ADDRESS = 'googleads.googleapis.com:443'
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = 'google.ads.googleads.v1.services.CampaignDraftService'

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
            CampaignDraftServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(
            filename)
        kwargs['credentials'] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def campaign_draft_path(cls, customer, campaign_draft):
        """Return a fully-qualified campaign_draft string."""
        return google.api_core.path_template.expand(
            'customers/{customer}/campaignDrafts/{campaign_draft}',
            customer=customer,
            campaign_draft=campaign_draft,
        )

    def __init__(self,
                 transport=None,
                 channel=None,
                 credentials=None,
                 client_config=None,
                 client_info=None):
        """Constructor.

        Args:
            transport (Union[~.CampaignDraftServiceGrpcTransport,
                    Callable[[~.Credentials, type], ~.CampaignDraftServiceGrpcTransport]): A transport
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
            client_config = campaign_draft_service_client_config.config

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
                    default_class=campaign_draft_service_grpc_transport.
                    CampaignDraftServiceGrpcTransport,
                )
            else:
                if credentials:
                    raise ValueError(
                        'Received both a transport instance and '
                        'credentials; these are mutually exclusive.')
                self.transport = transport
        else:
            self.transport = campaign_draft_service_grpc_transport.CampaignDraftServiceGrpcTransport(
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
    def get_campaign_draft(self,
                           resource_name,
                           retry=google.api_core.gapic_v1.method.DEFAULT,
                           timeout=google.api_core.gapic_v1.method.DEFAULT,
                           metadata=None):
        """
        Returns the requested campaign draft in full detail.

        Args:
            resource_name (str): The resource name of the campaign draft to fetch.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.ads.googleads_v1.types.CampaignDraft` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'get_campaign_draft' not in self._inner_api_calls:
            self._inner_api_calls[
                'get_campaign_draft'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.get_campaign_draft,
                    default_retry=self._method_configs['GetCampaignDraft'].
                    retry,
                    default_timeout=self._method_configs['GetCampaignDraft'].
                    timeout,
                    client_info=self._client_info,
                )

        request = campaign_draft_service_pb2.GetCampaignDraftRequest(
            resource_name=resource_name, )
        return self._inner_api_calls['get_campaign_draft'](
            request, retry=retry, timeout=timeout, metadata=metadata)

    def mutate_campaign_drafts(self,
                               customer_id,
                               operations,
                               partial_failure=None,
                               validate_only=None,
                               retry=google.api_core.gapic_v1.method.DEFAULT,
                               timeout=google.api_core.gapic_v1.method.DEFAULT,
                               metadata=None):
        """
        Creates, updates, or removes campaign drafts. Operation statuses are
        returned.

        Args:
            customer_id (str): The ID of the customer whose campaign drafts are being modified.
            operations (list[Union[dict, ~google.ads.googleads_v1.types.CampaignDraftOperation]]): The list of operations to perform on individual campaign drafts.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.ads.googleads_v1.types.CampaignDraftOperation`
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
            A :class:`~google.ads.googleads_v1.types.MutateCampaignDraftsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'mutate_campaign_drafts' not in self._inner_api_calls:
            self._inner_api_calls[
                'mutate_campaign_drafts'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.mutate_campaign_drafts,
                    default_retry=self._method_configs['MutateCampaignDrafts'].
                    retry,
                    default_timeout=self.
                    _method_configs['MutateCampaignDrafts'].timeout,
                    client_info=self._client_info,
                )

        request = campaign_draft_service_pb2.MutateCampaignDraftsRequest(
            customer_id=customer_id,
            operations=operations,
            partial_failure=partial_failure,
            validate_only=validate_only,
        )
        return self._inner_api_calls['mutate_campaign_drafts'](
            request, retry=retry, timeout=timeout, metadata=metadata)

    def promote_campaign_draft(self,
                               campaign_draft,
                               retry=google.api_core.gapic_v1.method.DEFAULT,
                               timeout=google.api_core.gapic_v1.method.DEFAULT,
                               metadata=None):
        """
        Promotes the changes in a draft back to the base campaign.

        This method returns a Long Running Operation (LRO) indicating if the
        Promote is done. Use [Operations.GetOperation] to poll the LRO until it
        is done. Only a done status is returned in the response. See the status
        in the Campaign Draft resource to determine if the promotion was
        successful. If the LRO failed, use
        ``CampaignDraftService.ListCampaignDraftAsyncErrors`` to view the list
        of error reasons.

        Args:
            campaign_draft (str): The resource name of the campaign draft to promote.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.ads.googleads_v1.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'promote_campaign_draft' not in self._inner_api_calls:
            self._inner_api_calls[
                'promote_campaign_draft'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.promote_campaign_draft,
                    default_retry=self._method_configs['PromoteCampaignDraft'].
                    retry,
                    default_timeout=self.
                    _method_configs['PromoteCampaignDraft'].timeout,
                    client_info=self._client_info,
                )

        request = campaign_draft_service_pb2.PromoteCampaignDraftRequest(
            campaign_draft=campaign_draft, )
        operation = self._inner_api_calls['promote_campaign_draft'](
            request, retry=retry, timeout=timeout, metadata=metadata)
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            empty_pb2.Empty,
            metadata_type=empty_pb2.Empty,
        )

    def list_campaign_draft_async_errors(
            self,
            resource_name,
            page_size=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Returns all errors that occurred during CampaignDraft promote. Throws an
        error if called before campaign draft is promoted.
        Supports standard list paging.

        Args:
            resource_name (str): The name of the campaign draft from which to retrieve the async errors.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
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
            is an iterable of :class:`~google.ads.googleads_v1.types.Status` instances.
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
        if 'list_campaign_draft_async_errors' not in self._inner_api_calls:
            self._inner_api_calls[
                'list_campaign_draft_async_errors'] = google.api_core.gapic_v1.method.wrap_method(
                    self.transport.list_campaign_draft_async_errors,
                    default_retry=self.
                    _method_configs['ListCampaignDraftAsyncErrors'].retry,
                    default_timeout=self.
                    _method_configs['ListCampaignDraftAsyncErrors'].timeout,
                    client_info=self._client_info,
                )

        request = campaign_draft_service_pb2.ListCampaignDraftAsyncErrorsRequest(
            resource_name=resource_name,
            page_size=page_size,
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls['list_campaign_draft_async_errors'],
                retry=retry,
                timeout=timeout,
                metadata=metadata),
            request=request,
            items_field='errors',
            request_token_field='page_token',
            response_token_field='next_page_token',
        )
        return iterator
