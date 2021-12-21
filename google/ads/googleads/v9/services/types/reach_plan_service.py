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

from google.ads.googleads.v9.common.types import criteria
from google.ads.googleads.v9.common.types import dates
from google.ads.googleads.v9.enums.types import frequency_cap_time_unit
from google.ads.googleads.v9.enums.types import reach_plan_ad_length
from google.ads.googleads.v9.enums.types import reach_plan_age_range
from google.ads.googleads.v9.enums.types import reach_plan_network


__protobuf__ = proto.module(
    package="google.ads.googleads.v9.services",
    marshal="google.ads.googleads.v9",
    manifest={
        "ListPlannableLocationsRequest",
        "ListPlannableLocationsResponse",
        "PlannableLocation",
        "ListPlannableProductsRequest",
        "ListPlannableProductsResponse",
        "ProductMetadata",
        "PlannableTargeting",
        "GenerateProductMixIdeasRequest",
        "Preferences",
        "GenerateProductMixIdeasResponse",
        "ProductAllocation",
        "GenerateReachForecastRequest",
        "EffectiveFrequencyLimit",
        "FrequencyCap",
        "Targeting",
        "CampaignDuration",
        "PlannedProduct",
        "GenerateReachForecastResponse",
        "ReachCurve",
        "ReachForecast",
        "Forecast",
        "PlannedProductReachForecast",
        "PlannedProductForecast",
        "OnTargetAudienceMetrics",
        "EffectiveFrequencyBreakdown",
    },
)


class ListPlannableLocationsRequest(proto.Message):
    r"""Request message for
    [ReachPlanService.ListPlannableLocations][google.ads.googleads.v9.services.ReachPlanService.ListPlannableLocations].

    """


class ListPlannableLocationsResponse(proto.Message):
    r"""The list of plannable locations.

    Attributes:
        plannable_locations (Sequence[google.ads.googleads.v9.services.types.PlannableLocation]):
            The list of locations available for planning
            (Countries, DMAs, sub-countries).
            For locations like Countries and DMAs see
            https://developers.google.com/google-
            ads/api/reference/data/geotargets for more
            information.
    """

    plannable_locations = proto.RepeatedField(
        proto.MESSAGE, number=1, message="PlannableLocation",
    )


class PlannableLocation(proto.Message):
    r"""A plannable location: a country, a DMA, a metro region, a tv
    region, a province.

    Attributes:
        id (str):
            The location identifier.

            This field is a member of `oneof`_ ``_id``.
        name (str):
            The unique location name in english.

            This field is a member of `oneof`_ ``_name``.
        parent_country_id (int):
            The parent country, not present if location is a country. If
            present will always be a GeoTargetConstant ID. Additional
            information, such as country name is provided by
            [ReachPlanService.ListPlannableLocations][google.ads.googleads.v9.services.ReachPlanService.ListPlannableLocations]
            or directly by accessing
            [GeoTargetConstantService.GetGeoTargetConstant][google.ads.googleads.v9.services.GeoTargetConstantService.GetGeoTargetConstant].

            This field is a member of `oneof`_ ``_parent_country_id``.
        country_code (str):
            The ISO-3166-1 alpha-2 country code that is
            associated with the location.

            This field is a member of `oneof`_ ``_country_code``.
        location_type (str):
            The location's type. Location types correspond to
            target_type returned by
            [GeoTargetConstantService.GetGeoTargetConstant][google.ads.googleads.v9.services.GeoTargetConstantService.GetGeoTargetConstant].

            This field is a member of `oneof`_ ``_location_type``.
    """

    id = proto.Field(proto.STRING, number=4, optional=True,)
    name = proto.Field(proto.STRING, number=5, optional=True,)
    parent_country_id = proto.Field(proto.INT64, number=6, optional=True,)
    country_code = proto.Field(proto.STRING, number=7, optional=True,)
    location_type = proto.Field(proto.STRING, number=8, optional=True,)


class ListPlannableProductsRequest(proto.Message):
    r"""Request to list available products in a given location.

    Attributes:
        plannable_location_id (str):
            Required. The ID of the selected location for planning. To
            list the available plannable location ids use
            [ReachPlanService.ListPlannableLocations][google.ads.googleads.v9.services.ReachPlanService.ListPlannableLocations].
    """

    plannable_location_id = proto.Field(proto.STRING, number=2,)


class ListPlannableProductsResponse(proto.Message):
    r"""A response with all available products.

    Attributes:
        product_metadata (Sequence[google.ads.googleads.v9.services.types.ProductMetadata]):
            The list of products available for planning
            and related targeting metadata.
    """

    product_metadata = proto.RepeatedField(
        proto.MESSAGE, number=1, message="ProductMetadata",
    )


class ProductMetadata(proto.Message):
    r"""The metadata associated with an available plannable product.

    Attributes:
        plannable_product_code (str):
            The code associated with the ad product. E.g. BUMPER,
            TRUEVIEW_IN_STREAM To list the available plannable product
            codes use ListPlannableProducts.

            This field is a member of `oneof`_ ``_plannable_product_code``.
        plannable_product_name (str):
            The name associated with the ad product.
        plannable_targeting (google.ads.googleads.v9.services.types.PlannableTargeting):
            The allowed plannable targeting for this
            product.
    """

    plannable_product_code = proto.Field(proto.STRING, number=4, optional=True,)
    plannable_product_name = proto.Field(proto.STRING, number=3,)
    plannable_targeting = proto.Field(
        proto.MESSAGE, number=2, message="PlannableTargeting",
    )


class PlannableTargeting(proto.Message):
    r"""The targeting for which traffic metrics will be reported.

    Attributes:
        age_ranges (Sequence[google.ads.googleads.v9.enums.types.ReachPlanAgeRangeEnum.ReachPlanAgeRange]):
            Allowed plannable age ranges for the product
            for which metrics will be reported. Actual
            targeting is computed by mapping this age range
            onto standard Google common.AgeRangeInfo values.
        genders (Sequence[google.ads.googleads.v9.common.types.GenderInfo]):
            Targetable genders for the ad product.
        devices (Sequence[google.ads.googleads.v9.common.types.DeviceInfo]):
            Targetable devices for the ad product. TABLET device
            targeting is automatically applied to reported metrics when
            MOBILE targeting is selected for CPM_MASTHEAD,
            GOOGLE_PREFERRED_BUMPER and GOOGLE_PREFERRED_SHORT products.
        networks (Sequence[google.ads.googleads.v9.enums.types.ReachPlanNetworkEnum.ReachPlanNetwork]):
            Targetable networks for the ad product.
    """

    age_ranges = proto.RepeatedField(
        proto.ENUM,
        number=1,
        enum=reach_plan_age_range.ReachPlanAgeRangeEnum.ReachPlanAgeRange,
    )
    genders = proto.RepeatedField(
        proto.MESSAGE, number=2, message=criteria.GenderInfo,
    )
    devices = proto.RepeatedField(
        proto.MESSAGE, number=3, message=criteria.DeviceInfo,
    )
    networks = proto.RepeatedField(
        proto.ENUM,
        number=4,
        enum=reach_plan_network.ReachPlanNetworkEnum.ReachPlanNetwork,
    )


class GenerateProductMixIdeasRequest(proto.Message):
    r"""Request message for
    [ReachPlanService.GenerateProductMixIdeas][google.ads.googleads.v9.services.ReachPlanService.GenerateProductMixIdeas].

    Attributes:
        customer_id (str):
            Required. The ID of the customer.
        plannable_location_id (str):
            Required. The ID of the location, this is one of the ids
            returned by
            [ReachPlanService.ListPlannableLocations][google.ads.googleads.v9.services.ReachPlanService.ListPlannableLocations].
        currency_code (str):
            Required. Currency code.
            Three-character ISO 4217 currency code.
        budget_micros (int):
            Required. Total budget.
            Amount in micros. One million is equivalent to
            one unit.
        preferences (google.ads.googleads.v9.services.types.Preferences):
            The preferences of the suggested product mix.
            An unset preference is interpreted as all
            possible values are allowed, unless explicitly
            specified.
    """

    customer_id = proto.Field(proto.STRING, number=1,)
    plannable_location_id = proto.Field(proto.STRING, number=6,)
    currency_code = proto.Field(proto.STRING, number=7,)
    budget_micros = proto.Field(proto.INT64, number=8,)
    preferences = proto.Field(proto.MESSAGE, number=5, message="Preferences",)


class Preferences(proto.Message):
    r"""Set of preferences about the planned mix.

    Attributes:
        is_skippable (bool):
            True if ad skippable.
            If not set, default is any value.

            This field is a member of `oneof`_ ``_is_skippable``.
        starts_with_sound (bool):
            True if ad start with sound.
            If not set, default is any value.

            This field is a member of `oneof`_ ``_starts_with_sound``.
        ad_length (google.ads.googleads.v9.enums.types.ReachPlanAdLengthEnum.ReachPlanAdLength):
            The length of the ad.
            If not set, default is any value.
        top_content_only (bool):
            True if ad will only show on the top content.
            If not set, default is false.

            This field is a member of `oneof`_ ``_top_content_only``.
        has_guaranteed_price (bool):
            True if the price guaranteed. The cost of
            serving the ad is agreed upfront and not subject
            to an auction. If not set, default is any value.

            This field is a member of `oneof`_ ``_has_guaranteed_price``.
    """

    is_skippable = proto.Field(proto.BOOL, number=6, optional=True,)
    starts_with_sound = proto.Field(proto.BOOL, number=7, optional=True,)
    ad_length = proto.Field(
        proto.ENUM,
        number=3,
        enum=reach_plan_ad_length.ReachPlanAdLengthEnum.ReachPlanAdLength,
    )
    top_content_only = proto.Field(proto.BOOL, number=8, optional=True,)
    has_guaranteed_price = proto.Field(proto.BOOL, number=9, optional=True,)


class GenerateProductMixIdeasResponse(proto.Message):
    r"""The suggested product mix.

    Attributes:
        product_allocation (Sequence[google.ads.googleads.v9.services.types.ProductAllocation]):
            A list of products (ad formats) and the
            associated budget allocation idea.
    """

    product_allocation = proto.RepeatedField(
        proto.MESSAGE, number=1, message="ProductAllocation",
    )


class ProductAllocation(proto.Message):
    r"""An allocation of a part of the budget on a given product.

    Attributes:
        plannable_product_code (str):
            Selected product for planning. The product
            codes returned are within the set of the ones
            returned by ListPlannableProducts when using the
            same location ID.

            This field is a member of `oneof`_ ``_plannable_product_code``.
        budget_micros (int):
            The value to be allocated for the suggested
            product in requested currency. Amount in micros.
            One million is equivalent to one unit.

            This field is a member of `oneof`_ ``_budget_micros``.
    """

    plannable_product_code = proto.Field(proto.STRING, number=3, optional=True,)
    budget_micros = proto.Field(proto.INT64, number=4, optional=True,)


class GenerateReachForecastRequest(proto.Message):
    r"""Request message for
    [ReachPlanService.GenerateReachForecast][google.ads.googleads.v9.services.ReachPlanService.GenerateReachForecast].

    Attributes:
        customer_id (str):
            Required. The ID of the customer.
        currency_code (str):
            The currency code.
            Three-character ISO 4217 currency code.

            This field is a member of `oneof`_ ``_currency_code``.
        campaign_duration (google.ads.googleads.v9.services.types.CampaignDuration):
            Required. Campaign duration.
        cookie_frequency_cap (int):
            Desired cookie frequency cap that will be applied to each
            planned product. This is equivalent to the frequency cap
            exposed in Google Ads when creating a campaign, it
            represents the maximum number of times an ad can be shown to
            the same user. If not specified no cap is applied.

            This field is deprecated in v4 and will eventually be
            removed. Please use cookie_frequency_cap_setting instead.

            This field is a member of `oneof`_ ``_cookie_frequency_cap``.
        cookie_frequency_cap_setting (google.ads.googleads.v9.services.types.FrequencyCap):
            Desired cookie frequency cap that will be applied to each
            planned product. This is equivalent to the frequency cap
            exposed in Google Ads when creating a campaign, it
            represents the maximum number of times an ad can be shown to
            the same user during a specified time interval. If not
            specified, a default of 0 (no cap) is applied.

            This field replaces the deprecated cookie_frequency_cap
            field.
        min_effective_frequency (int):
            Desired minimum effective frequency (the number of times a
            person was exposed to the ad) for the reported reach metrics
            [1-10]. This won't affect the targeting, but just the
            reporting. If not specified, a default of 1 is applied.

            This field cannot be combined with the
            effective_frequency_limit field.

            This field is a member of `oneof`_ ``_min_effective_frequency``.
        effective_frequency_limit (google.ads.googleads.v9.services.types.EffectiveFrequencyLimit):
            The highest minimum effective frequency (the number of times
            a person was exposed to the ad) value [1-10] to include in
            Forecast.effective_frequency_breakdowns. If not specified,
            Forecast.effective_frequency_breakdowns will not be
            provided.

            The effective frequency value provided here will also be
            used as the minimum effective frequency for the reported
            reach metrics.

            This field cannot be combined with the
            min_effective_frequency field.

            This field is a member of `oneof`_ ``_effective_frequency_limit``.
        targeting (google.ads.googleads.v9.services.types.Targeting):
            The targeting to be applied to all products
            selected in the product mix.
            This is planned targeting: execution details
            might vary based on the advertising product,
            please consult an implementation specialist.
            See specific metrics for details on how
            targeting affects them.
        planned_products (Sequence[google.ads.googleads.v9.services.types.PlannedProduct]):
            Required. The products to be forecast.
            The max number of allowed planned products is
            15.
    """

    customer_id = proto.Field(proto.STRING, number=1,)
    currency_code = proto.Field(proto.STRING, number=9, optional=True,)
    campaign_duration = proto.Field(
        proto.MESSAGE, number=3, message="CampaignDuration",
    )
    cookie_frequency_cap = proto.Field(proto.INT32, number=10, optional=True,)
    cookie_frequency_cap_setting = proto.Field(
        proto.MESSAGE, number=8, message="FrequencyCap",
    )
    min_effective_frequency = proto.Field(
        proto.INT32, number=11, optional=True,
    )
    effective_frequency_limit = proto.Field(
        proto.MESSAGE,
        number=12,
        optional=True,
        message="EffectiveFrequencyLimit",
    )
    targeting = proto.Field(proto.MESSAGE, number=6, message="Targeting",)
    planned_products = proto.RepeatedField(
        proto.MESSAGE, number=7, message="PlannedProduct",
    )


class EffectiveFrequencyLimit(proto.Message):
    r"""Effective frequency limit.

    Attributes:
        effective_frequency_breakdown_limit (int):
            The highest effective frequency value to include in
            Forecast.effective_frequency_breakdowns. This field supports
            frequencies 1-10, inclusive.
    """

    effective_frequency_breakdown_limit = proto.Field(proto.INT32, number=1,)


class FrequencyCap(proto.Message):
    r"""A rule specifying the maximum number of times an ad can be
    shown to a user over a particular time period.

    Attributes:
        impressions (int):
            Required. The number of impressions,
            inclusive.
        time_unit (google.ads.googleads.v9.enums.types.FrequencyCapTimeUnitEnum.FrequencyCapTimeUnit):
            Required. The type of time unit.
    """

    impressions = proto.Field(proto.INT32, number=3,)
    time_unit = proto.Field(
        proto.ENUM,
        number=2,
        enum=frequency_cap_time_unit.FrequencyCapTimeUnitEnum.FrequencyCapTimeUnit,
    )


class Targeting(proto.Message):
    r"""The targeting for which traffic metrics will be reported.

    Attributes:
        plannable_location_id (str):
            Required. The ID of the selected location. Plannable
            location IDs can be obtained from
            [ReachPlanService.ListPlannableLocations][google.ads.googleads.v9.services.ReachPlanService.ListPlannableLocations].

            This field is a member of `oneof`_ ``_plannable_location_id``.
        age_range (google.ads.googleads.v9.enums.types.ReachPlanAgeRangeEnum.ReachPlanAgeRange):
            Targeted age range.
            An unset value is equivalent to targeting all
            ages.
        genders (Sequence[google.ads.googleads.v9.common.types.GenderInfo]):
            Targeted genders.
            An unset value is equivalent to targeting MALE
            and FEMALE.
        devices (Sequence[google.ads.googleads.v9.common.types.DeviceInfo]):
            Targeted devices. If not specified, targets all applicable
            devices. Applicable devices vary by product and region and
            can be obtained from
            [ReachPlanService.ListPlannableProducts][google.ads.googleads.v9.services.ReachPlanService.ListPlannableProducts].
        network (google.ads.googleads.v9.enums.types.ReachPlanNetworkEnum.ReachPlanNetwork):
            Targetable network for the ad product. If not specified,
            targets all applicable networks. Applicable networks vary by
            product and region and can be obtained from
            [ReachPlanService.ListPlannableProducts][google.ads.googleads.v9.services.ReachPlanService.ListPlannableProducts].
    """

    plannable_location_id = proto.Field(proto.STRING, number=6, optional=True,)
    age_range = proto.Field(
        proto.ENUM,
        number=2,
        enum=reach_plan_age_range.ReachPlanAgeRangeEnum.ReachPlanAgeRange,
    )
    genders = proto.RepeatedField(
        proto.MESSAGE, number=3, message=criteria.GenderInfo,
    )
    devices = proto.RepeatedField(
        proto.MESSAGE, number=4, message=criteria.DeviceInfo,
    )
    network = proto.Field(
        proto.ENUM,
        number=5,
        enum=reach_plan_network.ReachPlanNetworkEnum.ReachPlanNetwork,
    )


class CampaignDuration(proto.Message):
    r"""The duration of a planned campaign.

    Attributes:
        duration_in_days (int):
            The duration value in days.

            This field cannot be combined with the date_range field.

            This field is a member of `oneof`_ ``_duration_in_days``.
        date_range (google.ads.googleads.v9.common.types.DateRange):
            Date range of the campaign. Dates are in the yyyy-mm-dd
            format and inclusive. The end date must be < 1 year in the
            future and the date range must be <= 92 days long.

            This field cannot be combined with the duration_in_days
            field.
    """

    duration_in_days = proto.Field(proto.INT32, number=2, optional=True,)
    date_range = proto.Field(proto.MESSAGE, number=3, message=dates.DateRange,)


class PlannedProduct(proto.Message):
    r"""A product being planned for reach.

    Attributes:
        plannable_product_code (str):
            Required. Selected product for planning. The code associated
            with the ad product. E.g. Trueview, Bumper To list the
            available plannable product codes use
            [ReachPlanService.ListPlannableProducts][google.ads.googleads.v9.services.ReachPlanService.ListPlannableProducts].

            This field is a member of `oneof`_ ``_plannable_product_code``.
        budget_micros (int):
            Required. Maximum budget allocation in micros for the
            selected product. The value is specified in the selected
            planning currency_code. E.g. 1 000 000$ = 1 000 000 000 000
            micros.

            This field is a member of `oneof`_ ``_budget_micros``.
    """

    plannable_product_code = proto.Field(proto.STRING, number=3, optional=True,)
    budget_micros = proto.Field(proto.INT64, number=4, optional=True,)


class GenerateReachForecastResponse(proto.Message):
    r"""Response message containing the generated reach curve.

    Attributes:
        on_target_audience_metrics (google.ads.googleads.v9.services.types.OnTargetAudienceMetrics):
            Reference on target audiences for this curve.
        reach_curve (google.ads.googleads.v9.services.types.ReachCurve):
            The generated reach curve for the planned
            product mix.
    """

    on_target_audience_metrics = proto.Field(
        proto.MESSAGE, number=1, message="OnTargetAudienceMetrics",
    )
    reach_curve = proto.Field(proto.MESSAGE, number=2, message="ReachCurve",)


class ReachCurve(proto.Message):
    r"""The reach curve for the planned products.

    Attributes:
        reach_forecasts (Sequence[google.ads.googleads.v9.services.types.ReachForecast]):
            All points on the reach curve.
    """

    reach_forecasts = proto.RepeatedField(
        proto.MESSAGE, number=1, message="ReachForecast",
    )


class ReachForecast(proto.Message):
    r"""A point on reach curve.

    Attributes:
        cost_micros (int):
            The cost in micros.
        forecast (google.ads.googleads.v9.services.types.Forecast):
            Forecasted traffic metrics for this point.
        planned_product_reach_forecasts (Sequence[google.ads.googleads.v9.services.types.PlannedProductReachForecast]):
            The forecasted allocation and traffic metrics
            for each planned product at this point on the
            reach curve.
    """

    cost_micros = proto.Field(proto.INT64, number=5,)
    forecast = proto.Field(proto.MESSAGE, number=2, message="Forecast",)
    planned_product_reach_forecasts = proto.RepeatedField(
        proto.MESSAGE, number=4, message="PlannedProductReachForecast",
    )


class Forecast(proto.Message):
    r"""Forecasted traffic metrics for the planned products and
    targeting.

    Attributes:
        on_target_reach (int):
            Number of unique people reached at least
            GenerateReachForecastRequest.min_effective_frequency or
            GenerateReachForecastRequest.effective_frequency_limit times
            that exactly matches the Targeting.

            Note that a minimum number of unique people must be reached
            in order for data to be reported. If the minimum number is
            not met, the on_target_reach value will be rounded to 0.

            This field is a member of `oneof`_ ``_on_target_reach``.
        total_reach (int):
            Total number of unique people reached at least
            GenerateReachForecastRequest.min_effective_frequency or
            GenerateReachForecastRequest.effective_frequency_limit
            times. This includes people that may fall outside the
            specified Targeting.

            Note that a minimum number of unique people must be reached
            in order for data to be reported. If the minimum number is
            not met, the total_reach value will be rounded to 0.

            This field is a member of `oneof`_ ``_total_reach``.
        on_target_impressions (int):
            Number of ad impressions that exactly matches
            the Targeting.

            This field is a member of `oneof`_ ``_on_target_impressions``.
        total_impressions (int):
            Total number of ad impressions. This includes
            impressions that may fall outside the specified
            Targeting, due to insufficient information on
            signed-in users.

            This field is a member of `oneof`_ ``_total_impressions``.
        viewable_impressions (int):
            Number of times the ad's impressions were
            considered viewable. See
            https://support.google.com/google-
            ads/answer/7029393 for more information about
            what makes an ad viewable and how viewability is
            measured.

            This field is a member of `oneof`_ ``_viewable_impressions``.
        effective_frequency_breakdowns (Sequence[google.ads.googleads.v9.services.types.EffectiveFrequencyBreakdown]):
            A list of effective frequency forecasts. The list is ordered
            starting with 1+ and ending with the value set in
            GenerateReachForecastRequest.effective_frequency_limit. If
            no effective_frequency_limit was set, this list will be
            empty.
    """

    on_target_reach = proto.Field(proto.INT64, number=5, optional=True,)
    total_reach = proto.Field(proto.INT64, number=6, optional=True,)
    on_target_impressions = proto.Field(proto.INT64, number=7, optional=True,)
    total_impressions = proto.Field(proto.INT64, number=8, optional=True,)
    viewable_impressions = proto.Field(proto.INT64, number=9, optional=True,)
    effective_frequency_breakdowns = proto.RepeatedField(
        proto.MESSAGE, number=10, message="EffectiveFrequencyBreakdown",
    )


class PlannedProductReachForecast(proto.Message):
    r"""The forecasted allocation and traffic metrics for a specific
    product at a point on the reach curve.

    Attributes:
        plannable_product_code (str):
            Selected product for planning. The product
            codes returned are within the set of the ones
            returned by ListPlannableProducts when using the
            same location ID.
        cost_micros (int):
            The cost in micros. This may differ from the
            product's input allocation if one or more
            planned products cannot fulfill the budget
            because of limited inventory.
        planned_product_forecast (google.ads.googleads.v9.services.types.PlannedProductForecast):
            Forecasted traffic metrics for this product.
    """

    plannable_product_code = proto.Field(proto.STRING, number=1,)
    cost_micros = proto.Field(proto.INT64, number=2,)
    planned_product_forecast = proto.Field(
        proto.MESSAGE, number=3, message="PlannedProductForecast",
    )


class PlannedProductForecast(proto.Message):
    r"""Forecasted traffic metrics for a planned product.

    Attributes:
        on_target_reach (int):
            Number of unique people reached that exactly matches the
            Targeting.

            Note that a minimum number of unique people must be reached
            in order for data to be reported. If the minimum number is
            not met, the on_target_reach value will be rounded to 0.
        total_reach (int):
            Number of unique people reached. This includes people that
            may fall outside the specified Targeting.

            Note that a minimum number of unique people must be reached
            in order for data to be reported. If the minimum number is
            not met, the total_reach value will be rounded to 0.
        on_target_impressions (int):
            Number of ad impressions that exactly matches
            the Targeting.
        total_impressions (int):
            Total number of ad impressions. This includes
            impressions that may fall outside the specified
            Targeting, due to insufficient information on
            signed-in users.
        viewable_impressions (int):
            Number of times the ad's impressions were
            considered viewable. See
            https://support.google.com/google-
            ads/answer/7029393 for more information about
            what makes an ad viewable and how viewability is
            measured.

            This field is a member of `oneof`_ ``_viewable_impressions``.
    """

    on_target_reach = proto.Field(proto.INT64, number=1,)
    total_reach = proto.Field(proto.INT64, number=2,)
    on_target_impressions = proto.Field(proto.INT64, number=3,)
    total_impressions = proto.Field(proto.INT64, number=4,)
    viewable_impressions = proto.Field(proto.INT64, number=5, optional=True,)


class OnTargetAudienceMetrics(proto.Message):
    r"""Audience metrics for the planned products.
    These metrics consider the following targeting dimensions:
    - Location
    - PlannableAgeRange
    - Gender

    Attributes:
        youtube_audience_size (int):
            Reference audience size matching the
            considered targeting for YouTube.

            This field is a member of `oneof`_ ``_youtube_audience_size``.
        census_audience_size (int):
            Reference audience size matching the
            considered targeting for Census.

            This field is a member of `oneof`_ ``_census_audience_size``.
    """

    youtube_audience_size = proto.Field(proto.INT64, number=3, optional=True,)
    census_audience_size = proto.Field(proto.INT64, number=4, optional=True,)


class EffectiveFrequencyBreakdown(proto.Message):
    r"""A breakdown of the number of unique people reached at a given
    effective frequency.

    Attributes:
        effective_frequency (int):
            The effective frequency [1-10].
        on_target_reach (int):
            The number of unique people reached at least
            effective_frequency times that exactly matches the
            Targeting.

            Note that a minimum number of unique people must be reached
            in order for data to be reported. If the minimum number is
            not met, the on_target_reach value will be rounded to 0.
        total_reach (int):
            Total number of unique people reached at least
            effective_frequency times. This includes people that may
            fall outside the specified Targeting.

            Note that a minimum number of unique people must be reached
            in order for data to be reported. If the minimum number is
            not met, the total_reach value will be rounded to 0.
    """

    effective_frequency = proto.Field(proto.INT32, number=1,)
    on_target_reach = proto.Field(proto.INT64, number=2,)
    total_reach = proto.Field(proto.INT64, number=3,)


__all__ = tuple(sorted(__protobuf__.manifest))
