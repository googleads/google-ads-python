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


from google.ads.googleads.v5.resources.types import feed_item_target


__protobuf__ = proto.module(
    package="google.ads.googleads.v5.services",
    marshal="google.ads.googleads.v5",
    manifest={
        "GetFeedItemTargetRequest",
        "MutateFeedItemTargetsRequest",
        "FeedItemTargetOperation",
        "MutateFeedItemTargetsResponse",
        "MutateFeedItemTargetResult",
    },
)


class GetFeedItemTargetRequest(proto.Message):
    r"""Request message for
    [FeedItemTargetService.GetFeedItemTarget][google.ads.googleads.v5.services.FeedItemTargetService.GetFeedItemTarget].

    Attributes:
        resource_name (str):
            Required. The resource name of the feed item
            targets to fetch.
    """

    resource_name = proto.Field(proto.STRING, number=1)


class MutateFeedItemTargetsRequest(proto.Message):
    r"""Request message for
    [FeedItemTargetService.MutateFeedItemTargets][google.ads.googleads.v5.services.FeedItemTargetService.MutateFeedItemTargets].

    Attributes:
        customer_id (str):
            Required. The ID of the customer whose feed
            item targets are being modified.
        operations (Sequence[google.ads.googleads.v5.services.types.FeedItemTargetOperation]):
            Required. The list of operations to perform
            on individual feed item targets.
    """

    customer_id = proto.Field(proto.STRING, number=1)
    operations = proto.RepeatedField(
        proto.MESSAGE, number=2, message="FeedItemTargetOperation",
    )


class FeedItemTargetOperation(proto.Message):
    r"""A single operation (create, remove) on an feed item target.

    Attributes:
        create (google.ads.googleads.v5.resources.types.FeedItemTarget):
            Create operation: No resource name is
            expected for the new feed item target.
        remove (str):
            Remove operation: A resource name for the removed feed item
            target is expected, in this format:

            ``customers/{customer_id}/feedItemTargets/{feed_id}~{feed_item_id}~{feed_item_target_type}~{feed_item_target_id}``
    """

    create = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="operation",
        message=feed_item_target.FeedItemTarget,
    )
    remove = proto.Field(proto.STRING, number=2, oneof="operation")


class MutateFeedItemTargetsResponse(proto.Message):
    r"""Response message for an feed item target mutate.

    Attributes:
        results (Sequence[google.ads.googleads.v5.services.types.MutateFeedItemTargetResult]):
            All results for the mutate.
    """

    results = proto.RepeatedField(
        proto.MESSAGE, number=2, message="MutateFeedItemTargetResult",
    )


class MutateFeedItemTargetResult(proto.Message):
    r"""The result for the feed item target mutate.

    Attributes:
        resource_name (str):
            Returned for successful operations.
    """

    resource_name = proto.Field(proto.STRING, number=1)


__all__ = tuple(sorted(__protobuf__.manifest))
