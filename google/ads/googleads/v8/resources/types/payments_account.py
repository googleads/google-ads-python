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


__protobuf__ = proto.module(
    package="google.ads.googleads.v8.resources",
    marshal="google.ads.googleads.v8",
    manifest={"PaymentsAccount",},
)


class PaymentsAccount(proto.Message):
    r"""A payments account, which can be used to set up billing for
    an Ads customer.

    Attributes:
        resource_name (str):
            Output only. The resource name of the payments account.
            PaymentsAccount resource names have the form:

            ``customers/{customer_id}/paymentsAccounts/{payments_account_id}``
        payments_account_id (str):
            Output only. A 16 digit ID used to identify a
            payments account.
        name (str):
            Output only. The name of the payments
            account.
        currency_code (str):
            Output only. The currency code of the
            payments account. A subset of the currency codes
            derived from the ISO 4217 standard is supported.
        payments_profile_id (str):
            Output only. A 12 digit ID used to identify
            the payments profile associated with the
            payments account.
        secondary_payments_profile_id (str):
            Output only. A secondary payments profile ID
            present in uncommon situations, e.g. when a
            sequential liability agreement has been
            arranged.
        paying_manager_customer (str):
            Output only. Paying manager of this payment
            account.
    """

    resource_name = proto.Field(proto.STRING, number=1,)
    payments_account_id = proto.Field(proto.STRING, number=8, optional=True,)
    name = proto.Field(proto.STRING, number=9, optional=True,)
    currency_code = proto.Field(proto.STRING, number=10, optional=True,)
    payments_profile_id = proto.Field(proto.STRING, number=11, optional=True,)
    secondary_payments_profile_id = proto.Field(
        proto.STRING, number=12, optional=True,
    )
    paying_manager_customer = proto.Field(
        proto.STRING, number=13, optional=True,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
