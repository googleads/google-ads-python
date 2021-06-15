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

from google.ads.googleads.v8.resources.types import (
    geo_target_constant as gagr_geo_target_constant,
)


__protobuf__ = proto.module(
    package="google.ads.googleads.v8.services",
    marshal="google.ads.googleads.v8",
    manifest={
        "GetGeoTargetConstantRequest",
        "SuggestGeoTargetConstantsRequest",
        "SuggestGeoTargetConstantsResponse",
        "GeoTargetConstantSuggestion",
    },
)


class GetGeoTargetConstantRequest(proto.Message):
    r"""Request message for
    [GeoTargetConstantService.GetGeoTargetConstant][google.ads.googleads.v8.services.GeoTargetConstantService.GetGeoTargetConstant].

    Attributes:
        resource_name (str):
            Required. The resource name of the geo target
            constant to fetch.
    """

    resource_name = proto.Field(proto.STRING, number=1,)


class SuggestGeoTargetConstantsRequest(proto.Message):
    r"""Request message for
    [GeoTargetConstantService.SuggestGeoTargetConstants][google.ads.googleads.v8.services.GeoTargetConstantService.SuggestGeoTargetConstants].

    Attributes:
        locale (str):
            If possible, returned geo targets are
            translated using this locale. If not, en is used
            by default. This is also used as a hint for
            returned geo targets.
        country_code (str):
            Returned geo targets are restricted to this
            country code.
        location_names (google.ads.googleads.v8.services.types.SuggestGeoTargetConstantsRequest.LocationNames):
            The location names to search by. At most 25
            names can be set.
        geo_targets (google.ads.googleads.v8.services.types.SuggestGeoTargetConstantsRequest.GeoTargets):
            The geo target constant resource names to
            filter by.
    """

    class LocationNames(proto.Message):
        r"""A list of location names.
        Attributes:
            names (Sequence[str]):
                A list of location names.
        """

        names = proto.RepeatedField(proto.STRING, number=2,)

    class GeoTargets(proto.Message):
        r"""A list of geo target constant resource names.
        Attributes:
            geo_target_constants (Sequence[str]):
                A list of geo target constant resource names.
        """

        geo_target_constants = proto.RepeatedField(proto.STRING, number=2,)

    locale = proto.Field(proto.STRING, number=6, optional=True,)
    country_code = proto.Field(proto.STRING, number=7, optional=True,)
    location_names = proto.Field(
        proto.MESSAGE, number=1, oneof="query", message=LocationNames,
    )
    geo_targets = proto.Field(
        proto.MESSAGE, number=2, oneof="query", message=GeoTargets,
    )


class SuggestGeoTargetConstantsResponse(proto.Message):
    r"""Response message for
    [GeoTargetConstantService.SuggestGeoTargetConstants][google.ads.googleads.v8.services.GeoTargetConstantService.SuggestGeoTargetConstants].

    Attributes:
        geo_target_constant_suggestions (Sequence[google.ads.googleads.v8.services.types.GeoTargetConstantSuggestion]):
            Geo target constant suggestions.
    """

    geo_target_constant_suggestions = proto.RepeatedField(
        proto.MESSAGE, number=1, message="GeoTargetConstantSuggestion",
    )


class GeoTargetConstantSuggestion(proto.Message):
    r"""A geo target constant suggestion.
    Attributes:
        locale (str):
            The language this GeoTargetConstantSuggestion
            is currently translated to. It affects the name
            of geo target fields. For example, if locale=en,
            then name=Spain. If locale=es, then name=España.
            The default locale will be returned if no
            translation exists for the locale in the
            request.
        reach (int):
            Approximate user population that will be
            targeted, rounded to the nearest 100.
        search_term (str):
            If the request searched by location name,
            this is the location name that matched the geo
            target.
        geo_target_constant (google.ads.googleads.v8.resources.types.GeoTargetConstant):
            The GeoTargetConstant result.
        geo_target_constant_parents (Sequence[google.ads.googleads.v8.resources.types.GeoTargetConstant]):
            The list of parents of the geo target
            constant.
    """

    locale = proto.Field(proto.STRING, number=6, optional=True,)
    reach = proto.Field(proto.INT64, number=7, optional=True,)
    search_term = proto.Field(proto.STRING, number=8, optional=True,)
    geo_target_constant = proto.Field(
        proto.MESSAGE,
        number=4,
        message=gagr_geo_target_constant.GeoTargetConstant,
    )
    geo_target_constant_parents = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message=gagr_geo_target_constant.GeoTargetConstant,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
