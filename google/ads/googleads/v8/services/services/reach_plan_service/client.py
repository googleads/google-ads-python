# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
from collections import OrderedDict
from distutils import util
import os
import re
from typing import Dict, Optional, Sequence, Tuple, Type, Union

from google.api_core import client_options as client_options_lib  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.ads.googleads.v8.services.types import reach_plan_service
from .transports.base import ReachPlanServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import ReachPlanServiceGrpcTransport


class ReachPlanServiceClientMeta(type):
    """Metaclass for the ReachPlanService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[ReachPlanServiceTransport]]
    _transport_registry["grpc"] = ReachPlanServiceGrpcTransport

    def get_transport_class(
        cls, label: str = None,
    ) -> Type[ReachPlanServiceTransport]:
        """Return an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class ReachPlanServiceClient(metaclass=ReachPlanServiceClientMeta):
    """Reach Plan Service gives users information about audience
    size that can be reached through advertisement on YouTube. In
    particular, GenerateReachForecast provides estimated number of
    people of specified demographics that can be reached by an ad in
    a given market by a campaign of certain duration with a defined
    budget.
    """

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Convert api endpoint to mTLS endpoint.
        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    DEFAULT_ENDPOINT = "googleads.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            ReachPlanServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_info(
            info
        )
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

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
            ReachPlanServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(
            filename
        )
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> ReachPlanServiceTransport:
        """Return the transport used by the client instance.

        Returns:
            ReachPlanServiceTransport: The transport used by the client instance.
        """
        return self._transport

    @staticmethod
    def common_billing_account_path(billing_account: str,) -> str:
        """Return a fully-qualified billing_account string."""
        return "billingAccounts/{billing_account}".format(
            billing_account=billing_account,
        )

    @staticmethod
    def parse_common_billing_account_path(path: str) -> Dict[str, str]:
        """Parse a billing_account path into its component segments."""
        m = re.match(r"^billingAccounts/(?P<billing_account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_folder_path(folder: str,) -> str:
        """Return a fully-qualified folder string."""
        return "folders/{folder}".format(folder=folder,)

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(organization: str,) -> str:
        """Return a fully-qualified organization string."""
        return "organizations/{organization}".format(organization=organization,)

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(project: str,) -> str:
        """Return a fully-qualified project string."""
        return "projects/{project}".format(project=project,)

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(project: str, location: str,) -> str:
        """Return a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(
            project=project, location=location,
        )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str, str]:
        """Parse a location path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path
        )
        return m.groupdict() if m else {}

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, ReachPlanServiceTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the reach plan service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.ReachPlanServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. It won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = client_options_lib.from_dict(client_options)
        if client_options is None:
            client_options = client_options_lib.ClientOptions()

        # Create SSL credentials for mutual TLS if needed.
        use_client_cert = bool(
            util.strtobool(
                os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false")
            )
        )

        ssl_credentials = None
        is_mtls = False
        if use_client_cert:
            if client_options.client_cert_source:
                import grpc  # type: ignore

                cert, key = client_options.client_cert_source()
                ssl_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )
                is_mtls = True
            else:
                creds = SslCredentials()
                is_mtls = creds.is_mtls
                ssl_credentials = creds.ssl_credentials if is_mtls else None

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        else:
            use_mtls_env = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
            if use_mtls_env == "never":
                api_endpoint = self.DEFAULT_ENDPOINT
            elif use_mtls_env == "always":
                api_endpoint = self.DEFAULT_MTLS_ENDPOINT
            elif use_mtls_env == "auto":
                api_endpoint = (
                    self.DEFAULT_MTLS_ENDPOINT
                    if is_mtls
                    else self.DEFAULT_ENDPOINT
                )
            else:
                raise MutualTLSChannelError(
                    "Unsupported GOOGLE_API_USE_MTLS_ENDPOINT value. Accepted values: never, auto, always"
                )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, ReachPlanServiceTransport):
            # transport is a ReachPlanServiceTransport instance.
            if credentials:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            self._transport = transport
        elif isinstance(transport, str):
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials, host=self.DEFAULT_ENDPOINT
            )
        else:
            self._transport = ReachPlanServiceGrpcTransport(
                credentials=credentials,
                host=api_endpoint,
                ssl_channel_credentials=ssl_credentials,
                client_info=client_info,
            )

    def list_plannable_locations(
        self,
        request: reach_plan_service.ListPlannableLocationsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> reach_plan_service.ListPlannableLocationsResponse:
        r"""Returns the list of plannable locations (for example, countries
        & DMAs).

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `HeaderError <>`__
        `InternalError <>`__ `QuotaError <>`__ `RequestError <>`__

        Args:
            request (:class:`google.ads.googleads.v8.services.types.ListPlannableLocationsRequest`):
                The request object. Request message for
                [ReachPlanService.ListPlannableLocations][google.ads.googleads.v8.services.ReachPlanService.ListPlannableLocations].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.ads.googleads.v8.services.types.ListPlannableLocationsResponse:
                The list of plannable locations.
        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a reach_plan_service.ListPlannableLocationsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, reach_plan_service.ListPlannableLocationsRequest
        ):
            request = reach_plan_service.ListPlannableLocationsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_plannable_locations
        ]

        # Send the request.
        response = rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_plannable_products(
        self,
        request: reach_plan_service.ListPlannableProductsRequest = None,
        *,
        plannable_location_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> reach_plan_service.ListPlannableProductsResponse:
        r"""Returns the list of per-location plannable YouTube ad formats
        with allowed targeting.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `HeaderError <>`__
        `InternalError <>`__ `QuotaError <>`__ `RequestError <>`__

        Args:
            request (:class:`google.ads.googleads.v8.services.types.ListPlannableProductsRequest`):
                The request object. Request to list available products
                in a given location.
            plannable_location_id (:class:`str`):
                Required. The ID of the selected
                location for planning. To list the
                available plannable location ids use
                ListPlannableLocations.

                This corresponds to the ``plannable_location_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.ads.googleads.v8.services.types.ListPlannableProductsResponse:
                A response with all available
                products.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([plannable_location_id]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a reach_plan_service.ListPlannableProductsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
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
        rpc = self._transport._wrapped_methods[
            self._transport.list_plannable_products
        ]

        # Send the request.
        response = rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

        # Done; return the response.
        return response

    def generate_product_mix_ideas(
        self,
        request: reach_plan_service.GenerateProductMixIdeasRequest = None,
        *,
        customer_id: str = None,
        plannable_location_id: str = None,
        currency_code: str = None,
        budget_micros: int = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> reach_plan_service.GenerateProductMixIdeasResponse:
        r"""Generates a product mix ideas given a set of preferences. This
        method helps the advertiser to obtain a good mix of ad formats
        and budget allocations based on its preferences.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `HeaderError <>`__
        `InternalError <>`__ `QuotaError <>`__ `ReachPlanError <>`__
        `RequestError <>`__

        Args:
            request (:class:`google.ads.googleads.v8.services.types.GenerateProductMixIdeasRequest`):
                The request object. Request message for
                [ReachPlanService.GenerateProductMixIdeas][google.ads.googleads.v8.services.ReachPlanService.GenerateProductMixIdeas].
            customer_id (:class:`str`):
                Required. The ID of the customer.
                This corresponds to the ``customer_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            plannable_location_id (:class:`str`):
                Required. The ID of the location,
                this is one of the ids returned by
                ListPlannableLocations.

                This corresponds to the ``plannable_location_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            currency_code (:class:`str`):
                Required. Currency code.
                Three-character ISO 4217 currency code.

                This corresponds to the ``currency_code`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            budget_micros (:class:`int`):
                Required. Total budget.
                Amount in micros. One million is
                equivalent to one unit.

                This corresponds to the ``budget_micros`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.ads.googleads.v8.services.types.GenerateProductMixIdeasResponse:
                The suggested product mix.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any(
            [customer_id, plannable_location_id, currency_code, budget_micros]
        ):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a reach_plan_service.GenerateProductMixIdeasRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, reach_plan_service.GenerateProductMixIdeasRequest
        ):
            request = reach_plan_service.GenerateProductMixIdeasRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if customer_id is not None:
                request.customer_id = customer_id
            if plannable_location_id is not None:
                request.plannable_location_id = plannable_location_id
            if currency_code is not None:
                request.currency_code = currency_code
            if budget_micros is not None:
                request.budget_micros = budget_micros

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.generate_product_mix_ideas
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("customer_id", request.customer_id),)
            ),
        )

        # Send the request.
        response = rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

        # Done; return the response.
        return response

    def generate_reach_forecast(
        self,
        request: reach_plan_service.GenerateReachForecastRequest = None,
        *,
        customer_id: str = None,
        campaign_duration: reach_plan_service.CampaignDuration = None,
        planned_products: Sequence[reach_plan_service.PlannedProduct] = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> reach_plan_service.GenerateReachForecastResponse:
        r"""Generates a reach forecast for a given targeting / product mix.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `FieldError <>`__ `HeaderError <>`__
        `InternalError <>`__ `QuotaError <>`__ `RangeError <>`__
        `ReachPlanError <>`__ `RequestError <>`__

        Args:
            request (:class:`google.ads.googleads.v8.services.types.GenerateReachForecastRequest`):
                The request object. Request message for
                [ReachPlanService.GenerateReachForecast][google.ads.googleads.v8.services.ReachPlanService.GenerateReachForecast].
            customer_id (:class:`str`):
                Required. The ID of the customer.
                This corresponds to the ``customer_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            campaign_duration (:class:`google.ads.googleads.v8.services.types.CampaignDuration`):
                Required. Campaign duration.
                This corresponds to the ``campaign_duration`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            planned_products (:class:`Sequence[google.ads.googleads.v8.services.types.PlannedProduct]`):
                Required. The products to be
                forecast. The max number of allowed
                planned products is 15.

                This corresponds to the ``planned_products`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.ads.googleads.v8.services.types.GenerateReachForecastResponse:
                Response message containing the
                generated reach curve.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any(
            [customer_id, campaign_duration, planned_products]
        ):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a reach_plan_service.GenerateReachForecastRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
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
            if planned_products is not None:
                request.planned_products = planned_products

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.generate_reach_forecast
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("customer_id", request.customer_id),)
            ),
        )

        # Send the request.
        response = rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

        # Done; return the response.
        return response


__all__ = ("ReachPlanServiceClient",)
