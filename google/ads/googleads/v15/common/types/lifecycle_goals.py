# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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


__protobuf__ = proto.module(
    package="google.ads.googleads.v15.common",
    marshal="google.ads.googleads.v15",
    manifest={
        "LifecycleGoalValueSettings",
    },
)


class LifecycleGoalValueSettings(proto.Message):
    r"""Lifecycle goal value settings.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        value (float):
            Value of the lifecycle goal. For example, for
            customer acquisition goal, value is the
            incremental conversion value for new customers
            who are not of high value.

            This field is a member of `oneof`_ ``_value``.
        high_lifetime_value (float):
            High lifetime value of the lifecycle goal.
            For example, for customer acquisition goal, high
            lifetime value is the incremental conversion
            value for new customers who are of high value.
            High lifetime value should be greater than
            value, if set.
            In current stage, high lifetime value feature is
            in beta and this field is read-only.

            This field is a member of `oneof`_ ``_high_lifetime_value``.
    """

    value: float = proto.Field(
        proto.DOUBLE,
        number=1,
        optional=True,
    )
    high_lifetime_value: float = proto.Field(
        proto.DOUBLE,
        number=2,
        optional=True,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
