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


from google.ads.googleads.v4.common.types import custom_parameter
from google.ads.googleads.v4.common.types import (
    explorer_auto_optimizer_setting as gagc_explorer_auto_optimizer_setting,
)
from google.ads.googleads.v4.common.types import (
    targeting_setting as gagc_targeting_setting,
)
from google.ads.googleads.v4.enums.types import ad_group_ad_rotation_mode
from google.ads.googleads.v4.enums.types import ad_group_status
from google.ads.googleads.v4.enums.types import ad_group_type
from google.ads.googleads.v4.enums.types import bidding_source
from google.ads.googleads.v4.enums.types import targeting_dimension
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.resources",
    marshal="google.ads.googleads.v4",
    manifest={"AdGroup",},
)


class AdGroup(proto.Message):
    r"""An ad group.

    Attributes:
        resource_name (str):
            Immutable. The resource name of the ad group. Ad group
            resource names have the form:

            ``customers/{customer_id}/adGroups/{ad_group_id}``
        id (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The ID of the ad group.
        name (google.protobuf.wrappers_pb2.StringValue):
            The name of the ad group.
            This field is required and should not be empty
            when creating new ad groups.

            It must contain fewer than 255 UTF-8 full-width
            characters.
            It must not contain any null (code point 0x0),
            NL line feed (code point 0xA) or carriage return
            (code point 0xD) characters.
        status (google.ads.googleads.v4.enums.types.AdGroupStatusEnum.AdGroupStatus):
            The status of the ad group.
        type_ (google.ads.googleads.v4.enums.types.AdGroupTypeEnum.AdGroupType):
            Immutable. The type of the ad group.
        ad_rotation_mode (google.ads.googleads.v4.enums.types.AdGroupAdRotationModeEnum.AdGroupAdRotationMode):
            The ad rotation mode of the ad group.
        base_ad_group (google.protobuf.wrappers_pb2.StringValue):
            Output only. For draft or experiment ad
            groups, this field is the resource name of the
            base ad group from which this ad group was
            created. If a draft or experiment ad group does
            not have a base ad group, then this field is
            null.
            For base ad groups, this field equals the ad
            group resource name.
            This field is read-only.
        tracking_url_template (google.protobuf.wrappers_pb2.StringValue):
            The URL template for constructing a tracking
            URL.
        url_custom_parameters (Sequence[google.ads.googleads.v4.common.types.CustomParameter]):
            The list of mappings used to substitute custom parameter
            tags in a ``tracking_url_template``, ``final_urls``, or
            ``mobile_final_urls``.
        campaign (google.protobuf.wrappers_pb2.StringValue):
            Immutable. The campaign to which the ad group
            belongs.
        cpc_bid_micros (google.protobuf.wrappers_pb2.Int64Value):
            The maximum CPC (cost-per-click) bid.
        cpm_bid_micros (google.protobuf.wrappers_pb2.Int64Value):
            The maximum CPM (cost-per-thousand viewable
            impressions) bid.
        target_cpa_micros (google.protobuf.wrappers_pb2.Int64Value):
            The target CPA (cost-per-acquisition).
        cpv_bid_micros (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The CPV (cost-per-view) bid.
        target_cpm_micros (google.protobuf.wrappers_pb2.Int64Value):
            Average amount in micros that the advertiser
            is willing to pay for every thousand times the
            ad is shown.
        target_roas (google.protobuf.wrappers_pb2.DoubleValue):
            The target ROAS (return-on-ad-spend)
            override. If the ad group's campaign bidding
            strategy is a standard Target ROAS strategy,
            then this field overrides the target ROAS
            specified in the campaign's bidding strategy.
            Otherwise, this value is ignored.
        percent_cpc_bid_micros (google.protobuf.wrappers_pb2.Int64Value):
            The percent cpc bid amount, expressed as a fraction of the
            advertised price for some good or service. The valid range
            for the fraction is [0,1) and the value stored here is
            1,000,000 \* [fraction].
        explorer_auto_optimizer_setting (google.ads.googleads.v4.common.types.ExplorerAutoOptimizerSetting):
            Settings for the Display Campaign Optimizer,
            initially termed "Explorer".
        display_custom_bid_dimension (google.ads.googleads.v4.enums.types.TargetingDimensionEnum.TargetingDimension):
            Allows advertisers to specify a targeting
            dimension on which to place absolute bids. This
            is only applicable for campaigns that target
            only the display network and not search.
        final_url_suffix (google.protobuf.wrappers_pb2.StringValue):
            URL template for appending params to Final
            URL.
        targeting_setting (google.ads.googleads.v4.common.types.TargetingSetting):
            Setting for targeting related features.
        effective_target_cpa_micros (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The effective target CPA (cost-
            er-acquisition). This field is read-only.
        effective_target_cpa_source (google.ads.googleads.v4.enums.types.BiddingSourceEnum.BiddingSource):
            Output only. Source of the effective target
            CPA. This field is read-only.
        effective_target_roas (google.protobuf.wrappers_pb2.DoubleValue):
            Output only. The effective target ROAS
            (return-on-ad-spend). This field is read-only.
        effective_target_roas_source (google.ads.googleads.v4.enums.types.BiddingSourceEnum.BiddingSource):
            Output only. Source of the effective target
            ROAS. This field is read-only.
        labels (Sequence[google.protobuf.wrappers_pb2.StringValue]):
            Output only. The resource names of labels
            attached to this ad group.
    """

    resource_name = proto.Field(proto.STRING, number=1)
    id = proto.Field(proto.MESSAGE, number=3, message=wrappers.Int64Value,)
    name = proto.Field(proto.MESSAGE, number=4, message=wrappers.StringValue,)
    status = proto.Field(
        proto.ENUM,
        number=5,
        enum=ad_group_status.AdGroupStatusEnum.AdGroupStatus,
    )
    type_ = proto.Field(
        proto.ENUM, number=12, enum=ad_group_type.AdGroupTypeEnum.AdGroupType,
    )
    ad_rotation_mode = proto.Field(
        proto.ENUM,
        number=22,
        enum=ad_group_ad_rotation_mode.AdGroupAdRotationModeEnum.AdGroupAdRotationMode,
    )
    base_ad_group = proto.Field(
        proto.MESSAGE, number=18, message=wrappers.StringValue,
    )
    tracking_url_template = proto.Field(
        proto.MESSAGE, number=13, message=wrappers.StringValue,
    )
    url_custom_parameters = proto.RepeatedField(
        proto.MESSAGE, number=6, message=custom_parameter.CustomParameter,
    )
    campaign = proto.Field(
        proto.MESSAGE, number=10, message=wrappers.StringValue,
    )
    cpc_bid_micros = proto.Field(
        proto.MESSAGE, number=14, message=wrappers.Int64Value,
    )
    cpm_bid_micros = proto.Field(
        proto.MESSAGE, number=15, message=wrappers.Int64Value,
    )
    target_cpa_micros = proto.Field(
        proto.MESSAGE, number=27, message=wrappers.Int64Value,
    )
    cpv_bid_micros = proto.Field(
        proto.MESSAGE, number=17, message=wrappers.Int64Value,
    )
    target_cpm_micros = proto.Field(
        proto.MESSAGE, number=26, message=wrappers.Int64Value,
    )
    target_roas = proto.Field(
        proto.MESSAGE, number=30, message=wrappers.DoubleValue,
    )
    percent_cpc_bid_micros = proto.Field(
        proto.MESSAGE, number=20, message=wrappers.Int64Value,
    )
    explorer_auto_optimizer_setting = proto.Field(
        proto.MESSAGE,
        number=21,
        message=gagc_explorer_auto_optimizer_setting.ExplorerAutoOptimizerSetting,
    )
    display_custom_bid_dimension = proto.Field(
        proto.ENUM,
        number=23,
        enum=targeting_dimension.TargetingDimensionEnum.TargetingDimension,
    )
    final_url_suffix = proto.Field(
        proto.MESSAGE, number=24, message=wrappers.StringValue,
    )
    targeting_setting = proto.Field(
        proto.MESSAGE,
        number=25,
        message=gagc_targeting_setting.TargetingSetting,
    )
    effective_target_cpa_micros = proto.Field(
        proto.MESSAGE, number=28, message=wrappers.Int64Value,
    )
    effective_target_cpa_source = proto.Field(
        proto.ENUM,
        number=29,
        enum=bidding_source.BiddingSourceEnum.BiddingSource,
    )
    effective_target_roas = proto.Field(
        proto.MESSAGE, number=31, message=wrappers.DoubleValue,
    )
    effective_target_roas_source = proto.Field(
        proto.ENUM,
        number=32,
        enum=bidding_source.BiddingSourceEnum.BiddingSource,
    )
    labels = proto.RepeatedField(
        proto.MESSAGE, number=33, message=wrappers.StringValue,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
