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


__protobuf__ = proto.module(
    package="google.ads.googleads.v25.common",
    marshal="google.ads.googleads.v25",
    manifest={
        "CustomerLifecycleOptimizationValueSettings",
    },
)


class CustomerLifecycleOptimizationValueSettings(proto.Message):
    r"""Lifecycle goal optimization value settings.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        additional_value (float):
            Incremental conversion value.

            This field is a member of `oneof`_ ``value_adjustment``.
        value_multiplier (float):
            Conversion value multiplier.

            This field is a member of `oneof`_ ``value_adjustment``.
        additional_high_lifetime_value (float):
            Incremental high lifetime conversion value.

            This field is a member of `oneof`_ ``high_lifetime_value_adjustment``.
        high_lifetime_value_multiplier (float):
            High lifetime conversion value multiplier.

            This field is a member of `oneof`_ ``high_lifetime_value_adjustment``.
    """

    additional_value: float = proto.Field(
        proto.DOUBLE,
        number=3,
        oneof="value_adjustment",
    )
    value_multiplier: float = proto.Field(
        proto.DOUBLE,
        number=4,
        oneof="value_adjustment",
    )
    additional_high_lifetime_value: float = proto.Field(
        proto.DOUBLE,
        number=5,
        oneof="high_lifetime_value_adjustment",
    )
    high_lifetime_value_multiplier: float = proto.Field(
        proto.DOUBLE,
        number=6,
        oneof="high_lifetime_value_adjustment",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
