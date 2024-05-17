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
from collections import OrderedDict
import os
import re
from typing import (
    Dict,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
)

from google.api_core import client_options as client_options_lib
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.ads.googleads.v16 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore

from google.ads.googleads.v16.enums.types import (
    advertising_channel_type as gage_advertising_channel_type,
)
from google.ads.googleads.v16.enums.types import recommendation_type
from google.ads.googleads.v16.services.types import recommendation_service
from google.rpc import status_pb2  # type: ignore
from .transports.base import RecommendationServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import RecommendationServiceGrpcTransport


class RecommendationServiceClientMeta(type):
    """Metaclass for the RecommendationService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[RecommendationServiceTransport]]
    _transport_registry["grpc"] = RecommendationServiceGrpcTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[RecommendationServiceTransport]:
        """Returns an appropriate transport class.

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


class RecommendationServiceClient(metaclass=RecommendationServiceClientMeta):
    """Service to manage recommendations."""

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Converts api endpoint to mTLS endpoint.

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
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            RecommendationServiceClient: The constructed client.
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
            RecommendationServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(
            filename
        )
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> RecommendationServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            RecommendationServiceTransport: The transport used by the client
                instance.
        """
        return self._transport

    def __enter__(self) -> "RecommendationServiceClient":
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()

    @staticmethod
    def ad_path(
        customer_id: str,
        ad_id: str,
    ) -> str:
        """Returns a fully-qualified ad string."""
        return "customers/{customer_id}/ads/{ad_id}".format(
            customer_id=customer_id,
            ad_id=ad_id,
        )

    @staticmethod
    def parse_ad_path(path: str) -> Dict[str, str]:
        """Parses a ad path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/ads/(?P<ad_id>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def ad_group_path(
        customer_id: str,
        ad_group_id: str,
    ) -> str:
        """Returns a fully-qualified ad_group string."""
        return "customers/{customer_id}/adGroups/{ad_group_id}".format(
            customer_id=customer_id,
            ad_group_id=ad_group_id,
        )

    @staticmethod
    def parse_ad_group_path(path: str) -> Dict[str, str]:
        """Parses a ad_group path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/adGroups/(?P<ad_group_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def asset_path(
        customer_id: str,
        asset_id: str,
    ) -> str:
        """Returns a fully-qualified asset string."""
        return "customers/{customer_id}/assets/{asset_id}".format(
            customer_id=customer_id,
            asset_id=asset_id,
        )

    @staticmethod
    def parse_asset_path(path: str) -> Dict[str, str]:
        """Parses a asset path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/assets/(?P<asset_id>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_path(
        customer_id: str,
        campaign_id: str,
    ) -> str:
        """Returns a fully-qualified campaign string."""
        return "customers/{customer_id}/campaigns/{campaign_id}".format(
            customer_id=customer_id,
            campaign_id=campaign_id,
        )

    @staticmethod
    def parse_campaign_path(path: str) -> Dict[str, str]:
        """Parses a campaign path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/campaigns/(?P<campaign_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def campaign_budget_path(
        customer_id: str,
        campaign_budget_id: str,
    ) -> str:
        """Returns a fully-qualified campaign_budget string."""
        return "customers/{customer_id}/campaignBudgets/{campaign_budget_id}".format(
            customer_id=customer_id,
            campaign_budget_id=campaign_budget_id,
        )

    @staticmethod
    def parse_campaign_budget_path(path: str) -> Dict[str, str]:
        """Parses a campaign_budget path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/campaignBudgets/(?P<campaign_budget_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def conversion_action_path(
        customer_id: str,
        conversion_action_id: str,
    ) -> str:
        """Returns a fully-qualified conversion_action string."""
        return "customers/{customer_id}/conversionActions/{conversion_action_id}".format(
            customer_id=customer_id,
            conversion_action_id=conversion_action_id,
        )

    @staticmethod
    def parse_conversion_action_path(path: str) -> Dict[str, str]:
        """Parses a conversion_action path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/conversionActions/(?P<conversion_action_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def recommendation_path(
        customer_id: str,
        recommendation_id: str,
    ) -> str:
        """Returns a fully-qualified recommendation string."""
        return "customers/{customer_id}/recommendations/{recommendation_id}".format(
            customer_id=customer_id,
            recommendation_id=recommendation_id,
        )

    @staticmethod
    def parse_recommendation_path(path: str) -> Dict[str, str]:
        """Parses a recommendation path into its component segments."""
        m = re.match(
            r"^customers/(?P<customer_id>.+?)/recommendations/(?P<recommendation_id>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(
        billing_account: str,
    ) -> str:
        """Returns a fully-qualified billing_account string."""
        return "billingAccounts/{billing_account}".format(
            billing_account=billing_account,
        )

    @staticmethod
    def parse_common_billing_account_path(path: str) -> Dict[str, str]:
        """Parse a billing_account path into its component segments."""
        m = re.match(r"^billingAccounts/(?P<billing_account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_folder_path(
        folder: str,
    ) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(
            folder=folder,
        )

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(
        organization: str,
    ) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(
            organization=organization,
        )

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(
        project: str,
    ) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(
            project=project,
        )

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(
        project: str,
        location: str,
    ) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(
            project=project,
            location=location,
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
        transport: Optional[Union[str, RecommendationServiceTransport]] = None,
        client_options: Optional[
            Union[client_options_lib.ClientOptions, dict]
        ] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the recommendation service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str, RecommendationServiceTransport]]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (Optional[Union[google.api_core.client_options.ClientOptions, dict]]): Custom options for the
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
        client_options = cast(client_options_lib.ClientOptions, client_options)

        # Create SSL credentials for mutual TLS if needed.
        if os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false") not in (
            "true",
            "false",
        ):
            raise ValueError(
                "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
            )
        use_client_cert = (
            os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false") == "true"
        )

        client_cert_source_func = None
        is_mtls = False
        if use_client_cert:
            if client_options.client_cert_source:
                is_mtls = True
                client_cert_source_func = client_options.client_cert_source
            else:
                is_mtls = mtls.has_default_client_cert_source()
                if is_mtls:
                    client_cert_source_func = mtls.default_client_cert_source()
                else:
                    client_cert_source_func = None

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
                    "Unsupported GOOGLE_API_USE_MTLS_ENDPOINT value. Accepted "
                    "values: never, auto, always"
                )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, RecommendationServiceTransport):
            # transport is a RecommendationServiceTransport instance.
            if credentials or client_options.credentials_file:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, provide its scopes "
                    "directly."
                )
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=api_endpoint,
                scopes=client_options.scopes,
                client_cert_source_for_mtls=client_cert_source_func,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
                always_use_jwt_access=True,
            )

    def apply_recommendation(
        self,
        request: Optional[
            Union[recommendation_service.ApplyRecommendationRequest, dict]
        ] = None,
        *,
        customer_id: Optional[str] = None,
        operations: Optional[
            MutableSequence[recommendation_service.ApplyRecommendationOperation]
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recommendation_service.ApplyRecommendationResponse:
        r"""Applies given recommendations with corresponding apply
        parameters.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `DatabaseError <>`__ `FieldError <>`__
        `HeaderError <>`__ `InternalError <>`__ `MutateError <>`__
        `QuotaError <>`__ `RecommendationError <>`__ `RequestError <>`__
        `UrlFieldError <>`__

        Args:
            request (Union[google.ads.googleads.v16.services.types.ApplyRecommendationRequest, dict, None]):
                The request object. Request message for
                [RecommendationService.ApplyRecommendation][google.ads.googleads.v16.services.RecommendationService.ApplyRecommendation].
            customer_id (str):
                Required. The ID of the customer with
                the recommendation.

                This corresponds to the ``customer_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            operations (MutableSequence[google.ads.googleads.v16.services.types.ApplyRecommendationOperation]):
                Required. The list of operations to apply
                recommendations. If partial_failure=false all
                recommendations should be of the same type There is a
                limit of 100 operations per request.

                This corresponds to the ``operations`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.ads.googleads.v16.services.types.ApplyRecommendationResponse:
                Response message for
                   [RecommendationService.ApplyRecommendation][google.ads.googleads.v16.services.RecommendationService.ApplyRecommendation].

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([customer_id, operations])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a recommendation_service.ApplyRecommendationRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, recommendation_service.ApplyRecommendationRequest
        ):
            request = recommendation_service.ApplyRecommendationRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if customer_id is not None:
                request.customer_id = customer_id
            if operations is not None:
                request.operations = operations

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.apply_recommendation
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
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def dismiss_recommendation(
        self,
        request: Optional[
            Union[recommendation_service.DismissRecommendationRequest, dict]
        ] = None,
        *,
        customer_id: Optional[str] = None,
        operations: Optional[
            MutableSequence[
                recommendation_service.DismissRecommendationRequest.DismissRecommendationOperation
            ]
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recommendation_service.DismissRecommendationResponse:
        r"""Dismisses given recommendations.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `HeaderError <>`__
        `InternalError <>`__ `QuotaError <>`__
        `RecommendationError <>`__ `RequestError <>`__

        Args:
            request (Union[google.ads.googleads.v16.services.types.DismissRecommendationRequest, dict, None]):
                The request object. Request message for
                [RecommendationService.DismissRecommendation][google.ads.googleads.v16.services.RecommendationService.DismissRecommendation].
            customer_id (str):
                Required. The ID of the customer with
                the recommendation.

                This corresponds to the ``customer_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            operations (MutableSequence[google.ads.googleads.v16.services.types.DismissRecommendationRequest.DismissRecommendationOperation]):
                Required. The list of operations to dismiss
                recommendations. If partial_failure=false all
                recommendations should be of the same type There is a
                limit of 100 operations per request.

                This corresponds to the ``operations`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.ads.googleads.v16.services.types.DismissRecommendationResponse:
                Response message for
                   [RecommendationService.DismissRecommendation][google.ads.googleads.v16.services.RecommendationService.DismissRecommendation].

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([customer_id, operations])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a recommendation_service.DismissRecommendationRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, recommendation_service.DismissRecommendationRequest
        ):
            request = recommendation_service.DismissRecommendationRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if customer_id is not None:
                request.customer_id = customer_id
            if operations is not None:
                request.operations = operations

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.dismiss_recommendation
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
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def generate_recommendations(
        self,
        request: Optional[
            Union[recommendation_service.GenerateRecommendationsRequest, dict]
        ] = None,
        *,
        customer_id: Optional[str] = None,
        recommendation_types: Optional[
            MutableSequence[
                recommendation_type.RecommendationTypeEnum.RecommendationType
            ]
        ] = None,
        advertising_channel_type: Optional[
            gage_advertising_channel_type.AdvertisingChannelTypeEnum.AdvertisingChannelType
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> recommendation_service.GenerateRecommendationsResponse:
        r"""Generates Recommendations based off the requested
        recommendation_types.

        List of thrown errors: `AuthenticationError <>`__
        `AuthorizationError <>`__ `HeaderError <>`__
        `InternalError <>`__ `QuotaError <>`__
        `RecommendationError <>`__ `RequestError <>`__

        Args:
            request (Union[google.ads.googleads.v16.services.types.GenerateRecommendationsRequest, dict, None]):
                The request object. Request message for
                [RecommendationService.GenerateRecommendations][google.ads.googleads.v16.services.RecommendationService.GenerateRecommendations].
            customer_id (str):
                Required. The ID of the customer
                generating recommendations.

                This corresponds to the ``customer_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            recommendation_types (MutableSequence[google.ads.googleads.v16.enums.types.RecommendationTypeEnum.RecommendationType]):
                Required. List of eligible recommendation_types to
                generate. If the uploaded criteria isn't sufficient to
                make a recommendation, or the campaign is already in the
                recommended state, no recommendation will be returned
                for that type. Generally, a recommendation is returned
                if all required fields for that recommendation_type are
                uploaded, but there are cases where this is still not
                sufficient.

                The following recommendation_types are supported for
                recommendation generation: KEYWORD,
                MAXIMIZE_CLICKS_OPT_IN, MAXIMIZE_CONVERSIONS_OPT_IN,
                MAXIMIZE_CONVERSION_VALUE_OPT_IN, SET_TARGET_CPA,
                SET_TARGET_ROAS, SITELINK_ASSET, TARGET_CPA_OPT_IN,
                TARGET_ROAS_OPT_IN

                This corresponds to the ``recommendation_types`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            advertising_channel_type (google.ads.googleads.v16.enums.types.AdvertisingChannelTypeEnum.AdvertisingChannelType):
                Required. Advertising channel type of the campaign. The
                following advertising_channel_types are supported for
                recommendation generation: PERFORMANCE_MAX and SEARCH

                This corresponds to the ``advertising_channel_type`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.ads.googleads.v16.services.types.GenerateRecommendationsResponse:
                Response message for
                   [RecommendationService.GenerateRecommendations][google.ads.googleads.v16.services.RecommendationService.GenerateRecommendations].

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any(
            [customer_id, recommendation_types, advertising_channel_type]
        )
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a recommendation_service.GenerateRecommendationsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, recommendation_service.GenerateRecommendationsRequest
        ):
            request = recommendation_service.GenerateRecommendationsRequest(
                request
            )
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if customer_id is not None:
                request.customer_id = customer_id
            if recommendation_types is not None:
                request.recommendation_types = recommendation_types
            if advertising_channel_type is not None:
                request.advertising_channel_type = advertising_channel_type

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.generate_recommendations
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
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("RecommendationServiceClient",)
