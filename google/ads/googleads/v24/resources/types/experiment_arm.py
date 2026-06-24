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

from google.ads.googleads.v24.enums.types import asset_field_type
from google.ads.googleads.v24.enums.types import (
    bidding_strategy_type as gage_bidding_strategy_type,
)
from google.ads.googleads.v24.enums.types import (
    experiment_asset_detail_operation,
)


__protobuf__ = proto.module(
    package="google.ads.googleads.v24.resources",
    marshal="google.ads.googleads.v24",
    manifest={
        "ExperimentArm",
    },
)


class ExperimentArm(proto.Message):
    r"""A Google ads experiment for users to experiment changes on
    multiple campaigns, compare the performance, and apply the
    effective changes.

    Attributes:
        resource_name (str):
            Immutable. The resource name of the experiment arm.
            Experiment arm resource names have the form:

            ``customers/{customer_id}/experimentArms/{TrialArm.trial_id}~{TrialArm.trial_arm_id}``
        experiment (str):
            Immutable. The experiment to which the
            ExperimentArm belongs.
        name (str):
            Required. The name of the experiment arm. It
            must have a minimum length of 1 and maximum
            length of 1024. It must be unique under an
            experiment.
        control (bool):
            Whether this arm is a control arm. A control
            arm is the arm against which the other arms are
            compared.
        traffic_split (int):
            Traffic split of the trial arm. The value
            should be between 1 and 100 and must total 100
            between the two trial arms.
        campaigns (MutableSequence[str]):
            List of campaigns in the trial arm. The max
            length is one.
        in_design_campaigns (MutableSequence[str]):
            Output only. The in design campaigns in the
            treatment experiment arm.
        asset_testing_info (google.ads.googleads.v24.resources.types.ExperimentArm.AssetTestingInfo):
            Details of assets under experiment.
        asset_groups (MutableSequence[google.ads.googleads.v24.resources.types.ExperimentArm.AssetGroupInfo]):
            List of asset groups in the experiment arm.
            The max length is one. In the Optimize Assets
            experiment construction, the control arm and
            treatment arm should both contain the same asset
            group ID.
        performance_max_experiment_arm_info (google.ads.googleads.v24.resources.types.ExperimentArm.PerformanceMaxExperimentArmInfo):
            Immutable. Information specific to the control or treatment
            campaign of a Performance Max experiment.

            This field is specific to experiments of type
            PMAX_REPLACEMENT_SHOPPING. For example, the treatment
            experiment arm contains the information of treatment
            Performance Max campaign settings for
            PMAX_REPLACEMENT_SHOPPING experiments.
    """

    class AssetTestingInfo(proto.Message):
        r"""Details of assets associated with the experimental copies of
        ads.

        Attributes:
            asset_variation_infos (MutableSequence[google.ads.googleads.v24.resources.types.ExperimentArm.AssetVariationInfo]):
                Details of assets associated for each
                experimental copy of the ad.
        """

        asset_variation_infos: MutableSequence[
            "ExperimentArm.AssetVariationInfo"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="ExperimentArm.AssetVariationInfo",
        )

    class AssetVariationInfo(proto.Message):
        r"""Details of asset variations to be performed on an ad in the
        control ad group.

        Attributes:
            base_ad_group (str):
                Associated base AdGroup resource name.
            base_ad (str):
                Associated base ad resource name.
            asset_details (MutableSequence[google.ads.googleads.v24.resources.types.ExperimentArm.AssetDetail]):
                Details for each asset that is being modified
                from the base ad.
        """

        base_ad_group: str = proto.Field(
            proto.STRING,
            number=1,
        )
        base_ad: str = proto.Field(
            proto.STRING,
            number=2,
        )
        asset_details: MutableSequence["ExperimentArm.AssetDetail"] = (
            proto.RepeatedField(
                proto.MESSAGE,
                number=3,
                message="ExperimentArm.AssetDetail",
            )
        )

    class AssetDetail(proto.Message):
        r"""Details of an asset modification for the experiment ad, such
        as adding or removing the asset.

        Attributes:
            asset (str):
                The asset that is being modified for the
                experiment.
            field_type (google.ads.googleads.v24.enums.types.AssetFieldTypeEnum.AssetFieldType):
                Field type for the asset.
            asset_detail_operation (google.ads.googleads.v24.enums.types.ExperimentAssetDetailOperationEnum.ExperimentAssetDetailOperation):
                Enum to specify whether the asset is removed
                or added from the base ad.
        """

        asset: str = proto.Field(
            proto.STRING,
            number=1,
        )
        field_type: asset_field_type.AssetFieldTypeEnum.AssetFieldType = (
            proto.Field(
                proto.ENUM,
                number=2,
                enum=asset_field_type.AssetFieldTypeEnum.AssetFieldType,
            )
        )
        asset_detail_operation: (
            experiment_asset_detail_operation.ExperimentAssetDetailOperationEnum.ExperimentAssetDetailOperation
        ) = proto.Field(
            proto.ENUM,
            number=3,
            enum=experiment_asset_detail_operation.ExperimentAssetDetailOperationEnum.ExperimentAssetDetailOperation,
        )

    class AssetGroupInfo(proto.Message):
        r"""Holds the asset groups included in an arm of an Optimize
        Assets experiment.

        Attributes:
            asset_group (str):
                Asset group resource name.
            asset_group_assets (MutableSequence[google.ads.googleads.v24.resources.types.ExperimentArm.AssetGroupAssetInfo]):
                List of asset group assets under the asset
                group.
        """

        asset_group: str = proto.Field(
            proto.STRING,
            number=1,
        )
        asset_group_assets: MutableSequence[
            "ExperimentArm.AssetGroupAssetInfo"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="ExperimentArm.AssetGroupAssetInfo",
        )

    class AssetGroupAssetInfo(proto.Message):
        r"""Holds the details of an asset within an asset group for an
        Optimize Assets experiment arm.

        Attributes:
            asset (str):
                Asset resource name of the asset group asset.
            field_type (google.ads.googleads.v24.enums.types.AssetFieldTypeEnum.AssetFieldType):
                Field type of the asset group asset.
        """

        asset: str = proto.Field(
            proto.STRING,
            number=1,
        )
        field_type: asset_field_type.AssetFieldTypeEnum.AssetFieldType = (
            proto.Field(
                proto.ENUM,
                number=2,
                enum=asset_field_type.AssetFieldTypeEnum.AssetFieldType,
            )
        )

    class ExperimentalPerformanceMaxCampaignSettings(proto.Message):
        r"""Parameters for an experiment to create a Performance Max
        campaign. The experimental Performance Max campaign gets created
        automatically based on the existing SHOPPING campaign settings
        and the settings specified in this field.

        Attributes:
            budget_amount_micros (int):
                Immutable. The amount of budget of the
                Performance Max experiment campaign.
            target_roas (float):
                Immutable. Target ROAS of the Performance Max
                experiment campaign.
            target_cpa_micros (int):
                Immutable. Target CPA of the Performance Max
                experiment campaign.
            bidding_strategy_type (google.ads.googleads.v24.enums.types.BiddingStrategyTypeEnum.BiddingStrategyType):
                Immutable. Bidding strategy type of the
                Performance Max experiment campaign.
        """

        budget_amount_micros: int = proto.Field(
            proto.INT64,
            number=1,
        )
        target_roas: float = proto.Field(
            proto.DOUBLE,
            number=2,
        )
        target_cpa_micros: int = proto.Field(
            proto.INT64,
            number=3,
        )
        bidding_strategy_type: (
            gage_bidding_strategy_type.BiddingStrategyTypeEnum.BiddingStrategyType
        ) = proto.Field(
            proto.ENUM,
            number=4,
            enum=gage_bidding_strategy_type.BiddingStrategyTypeEnum.BiddingStrategyType,
        )

    class PerformanceMaxExperimentArmInfo(proto.Message):
        r"""Information specific to the control or treatment campaign of
        a Performance Max experiment.

        Attributes:
            experimental_performance_max_campaign_settings (google.ads.googleads.v24.resources.types.ExperimentArm.ExperimentalPerformanceMaxCampaignSettings):
                Immutable. Performance Max campaign settings
                to be applied on the Google-created experimental
                campaign in a Performance Max experiment. The
                experimental campaign is automatically created
                by Google upon experiment creation.
        """

        experimental_performance_max_campaign_settings: (
            "ExperimentArm.ExperimentalPerformanceMaxCampaignSettings"
        ) = proto.Field(
            proto.MESSAGE,
            number=1,
            message="ExperimentArm.ExperimentalPerformanceMaxCampaignSettings",
        )

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    experiment: str = proto.Field(
        proto.STRING,
        number=8,
    )
    name: str = proto.Field(
        proto.STRING,
        number=3,
    )
    control: bool = proto.Field(
        proto.BOOL,
        number=4,
    )
    traffic_split: int = proto.Field(
        proto.INT64,
        number=5,
    )
    campaigns: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=6,
    )
    in_design_campaigns: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=7,
    )
    asset_testing_info: AssetTestingInfo = proto.Field(
        proto.MESSAGE,
        number=9,
        message=AssetTestingInfo,
    )
    asset_groups: MutableSequence[AssetGroupInfo] = proto.RepeatedField(
        proto.MESSAGE,
        number=10,
        message=AssetGroupInfo,
    )
    performance_max_experiment_arm_info: PerformanceMaxExperimentArmInfo = (
        proto.Field(
            proto.MESSAGE,
            number=11,
            message=PerformanceMaxExperimentArmInfo,
        )
    )


__all__ = tuple(sorted(__protobuf__.manifest))
