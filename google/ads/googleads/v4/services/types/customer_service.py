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


from google.ads.googleads.v4.enums.types import access_role as gage_access_role
from google.ads.googleads.v4.resources.types import customer
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.services",
    marshal="google.ads.googleads.v4",
    manifest={
        "GetCustomerRequest",
        "MutateCustomerRequest",
        "CreateCustomerClientRequest",
        "CustomerOperation",
        "CreateCustomerClientResponse",
        "MutateCustomerResponse",
        "MutateCustomerResult",
        "ListAccessibleCustomersRequest",
        "ListAccessibleCustomersResponse",
    },
)


class GetCustomerRequest(proto.Message):
    r"""Request message for
    [CustomerService.GetCustomer][google.ads.googleads.v4.services.CustomerService.GetCustomer].

    Attributes:
        resource_name (str):
            Required. The resource name of the customer
            to fetch.
    """

    resource_name = proto.Field(proto.STRING, number=1)


class MutateCustomerRequest(proto.Message):
    r"""Request message for
    [CustomerService.MutateCustomer][google.ads.googleads.v4.services.CustomerService.MutateCustomer].

    Attributes:
        customer_id (str):
            Required. The ID of the customer being
            modified.
        operation (google.ads.googleads.v4.services.types.CustomerOperation):
            Required. The operation to perform on the
            customer
        validate_only (bool):
            If true, the request is validated but not
            executed. Only errors are returned, not results.
    """

    customer_id = proto.Field(proto.STRING, number=1)
    operation = proto.Field(
        proto.MESSAGE, number=4, message="CustomerOperation",
    )
    validate_only = proto.Field(proto.BOOL, number=5)


class CreateCustomerClientRequest(proto.Message):
    r"""Request message for
    [CustomerService.CreateCustomerClient][google.ads.googleads.v4.services.CustomerService.CreateCustomerClient].

    Attributes:
        customer_id (str):
            Required. The ID of the Manager under whom
            client customer is being created.
        customer_client (google.ads.googleads.v4.resources.types.Customer):
            Required. The new client customer to create.
            The resource name on this customer will be
            ignored.
        email_address (google.protobuf.wrappers_pb2.StringValue):
            Email address of the user who should be
            invited on the created client customer.
            Accessible only to customers on the allow-list.
        access_role (google.ads.googleads.v4.enums.types.AccessRoleEnum.AccessRole):
            The proposed role of user on the created
            client customer. Accessible only to customers on
            the allow-list.
    """

    customer_id = proto.Field(proto.STRING, number=1)
    customer_client = proto.Field(
        proto.MESSAGE, number=2, message=customer.Customer,
    )
    email_address = proto.Field(
        proto.MESSAGE, number=3, message=wrappers.StringValue,
    )
    access_role = proto.Field(
        proto.ENUM, number=4, enum=gage_access_role.AccessRoleEnum.AccessRole,
    )


class CustomerOperation(proto.Message):
    r"""A single update on a customer.

    Attributes:
        update (google.ads.googleads.v4.resources.types.Customer):
            Mutate operation. Only updates are supported
            for customer.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            FieldMask that determines which resource
            fields are modified in an update.
    """

    update = proto.Field(proto.MESSAGE, number=1, message=customer.Customer,)
    update_mask = proto.Field(
        proto.MESSAGE, number=2, message=field_mask.FieldMask,
    )


class CreateCustomerClientResponse(proto.Message):
    r"""Response message for CreateCustomerClient mutate.

    Attributes:
        resource_name (str):
            The resource name of the newly created
            customer client.
        invitation_link (str):
            Link for inviting user to access the created
            customer. Accessible to allowlisted customers
            only.
    """

    resource_name = proto.Field(proto.STRING, number=2)
    invitation_link = proto.Field(proto.STRING, number=3)


class MutateCustomerResponse(proto.Message):
    r"""Response message for customer mutate.

    Attributes:
        result (google.ads.googleads.v4.services.types.MutateCustomerResult):
            Result for the mutate.
    """

    result = proto.Field(
        proto.MESSAGE, number=2, message="MutateCustomerResult",
    )


class MutateCustomerResult(proto.Message):
    r"""The result for the customer mutate.

    Attributes:
        resource_name (str):
            Returned for successful operations.
    """

    resource_name = proto.Field(proto.STRING, number=1)


class ListAccessibleCustomersRequest(proto.Message):
    r"""Request message for
    [CustomerService.ListAccessibleCustomers][google.ads.googleads.v4.services.CustomerService.ListAccessibleCustomers].
    """


class ListAccessibleCustomersResponse(proto.Message):
    r"""Response message for
    [CustomerService.ListAccessibleCustomers][google.ads.googleads.v4.services.CustomerService.ListAccessibleCustomers].

    Attributes:
        resource_names (Sequence[str]):
            Resource name of customers directly
            accessible by the user authenticating the call.
    """

    resource_names = proto.RepeatedField(proto.STRING, number=1)


__all__ = tuple(sorted(__protobuf__.manifest))
