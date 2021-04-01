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

import proto  # type: ignore


from google.ads.googleads.v6.resources.types import billing_setup


__protobuf__ = proto.module(
    package="google.ads.googleads.v6.services",
    marshal="google.ads.googleads.v6",
    manifest={
        "GetBillingSetupRequest",
        "MutateBillingSetupRequest",
        "BillingSetupOperation",
        "MutateBillingSetupResponse",
        "MutateBillingSetupResult",
    },
)


class GetBillingSetupRequest(proto.Message):
    r"""Request message for
    [BillingSetupService.GetBillingSetup][google.ads.googleads.v6.services.BillingSetupService.GetBillingSetup].

    Attributes:
        resource_name (str):
            Required. The resource name of the billing
            setup to fetch.
    """

    resource_name = proto.Field(proto.STRING, number=1)


class MutateBillingSetupRequest(proto.Message):
    r"""Request message for billing setup mutate operations.

    Attributes:
        customer_id (str):
            Required. Id of the customer to apply the
            billing setup mutate operation to.
        operation (google.ads.googleads.v6.services.types.BillingSetupOperation):
            Required. The operation to perform.
    """

    customer_id = proto.Field(proto.STRING, number=1)
    operation = proto.Field(
        proto.MESSAGE, number=2, message="BillingSetupOperation",
    )


class BillingSetupOperation(proto.Message):
    r"""A single operation on a billing setup, which describes the
    cancellation of an existing billing setup.

    Attributes:
        create (google.ads.googleads.v6.resources.types.BillingSetup):
            Creates a billing setup. No resource name is
            expected for the new billing setup.
        remove (str):
            Resource name of the billing setup to remove. A setup cannot
            be removed unless it is in a pending state or its scheduled
            start time is in the future. The resource name looks like
            ``customers/{customer_id}/billingSetups/{billing_id}``.
    """

    create = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="operation",
        message=billing_setup.BillingSetup,
    )
    remove = proto.Field(proto.STRING, number=1, oneof="operation")


class MutateBillingSetupResponse(proto.Message):
    r"""Response message for a billing setup operation.

    Attributes:
        result (google.ads.googleads.v6.services.types.MutateBillingSetupResult):
            A result that identifies the resource
            affected by the mutate request.
    """

    result = proto.Field(
        proto.MESSAGE, number=1, message="MutateBillingSetupResult",
    )


class MutateBillingSetupResult(proto.Message):
    r"""Result for a single billing setup mutate.

    Attributes:
        resource_name (str):
            Returned for successful operations.
    """

    resource_name = proto.Field(proto.STRING, number=1)


__all__ = tuple(sorted(__protobuf__.manifest))
