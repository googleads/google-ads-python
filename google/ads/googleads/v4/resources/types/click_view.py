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


from google.ads.googleads.v4.common.types import click_location
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.resources",
    marshal="google.ads.googleads.v4",
    manifest={"ClickView",},
)


class ClickView(proto.Message):
    r"""A click view with metrics aggregated at each click level,
    including both valid and invalid clicks. For non-Search
    campaigns, metrics.clicks represents the number of valid and
    invalid interactions. Queries including ClickView must have a
    filter limiting the results to one day and can be requested for
    dates back to 90 days before the time of the request.

    Attributes:
        resource_name (str):
            Output only. The resource name of the click view. Click view
            resource names have the form:

            ``customers/{customer_id}/clickViews/{date (yyyy-MM-dd)}~{gclid}``
        gclid (google.protobuf.wrappers_pb2.StringValue):
            Output only. The Google Click ID.
        area_of_interest (google.ads.googleads.v4.common.types.ClickLocation):
            Output only. The location criteria matching
            the area of interest associated with the
            impression.
        location_of_presence (google.ads.googleads.v4.common.types.ClickLocation):
            Output only. The location criteria matching
            the location of presence associated with the
            impression.
        page_number (google.protobuf.wrappers_pb2.Int64Value):
            Output only. Page number in search results
            where the ad was shown.
        ad_group_ad (google.protobuf.wrappers_pb2.StringValue):
            Output only. The associated ad.
    """

    resource_name = proto.Field(proto.STRING, number=1)
    gclid = proto.Field(proto.MESSAGE, number=2, message=wrappers.StringValue,)
    area_of_interest = proto.Field(
        proto.MESSAGE, number=3, message=click_location.ClickLocation,
    )
    location_of_presence = proto.Field(
        proto.MESSAGE, number=4, message=click_location.ClickLocation,
    )
    page_number = proto.Field(
        proto.MESSAGE, number=5, message=wrappers.Int64Value,
    )
    ad_group_ad = proto.Field(
        proto.MESSAGE, number=7, message=wrappers.StringValue,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
