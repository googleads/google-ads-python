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


from google.ads.googleads.v4.enums.types import campaign_draft_status
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.resources",
    marshal="google.ads.googleads.v4",
    manifest={"CampaignDraft",},
)


class CampaignDraft(proto.Message):
    r"""A campaign draft.

    Attributes:
        resource_name (str):
            Immutable. The resource name of the campaign draft. Campaign
            draft resource names have the form:

            ``customers/{customer_id}/campaignDrafts/{base_campaign_id}~{draft_id}``
        draft_id (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The ID of the draft.
            This field is read-only.
        base_campaign (google.protobuf.wrappers_pb2.StringValue):
            Immutable. The base campaign to which the
            draft belongs.
        name (google.protobuf.wrappers_pb2.StringValue):
            The name of the campaign draft.
            This field is required and should not be empty
            when creating new campaign drafts.

            It must not contain any null (code point 0x0),
            NL line feed (code point 0xA) or carriage return
            (code point 0xD) characters.
        draft_campaign (google.protobuf.wrappers_pb2.StringValue):
            Output only. Resource name of the Campaign
            that results from overlaying the draft changes
            onto the base campaign.
            This field is read-only.
        status (google.ads.googleads.v4.enums.types.CampaignDraftStatusEnum.CampaignDraftStatus):
            Output only. The status of the campaign
            draft. This field is read-only.
            When a new campaign draft is added, the status
            defaults to PROPOSED.
        has_experiment_running (google.protobuf.wrappers_pb2.BoolValue):
            Output only. Whether there is an experiment
            based on this draft currently serving.
        long_running_operation (google.protobuf.wrappers_pb2.StringValue):
            Output only. The resource name of the long-
            unning operation that can be used to poll for
            completion of draft promotion. This is only set
            if the draft promotion is in progress or
            finished.
    """

    resource_name = proto.Field(proto.STRING, number=1)
    draft_id = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.Int64Value,
    )
    base_campaign = proto.Field(
        proto.MESSAGE, number=3, message=wrappers.StringValue,
    )
    name = proto.Field(proto.MESSAGE, number=4, message=wrappers.StringValue,)
    draft_campaign = proto.Field(
        proto.MESSAGE, number=5, message=wrappers.StringValue,
    )
    status = proto.Field(
        proto.ENUM,
        number=6,
        enum=campaign_draft_status.CampaignDraftStatusEnum.CampaignDraftStatus,
    )
    has_experiment_running = proto.Field(
        proto.MESSAGE, number=7, message=wrappers.BoolValue,
    )
    long_running_operation = proto.Field(
        proto.MESSAGE, number=8, message=wrappers.StringValue,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
