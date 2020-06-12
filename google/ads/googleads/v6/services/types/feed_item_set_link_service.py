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


from google.ads.googleads.v6.resources.types import feed_item_set_link


__protobuf__ = proto.module(
    package="google.ads.googleads.v6.services",
    marshal="google.ads.googleads.v6",
    manifest={
        "GetFeedItemSetLinkRequest",
        "MutateFeedItemSetLinksRequest",
        "FeedItemSetLinkOperation",
        "MutateFeedItemSetLinksResponse",
        "MutateFeedItemSetLinkResult",
    },
)


class GetFeedItemSetLinkRequest(proto.Message):
    r"""Request message for [FeedItemSetLinkService.GetFeedItemSetLinks][].

    Attributes:
        resource_name (str):
            Required. The resource name of the feed item
            set link to fetch.
    """

    resource_name = proto.Field(proto.STRING, number=1)


class MutateFeedItemSetLinksRequest(proto.Message):
    r"""Request message for
    [FeedItemSetLinkService.MutateFeedItemSetLinks][google.ads.googleads.v6.services.FeedItemSetLinkService.MutateFeedItemSetLinks].

    Attributes:
        customer_id (str):
            Required. The ID of the customer whose feed
            item set links are being modified.
        operations (Sequence[google.ads.googleads.v6.services.types.FeedItemSetLinkOperation]):
            Required. The list of operations to perform
            on individual feed item set links.
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

    customer_id = proto.Field(proto.STRING, number=1)
    operations = proto.RepeatedField(
        proto.MESSAGE, number=2, message="FeedItemSetLinkOperation",
    )
    partial_failure = proto.Field(proto.BOOL, number=3)
    validate_only = proto.Field(proto.BOOL, number=4)


class FeedItemSetLinkOperation(proto.Message):
    r"""A single operation (create, update, remove) on a feed item
    set link.

    Attributes:
        create (google.ads.googleads.v6.resources.types.FeedItemSetLink):
            Create operation: No resource name is
            expected for the new feed item set link.
        remove (str):
            Remove operation: A resource name for the removed feed item
            set link is expected, in this format:

            ``customers/{customer_id}/feedItemSetLinks/{feed_id}_{feed_item_set_id}_{feed_item_id}``
    """

    create = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="operation",
        message=feed_item_set_link.FeedItemSetLink,
    )
    remove = proto.Field(proto.STRING, number=2, oneof="operation")


class MutateFeedItemSetLinksResponse(proto.Message):
    r"""Response message for a feed item set link mutate.

    Attributes:
        results (Sequence[google.ads.googleads.v6.services.types.MutateFeedItemSetLinkResult]):
            All results for the mutate.
    """

    results = proto.RepeatedField(
        proto.MESSAGE, number=1, message="MutateFeedItemSetLinkResult",
    )


class MutateFeedItemSetLinkResult(proto.Message):
    r"""The result for the feed item set link mutate.

    Attributes:
        resource_name (str):
            Returned for successful operations.
    """

    resource_name = proto.Field(proto.STRING, number=1)


__all__ = tuple(sorted(__protobuf__.manifest))
