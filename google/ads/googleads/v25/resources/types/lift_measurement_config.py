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

from typing import MutableSequence

import proto  # type: ignore

from google.ads.googleads.v25.enums.types import brand_lift_measurement_type
from google.ads.googleads.v25.enums.types import survey_intended_action
from google.ads.googleads.v25.enums.types import survey_subject_type


__protobuf__ = proto.module(
    package="google.ads.googleads.v25.resources",
    marshal="google.ads.googleads.v25",
    manifest={
        "LiftMeasurementConfig",
    },
)


class LiftMeasurementConfig(proto.Message):
    r"""A Lift Measurement Configuration (LMC), which is a lift
    study. This groups all associated Brand Lift, Conversion Lift,
    and Search Lift measurements.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        resource_name (str):
            Immutable. The resource name of the lift measurement config.
            Lift measurement config resource names have the form:

            ``customers/{customer_id}/liftMeasurementConfigs/{lift_measurement_config_id}``
        lift_measurement_config_id (int):
            Output only. The unique identifier for the
            Lift Measurement Configuration (LMC).
        name (str):
            Output only. The name of the lift study.
        conversion_actions (MutableSequence[str]):
            Output only. The list of conversion action
            resource names associated with this lift
            measurement configuration.
        campaigns (MutableSequence[str]):
            Output only. The resource names of campaigns
            associated with this lift measurement config.
            These are the ones currently linked, not
            historical.
        survey_language (str):
            Output only. The survey language.
        single_measurement_question_set (google.ads.googleads.v25.resources.types.LiftMeasurementConfig.SingleMeasurementQuestionSet):
            Output only. The single measurement question
            set.
        conversion_lift_holdback_ratio_micros (int):
            Output only. The holdback ratio for
            Conversion Lift.

            This field is a member of `oneof`_ ``_conversion_lift_holdback_ratio_micros``.
    """

    class SingleMeasurementQuestionSet(proto.Message):
        r"""A single measurement question set for a survey.

        Attributes:
            question_text_intended_action (google.ads.googleads.v25.enums.types.SurveyIntendedActionEnum.SurveyIntendedAction):
                Output only. The intended action for the
                question text.
            question_text_subject_type (google.ads.googleads.v25.enums.types.SurveySubjectTypeEnum.SurveySubjectType):
                Output only. The subject type for the
                question text.
            question_measurements (MutableSequence[google.ads.googleads.v25.enums.types.BrandLiftMeasurementTypeEnum.BrandLiftMeasurementType]):
                Output only. The brand measurement types for
                the question.
            advertiser_preferred_choice (str):
                Output only. The advertiser preferred choice.
            competitor_choices (MutableSequence[str]):
                Output only. The competitor choices.
        """

        question_text_intended_action: (
            survey_intended_action.SurveyIntendedActionEnum.SurveyIntendedAction
        ) = proto.Field(
            proto.ENUM,
            number=1,
            enum=survey_intended_action.SurveyIntendedActionEnum.SurveyIntendedAction,
        )
        question_text_subject_type: (
            survey_subject_type.SurveySubjectTypeEnum.SurveySubjectType
        ) = proto.Field(
            proto.ENUM,
            number=2,
            enum=survey_subject_type.SurveySubjectTypeEnum.SurveySubjectType,
        )
        question_measurements: MutableSequence[
            brand_lift_measurement_type.BrandLiftMeasurementTypeEnum.BrandLiftMeasurementType
        ] = proto.RepeatedField(
            proto.ENUM,
            number=3,
            enum=brand_lift_measurement_type.BrandLiftMeasurementTypeEnum.BrandLiftMeasurementType,
        )
        advertiser_preferred_choice: str = proto.Field(
            proto.STRING,
            number=4,
        )
        competitor_choices: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=5,
        )

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    lift_measurement_config_id: int = proto.Field(
        proto.INT64,
        number=2,
    )
    name: str = proto.Field(
        proto.STRING,
        number=3,
    )
    conversion_actions: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=4,
    )
    campaigns: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=5,
    )
    survey_language: str = proto.Field(
        proto.STRING,
        number=7,
    )
    single_measurement_question_set: SingleMeasurementQuestionSet = proto.Field(
        proto.MESSAGE,
        number=9,
        message=SingleMeasurementQuestionSet,
    )
    conversion_lift_holdback_ratio_micros: int = proto.Field(
        proto.INT64,
        number=10,
        optional=True,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
