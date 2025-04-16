# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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

from google.ads.googleads.v19 import gapic_version as package_version

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

from google.ads.googleads.v19.services.types import campaign_service
from google.rpc import status_pb2  # type: ignore
from .transports.base import CampaignServiceTransport, DEFAULT_CLIENT_INFO
from .client import CampaignServiceClient

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = std_logging.getLogger(__name__)


class CampaignServiceAsyncClient:
    """Service to manage campaigns."""

    _client: CampaignServiceClient

    # Copy defaults from the synchronous client for use here.
    # Note: DEFAULT_ENDPOINT is deprecated. Use _DEFAULT_ENDPOINT_TEMPLATE instead.
    DEFAULT_ENDPOINT = CampaignServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = CampaignServiceClient.DEFAULT_MTLS_ENDPOINT
    _DEFAULT_ENDPOINT_TEMPLATE = (
        CampaignServiceClient._DEFAULT_ENDPOINT_TEMPLATE
    )
    _DEFAULT_UNIVERSE = CampaignServiceClient._DEFAULT_UNIVERSE

    accessible_bidding_strategy_path = staticmethod(
        CampaignServiceClient.accessible_bidding_strategy_path
    )
    parse_accessible_bidding_strategy_path = staticmethod(
        CampaignServiceClient.parse_accessible_bidding_strategy_path
    )
    asset_set_path = staticmethod(CampaignServiceClient.asset_set_path)
    parse_asset_set_path = staticmethod(
        CampaignServiceClient.parse_asset_set_path
    )
    bidding_strategy_path = staticmethod(
        CampaignServiceClient.bidding_strategy_path
    )
    parse_bidding_strategy_path = staticmethod(
        CampaignServiceClient.parse_bidding_strategy_path
    )
    campaign_path = staticmethod(CampaignServiceClient.campaign_path)
    parse_campaign_path = staticmethod(
        CampaignServiceClient.parse_campaign_path
    )
    campaign_budget_path = staticmethod(
        CampaignServiceClient.campaign_budget_path
    )
    parse_campaign_budget_path = staticmethod(
        CampaignServiceClient.parse_campaign_budget_path
    )
    campaign_group_path = staticmethod(
        CampaignServiceClient.campaign_group_path
    )
    parse_campaign_group_path = staticmethod(
        CampaignServiceClient.parse_campaign_group_path
    )
    campaign_label_path = staticmethod(
        CampaignServiceClient.campaign_label_path
    )
    parse_campaign_label_path = staticmethod(
        CampaignServiceClient.parse_campaign_label_path
    )
    conversion_action_path = staticmethod(
        CampaignServiceClient.conversion_action_path
    )
    parse_conversion_action_path = staticmethod(
        CampaignServiceClient.parse_conversion_action_path
    )
    common_billing_account_path = staticmethod(
        CampaignServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        CampaignServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(CampaignServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        CampaignServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        CampaignServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        CampaignServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(
        CampaignServiceClient.common_project_path
    )
    parse_common_project_path = staticmethod(
        CampaignServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(
        CampaignServiceClient.common_location_path
    )
    parse_common_location_path = staticmethod(
        CampaignServiceClient.parse_common_location_path
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
            CampaignServiceAsyncClient: The constructed client.
        """
        return CampaignServiceClient.from_service_account_info.__func__(CampaignServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            CampaignServiceAsyncClient: The constructed client.
        """
        return CampaignServiceClient.from_service_account_file.__func__(CampaignServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return CampaignServiceClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> CampaignServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            CampaignServiceTransport: The transport used by the client instance.
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

    get_transport_class = CampaignServiceClient.get_transport_class

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Optional[
            Union[
                str,
                CampaignServiceTransport,
                Callable[..., CampaignServiceTransport],
            ]
        ] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the campaign service async client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str,CampaignServiceTransport,Callable[..., CampaignServiceTransport]]]):
                The transport to use, or a Callable that constructs and returns a new transport to use.
                If a Callable is given, it will be called with the same set of initialization
                arguments as used in the CampaignServiceTransport constructor.
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
        self._client = CampaignServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

        if CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
            std_logging.DEBUG
        ):  # pragma: NO COVER
            _LOGGER.debug(
                "Created client `google.ads.googleads.v19.services.CampaignServiceAsyncClient`.",
                extra=(
                    {
                        "serviceName": "google.ads.googleads.v19.services.CampaignService",
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
                        "serviceName": "google.ads.googleads.v19.services.CampaignService",
                        "credentialsType": None,
                    }
                ),
            )

    async def mutate_campaigns(
        self,
        request: Optional[
            Union[campaign_service.MutateCampaignsRequest, dict]
        ] = None,
        *,
        customer_id: Optional[str] = None,
        operations: Optional[
            MutableSequence[campaign_service.CampaignOperation]
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> campaign_service.MutateCampaignsResponse:
        r"""Creates, updates, or removes campaigns. Operation statuses are
        returned.

        List of thrown errors: `AdxError <>`__
        `AuthenticationError <>`__ `AuthorizationError <>`__
        `BiddingError <>`__ `BiddingStrategyError <>`__
        `CampaignBudgetError <>`__ `CampaignError <>`__
        `ContextError <>`__ `DatabaseError <>`__ `DateError <>`__
        `DateRangeError <>`__ `DistinctError <>`__ `FieldError <>`__
        `FieldMaskError <>`__ `HeaderError <>`__ `IdError <>`__
        `InternalError <>`__ `ListOperationError <>`__
        `MutateError <>`__ `NewResourceCreationError <>`__
        `NotAllowlistedError <>`__ `NotEmptyError <>`__ `NullError <>`__
        `OperationAccessDeniedError <>`__ `OperatorError <>`__
        `QuotaError <>`__ `RangeError <>`__ `RegionCodeError <>`__
        `RequestError <>`__ `ResourceCountLimitExceededError <>`__
        `SettingError <>`__ `SizeLimitError <>`__
        `StringFormatError <>`__ `StringLengthError <>`__
        `UrlFieldError <>`__

        Args:
            request (Optional[Union[google.ads.googleads.v19.services.types.MutateCampaignsRequest, dict]]):
                The request object. Request message for
                [CampaignService.MutateCampaigns][google.ads.googleads.v19.services.CampaignService.MutateCampaigns].
            customer_id (:class:`str`):
                Required. The ID of the customer
                whose campaigns are being modified.

                This corresponds to the ``customer_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            operations (:class:`MutableSequence[google.ads.googleads.v19.services.types.CampaignOperation]`):
                Required. The list of operations to
                perform on individual campaigns.

                This corresponds to the ``operations`` field
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
            google.ads.googleads.v19.services.types.MutateCampaignsResponse:
                Response message for campaign mutate.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [customer_id, operations]
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
        if not isinstance(request, campaign_service.MutateCampaignsRequest):
            request = campaign_service.MutateCampaignsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if customer_id is not None:
            request.customer_id = customer_id
        if operations:
            request.operations.extend(operations)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.mutate_campaigns
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

    async def enable_p_max_brand_guidelines(
        self,
        request: Optional[
            Union[campaign_service.EnablePMaxBrandGuidelinesRequest, dict]
        ] = None,
        *,
        customer_id: Optional[str] = None,
        operations: Optional[
            MutableSequence[campaign_service.EnableOperation]
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, Union[str, bytes]]] = (),
    ) -> campaign_service.EnablePMaxBrandGuidelinesResponse:
        r"""Enables Brand Guidelines for Performance Max campaigns.

        List of thrown errors: `AuthenticationError <>`__
        `AssetError <>`__ `AssetLinkError <>`__
        `AuthorizationError <>`__ `BrandGuidelinesMigrationError <>`__
        `CampaignError <>`__ `HeaderError <>`__ `InternalError <>`__
        `MutateError <>`__ `QuotaError <>`__ `RequestError <>`__
        `ResourceCountLimitExceededError <>`__

        Args:
            request (Optional[Union[google.ads.googleads.v19.services.types.EnablePMaxBrandGuidelinesRequest, dict]]):
                The request object. Request to enable Brand Guidelines
                for a Performance Max campaign.
            customer_id (:class:`str`):
                Required. The ID of the customer
                whose campaigns are being enabled.

                This corresponds to the ``customer_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            operations (:class:`MutableSequence[google.ads.googleads.v19.services.types.EnableOperation]`):
                Required. The list of individual
                campaign operations. A maximum of 10
                enable operations can be executed in a
                request.

                This corresponds to the ``operations`` field
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
            google.ads.googleads.v19.services.types.EnablePMaxBrandGuidelinesResponse:
                Brand Guidelines campaign enablement
                response.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        flattened_params = [customer_id, operations]
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
            request, campaign_service.EnablePMaxBrandGuidelinesRequest
        ):
            request = campaign_service.EnablePMaxBrandGuidelinesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if customer_id is not None:
            request.customer_id = customer_id
        if operations:
            request.operations.extend(operations)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.enable_p_max_brand_guidelines
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

    async def __aenter__(self) -> "CampaignServiceAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("CampaignServiceAsyncClient",)
