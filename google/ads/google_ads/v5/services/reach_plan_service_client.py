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

"""Accesses the google.ads.googleads.v5.services ReachPlanService API."""

import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.client_options
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers

from google.ads.google_ads.v5.services import reach_plan_service_client_config
from google.ads.google_ads.v5.services.transports import reach_plan_service_grpc_transport
from google.ads.google_ads.v5.proto.services import reach_plan_service_pb2



_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'google-ads',
).version


class ReachPlanServiceClient(object):
    """
    Reach Plan Service gives users information about audience size that can
    be reached through advertisement on YouTube. In particular,
    GenerateReachForecast provides estimated number of people of specified
    demographics that can be reached by an ad in a given market by a campaign of
    certain duration with a defined budget.
    """

    SERVICE_ADDRESS = 'googleads.googleapis.com:443'
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = 'google.ads.googleads.v5.services.ReachPlanService'


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
            ReachPlanServiceClient: The constructed client.
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
            transport (Union[~.ReachPlanServiceGrpcTransport,
                    Callable[[~.Credentials, type], ~.ReachPlanServiceGrpcTransport]): A transport
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
            client_config = reach_plan_service_client_config.config

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
                    default_class=reach_plan_service_grpc_transport.ReachPlanServiceGrpcTransport,
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
            self.transport = reach_plan_service_grpc_transport.ReachPlanServiceGrpcTransport(
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
    def list_plannable_locations(
            self,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Returns the list of plannable locations (for example, countries & DMAs).

        Args:
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.ads.googleads_v5.types.ListPlannableLocationsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'list_plannable_locations' not in self._inner_api_calls:
            self._inner_api_calls['list_plannable_locations'] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_plannable_locations,
                default_retry=self._method_configs['ListPlannableLocations'].retry,
                default_timeout=self._method_configs['ListPlannableLocations'].timeout,
                client_info=self._client_info,
            )

        request = reach_plan_service_pb2.ListPlannableLocationsRequest()
        return self._inner_api_calls['list_plannable_locations'](request, retry=retry, timeout=timeout, metadata=metadata)

    def list_plannable_products(
            self,
            plannable_location_id,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Returns the list of per-location plannable YouTube ad formats with allowed
        targeting.

        Args:
            plannable_location_id (Union[dict, ~google.ads.googleads_v5.types.StringValue]): Required. The ID of the selected location for planning. To list the available
                plannable location ids use ListPlannableLocations.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.ads.googleads_v5.types.StringValue`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.ads.googleads_v5.types.ListPlannableProductsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'list_plannable_products' not in self._inner_api_calls:
            self._inner_api_calls['list_plannable_products'] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_plannable_products,
                default_retry=self._method_configs['ListPlannableProducts'].retry,
                default_timeout=self._method_configs['ListPlannableProducts'].timeout,
                client_info=self._client_info,
            )

        request = reach_plan_service_pb2.ListPlannableProductsRequest(
            plannable_location_id=plannable_location_id,
        )
        return self._inner_api_calls['list_plannable_products'](request, retry=retry, timeout=timeout, metadata=metadata)

    def generate_product_mix_ideas(
            self,
            customer_id,
            plannable_location_id,
            currency_code,
            budget_micros,
            preferences=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Generates a product mix ideas given a set of preferences. This method
        helps the advertiser to obtain a good mix of ad formats and budget
        allocations based on its preferences.

        Args:
            customer_id (str): Required. The ID of the customer.
            plannable_location_id (Union[dict, ~google.ads.googleads_v5.types.StringValue]): Required. The ID of the location, this is one of the ids returned by
                ListPlannableLocations.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.ads.googleads_v5.types.StringValue`
            currency_code (Union[dict, ~google.ads.googleads_v5.types.StringValue]): Required. Currency code.
                Three-character ISO 4217 currency code.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.ads.googleads_v5.types.StringValue`
            budget_micros (Union[dict, ~google.ads.googleads_v5.types.Int64Value]): Required. Total budget.
                Amount in micros. One million is equivalent to one unit.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.ads.googleads_v5.types.Int64Value`
            preferences (Union[dict, ~google.ads.googleads_v5.types.Preferences]): The preferences of the suggested product mix.
                An unset preference is interpreted as all possible values are allowed,
                unless explicitly specified.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.ads.googleads_v5.types.Preferences`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.ads.googleads_v5.types.GenerateProductMixIdeasResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'generate_product_mix_ideas' not in self._inner_api_calls:
            self._inner_api_calls['generate_product_mix_ideas'] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.generate_product_mix_ideas,
                default_retry=self._method_configs['GenerateProductMixIdeas'].retry,
                default_timeout=self._method_configs['GenerateProductMixIdeas'].timeout,
                client_info=self._client_info,
            )

        request = reach_plan_service_pb2.GenerateProductMixIdeasRequest(
            customer_id=customer_id,
            plannable_location_id=plannable_location_id,
            currency_code=currency_code,
            budget_micros=budget_micros,
            preferences=preferences,
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

        return self._inner_api_calls['generate_product_mix_ideas'](request, retry=retry, timeout=timeout, metadata=metadata)

    def generate_reach_forecast(
            self,
            customer_id,
            campaign_duration,
            planned_products,
            currency_code=None,
            cookie_frequency_cap=None,
            cookie_frequency_cap_setting=None,
            min_effective_frequency=None,
            targeting=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT,
            metadata=None):
        """
        Generates a reach forecast for a given targeting / product mix.

        Args:
            customer_id (str): Required. The ID of the customer.
            campaign_duration (Union[dict, ~google.ads.googleads_v5.types.CampaignDuration]): Required. Campaign duration.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.ads.googleads_v5.types.CampaignDuration`
            planned_products (list[Union[dict, ~google.ads.googleads_v5.types.PlannedProduct]]): Required. The products to be forecast.
                The max number of allowed planned products is 15.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.ads.googleads_v5.types.PlannedProduct`
            currency_code (Union[dict, ~google.ads.googleads_v5.types.StringValue]): The currency code.
                Three-character ISO 4217 currency code.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.ads.googleads_v5.types.StringValue`
            cookie_frequency_cap (Union[dict, ~google.ads.googleads_v5.types.Int32Value]): Desired cookie frequency cap that will be applied to each planned
                product. This is equivalent to the frequency cap exposed in Google Ads
                when creating a campaign, it represents the maximum number of times an
                ad can be shown to the same user. If not specified no cap is applied.

                This field is deprecated in v4 and will eventually be removed. Please
                use cookie\_frequency\_cap\_setting instead.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.ads.googleads_v5.types.Int32Value`
            cookie_frequency_cap_setting (Union[dict, ~google.ads.googleads_v5.types.FrequencyCap]): Desired cookie frequency cap that will be applied to each planned
                product. This is equivalent to the frequency cap exposed in Google Ads
                when creating a campaign, it represents the maximum number of times an
                ad can be shown to the same user during a specified time interval. If
                not specified, no cap is applied.

                This field replaces the deprecated cookie\_frequency\_cap field.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.ads.googleads_v5.types.FrequencyCap`
            min_effective_frequency (Union[dict, ~google.ads.googleads_v5.types.Int32Value]): Desired minimum effective frequency (the number of times a person was
                exposed to the ad) for the reported reach metrics [1-10]. This won't
                affect the targeting, but just the reporting. If not specified, a
                default of 1 is applied.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.ads.googleads_v5.types.Int32Value`
            targeting (Union[dict, ~google.ads.googleads_v5.types.Targeting]): The targeting to be applied to all products selected in the product mix.

                This is planned targeting: execution details might vary based on the
                advertising product, please consult an implementation specialist.

                See specific metrics for details on how targeting affects them.

                In some cases, targeting may be overridden using the
                PlannedProduct.advanced\_product\_targeting field.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.ads.googleads_v5.types.Targeting`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.ads.googleads_v5.types.GenerateReachForecastResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if 'generate_reach_forecast' not in self._inner_api_calls:
            self._inner_api_calls['generate_reach_forecast'] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.generate_reach_forecast,
                default_retry=self._method_configs['GenerateReachForecast'].retry,
                default_timeout=self._method_configs['GenerateReachForecast'].timeout,
                client_info=self._client_info,
            )

        request = reach_plan_service_pb2.GenerateReachForecastRequest(
            customer_id=customer_id,
            campaign_duration=campaign_duration,
            planned_products=planned_products,
            currency_code=currency_code,
            cookie_frequency_cap=cookie_frequency_cap,
            cookie_frequency_cap_setting=cookie_frequency_cap_setting,
            min_effective_frequency=min_effective_frequency,
            targeting=targeting,
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

        return self._inner_api_calls['generate_reach_forecast'](request, retry=retry, timeout=timeout, metadata=metadata)
