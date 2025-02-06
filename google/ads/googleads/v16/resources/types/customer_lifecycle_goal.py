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
from __future__ import annotations

from typing import MutableSequence

import proto  # type: ignore

from google.ads.googleads.v16.common.types import lifecycle_goals


__protobuf__ = proto.module(
    package="google.ads.googleads.v16.resources",
    marshal="google.ads.googleads.v16",
    manifest={
        "CustomerLifecycleGoal",
    },
)


class CustomerLifecycleGoal(proto.Message):
    r"""Account level customer lifecycle goal settings.
    Attributes:
        resource_name (str):
            Immutable. The resource name of the customer lifecycle goal.
            Customer lifecycle resource names have the form:

            ``customers/{customer_id}/customerLifecycleGoal``
        lifecycle_goal_customer_definition_settings (google.ads.googleads.v16.resources.types.CustomerLifecycleGoal.LifecycleGoalCustomerDefinitionSettings):
            Output only. Common lifecycle goal settings
            shared among different types of lifecycle goals.
        customer_acquisition_goal_value_settings (google.ads.googleads.v16.common.types.LifecycleGoalValueSettings):
            Output only. Customer acquisition goal
            customer level value settings.
    """

    class LifecycleGoalCustomerDefinitionSettings(proto.Message):
        r"""Lifecycle goal common settings, including existing user lists
        and existing high lifetime value user lists, shared among
        different types of lifecycle goals.

        Attributes:
            existing_user_lists (MutableSequence[str]):
                Output only. User lists which represent
                existing customers.
            high_lifetime_value_user_lists (MutableSequence[str]):
                Output only. User lists which represent
                customers of high lifetime value. In current
                stage, high lifetime value feature is in beta
                and this field is read-only.
        """

        existing_user_lists: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=1,
        )
        high_lifetime_value_user_lists: MutableSequence[
            str
        ] = proto.RepeatedField(
            proto.STRING,
            number=2,
        )

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    lifecycle_goal_customer_definition_settings: LifecycleGoalCustomerDefinitionSettings = proto.Field(
        proto.MESSAGE,
        number=2,
        message=LifecycleGoalCustomerDefinitionSettings,
    )
    customer_acquisition_goal_value_settings: lifecycle_goals.LifecycleGoalValueSettings = proto.Field(
        proto.MESSAGE,
        number=3,
        message=lifecycle_goals.LifecycleGoalValueSettings,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
