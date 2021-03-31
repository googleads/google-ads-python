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


from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v5.resources",
    marshal="google.ads.googleads.v5",
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
        payments_account_id (google.protobuf.wrappers_pb2.StringValue):
            Output only. A 16 digit ID used to identify a
            payments account.
        name (google.protobuf.wrappers_pb2.StringValue):
            Output only. The name of the payments
            account.
        currency_code (google.protobuf.wrappers_pb2.StringValue):
            Output only. The currency code of the
            payments account. A subset of the currency codes
            derived from the ISO 4217 standard is supported.
        payments_profile_id (google.protobuf.wrappers_pb2.StringValue):
            Output only. A 12 digit ID used to identify
            the payments profile associated with the
            payments account.
        secondary_payments_profile_id (google.protobuf.wrappers_pb2.StringValue):
            Output only. A secondary payments profile ID
            present in uncommon situations, e.g. when a
            sequential liability agreement has been
            arranged.
        paying_manager_customer (google.protobuf.wrappers_pb2.StringValue):
            Output only. Paying manager of this payment
            account.
    """

    resource_name = proto.Field(proto.STRING, number=1)
    payments_account_id = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.StringValue,
    )
    name = proto.Field(proto.MESSAGE, number=3, message=wrappers.StringValue,)
    currency_code = proto.Field(
        proto.MESSAGE, number=4, message=wrappers.StringValue,
    )
    payments_profile_id = proto.Field(
        proto.MESSAGE, number=5, message=wrappers.StringValue,
    )
    secondary_payments_profile_id = proto.Field(
        proto.MESSAGE, number=6, message=wrappers.StringValue,
    )
    paying_manager_customer = proto.Field(
        proto.MESSAGE, number=7, message=wrappers.StringValue,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
