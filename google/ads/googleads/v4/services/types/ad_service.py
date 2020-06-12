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


from google.ads.googleads.v4.resources.types import ad
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.services",
    marshal="google.ads.googleads.v4",
    manifest={
        "GetAdRequest",
        "MutateAdsRequest",
        "AdOperation",
        "MutateAdsResponse",
        "MutateAdResult",
    },
)


class GetAdRequest(proto.Message):
    r"""Request message for
    [AdService.GetAd][google.ads.googleads.v4.services.AdService.GetAd].

    Attributes:
        resource_name (str):
            Required. The resource name of the ad to
            fetch.
    """

    resource_name = proto.Field(proto.STRING, number=1)


class MutateAdsRequest(proto.Message):
    r"""Request message for
    [AdService.MutateAds][google.ads.googleads.v4.services.AdService.MutateAds].

    Attributes:
        customer_id (str):
            Required. The ID of the customer whose ads
            are being modified.
        operations (Sequence[google.ads.googleads.v4.services.types.AdOperation]):
            Required. The list of operations to perform
            on individual ads.
    """

    customer_id = proto.Field(proto.STRING, number=1)
    operations = proto.RepeatedField(
        proto.MESSAGE, number=2, message="AdOperation",
    )


class AdOperation(proto.Message):
    r"""A single update operation on an ad.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            FieldMask that determines which resource
            fields are modified in an update.
        update (google.ads.googleads.v4.resources.types.Ad):
            Update operation: The ad is expected to have a valid
            resource name in this format:

            ``customers/{customer_id}/ads/{ad_id}``
    """

    update_mask = proto.Field(
        proto.MESSAGE, number=2, message=field_mask.FieldMask,
    )
    update = proto.Field(
        proto.MESSAGE, number=1, oneof="operation", message=ad.Ad,
    )


class MutateAdsResponse(proto.Message):
    r"""Response message for an ad mutate.

    Attributes:
        results (Sequence[google.ads.googleads.v4.services.types.MutateAdResult]):
            All results for the mutate.
    """

    results = proto.RepeatedField(
        proto.MESSAGE, number=2, message="MutateAdResult",
    )


class MutateAdResult(proto.Message):
    r"""The result for the ad mutate.

    Attributes:
        resource_name (str):
            The resource name returned for successful
            operations.
    """

    resource_name = proto.Field(proto.STRING, number=1)


__all__ = tuple(sorted(__protobuf__.manifest))
