# -*- coding: utf-8 -*-
# Copyright 2026 Google LLC
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

from google.ads.googleads.v26.common.types import budget_network_common


__protobuf__ = proto.module(
    package="google.ads.googleads.v26.resources",
    marshal="google.ads.googleads.v26",
    manifest={
        "CustomerBudgetNetworkSetting",
    },
)


class CustomerBudgetNetworkSetting(proto.Message):
    r"""Account-level default waterfall priorities and budget caps. Applies
    to every campaign budget whose ``budget_network_settings`` is unset.

    Attributes:
        resource_name (str):
            Immutable. The resource name of the customer budget network
            setting. Customer budget network setting resource names have
            the form:

            ``customers/{customer_id}/customerBudgetNetworkSettings``
        budget_network_settings (google.ads.googleads.v26.common.types.BudgetNetworkSettings):
            Account default settings, at most one entry
            per advertising channel type.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    budget_network_settings: budget_network_common.BudgetNetworkSettings = (
        proto.Field(
            proto.MESSAGE,
            number=2,
            message=budget_network_common.BudgetNetworkSettings,
        )
    )


__all__ = tuple(sorted(__protobuf__.manifest))
