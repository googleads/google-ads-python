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

"""Accesses the google.ads.googleads.v5.services CampaignExperimentService API."""

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
import google.api_core.operation
import google.api_core.operations_v1
import google.api_core.page_iterator
import google.api_core.path_template

from google.ads.google_ads.v5.services import campaign_experiment_service_client_config
from google.ads.google_ads.v5.services.transports import campaign_experiment_service_grpc_transport
from google.ads.google_ads.v5.proto.services import campaign_experiment_service_pb2
from google.protobuf import empty_pb2



_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'google-ads',
).version


class CampaignExperimentServiceClient(object):
    """
    CampaignExperimentService manages the life cycle of campaign experiments.
    It is used to create new experiments from drafts, modify experiment
    properties, promote changes in an experiment back to its base campaign,
    graduate experiments into new stand-alone campaigns, and to remove an
    experiment.

    An experiment consists of two variants or arms - the base campaign and the
    experiment campaign, directing a fixed share of traffic to each arm.
    A campaign experiment is created from a draft of changes to the base campaign
    and will be a snapshot of changes in the draft at the time of creation.
    """

    SERVICE_ADDRESS = 'googleads.googleapis.com:443'
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = 'google.ads.googleads.v5.services.CampaignExperimentService'


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
            CampaignExperimentServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(
            filename)
        kwargs['credentials'] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file


    @classmethod
    def campaign_experiment_path(cls, customer, campaign_experiment):
        """Return a fully-qualified campaign_experiment string."""
        return google.api_core.path_template.expand(
            'customers/{customer}/campaignExperiments/{campaign_experiment}',
            customer=customer,
            campaign_experiment=campaign_experiment,
        )

    def __init__(self, transport=None, channel=None, credentials=None,
            client_config=None, client_info=None, client_options=None):
        """Constructor.

        Args:
            transport (Union[~.CampaignExperimentServiceGrpcTransport,
                    Callable[[~.Credentials, type], ~.CampaignExperimentServiceGrpcTransport]): A transport
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
            client_config = campaign_experiment_service_client_config.config

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
                    default_class=campaign_experiment_service_grpc_transport.CampaignExperimentServiceGrpcTransport,
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
            self.transport = campaign_experiment_service_grpc_transport.CampaignExperimentServiceGrpcTransport(
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
    def get_campaign_experiment(
            self,
            resource_name,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Returns the requested campaign experiment in full detail.

        Args:
            resource_name (str): Required. The resource name of the campaign experiment to fetch.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.ads.googleads_v5.types.CampaignExperiment` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'get_campaign_experiment' not in self._inner_api_calls:
            self._inner_api_calls['get_campaign_experiment'] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_campaign_experiment,
                default_retry=self._method_configs['GetCampaignExperiment'].retry,
                default_timeout=self._method_configs['GetCampaignExperiment'].timeout,
                client_info=self._client_info,
            )

        request = campaign_experiment_service_pb2.GetCampaignExperimentRequest(
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

        return self._inner_api_calls['get_campaign_experiment'](request, retry=retry, timeout=timeout, metadata=metadata)

    def create_campaign_experiment(
            self,
            customer_id,
            campaign_experiment,
            validate_only=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Creates a campaign experiment based on a campaign draft. The draft campaign
        will be forked into a real campaign (called the experiment campaign) that
        will begin serving ads if successfully created.

        The campaign experiment is created immediately with status INITIALIZING.
        This method return a long running operation that tracks the forking of the
        draft campaign. If the forking fails, a list of errors can be retrieved
        using the ListCampaignExperimentAsyncErrors method. The operation's
        metadata will be a StringValue containing the resource name of the created
        campaign experiment.

        Args:
            customer_id (str): Required. The ID of the customer whose campaign experiment is being created.
            campaign_experiment (Union[dict, ~google.ads.googleads_v5.types.CampaignExperiment]): Required. The campaign experiment to be created.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.ads.googleads_v5.types.CampaignExperiment`
            validate_only (bool): If true, the request is validated but not executed. Only errors are
                returned, not results.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.ads.googleads_v5.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'create_campaign_experiment' not in self._inner_api_calls:
            self._inner_api_calls['create_campaign_experiment'] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_campaign_experiment,
                default_retry=self._method_configs['CreateCampaignExperiment'].retry,
                default_timeout=self._method_configs['CreateCampaignExperiment'].timeout,
                client_info=self._client_info,
            )

        request = campaign_experiment_service_pb2.CreateCampaignExperimentRequest(
            customer_id=customer_id,
            campaign_experiment=campaign_experiment,
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

        operation = self._inner_api_calls['create_campaign_experiment'](request, retry=retry, timeout=timeout, metadata=metadata)
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            empty_pb2.Empty,
            metadata_type=campaign_experiment_service_pb2.CreateCampaignExperimentMetadata,
        )

    def mutate_campaign_experiments(
            self,
            customer_id,
            operations,
            partial_failure=None,
            validate_only=None,
            response_content_type=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Updates campaign experiments. Operation statuses are returned.

        Args:
            customer_id (str): Required. The ID of the customer whose campaign experiments are being modified.
            operations (list[Union[dict, ~google.ads.googleads_v5.types.CampaignExperimentOperation]]): Required. The list of operations to perform on individual campaign experiments.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.ads.googleads_v5.types.CampaignExperimentOperation`
            partial_failure (bool): If true, successful operations will be carried out and invalid
                operations will return errors. If false, all operations will be carried
                out in one transaction if and only if they are all valid.
                Default is false.
            validate_only (bool): If true, the request is validated but not executed. Only errors are
                returned, not results.
            response_content_type (~google.ads.googleads_v5.types.ResponseContentType): The response content type setting. Determines whether the mutable resource
                or just the resource name should be returned post mutation.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.ads.googleads_v5.types.MutateCampaignExperimentsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'mutate_campaign_experiments' not in self._inner_api_calls:
            self._inner_api_calls['mutate_campaign_experiments'] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.mutate_campaign_experiments,
                default_retry=self._method_configs['MutateCampaignExperiments'].retry,
                default_timeout=self._method_configs['MutateCampaignExperiments'].timeout,
                client_info=self._client_info,
            )

        request = campaign_experiment_service_pb2.MutateCampaignExperimentsRequest(
            customer_id=customer_id,
            operations=operations,
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

        return self._inner_api_calls['mutate_campaign_experiments'](request, retry=retry, timeout=timeout, metadata=metadata)

    def graduate_campaign_experiment(
            self,
            campaign_experiment,
            campaign_budget,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Graduates a campaign experiment to a full campaign. The base and experiment
        campaigns will start running independently with their own budgets.

        Args:
            campaign_experiment (str): Required. The resource name of the campaign experiment to graduate.
            campaign_budget (str): Required. Resource name of the budget to attach to the campaign graduated from the
                experiment.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.ads.googleads_v5.types.GraduateCampaignExperimentResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'graduate_campaign_experiment' not in self._inner_api_calls:
            self._inner_api_calls['graduate_campaign_experiment'] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.graduate_campaign_experiment,
                default_retry=self._method_configs['GraduateCampaignExperiment'].retry,
                default_timeout=self._method_configs['GraduateCampaignExperiment'].timeout,
                client_info=self._client_info,
            )

        request = campaign_experiment_service_pb2.GraduateCampaignExperimentRequest(
            campaign_experiment=campaign_experiment,
            campaign_budget=campaign_budget,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [('campaign_experiment', campaign_experiment)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(routing_header)
            metadata.append(routing_metadata)

        return self._inner_api_calls['graduate_campaign_experiment'](request, retry=retry, timeout=timeout, metadata=metadata)

    def promote_campaign_experiment(
            self,
            campaign_experiment,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Promotes the changes in a experiment campaign back to the base campaign.

        The campaign experiment is updated immediately with status PROMOTING.
        This method return a long running operation that tracks the promoting of
        the experiment campaign. If the promoting fails, a list of errors can be
        retrieved using the ListCampaignExperimentAsyncErrors method.

        Args:
            campaign_experiment (str): Required. The resource name of the campaign experiment to promote.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.ads.googleads_v5.types._OperationFuture` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'promote_campaign_experiment' not in self._inner_api_calls:
            self._inner_api_calls['promote_campaign_experiment'] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.promote_campaign_experiment,
                default_retry=self._method_configs['PromoteCampaignExperiment'].retry,
                default_timeout=self._method_configs['PromoteCampaignExperiment'].timeout,
                client_info=self._client_info,
            )

        request = campaign_experiment_service_pb2.PromoteCampaignExperimentRequest(
            campaign_experiment=campaign_experiment,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [('campaign_experiment', campaign_experiment)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(routing_header)
            metadata.append(routing_metadata)

        operation = self._inner_api_calls['promote_campaign_experiment'](request, retry=retry, timeout=timeout, metadata=metadata)
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            empty_pb2.Empty,
            metadata_type=empty_pb2.Empty,
        )

    def end_campaign_experiment(
            self,
            campaign_experiment,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Immediately ends a campaign experiment, changing the experiment's scheduled
        end date and without waiting for end of day. End date is updated to be the
        time of the request.

        Args:
            campaign_experiment (str): Required. The resource name of the campaign experiment to end.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'end_campaign_experiment' not in self._inner_api_calls:
            self._inner_api_calls['end_campaign_experiment'] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.end_campaign_experiment,
                default_retry=self._method_configs['EndCampaignExperiment'].retry,
                default_timeout=self._method_configs['EndCampaignExperiment'].timeout,
                client_info=self._client_info,
            )

        request = campaign_experiment_service_pb2.EndCampaignExperimentRequest(
            campaign_experiment=campaign_experiment,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [('campaign_experiment', campaign_experiment)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(routing_header)
            metadata.append(routing_metadata)

        self._inner_api_calls['end_campaign_experiment'](request, retry=retry, timeout=timeout, metadata=metadata)

    def list_campaign_experiment_async_errors(
            self,
            resource_name,
            page_size=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Returns all errors that occurred during CampaignExperiment create or
        promote (whichever occurred last).
        Supports standard list paging.

        Args:
            resource_name (str): Required. The name of the campaign experiment from which to retrieve the async
                errors.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
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
            An iterable of :class:`~google.ads.googleads_v5.types.Status` instances.
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
        if 'list_campaign_experiment_async_errors' not in self._inner_api_calls:
            self._inner_api_calls['list_campaign_experiment_async_errors'] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_campaign_experiment_async_errors,
                default_retry=self._method_configs['ListCampaignExperimentAsyncErrors'].retry,
                default_timeout=self._method_configs['ListCampaignExperimentAsyncErrors'].timeout,
                client_info=self._client_info,
            )

        request = campaign_experiment_service_pb2.ListCampaignExperimentAsyncErrorsRequest(
            resource_name=resource_name,
            page_size=page_size,
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

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(self._inner_api_calls['list_campaign_experiment_async_errors'], retry=retry, timeout=timeout, metadata=metadata),
            request=request,
            items_field='errors',
            request_token_field='page_token',
            response_token_field='next_page_token',
        )
        return iterator
