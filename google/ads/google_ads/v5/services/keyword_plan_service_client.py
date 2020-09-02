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

"""Accesses the google.ads.googleads.v5.services KeywordPlanService API."""

import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.client_options
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.path_template

from google.ads.google_ads.v5.services import keyword_plan_service_client_config
from google.ads.google_ads.v5.services.transports import keyword_plan_service_grpc_transport
from google.ads.google_ads.v5.proto.services import keyword_plan_service_pb2



_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'google-ads',
).version


class KeywordPlanServiceClient(object):
    """Service to manage keyword plans."""

    SERVICE_ADDRESS = 'googleads.googleapis.com:443'
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = 'google.ads.googleads.v5.services.KeywordPlanService'


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
            KeywordPlanServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(
            filename)
        kwargs['credentials'] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file


    @classmethod
    def keyword_plan_path(cls, customer, keyword_plan):
        """Return a fully-qualified keyword_plan string."""
        return google.api_core.path_template.expand(
            'customers/{customer}/keywordPlans/{keyword_plan}',
            customer=customer,
            keyword_plan=keyword_plan,
        )

    def __init__(self, transport=None, channel=None, credentials=None,
            client_config=None, client_info=None, client_options=None):
        """Constructor.

        Args:
            transport (Union[~.KeywordPlanServiceGrpcTransport,
                    Callable[[~.Credentials, type], ~.KeywordPlanServiceGrpcTransport]): A transport
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
            client_config = keyword_plan_service_client_config.config

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
                    default_class=keyword_plan_service_grpc_transport.KeywordPlanServiceGrpcTransport,
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
            self.transport = keyword_plan_service_grpc_transport.KeywordPlanServiceGrpcTransport(
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
    def get_keyword_plan(
            self,
            resource_name,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Returns the requested plan in full detail.

        Args:
            resource_name (str): Required. The resource name of the plan to fetch.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.ads.googleads_v5.types.KeywordPlan` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'get_keyword_plan' not in self._inner_api_calls:
            self._inner_api_calls['get_keyword_plan'] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.get_keyword_plan,
                default_retry=self._method_configs['GetKeywordPlan'].retry,
                default_timeout=self._method_configs['GetKeywordPlan'].timeout,
                client_info=self._client_info,
            )

        request = keyword_plan_service_pb2.GetKeywordPlanRequest(
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

        return self._inner_api_calls['get_keyword_plan'](request, retry=retry, timeout=timeout, metadata=metadata)

    def mutate_keyword_plans(
            self,
            customer_id,
            operations,
            partial_failure=None,
            validate_only=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Creates, updates, or removes keyword plans. Operation statuses are
        returned.

        Args:
            customer_id (str): Required. The ID of the customer whose keyword plans are being modified.
            operations (list[Union[dict, ~google.ads.googleads_v5.types.KeywordPlanOperation]]): Required. The list of operations to perform on individual keyword plans.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.ads.googleads_v5.types.KeywordPlanOperation`
            partial_failure (bool): If true, successful operations will be carried out and invalid
                operations will return errors. If false, all operations will be carried
                out in one transaction if and only if they are all valid.
                Default is false.
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
            A :class:`~google.ads.googleads_v5.types.MutateKeywordPlansResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'mutate_keyword_plans' not in self._inner_api_calls:
            self._inner_api_calls['mutate_keyword_plans'] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.mutate_keyword_plans,
                default_retry=self._method_configs['MutateKeywordPlans'].retry,
                default_timeout=self._method_configs['MutateKeywordPlans'].timeout,
                client_info=self._client_info,
            )

        request = keyword_plan_service_pb2.MutateKeywordPlansRequest(
            customer_id=customer_id,
            operations=operations,
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

        return self._inner_api_calls['mutate_keyword_plans'](request, retry=retry, timeout=timeout, metadata=metadata)

    def generate_forecast_curve(
            self,
            keyword_plan,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Returns the requested Keyword Plan forecast curve.
        Only the bidding strategy is considered for generating forecast curve.
        The bidding strategy value specified in the plan is ignored.

        To generate a forecast at a value specified in the plan, use
        KeywordPlanService.GenerateForecastMetrics.

        Args:
            keyword_plan (str): Required. The resource name of the keyword plan to be forecasted.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.ads.googleads_v5.types.GenerateForecastCurveResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'generate_forecast_curve' not in self._inner_api_calls:
            self._inner_api_calls['generate_forecast_curve'] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.generate_forecast_curve,
                default_retry=self._method_configs['GenerateForecastCurve'].retry,
                default_timeout=self._method_configs['GenerateForecastCurve'].timeout,
                client_info=self._client_info,
            )

        request = keyword_plan_service_pb2.GenerateForecastCurveRequest(
            keyword_plan=keyword_plan,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [('keyword_plan', keyword_plan)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(routing_header)
            metadata.append(routing_metadata)

        return self._inner_api_calls['generate_forecast_curve'](request, retry=retry, timeout=timeout, metadata=metadata)

    def generate_forecast_time_series(
            self,
            keyword_plan,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Returns a forecast in the form of a time series for the Keyword Plan over
        the next 52 weeks.
        (1) Forecasts closer to the current date are generally more accurate than
        further out.

        (2) The forecast reflects seasonal trends using current and
        prior traffic patterns. The forecast period of the plan is ignored.

        Args:
            keyword_plan (str): Required. The resource name of the keyword plan to be forecasted.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.ads.googleads_v5.types.GenerateForecastTimeSeriesResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'generate_forecast_time_series' not in self._inner_api_calls:
            self._inner_api_calls['generate_forecast_time_series'] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.generate_forecast_time_series,
                default_retry=self._method_configs['GenerateForecastTimeSeries'].retry,
                default_timeout=self._method_configs['GenerateForecastTimeSeries'].timeout,
                client_info=self._client_info,
            )

        request = keyword_plan_service_pb2.GenerateForecastTimeSeriesRequest(
            keyword_plan=keyword_plan,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [('keyword_plan', keyword_plan)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(routing_header)
            metadata.append(routing_metadata)

        return self._inner_api_calls['generate_forecast_time_series'](request, retry=retry, timeout=timeout, metadata=metadata)

    def generate_forecast_metrics(
            self,
            keyword_plan,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Returns the requested Keyword Plan forecasts.

        Args:
            keyword_plan (str): Required. The resource name of the keyword plan to be forecasted.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.ads.googleads_v5.types.GenerateForecastMetricsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'generate_forecast_metrics' not in self._inner_api_calls:
            self._inner_api_calls['generate_forecast_metrics'] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.generate_forecast_metrics,
                default_retry=self._method_configs['GenerateForecastMetrics'].retry,
                default_timeout=self._method_configs['GenerateForecastMetrics'].timeout,
                client_info=self._client_info,
            )

        request = keyword_plan_service_pb2.GenerateForecastMetricsRequest(
            keyword_plan=keyword_plan,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [('keyword_plan', keyword_plan)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(routing_header)
            metadata.append(routing_metadata)

        return self._inner_api_calls['generate_forecast_metrics'](request, retry=retry, timeout=timeout, metadata=metadata)

    def generate_historical_metrics(
            self,
            keyword_plan,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Returns the requested Keyword Plan historical metrics.

        Args:
            keyword_plan (str): Required. The resource name of the keyword plan of which historical metrics are
                requested.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.ads.googleads_v5.types.GenerateHistoricalMetricsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'generate_historical_metrics' not in self._inner_api_calls:
            self._inner_api_calls['generate_historical_metrics'] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.generate_historical_metrics,
                default_retry=self._method_configs['GenerateHistoricalMetrics'].retry,
                default_timeout=self._method_configs['GenerateHistoricalMetrics'].timeout,
                client_info=self._client_info,
            )

        request = keyword_plan_service_pb2.GenerateHistoricalMetricsRequest(
            keyword_plan=keyword_plan,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [('keyword_plan', keyword_plan)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(routing_header)
            metadata.append(routing_metadata)

        return self._inner_api_calls['generate_historical_metrics'](request, retry=retry, timeout=timeout, metadata=metadata)
