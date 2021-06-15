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

from google.ads.googleads.v8.resources.types import feed_item_set
from google.protobuf import field_mask_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v8.services",
    marshal="google.ads.googleads.v8",
    manifest={
        "GetFeedItemSetRequest",
        "MutateFeedItemSetsRequest",
        "FeedItemSetOperation",
        "MutateFeedItemSetsResponse",
        "MutateFeedItemSetResult",
    },
)


class GetFeedItemSetRequest(proto.Message):
    r"""Request message for
    [FeedItemSetService.GetFeedItemSet][google.ads.googleads.v8.services.FeedItemSetService.GetFeedItemSet].

    Attributes:
        resource_name (str):
            Required. The resource name of the feed item
            set to fetch.
    """

    resource_name = proto.Field(proto.STRING, number=1,)


class MutateFeedItemSetsRequest(proto.Message):
    r"""Request message for
    [FeedItemSetService.MutateFeedItemSets][google.ads.googleads.v8.services.FeedItemSetService.MutateFeedItemSets].

    Attributes:
        customer_id (str):
            Required. The ID of the customer whose feed
            item sets are being modified.
        operations (Sequence[google.ads.googleads.v8.services.types.FeedItemSetOperation]):
            Required. The list of operations to perform
            on individual feed item sets.
        partial_failure (bool):
            If true, successful operations will be
            carried out and invalid operations will return
            errors. If false, all operations will be carried
            out in one transaction if and only if they are
            all valid. Default is false.
        validate_only (bool):
            If true, the request is validated but not
            executed. Only errors are returned, not results.
    """

    customer_id = proto.Field(proto.STRING, number=1,)
    operations = proto.RepeatedField(
        proto.MESSAGE, number=2, message="FeedItemSetOperation",
    )
    partial_failure = proto.Field(proto.BOOL, number=3,)
    validate_only = proto.Field(proto.BOOL, number=4,)


class FeedItemSetOperation(proto.Message):
    r"""A single operation (create, remove) on an feed item set.
    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            FieldMask that determines which resource
            fields are modified in an update.
        create (google.ads.googleads.v8.resources.types.FeedItemSet):
            Create operation: No resource name is
            expected for the new feed item set
        update (google.ads.googleads.v8.resources.types.FeedItemSet):
            Update operation: The feed item set is
            expected to have a valid resource name.
        remove (str):
            Remove operation: A resource name for the removed feed item
            is expected, in this format:
            ``customers/{customer_id}/feedItems/{feed_id}~{feed_item_set_id}``
    """

    update_mask = proto.Field(
        proto.MESSAGE, number=4, message=field_mask_pb2.FieldMask,
    )
    create = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="operation",
        message=feed_item_set.FeedItemSet,
    )
    update = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="operation",
        message=feed_item_set.FeedItemSet,
    )
    remove = proto.Field(proto.STRING, number=3, oneof="operation",)


class MutateFeedItemSetsResponse(proto.Message):
    r"""Response message for an feed item set mutate.
    Attributes:
        results (Sequence[google.ads.googleads.v8.services.types.MutateFeedItemSetResult]):
            All results for the mutate.
    """

    results = proto.RepeatedField(
        proto.MESSAGE, number=1, message="MutateFeedItemSetResult",
    )


class MutateFeedItemSetResult(proto.Message):
    r"""The result for the feed item set mutate.
    Attributes:
        resource_name (str):
            Returned for successful operations.
    """

    resource_name = proto.Field(proto.STRING, number=1,)


__all__ = tuple(sorted(__protobuf__.manifest))
