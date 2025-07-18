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
from __future__ import annotations

from typing import MutableSequence

import proto  # type: ignore

from google.ads.googleads.v20.resources.types import payments_account


__protobuf__ = proto.module(
    package="google.ads.googleads.v20.services",
    marshal="google.ads.googleads.v20",
    manifest={
        "ListPaymentsAccountsRequest",
        "ListPaymentsAccountsResponse",
    },
)


class ListPaymentsAccountsRequest(proto.Message):
    r"""Request message for fetching all accessible payments
    accounts.

    Attributes:
        customer_id (str):
            Required. The ID of the customer to apply the
            PaymentsAccount list operation to.
    """

    customer_id: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListPaymentsAccountsResponse(proto.Message):
    r"""Response message for
    [PaymentsAccountService.ListPaymentsAccounts][google.ads.googleads.v20.services.PaymentsAccountService.ListPaymentsAccounts].

    Attributes:
        payments_accounts (MutableSequence[google.ads.googleads.v20.resources.types.PaymentsAccount]):
            The list of accessible payments accounts.
    """

    payments_accounts: MutableSequence[payments_account.PaymentsAccount] = (
        proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message=payments_account.PaymentsAccount,
        )
    )


__all__ = tuple(sorted(__protobuf__.manifest))
