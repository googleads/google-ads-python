# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import logging as std_logging
from typing import Callable, MutableSequence, Optional, Sequence, Tuple, Union

from google.ads.googleads.v18 import gapic_version as package_version

from google.api_core.client_options import ClientOptions
from google.api_core import gapic_v1
from google.api_core import retry_async as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore


try:
    OptionalRetry = Union[
        retries.AsyncRetry, gapic_v1.method._MethodDefault, None
    ]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.AsyncRetry, object, None]  # type: ignore

from google.ads.googleads.v18.services.types import reach_plan_service
from .transports.base import ReachPlanServiceTransport, DEFAULT_CLIENT_INFO
from .client import ReachPlanServiceClient

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = std_logging.getLogger(__name__)


class ReachPlanServiceAsyncClient:
    """Reach Plan Service gives users information about audience
    size that can be reached through advertisement on YouTube. In
    particular, GenerateReachForecast provides estimated number of
    people of specified demographics that can be reached by an ad in
    a given market by a campaign of certain duration with a defined
    budget.
    """

    _client: ReachPlanServiceClient

    # Copy defaults from the synchronous client for use here.
    # Note: DEFAULT_ENDPOINT is deprecated. Use _DEFAULT_ENDPOINT_TEMPLATE instead.
    DEFAULT_ENDPOINT = ReachPlanServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = ReachPlanServiceClient.DEFAULT_MTLS_ENDPOINT
    _DEFAULT_ENDPOINT_TEMPLATE = (
        ReachPlanServiceClient._DEFAULT_ENDPOINT_TEMPLATE
    )
    _DEFAULT_UNIVERSE = ReachPlanServiceClient._DEFAULT_UNIVERSE

    common_billing_account_path = staticmethod(
        ReachPlanServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        ReachPlanServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(ReachPlanServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        ReachPlanServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        ReachPlanServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        ReachPlanServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(
        ReachPlanServiceClient.common_project_path
    )
    parse_common_project_path = staticmethod(
        ReachPlanServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(
        ReachPlanServiceClient.common_location_path
    )
    parse_common_location_path = staticmethod(
        ReachPlanServiceClient.parse_common_location_path
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            ReachPlanServiceAsyncClient: The constructed client.
        """
        return ReachPlanServiceClient.from_service_account_info.__func__(ReachPlanServiceAsyncClient, info, *args, **kwargs)  # type: ignore

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            ReachPlanServiceAsyncClient: The constructed client.
        """
        return ReachPlanServiceClient.from_service_account_file.__func__(ReachPlanServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[ClientOptions] = None
    ):
        """Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variable is "never", use the default API
        endpoint; otherwise if client cert source exists, use the default mTLS endpoint, otherwise
        use the default API endpoint.

        More details can be found at https://google.aip.dev/auth/4114.

        Args:
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. Only the `api_endpoint` and `client_cert_source` properties may be used
                in this method.

        Returns:
            Tuple[str, Callable[[], Tuple[bytes, bytes]]]: returns the API endpoint and the
                client cert source to use.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If any errors happen.
        """
        return ReachPlanServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> ReachPlanServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            ReachPlanServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    @property
    def api_endpoint(self):
        """Return the API endpoint used by the client instance.

        Returns:
            str: The API endpoint used by the client instance.
        """
        return self._client._api_endpoint

    @property
    def universe_domain(self) -> str:
        """Return the universe domain used by the client instance.

        Returns:
            str: The universe domain used
                by the client instance.
        """
        return self._client._universe_domain

    get_transport_class = ReachPlanServiceClient.get_transport_class

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Optional[
            Union[
                str,
                ReachPlanServiceTransport,
                Callable[..., ReachPlanServiceTransport],
            ]
        ] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the reach plan service async client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str,ReachPlanServiceTransport,Callable[..., ReachPlanServiceTransport]]]):
                The transport to use, or a Callable that constructs and returns a new transport to use.
                If a Callable is given, it will be called with the same set of initialization
                arguments as used in the ReachPlanServiceTransport constructor.
                If set to None, a transport is chosen automatically.
            client_options (Optional[Union[google.api_core.client_options.ClientOptions, dict]]):
                Custom options for the client.

                1. The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client when ``transport`` is
                not explicitly provided. Only if this property is not set and
                ``transport`` was not explicitly provided, the endpoint is
                determined by the GOOGLE_API_USE_MTLS_ENDPOINT environment
                variable, which have one of the following values:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto-switch to the
                default mTLS endpoint if client certificate is present; this is
                the default value).

                2. If the GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide a client certificate for mTLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

                3. The ``universe_domain`` property can be used to override the
                default "googleapis.com" universe. Note that ``api_endpoint``
                property still takes precedence; and ``universe_domain`` is
                currently not supported for mTLS.

            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client = ReachPlanServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

        if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
            std_logging.DEBUG
        ):  # pragma: NO COVER
            _LOGGER.debug(
                "Created client `google.ads.googleads.v18.services.ReachPlanServiceAsyncClient`.",
                extra=(
                    {
                        "serviceName": "google.ads.googleads.v18.services.ReachPlanService",
                        "universeDomain": getattr(
                            self._client._transport._credentials,
                            "universe_domain",
                            "",
                        ),
                        "credentialsType": f"{type(self._client._transport._credentials).__module__}.{type(self._client._transport._credentials).__qualname__}",
                        "credentialsInfo": getattr(
                            self.transport._credentials,
                            "get_cred_info",
                            lambda: None,
                        )(),
                    }
                    if hasattr(self._client._transport, "_credentials")
                    else {
                        "serviceName": "google.ads.googleads.v18.services.ReachPlanService",
                        "credentialsType": None,
                    }
                ),
            )

    async def list_plannable_locations(
        self,
        request: Optional[
            Union[reach_plan_service.ListPlannableLocationsRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> reach_plan_service.ListPlannableLocationsResponse:
        r"""Returns the list of plannable locations (for example,
        countries).

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `HeaderError <>`__
        `InternalError <>`__ `QuotaError <>`__ `RequestError <>`__

        Args:
            request (Optional[Union[google.ads.googleads.v18.services.types.ListPlannableLocationsRequest, dict]]):
                The request object. Request message for
                [ReachPlanService.ListPlannableLocations][google.ads.googleads.v18.services.ReachPlanService.ListPlannableLocations].
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.ads.googleads.v18.services.types.ListPlannableLocationsResponse:
                The list of plannable locations.
        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, reach_plan_service.ListPlannableLocationsRequest
        ):
            request = reach_plan_service.ListPlannableLocationsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.list_plannable_locations
        ]

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_plannable_products(
        self,
        request: Optional[
            Union[reach_plan_service.ListPlannableProductsRequest, dict]
        ] = None,
        *,
        plannable_location_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> reach_plan_service.ListPlannableProductsResponse:
        r"""Returns the list of per-location plannable YouTube ad formats
        with allowed targeting.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `HeaderError <>`__
        `InternalError <>`__ `QuotaError <>`__ `RequestError <>`__

        Args:
            request (Optional[Union[google.ads.googleads.v18.services.types.ListPlannableProductsRequest, dict]]):
                The request object. Request to list available products in
                a given location.
            plannable_location_id (:class:`str`):
                Required. The ID of the selected location for planning.
                To list the available plannable location IDs use
                [ReachPlanService.ListPlannableLocations][google.ads.googleads.v18.services.ReachPlanService.ListPlannableLocations].

                This corresponds to the ``plannable_location_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.ads.googleads.v18.services.types.ListPlannableProductsResponse:
                A response with all available
                products.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [plannable_location_id]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, reach_plan_service.ListPlannableProductsRequest
        ):
            request = reach_plan_service.ListPlannableProductsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if plannable_location_id is not None:
            request.plannable_location_id = plannable_location_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.list_plannable_products
        ]

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def generate_reach_forecast(
        self,
        request: Optional[
            Union[reach_plan_service.GenerateReachForecastRequest, dict]
        ] = None,
        *,
        customer_id: Optional[str] = None,
        campaign_duration: Optional[reach_plan_service.CampaignDuration] = None,
        planned_products: Optional[
            MutableSequence[reach_plan_service.PlannedProduct]
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> reach_plan_service.GenerateReachForecastResponse:
        r"""Generates a reach forecast for a given targeting / product mix.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `FieldError <>`__ `HeaderError <>`__
        `InternalError <>`__ `QuotaError <>`__ `RangeError <>`__
        `ReachPlanError <>`__ `RequestError <>`__

        Args:
            request (Optional[Union[google.ads.googleads.v18.services.types.GenerateReachForecastRequest, dict]]):
                The request object. Request message for
                [ReachPlanService.GenerateReachForecast][google.ads.googleads.v18.services.ReachPlanService.GenerateReachForecast].
            customer_id (:class:`str`):
                Required. The ID of the customer.
                This corresponds to the ``customer_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            campaign_duration (:class:`google.ads.googleads.v18.services.types.CampaignDuration`):
                Required. Campaign duration.
                This corresponds to the ``campaign_duration`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            planned_products (:class:`MutableSequence[google.ads.googleads.v18.services.types.PlannedProduct]`):
                Required. The products to be
                forecast. The max number of allowed
                planned products is 15.

                This corresponds to the ``planned_products`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, Union[str, bytes]]]): Key/value pairs which should be
                sent along with the request as metadata. Normally, each value must be of type `str`,
                but for metadata keys ending with the suffix `-bin`, the corresponding values must
                be of type `bytes`.

        Returns:
            google.ads.googleads.v18.services.types.GenerateReachForecastResponse:
                Response message containing the
                generated reach curve.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [customer_id, campaign_duration, planned_products]
        has_flattened_params = (
            len([param for param in flattened_params if param is not None]) > 0
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, reach_plan_service.GenerateReachForecastRequest
        ):
            request = reach_plan_service.GenerateReachForecastRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if customer_id is not None:
            request.customer_id = customer_id
        if campaign_duration is not None:
            request.campaign_duration = campaign_duration
        if planned_products:
            request.planned_products.extend(planned_products)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.generate_reach_forecast
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("customer_id", request.customer_id),)
            ),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def __aenter__(self) -> "ReachPlanServiceAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("ReachPlanServiceAsyncClient",)
