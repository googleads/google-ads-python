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

from google.ads.googleads.v20.common.types import metric_goal
from google.ads.googleads.v20.enums.types import async_action_status
from google.ads.googleads.v20.enums.types import experiment_status
from google.ads.googleads.v20.enums.types import experiment_type


__protobuf__ = proto.module(
    package="google.ads.googleads.v20.resources",
    marshal="google.ads.googleads.v20",
    manifest={
        "Experiment",
    },
)


class Experiment(proto.Message):
    r"""A Google ads experiment for users to experiment changes on
    multiple campaigns, compare the performance, and apply the
    effective changes.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        resource_name (str):
            Immutable. The resource name of the experiment. Experiment
            resource names have the form:

            ``customers/{customer_id}/experiments/{experiment_id}``
        experiment_id (int):
            Output only. The ID of the experiment. Read
            only.

            This field is a member of `oneof`_ ``_experiment_id``.
        name (str):
            Required. The name of the experiment. It must
            have a minimum length of 1 and maximum length of
            1024. It must be unique under a customer.
        description (str):
            The description of the experiment. It must
            have a minimum length of 1 and maximum length of
            2048.
        suffix (str):
            For system managed experiments, the
            advertiser must provide a suffix during
            construction, in the setup stage before moving
            to initiated. The suffix will be appended to the
            in-design and experiment campaign names so that
            the name is base campaign name + suffix.
        type_ (google.ads.googleads.v20.enums.types.ExperimentTypeEnum.ExperimentType):
            Required. The product/feature that uses this
            experiment.
        status (google.ads.googleads.v20.enums.types.ExperimentStatusEnum.ExperimentStatus):
            The Advertiser-chosen status of this
            experiment.
        start_date (str):
            Date when the experiment starts. By default,
            the experiment starts now or on the campaign's
            start date, whichever is later. If this field is
            set, then the experiment starts at the beginning
            of the specified date in the customer's time
            zone.

            Format: YYYY-MM-DD
            Example: 2019-03-14

            This field is a member of `oneof`_ ``_start_date``.
        end_date (str):
            Date when the experiment ends. By default,
            the experiment ends on the campaign's end date.
            If this field is set, then the experiment ends
            at the end of the specified date in the
            customer's time zone.

            Format: YYYY-MM-DD
            Example: 2019-04-18

            This field is a member of `oneof`_ ``_end_date``.
        goals (MutableSequence[google.ads.googleads.v20.common.types.MetricGoal]):
            The goals of this experiment.
        long_running_operation (str):
            Output only. The resource name of the
            long-running operation that can be used to poll
            for completion of experiment schedule or
            promote. The most recent long running operation
            is returned.

            This field is a member of `oneof`_ ``_long_running_operation``.
        promote_status (google.ads.googleads.v20.enums.types.AsyncActionStatusEnum.AsyncActionStatus):
            Output only. The status of the experiment
            promotion process.
        sync_enabled (bool):
            Immutable. Set to true if changes to base
            campaigns should be synced to the trial
            campaigns. Any changes made directly to trial
            campaigns will be preserved. This field can only
            be set when the experiment is being created.

            This field is a member of `oneof`_ ``_sync_enabled``.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    experiment_id: int = proto.Field(
        proto.INT64,
        number=9,
        optional=True,
    )
    name: str = proto.Field(
        proto.STRING,
        number=10,
    )
    description: str = proto.Field(
        proto.STRING,
        number=11,
    )
    suffix: str = proto.Field(
        proto.STRING,
        number=12,
    )
    type_: experiment_type.ExperimentTypeEnum.ExperimentType = proto.Field(
        proto.ENUM,
        number=13,
        enum=experiment_type.ExperimentTypeEnum.ExperimentType,
    )
    status: experiment_status.ExperimentStatusEnum.ExperimentStatus = (
        proto.Field(
            proto.ENUM,
            number=14,
            enum=experiment_status.ExperimentStatusEnum.ExperimentStatus,
        )
    )
    start_date: str = proto.Field(
        proto.STRING,
        number=15,
        optional=True,
    )
    end_date: str = proto.Field(
        proto.STRING,
        number=16,
        optional=True,
    )
    goals: MutableSequence[metric_goal.MetricGoal] = proto.RepeatedField(
        proto.MESSAGE,
        number=17,
        message=metric_goal.MetricGoal,
    )
    long_running_operation: str = proto.Field(
        proto.STRING,
        number=18,
        optional=True,
    )
    promote_status: (
        async_action_status.AsyncActionStatusEnum.AsyncActionStatus
    ) = proto.Field(
        proto.ENUM,
        number=19,
        enum=async_action_status.AsyncActionStatusEnum.AsyncActionStatus,
    )
    sync_enabled: bool = proto.Field(
        proto.BOOL,
        number=20,
        optional=True,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
