# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from __future__ import annotations


import proto  # type: ignore

from google.ads.googleads.v14.resources.types import (
    customer_sk_ad_network_conversion_value_schema,
)


__protobuf__ = proto.module(
    package="google.ads.googleads.v14.services",
    marshal="google.ads.googleads.v14",
    manifest={
        "CustomerSkAdNetworkConversionValueSchemaOperation",
        "MutateCustomerSkAdNetworkConversionValueSchemaRequest",
        "MutateCustomerSkAdNetworkConversionValueSchemaResult",
        "MutateCustomerSkAdNetworkConversionValueSchemaResponse",
    },
)


class CustomerSkAdNetworkConversionValueSchemaOperation(proto.Message):
    r"""A single update operation for a
    CustomerSkAdNetworkConversionValueSchema.

    Attributes:
        update (google.ads.googleads.v14.resources.types.CustomerSkAdNetworkConversionValueSchema):
            Update operation: The schema is expected to
            have a valid resource name.
    """

    update: customer_sk_ad_network_conversion_value_schema.CustomerSkAdNetworkConversionValueSchema = proto.Field(
        proto.MESSAGE,
        number=1,
        message=customer_sk_ad_network_conversion_value_schema.CustomerSkAdNetworkConversionValueSchema,
    )


class MutateCustomerSkAdNetworkConversionValueSchemaRequest(proto.Message):
    r"""Request message for
    [CustomerSkAdNetworkConversionValueSchemaService.MutateCustomerSkAdNetworkConversionValueSchema][google.ads.googleads.v14.services.CustomerSkAdNetworkConversionValueSchemaService.MutateCustomerSkAdNetworkConversionValueSchema].

    Attributes:
        customer_id (str):
            The ID of the customer whose shared sets are
            being modified.
        operation (google.ads.googleads.v14.services.types.CustomerSkAdNetworkConversionValueSchemaOperation):
            The operation to perform.
        validate_only (bool):
            If true, the request is validated but not
            executed. Only errors are returned, not results.
    """

    customer_id: str = proto.Field(
        proto.STRING, number=1,
    )
    operation: "CustomerSkAdNetworkConversionValueSchemaOperation" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="CustomerSkAdNetworkConversionValueSchemaOperation",
    )
    validate_only: bool = proto.Field(
        proto.BOOL, number=3,
    )


class MutateCustomerSkAdNetworkConversionValueSchemaResult(proto.Message):
    r"""The result for the CustomerSkAdNetworkConversionValueSchema
    mutate.

    Attributes:
        resource_name (str):
            Resource name of the customer that was
            modified.
        app_id (str):
            App ID of the SkanConversionValue modified.
    """

    resource_name: str = proto.Field(
        proto.STRING, number=1,
    )
    app_id: str = proto.Field(
        proto.STRING, number=2,
    )


class MutateCustomerSkAdNetworkConversionValueSchemaResponse(proto.Message):
    r"""Response message for
    MutateCustomerSkAdNetworkConversionValueSchema.

    Attributes:
        result (google.ads.googleads.v14.services.types.MutateCustomerSkAdNetworkConversionValueSchemaResult):
            All results for the mutate.
    """

    result: "MutateCustomerSkAdNetworkConversionValueSchemaResult" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="MutateCustomerSkAdNetworkConversionValueSchemaResult",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
