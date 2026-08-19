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
    package="google.ads.googleads.v25.resources",
    marshal="google.ads.googleads.v25",
    manifest={
        "LiftMeasurementCampaign",
    },
)


class LiftMeasurementCampaign(proto.Message):
    r"""A brand lift measurement by campaign.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        resource_name (str):
            Output only. The resource name of the lift measurement
            campaign. Lift measurement campaign resource names have the
            form:

            ``customers/{customer_id}/liftMeasurementCampaigns/{lift_measurement_config_id}~{campaign_id}``
        lift_measurement_config_id (int):
            Output only. The lift measurement config ID.

            This field is a member of `oneof`_ ``_lift_measurement_config_id``.
        campaign (str):
            Output only. The campaign resource name.

            This field is a member of `oneof`_ ``_campaign``.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    lift_measurement_config_id: int = proto.Field(
        proto.INT64,
        number=2,
        optional=True,
    )
    campaign: str = proto.Field(
        proto.STRING,
        number=4,
        optional=True,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
