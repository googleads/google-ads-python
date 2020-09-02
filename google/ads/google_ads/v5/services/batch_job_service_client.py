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

"""Accesses the google.ads.googleads.v5.services BatchJobService API."""

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

from google.ads.google_ads.v5.services import batch_job_service_client_config
from google.ads.google_ads.v5.services.transports import batch_job_service_grpc_transport
from google.ads.google_ads.v5.proto.resources import batch_job_pb2
from google.ads.google_ads.v5.proto.services import batch_job_service_pb2
from google.protobuf import empty_pb2



_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'google-ads',
).version


class BatchJobServiceClient(object):
    """Service to manage batch jobs."""

    SERVICE_ADDRESS = 'googleads.googleapis.com:443'
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = 'google.ads.googleads.v5.services.BatchJobService'


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
            BatchJobServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(
            filename)
        kwargs['credentials'] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file


    @classmethod
    def batch_job_path(cls, customer, batch_job):
        """Return a fully-qualified batch_job string."""
        return google.api_core.path_template.expand(
            'customers/{customer}/batchJobs/{batch_job}',
            customer=customer,
            batch_job=batch_job,
        )

    def __init__(self, transport=None, channel=None, credentials=None,
            client_config=None, client_info=None, client_options=None):
        """Constructor.

        Args:
            transport (Union[~.BatchJobServiceGrpcTransport,
                    Callable[[~.Credentials, type], ~.BatchJobServiceGrpcTransport]): A transport
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
            client_config = batch_job_service_client_config.config

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
                    default_class=batch_job_service_grpc_transport.BatchJobServiceGrpcTransport,
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
            self.transport = batch_job_service_grpc_transport.BatchJobServiceGrpcTransport(
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
    def mutate_batch_job(
            self,
            customer_id,
            operation_,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Mutates a batch job.

        Args:
            customer_id (str): Required. The ID of the customer for which to create a batch job.
            operation_ (Union[dict, ~google.ads.googleads_v5.types.BatchJobOperation]): Required. The operation to perform on an individual batch job.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.ads.googleads_v5.types.BatchJobOperation`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.ads.googleads_v5.types.MutateBatchJobResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'mutate_batch_job' not in self._inner_api_calls:
            self._inner_api_calls['mutate_batch_job'] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.mutate_batch_job,
                default_retry=self._method_configs['MutateBatchJob'].retry,
                default_timeout=self._method_configs['MutateBatchJob'].timeout,
                client_info=self._client_info,
            )

        request = batch_job_service_pb2.MutateBatchJobRequest(
            customer_id=customer_id,
            operation=operation_,
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

        return self._inner_api_calls['mutate_batch_job'](request, retry=retry, timeout=timeout, metadata=metadata)

    def get_batch_job(
            self,
            resource_name,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Returns the batch job.

        Args:
            resource_name (str): Required. The resource name of the batch job to get.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.ads.googleads_v5.types.BatchJob` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'get_batch_job' not in self._inner_api_calls:
            self._inner_api_calls['get_batch_job'] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_batch_job,
                default_retry=self._method_configs['GetBatchJob'].retry,
                default_timeout=self._method_configs['GetBatchJob'].timeout,
                client_info=self._client_info,
            )

        request = batch_job_service_pb2.GetBatchJobRequest(
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

        return self._inner_api_calls['get_batch_job'](request, retry=retry, timeout=timeout, metadata=metadata)

    def list_batch_job_results(
            self,
            resource_name,
            page_size=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Returns the results of the batch job. The job must be done.
        Supports standard list paging.

        Args:
            resource_name (str): Required. The resource name of the batch job whose results are being listed.
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
            An iterable of :class:`~google.ads.googleads_v5.types.BatchJobResult` instances.
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
        if 'list_batch_job_results' not in self._inner_api_calls:
            self._inner_api_calls['list_batch_job_results'] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_batch_job_results,
                default_retry=self._method_configs['ListBatchJobResults'].retry,
                default_timeout=self._method_configs['ListBatchJobResults'].timeout,
                client_info=self._client_info,
            )

        request = batch_job_service_pb2.ListBatchJobResultsRequest(
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
            method=functools.partial(self._inner_api_calls['list_batch_job_results'], retry=retry, timeout=timeout, metadata=metadata),
            request=request,
            items_field='results',
            request_token_field='page_token',
            response_token_field='next_page_token',
        )
        return iterator

    def run_batch_job(
            self,
            resource_name,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Runs the batch job.

        The Operation.metadata field type is BatchJobMetadata. When finished, the
        long running operation will not contain errors or a response. Instead, use
        ListBatchJobResults to get the results of the job.

        Args:
            resource_name (str): Required. The resource name of the BatchJob to run.
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
        if 'run_batch_job' not in self._inner_api_calls:
            self._inner_api_calls['run_batch_job'] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.run_batch_job,
                default_retry=self._method_configs['RunBatchJob'].retry,
                default_timeout=self._method_configs['RunBatchJob'].timeout,
                client_info=self._client_info,
            )

        request = batch_job_service_pb2.RunBatchJobRequest(
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

        operation = self._inner_api_calls['run_batch_job'](request, retry=retry, timeout=timeout, metadata=metadata)
        return google.api_core.operation.from_gapic(
            operation,
            self.transport._operations_client,
            empty_pb2.Empty,
            metadata_type=batch_job_pb2.BatchJob.BatchJobMetadata,
        )

    def add_batch_job_operations(
            self,
            resource_name,
            sequence_token,
            mutate_operations,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Add operations to the batch job.

        Args:
            resource_name (str): Required. The resource name of the batch job.
            sequence_token (str): A token used to enforce sequencing.

                The first AddBatchJobOperations request for a batch job should not set
                sequence\_token. Subsequent requests must set sequence\_token to the
                value of next\_sequence\_token received in the previous
                AddBatchJobOperations response.
            mutate_operations (list[Union[dict, ~google.ads.googleads_v5.types.MutateOperation]]): Required. The list of mutates being added.

                Operations can use negative integers as temp ids to signify dependencies
                between entities created in this batch job. For example, a customer with
                id = 1234 can create a campaign and an ad group in that same campaign by
                creating a campaign in the first operation with the resource name
                explicitly set to "customers/1234/campaigns/-1", and creating an ad group
                in the second operation with the campaign field also set to
                "customers/1234/campaigns/-1".

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.ads.googleads_v5.types.MutateOperation`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.ads.googleads_v5.types.AddBatchJobOperationsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'add_batch_job_operations' not in self._inner_api_calls:
            self._inner_api_calls['add_batch_job_operations'] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.add_batch_job_operations,
                default_retry=self._method_configs['AddBatchJobOperations'].retry,
                default_timeout=self._method_configs['AddBatchJobOperations'].timeout,
                client_info=self._client_info,
            )

        request = batch_job_service_pb2.AddBatchJobOperationsRequest(
            resource_name=resource_name,
            sequence_token=sequence_token,
            mutate_operations=mutate_operations,
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

        return self._inner_api_calls['add_batch_job_operations'](request, retry=retry, timeout=timeout, metadata=metadata)
