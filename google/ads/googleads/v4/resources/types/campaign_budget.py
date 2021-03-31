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


from google.ads.googleads.v4.enums.types import budget_delivery_method
from google.ads.googleads.v4.enums.types import budget_period
from google.ads.googleads.v4.enums.types import budget_status
from google.ads.googleads.v4.enums.types import budget_type
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.resources",
    marshal="google.ads.googleads.v4",
    manifest={"CampaignBudget",},
)


class CampaignBudget(proto.Message):
    r"""A campaign budget.

    Attributes:
        resource_name (str):
            Immutable. The resource name of the campaign budget.
            Campaign budget resource names have the form:

            ``customers/{customer_id}/campaignBudgets/{campaign_budget_id}``
        id (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The ID of the campaign budget.
            A campaign budget is created using the
            CampaignBudgetService create operation and is
            assigned a budget ID. A budget ID can be shared
            across different campaigns; the system will then
            allocate the campaign budget among different
            campaigns to get optimum results.
        name (google.protobuf.wrappers_pb2.StringValue):
            The name of the campaign budget.
            When creating a campaign budget through
            CampaignBudgetService, every explicitly shared
            campaign budget must have a non-null, non-empty
            name. Campaign budgets that are not explicitly
            shared derive their name from the attached
            campaign's name.

            The length of this string must be between 1 and
            255, inclusive, in UTF-8 bytes, (trimmed).
        amount_micros (google.protobuf.wrappers_pb2.Int64Value):
            The amount of the budget, in the local
            currency for the account. Amount is specified in
            micros, where one million is equivalent to one
            currency unit. Monthly spend is capped at 30.4
            times this amount.
        total_amount_micros (google.protobuf.wrappers_pb2.Int64Value):
            The lifetime amount of the budget, in the
            local currency for the account. Amount is
            specified in micros, where one million is
            equivalent to one currency unit.
        status (google.ads.googleads.v4.enums.types.BudgetStatusEnum.BudgetStatus):
            Output only. The status of this campaign
            budget. This field is read-only.
        delivery_method (google.ads.googleads.v4.enums.types.BudgetDeliveryMethodEnum.BudgetDeliveryMethod):
            The delivery method that determines the rate
            at which the campaign budget is spent.

            Defaults to STANDARD if unspecified in a create
            operation.
        explicitly_shared (google.protobuf.wrappers_pb2.BoolValue):
            Specifies whether the budget is explicitly
            shared. Defaults to true if unspecified in a
            create operation.
            If true, the budget was created with the purpose
            of sharing across one or more campaigns.

            If false, the budget was created with the
            intention of only being used with a single
            campaign. The budget's name and status will stay
            in sync with the campaign's name and status.
            Attempting to share the budget with a second
            campaign will result in an error.

            A non-shared budget can become an explicitly
            shared. The same operation must also assign the
            budget a name.

            A shared campaign budget can never become non-
            shared.
        reference_count (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The number of campaigns actively
            using the budget.
            This field is read-only.
        has_recommended_budget (google.protobuf.wrappers_pb2.BoolValue):
            Output only. Indicates whether there is a
            recommended budget for this campaign budget.
            This field is read-only.
        recommended_budget_amount_micros (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The recommended budget amount.
            If no recommendation is available, this will be
            set to the budget amount. Amount is specified in
            micros, where one million is equivalent to one
            currency unit.

            This field is read-only.
        period (google.ads.googleads.v4.enums.types.BudgetPeriodEnum.BudgetPeriod):
            Immutable. Period over which to spend the
            budget. Defaults to DAILY if not specified.
        recommended_budget_estimated_change_weekly_clicks (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The estimated change in weekly
            clicks if the recommended budget is applied.
            This field is read-only.
        recommended_budget_estimated_change_weekly_cost_micros (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The estimated change in weekly
            cost in micros if the recommended budget is
            applied. One million is equivalent to one
            currency unit.
            This field is read-only.
        recommended_budget_estimated_change_weekly_interactions (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The estimated change in weekly
            interactions if the recommended budget is
            applied.
            This field is read-only.
        recommended_budget_estimated_change_weekly_views (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The estimated change in weekly
            views if the recommended budget is applied.
            This field is read-only.
        type_ (google.ads.googleads.v4.enums.types.BudgetTypeEnum.BudgetType):
            Immutable. The type of the campaign budget.
    """

    resource_name = proto.Field(proto.STRING, number=1)
    id = proto.Field(proto.MESSAGE, number=3, message=wrappers.Int64Value,)
    name = proto.Field(proto.MESSAGE, number=4, message=wrappers.StringValue,)
    amount_micros = proto.Field(
        proto.MESSAGE, number=5, message=wrappers.Int64Value,
    )
    total_amount_micros = proto.Field(
        proto.MESSAGE, number=10, message=wrappers.Int64Value,
    )
    status = proto.Field(
        proto.ENUM, number=6, enum=budget_status.BudgetStatusEnum.BudgetStatus,
    )
    delivery_method = proto.Field(
        proto.ENUM,
        number=7,
        enum=budget_delivery_method.BudgetDeliveryMethodEnum.BudgetDeliveryMethod,
    )
    explicitly_shared = proto.Field(
        proto.MESSAGE, number=8, message=wrappers.BoolValue,
    )
    reference_count = proto.Field(
        proto.MESSAGE, number=9, message=wrappers.Int64Value,
    )
    has_recommended_budget = proto.Field(
        proto.MESSAGE, number=11, message=wrappers.BoolValue,
    )
    recommended_budget_amount_micros = proto.Field(
        proto.MESSAGE, number=12, message=wrappers.Int64Value,
    )
    period = proto.Field(
        proto.ENUM, number=13, enum=budget_period.BudgetPeriodEnum.BudgetPeriod,
    )
    recommended_budget_estimated_change_weekly_clicks = proto.Field(
        proto.MESSAGE, number=14, message=wrappers.Int64Value,
    )
    recommended_budget_estimated_change_weekly_cost_micros = proto.Field(
        proto.MESSAGE, number=15, message=wrappers.Int64Value,
    )
    recommended_budget_estimated_change_weekly_interactions = proto.Field(
        proto.MESSAGE, number=16, message=wrappers.Int64Value,
    )
    recommended_budget_estimated_change_weekly_views = proto.Field(
        proto.MESSAGE, number=17, message=wrappers.Int64Value,
    )
    type_ = proto.Field(
        proto.ENUM, number=18, enum=budget_type.BudgetTypeEnum.BudgetType,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
