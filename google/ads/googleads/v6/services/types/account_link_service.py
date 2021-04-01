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


from google.ads.googleads.v6.resources.types import (
    account_link as gagr_account_link,
)
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v6.services",
    marshal="google.ads.googleads.v6",
    manifest={
        "GetAccountLinkRequest",
        "CreateAccountLinkRequest",
        "CreateAccountLinkResponse",
        "MutateAccountLinkRequest",
        "AccountLinkOperation",
        "MutateAccountLinkResponse",
        "MutateAccountLinkResult",
    },
)


class GetAccountLinkRequest(proto.Message):
    r"""Request message for
    [AccountLinkService.GetAccountLink][google.ads.googleads.v6.services.AccountLinkService.GetAccountLink].

    Attributes:
        resource_name (str):
            Required. Resource name of the account link.
    """

    resource_name = proto.Field(proto.STRING, number=1)


class CreateAccountLinkRequest(proto.Message):
    r"""Request message for
    [AccountLinkService.CreateAccountLink][google.ads.googleads.v6.services.AccountLinkService.CreateAccountLink].

    Attributes:
        customer_id (str):
            Required. The ID of the customer for which
            the account link is created.
        account_link (google.ads.googleads.v6.resources.types.AccountLink):
            Required. The account link to be created.
    """

    customer_id = proto.Field(proto.STRING, number=1)
    account_link = proto.Field(
        proto.MESSAGE, number=2, message=gagr_account_link.AccountLink,
    )


class CreateAccountLinkResponse(proto.Message):
    r"""Response message for
    [AccountLinkService.CreateAccountLink][google.ads.googleads.v6.services.AccountLinkService.CreateAccountLink].

    Attributes:
        resource_name (str):
            Returned for successful operations. Resource
            name of the account link.
    """

    resource_name = proto.Field(proto.STRING, number=1)


class MutateAccountLinkRequest(proto.Message):
    r"""Request message for
    [AccountLinkService.MutateAccountLink][google.ads.googleads.v6.services.AccountLinkService.MutateAccountLink].

    Attributes:
        customer_id (str):
            Required. The ID of the customer being
            modified.
        operation (google.ads.googleads.v6.services.types.AccountLinkOperation):
            Required. The operation to perform on the
            link.
        partial_failure (bool):
            If true, successful operations will be
            carried out and invalid operations will return
            errors. If false, all operations will be carried
            out in one transaction if and only if they are
            all valid. Default is false.
        validate_only (bool):
            If true, the request is validated but not
            executed. Only errors are returned, not results.
    """

    customer_id = proto.Field(proto.STRING, number=1)
    operation = proto.Field(
        proto.MESSAGE, number=2, message="AccountLinkOperation",
    )
    partial_failure = proto.Field(proto.BOOL, number=3)
    validate_only = proto.Field(proto.BOOL, number=4)


class AccountLinkOperation(proto.Message):
    r"""A single update on an account link.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            FieldMask that determines which resource
            fields are modified in an update.
        update (google.ads.googleads.v6.resources.types.AccountLink):
            Update operation: The account link is
            expected to have a valid resource name.
        remove (str):
            Remove operation: A resource name for the account link to
            remove is expected, in this format:

            ``customers/{customer_id}/accountLinks/{account_link_id}``
    """

    update_mask = proto.Field(
        proto.MESSAGE, number=4, message=field_mask.FieldMask,
    )
    update = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="operation",
        message=gagr_account_link.AccountLink,
    )
    remove = proto.Field(proto.STRING, number=3, oneof="operation")


class MutateAccountLinkResponse(proto.Message):
    r"""Response message for account link mutate.

    Attributes:
        result (google.ads.googleads.v6.services.types.MutateAccountLinkResult):
            Result for the mutate.
    """

    result = proto.Field(
        proto.MESSAGE, number=1, message="MutateAccountLinkResult",
    )


class MutateAccountLinkResult(proto.Message):
    r"""The result for the account link mutate.

    Attributes:
        resource_name (str):
            Returned for successful operations.
    """

    resource_name = proto.Field(proto.STRING, number=1)


__all__ = tuple(sorted(__protobuf__.manifest))
