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

from google.ads.googleads.v25.enums.types import lift_measurement_flight_status
from google.ads.googleads.v25.enums.types import lift_metric_type
from google.ads.googleads.v25.enums.types import (
    survey_lift_flight_target_response_mode,
)


__protobuf__ = proto.module(
    package="google.ads.googleads.v25.resources",
    marshal="google.ads.googleads.v25",
    manifest={
        "LiftMeasurementFlight",
        "LiftMeasurementFlightSurveyLiftInfo",
        "LiftMeasurementFlightSurveyLiftMeasurement",
    },
)


class LiftMeasurementFlight(proto.Message):
    r"""A brand lift measurement flight.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        resource_name (str):
            Immutable. The resource name of the lift measurement flight.
            Lift measurement flight resource names have the form:

            ``customers/{customer_id}/liftMeasurementFlights/{lift_measurement_configuration_id}~{flight_id}``
        lift_measurement_config_id (int):
            Output only. The lift measurement
            configuration ID.

            This field is a member of `oneof`_ ``_lift_measurement_config_id``.
        lift_measurement_flight_id (int):
            Output only. The lift measurement flight ID.

            This field is a member of `oneof`_ ``_lift_measurement_flight_id``.
        survey_lift_info (google.ads.googleads.v25.resources.types.LiftMeasurementFlightSurveyLiftInfo):
            Output only. Flight configuration specific to
            Survey Lift.

            This field is a member of `oneof`_ ``_survey_lift_info``.
        name (str):
            Output only. The name of the lift measurement
            flight.

            This field is a member of `oneof`_ ``_name``.
        status (google.ads.googleads.v25.enums.types.LiftMeasurementFlightStatusEnum.LiftMeasurementFlightStatus):
            Output only. The status of the lift
            measurement flight.
        lift_type (google.ads.googleads.v25.enums.types.LiftMetricTypeEnum.LiftMetricType):
            Output only. The lift type measured during
            this flight.
        survey_lift_measurement (google.ads.googleads.v25.resources.types.LiftMeasurementFlightSurveyLiftMeasurement):
            Output only. Data about survey lift
            measurement.

            This field is a member of `oneof`_ ``_survey_lift_measurement``.
        start_date (str):
            Output only. The start date of the lift
            measurement flight in the customer's time zone.

            Format: YYYY-MM-DD

            This field is a member of `oneof`_ ``_start_date``.
        end_date (str):
            Output only. The end date of the lift
            measurement flight in the customer's time zone.

            Format: YYYY-MM-DD

            This field is a member of `oneof`_ ``_end_date``.
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
    lift_measurement_flight_id: int = proto.Field(
        proto.INT64,
        number=3,
        optional=True,
    )
    survey_lift_info: "LiftMeasurementFlightSurveyLiftInfo" = proto.Field(
        proto.MESSAGE,
        number=4,
        optional=True,
        message="LiftMeasurementFlightSurveyLiftInfo",
    )
    name: str = proto.Field(
        proto.STRING,
        number=5,
        optional=True,
    )
    status: (
        lift_measurement_flight_status.LiftMeasurementFlightStatusEnum.LiftMeasurementFlightStatus
    ) = proto.Field(
        proto.ENUM,
        number=8,
        enum=lift_measurement_flight_status.LiftMeasurementFlightStatusEnum.LiftMeasurementFlightStatus,
    )
    lift_type: lift_metric_type.LiftMetricTypeEnum.LiftMetricType = proto.Field(
        proto.ENUM,
        number=9,
        enum=lift_metric_type.LiftMetricTypeEnum.LiftMetricType,
    )
    survey_lift_measurement: "LiftMeasurementFlightSurveyLiftMeasurement" = (
        proto.Field(
            proto.MESSAGE,
            number=12,
            optional=True,
            message="LiftMeasurementFlightSurveyLiftMeasurement",
        )
    )
    start_date: str = proto.Field(
        proto.STRING,
        number=14,
        optional=True,
    )
    end_date: str = proto.Field(
        proto.STRING,
        number=15,
        optional=True,
    )


class LiftMeasurementFlightSurveyLiftInfo(proto.Message):
    r"""Survey Lift specific flight configuration.

    Attributes:
        target_response_mode (google.ads.googleads.v25.enums.types.SurveyLiftFlightTargetResponseModeEnum.SurveyLiftFlightTargetResponseMode):
            Output only. The target response mode that
            will be used to collect survey responses.
    """

    target_response_mode: (
        survey_lift_flight_target_response_mode.SurveyLiftFlightTargetResponseModeEnum.SurveyLiftFlightTargetResponseMode
    ) = proto.Field(
        proto.ENUM,
        number=1,
        enum=survey_lift_flight_target_response_mode.SurveyLiftFlightTargetResponseModeEnum.SurveyLiftFlightTargetResponseMode,
    )


class LiftMeasurementFlightSurveyLiftMeasurement(proto.Message):
    r"""Survey Lift measurement info.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        response_collection_ratio_micros (int):
            Output only. The ratio of target survey
            responses that have been collected so far.
            Expressed in micros: 0 = 0%, 1000000 = 100%.

            This field is a member of `oneof`_ ``_response_collection_ratio_micros``.
        min_survey_response_date (str):
            Output only. The earliest date in which
            survey responses were recorded.

            This field is a member of `oneof`_ ``_min_survey_response_date``.
        max_survey_response_date (str):
            Output only. The latest date in which survey
            responses were recorded.

            This field is a member of `oneof`_ ``_max_survey_response_date``.
    """

    response_collection_ratio_micros: int = proto.Field(
        proto.INT64,
        number=1,
        optional=True,
    )
    min_survey_response_date: str = proto.Field(
        proto.STRING,
        number=2,
        optional=True,
    )
    max_survey_response_date: str = proto.Field(
        proto.STRING,
        number=3,
        optional=True,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
