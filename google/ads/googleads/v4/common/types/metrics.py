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


from google.ads.googleads.v4.enums.types import interaction_event_type
from google.ads.googleads.v4.enums.types import quality_score_bucket
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.common",
    marshal="google.ads.googleads.v4",
    manifest={"Metrics",},
)


class Metrics(proto.Message):
    r"""Metrics data.

    Attributes:
        absolute_top_impression_percentage (google.protobuf.wrappers_pb2.DoubleValue):
            The percent of your ad impressions that are
            shown as the very first ad above the organic
            search results.
        active_view_cpm (google.protobuf.wrappers_pb2.DoubleValue):
            Average cost of viewable impressions
            (``active_view_impressions``).
        active_view_ctr (google.protobuf.wrappers_pb2.DoubleValue):
            Active view measurable clicks divided by
            active view viewable impressions. This metric is
            reported only for display network.
        active_view_impressions (google.protobuf.wrappers_pb2.Int64Value):
            A measurement of how often your ad has become
            viewable on a Display Network site.
        active_view_measurability (google.protobuf.wrappers_pb2.DoubleValue):
            The ratio of impressions that could be
            measured by Active View over the number of
            served impressions.
        active_view_measurable_cost_micros (google.protobuf.wrappers_pb2.Int64Value):
            The cost of the impressions you received that
            were measurable by Active View.
        active_view_measurable_impressions (google.protobuf.wrappers_pb2.Int64Value):
            The number of times your ads are appearing on
            placements in positions where they can be seen.
        active_view_viewability (google.protobuf.wrappers_pb2.DoubleValue):
            The percentage of time when your ad appeared
            on an Active View enabled site (measurable
            impressions) and was viewable (viewable
            impressions).
        all_conversions_from_interactions_rate (google.protobuf.wrappers_pb2.DoubleValue):
            All conversions from interactions (as oppose
            to view through conversions) divided by the
            number of ad interactions.
        all_conversions_value (google.protobuf.wrappers_pb2.DoubleValue):
            The value of all conversions.
        all_conversions (google.protobuf.wrappers_pb2.DoubleValue):
            The total number of conversions. This includes all
            conversions regardless of the value of
            include_in_conversions_metric.
        all_conversions_value_per_cost (google.protobuf.wrappers_pb2.DoubleValue):
            The value of all conversions divided by the
            total cost of ad interactions (such as clicks
            for text ads or views for video ads).
        all_conversions_from_click_to_call (google.protobuf.wrappers_pb2.DoubleValue):
            The number of times people clicked the "Call"
            button to call a store during or after clicking
            an ad. This number doesn't include whether or
            not calls were connected, or the duration of any
            calls. This metric applies to feed items only.
        all_conversions_from_directions (google.protobuf.wrappers_pb2.DoubleValue):
            The number of times people clicked a "Get
            directions" button to navigate to a store after
            clicking an ad. This metric applies to feed
            items only.
        all_conversions_from_interactions_value_per_interaction (google.protobuf.wrappers_pb2.DoubleValue):
            The value of all conversions from
            interactions divided by the total number of
            interactions.
        all_conversions_from_menu (google.protobuf.wrappers_pb2.DoubleValue):
            The number of times people clicked a link to
            view a store's menu after clicking an ad.
            This metric applies to feed items only.
        all_conversions_from_order (google.protobuf.wrappers_pb2.DoubleValue):
            The number of times people placed an order at
            a store after clicking an ad. This metric
            applies to feed items only.
        all_conversions_from_other_engagement (google.protobuf.wrappers_pb2.DoubleValue):
            The number of other conversions (for example,
            posting a review or saving a location for a
            store) that occurred after people clicked an ad.
            This metric applies to feed items only.
        all_conversions_from_store_visit (google.protobuf.wrappers_pb2.DoubleValue):
            Estimated number of times people visited a
            store after clicking an ad. This metric applies
            to feed items only.
        all_conversions_from_store_website (google.protobuf.wrappers_pb2.DoubleValue):
            The number of times that people were taken to
            a store's URL after clicking an ad.
            This metric applies to feed items only.
        average_cost (google.protobuf.wrappers_pb2.DoubleValue):
            The average amount you pay per interaction.
            This amount is the total cost of your ads
            divided by the total number of interactions.
        average_cpc (google.protobuf.wrappers_pb2.DoubleValue):
            The total cost of all clicks divided by the
            total number of clicks received.
        average_cpe (google.protobuf.wrappers_pb2.DoubleValue):
            The average amount that you've been charged
            for an ad engagement. This amount is the total
            cost of all ad engagements divided by the total
            number of ad engagements.
        average_cpm (google.protobuf.wrappers_pb2.DoubleValue):
            Average cost-per-thousand impressions (CPM).
        average_cpv (google.protobuf.wrappers_pb2.DoubleValue):
            The average amount you pay each time someone
            views your ad. The average CPV is defined by the
            total cost of all ad views divided by the number
            of views.
        average_page_views (google.protobuf.wrappers_pb2.DoubleValue):
            Average number of pages viewed per session.
        average_time_on_site (google.protobuf.wrappers_pb2.DoubleValue):
            Total duration of all sessions (in seconds) /
            number of sessions. Imported from Google
            Analytics.
        benchmark_average_max_cpc (google.protobuf.wrappers_pb2.DoubleValue):
            An indication of how other advertisers are
            bidding on similar products.
        benchmark_ctr (google.protobuf.wrappers_pb2.DoubleValue):
            An indication on how other advertisers'
            Shopping ads for similar products are performing
            based on how often people who see their ad click
            on it.
        bounce_rate (google.protobuf.wrappers_pb2.DoubleValue):
            Percentage of clicks where the user only
            visited a single page on your site. Imported
            from Google Analytics.
        clicks (google.protobuf.wrappers_pb2.Int64Value):
            The number of clicks.
        combined_clicks (google.protobuf.wrappers_pb2.Int64Value):
            The number of times your ad or your site's
            listing in the unpaid results was clicked. See
            the help page at
            https://support.google.com/google-
            ads/answer/3097241 for details.
        combined_clicks_per_query (google.protobuf.wrappers_pb2.DoubleValue):
            The number of times your ad or your site's listing in the
            unpaid results was clicked (combined_clicks) divided by
            combined_queries. See the help page at
            https://support.google.com/google-ads/answer/3097241 for
            details.
        combined_queries (google.protobuf.wrappers_pb2.Int64Value):
            The number of searches that returned pages
            from your site in the unpaid results or showed
            one of your text ads. See the help page at
            https://support.google.com/google-
            ads/answer/3097241 for details.
        content_budget_lost_impression_share (google.protobuf.wrappers_pb2.DoubleValue):
            The estimated percent of times that your ad
            was eligible to show on the Display Network but
            didn't because your budget was too low. Note:
            Content budget lost impression share is reported
            in the range of 0 to 0.9. Any value above 0.9 is
            reported as 0.9001.
        content_impression_share (google.protobuf.wrappers_pb2.DoubleValue):
            The impressions you've received on the
            Display Network divided by the estimated number
            of impressions you were eligible to receive.
            Note: Content impression share is reported in
            the range of 0.1 to 1. Any value below 0.1 is
            reported as 0.0999.
        conversion_last_received_request_date_time (google.protobuf.wrappers_pb2.StringValue):
            The last date/time a conversion tag for this
            conversion action successfully fired and was
            seen by Google Ads. This firing event may not
            have been the result of an attributable
            conversion (e.g. because the tag was fired from
            a browser that did not previously click an ad
            from an appropriate advertiser). The date/time
            is in the customer's time zone.
        conversion_last_conversion_date (google.protobuf.wrappers_pb2.StringValue):
            The date of the most recent conversion for
            this conversion action. The date is in the
            customer's time zone.
        content_rank_lost_impression_share (google.protobuf.wrappers_pb2.DoubleValue):
            The estimated percentage of impressions on
            the Display Network that your ads didn't receive
            due to poor Ad Rank. Note: Content rank lost
            impression share is reported in the range of 0
            to 0.9. Any value above 0.9 is reported as
            0.9001.
        conversions_from_interactions_rate (google.protobuf.wrappers_pb2.DoubleValue):
            Conversions from interactions divided by the number of ad
            interactions (such as clicks for text ads or views for video
            ads). This only includes conversion actions which
            include_in_conversions_metric attribute is set to true. If
            you use conversion-based bidding, your bid strategies will
            optimize for these conversions.
        conversions_value (google.protobuf.wrappers_pb2.DoubleValue):
            The value of conversions. This only includes conversion
            actions which include_in_conversions_metric attribute is set
            to true. If you use conversion-based bidding, your bid
            strategies will optimize for these conversions.
        conversions_value_per_cost (google.protobuf.wrappers_pb2.DoubleValue):
            The value of conversions divided by the cost of ad
            interactions. This only includes conversion actions which
            include_in_conversions_metric attribute is set to true. If
            you use conversion-based bidding, your bid strategies will
            optimize for these conversions.
        conversions_from_interactions_value_per_interaction (google.protobuf.wrappers_pb2.DoubleValue):
            The value of conversions from interactions divided by the
            number of ad interactions. This only includes conversion
            actions which include_in_conversions_metric attribute is set
            to true. If you use conversion-based bidding, your bid
            strategies will optimize for these conversions.
        conversions (google.protobuf.wrappers_pb2.DoubleValue):
            The number of conversions. This only includes conversion
            actions which include_in_conversions_metric attribute is set
            to true. If you use conversion-based bidding, your bid
            strategies will optimize for these conversions.
        cost_micros (google.protobuf.wrappers_pb2.Int64Value):
            The sum of your cost-per-click (CPC) and
            cost-per-thousand impressions (CPM) costs during
            this period.
        cost_per_all_conversions (google.protobuf.wrappers_pb2.DoubleValue):
            The cost of ad interactions divided by all
            conversions.
        cost_per_conversion (google.protobuf.wrappers_pb2.DoubleValue):
            The cost of ad interactions divided by conversions. This
            only includes conversion actions which
            include_in_conversions_metric attribute is set to true. If
            you use conversion-based bidding, your bid strategies will
            optimize for these conversions.
        cost_per_current_model_attributed_conversion (google.protobuf.wrappers_pb2.DoubleValue):
            The cost of ad interactions divided by current model
            attributed conversions. This only includes conversion
            actions which include_in_conversions_metric attribute is set
            to true. If you use conversion-based bidding, your bid
            strategies will optimize for these conversions.
        cross_device_conversions (google.protobuf.wrappers_pb2.DoubleValue):
            Conversions from when a customer clicks on a Google Ads ad
            on one device, then converts on a different device or
            browser. Cross-device conversions are already included in
            all_conversions.
        ctr (google.protobuf.wrappers_pb2.DoubleValue):
            The number of clicks your ad receives
            (Clicks) divided by the number of times your ad
            is shown (Impressions).
        current_model_attributed_conversions (google.protobuf.wrappers_pb2.DoubleValue):
            Shows how your historic conversions data would look under
            the attribution model you've currently selected. This only
            includes conversion actions which
            include_in_conversions_metric attribute is set to true. If
            you use conversion-based bidding, your bid strategies will
            optimize for these conversions.
        current_model_attributed_conversions_from_interactions_rate (google.protobuf.wrappers_pb2.DoubleValue):
            Current model attributed conversions from interactions
            divided by the number of ad interactions (such as clicks for
            text ads or views for video ads). This only includes
            conversion actions which include_in_conversions_metric
            attribute is set to true. If you use conversion-based
            bidding, your bid strategies will optimize for these
            conversions.
        current_model_attributed_conversions_from_interactions_value_per_interaction (google.protobuf.wrappers_pb2.DoubleValue):
            The value of current model attributed conversions from
            interactions divided by the number of ad interactions. This
            only includes conversion actions which
            include_in_conversions_metric attribute is set to true. If
            you use conversion-based bidding, your bid strategies will
            optimize for these conversions.
        current_model_attributed_conversions_value (google.protobuf.wrappers_pb2.DoubleValue):
            The value of current model attributed conversions. This only
            includes conversion actions which
            include_in_conversions_metric attribute is set to true. If
            you use conversion-based bidding, your bid strategies will
            optimize for these conversions.
        current_model_attributed_conversions_value_per_cost (google.protobuf.wrappers_pb2.DoubleValue):
            The value of current model attributed conversions divided by
            the cost of ad interactions. This only includes conversion
            actions which include_in_conversions_metric attribute is set
            to true. If you use conversion-based bidding, your bid
            strategies will optimize for these conversions.
        engagement_rate (google.protobuf.wrappers_pb2.DoubleValue):
            How often people engage with your ad after
            it's shown to them. This is the number of ad
            expansions divided by the number of times your
            ad is shown.
        engagements (google.protobuf.wrappers_pb2.Int64Value):
            The number of engagements.
            An engagement occurs when a viewer expands your
            Lightbox ad. Also, in the future, other ad types
            may support engagement metrics.
        hotel_average_lead_value_micros (google.protobuf.wrappers_pb2.DoubleValue):
            Average lead value based on clicks.
        hotel_price_difference_percentage (google.protobuf.wrappers_pb2.DoubleValue):
            The average price difference between the
            price offered by reporting hotel advertiser and
            the cheapest price offered by the competing
            advertiser.
        hotel_eligible_impressions (google.protobuf.wrappers_pb2.Int64Value):
            The number of impressions that hotel partners
            could have had given their feed performance.
        historical_creative_quality_score (google.ads.googleads.v4.enums.types.QualityScoreBucketEnum.QualityScoreBucket):
            The creative historical quality score.
        historical_landing_page_quality_score (google.ads.googleads.v4.enums.types.QualityScoreBucketEnum.QualityScoreBucket):
            The quality of historical landing page
            experience.
        historical_quality_score (google.protobuf.wrappers_pb2.Int64Value):
            The historical quality score.
        historical_search_predicted_ctr (google.ads.googleads.v4.enums.types.QualityScoreBucketEnum.QualityScoreBucket):
            The historical search predicted click through
            rate (CTR).
        gmail_forwards (google.protobuf.wrappers_pb2.Int64Value):
            The number of times the ad was forwarded to
            someone else as a message.
        gmail_saves (google.protobuf.wrappers_pb2.Int64Value):
            The number of times someone has saved your
            Gmail ad to their inbox as a message.
        gmail_secondary_clicks (google.protobuf.wrappers_pb2.Int64Value):
            The number of clicks to the landing page on
            the expanded state of Gmail ads.
        impressions_from_store_reach (google.protobuf.wrappers_pb2.Int64Value):
            The number of times a store's location-based
            ad was shown. This metric applies to feed items
            only.
        impressions (google.protobuf.wrappers_pb2.Int64Value):
            Count of how often your ad has appeared on a
            search results page or website on the Google
            Network.
        interaction_rate (google.protobuf.wrappers_pb2.DoubleValue):
            How often people interact with your ad after
            it is shown to them. This is the number of
            interactions divided by the number of times your
            ad is shown.
        interactions (google.protobuf.wrappers_pb2.Int64Value):
            The number of interactions.
            An interaction is the main user action
            associated with an ad format-clicks for text and
            shopping ads, views for video ads, and so on.
        interaction_event_types (Sequence[google.ads.googleads.v4.enums.types.InteractionEventTypeEnum.InteractionEventType]):
            The types of payable and free interactions.
        invalid_click_rate (google.protobuf.wrappers_pb2.DoubleValue):
            The percentage of clicks filtered out of your
            total number of clicks (filtered + non-filtered
            clicks) during the reporting period.
        invalid_clicks (google.protobuf.wrappers_pb2.Int64Value):
            Number of clicks Google considers
            illegitimate and doesn't charge you for.
        message_chats (google.protobuf.wrappers_pb2.Int64Value):
            Number of message chats initiated for Click
            To Message impressions that were message
            tracking eligible.
        message_impressions (google.protobuf.wrappers_pb2.Int64Value):
            Number of Click To Message impressions that
            were message tracking eligible.
        message_chat_rate (google.protobuf.wrappers_pb2.DoubleValue):
            Number of message chats initiated (message_chats) divided by
            the number of message impressions (message_impressions).
            Rate at which a user initiates a message chat from an ad
            impression with a messaging option and message tracking
            enabled. Note that this rate can be more than 1.0 for a
            given message impression.
        mobile_friendly_clicks_percentage (google.protobuf.wrappers_pb2.DoubleValue):
            The percentage of mobile clicks that go to a
            mobile-friendly page.
        organic_clicks (google.protobuf.wrappers_pb2.Int64Value):
            The number of times someone clicked your
            site's listing in the unpaid results for a
            particular query. See the help page at
            https://support.google.com/google-
            ads/answer/3097241 for details.
        organic_clicks_per_query (google.protobuf.wrappers_pb2.DoubleValue):
            The number of times someone clicked your site's listing in
            the unpaid results (organic_clicks) divided by the total
            number of searches that returned pages from your site
            (organic_queries). See the help page at
            https://support.google.com/google-ads/answer/3097241 for
            details.
        organic_impressions (google.protobuf.wrappers_pb2.Int64Value):
            The number of listings for your site in the
            unpaid search results. See the help page at
            https://support.google.com/google-
            ads/answer/3097241 for details.
        organic_impressions_per_query (google.protobuf.wrappers_pb2.DoubleValue):
            The number of times a page from your site was listed in the
            unpaid search results (organic_impressions) divided by the
            number of searches returning your site's listing in the
            unpaid results (organic_queries). See the help page at
            https://support.google.com/google-ads/answer/3097241 for
            details.
        organic_queries (google.protobuf.wrappers_pb2.Int64Value):
            The total number of searches that returned
            your site's listing in the unpaid results. See
            the help page at
            https://support.google.com/google-
            ads/answer/3097241 for details.
        percent_new_visitors (google.protobuf.wrappers_pb2.DoubleValue):
            Percentage of first-time sessions (from
            people who had never visited your site before).
            Imported from Google Analytics.
        phone_calls (google.protobuf.wrappers_pb2.Int64Value):
            Number of offline phone calls.
        phone_impressions (google.protobuf.wrappers_pb2.Int64Value):
            Number of offline phone impressions.
        phone_through_rate (google.protobuf.wrappers_pb2.DoubleValue):
            Number of phone calls received (phone_calls) divided by the
            number of times your phone number is shown
            (phone_impressions).
        relative_ctr (google.protobuf.wrappers_pb2.DoubleValue):
            Your clickthrough rate (Ctr) divided by the
            average clickthrough rate of all advertisers on
            the websites that show your ads. Measures how
            your ads perform on Display Network sites
            compared to other ads on the same sites.
        search_absolute_top_impression_share (google.protobuf.wrappers_pb2.DoubleValue):
            The percentage of the customer's Shopping or
            Search ad impressions that are shown in the most
            prominent Shopping position. See
            https://support.google.com/google-
            ads/answer/7501826 for details. Any value below
            0.1 is reported as 0.0999.
        search_budget_lost_absolute_top_impression_share (google.protobuf.wrappers_pb2.DoubleValue):
            The number estimating how often your ad
            wasn't the very first ad above the organic
            search results due to a low budget. Note: Search
            budget lost absolute top impression share is
            reported in the range of 0 to 0.9. Any value
            above 0.9 is reported as 0.9001.
        search_budget_lost_impression_share (google.protobuf.wrappers_pb2.DoubleValue):
            The estimated percent of times that your ad
            was eligible to show on the Search Network but
            didn't because your budget was too low. Note:
            Search budget lost impression share is reported
            in the range of 0 to 0.9. Any value above 0.9 is
            reported as 0.9001.
        search_budget_lost_top_impression_share (google.protobuf.wrappers_pb2.DoubleValue):
            The number estimating how often your ad
            didn't show anywhere above the organic search
            results due to a low budget. Note: Search budget
            lost top impression share is reported in the
            range of 0 to 0.9. Any value above 0.9 is
            reported as 0.9001.
        search_click_share (google.protobuf.wrappers_pb2.DoubleValue):
            The number of clicks you've received on the
            Search Network divided by the estimated number
            of clicks you were eligible to receive. Note:
            Search click share is reported in the range of
            0.1 to 1. Any value below 0.1 is reported as
            0.0999.
        search_exact_match_impression_share (google.protobuf.wrappers_pb2.DoubleValue):
            The impressions you've received divided by
            the estimated number of impressions you were
            eligible to receive on the Search Network for
            search terms that matched your keywords exactly
            (or were close variants of your keyword),
            regardless of your keyword match types. Note:
            Search exact match impression share is reported
            in the range of 0.1 to 1. Any value below 0.1 is
            reported as 0.0999.
        search_impression_share (google.protobuf.wrappers_pb2.DoubleValue):
            The impressions you've received on the Search
            Network divided by the estimated number of
            impressions you were eligible to receive. Note:
            Search impression share is reported in the range
            of 0.1 to 1. Any value below 0.1 is reported as
            0.0999.
        search_rank_lost_absolute_top_impression_share (google.protobuf.wrappers_pb2.DoubleValue):
            The number estimating how often your ad
            wasn't the very first ad above the organic
            search results due to poor Ad Rank. Note: Search
            rank lost absolute top impression share is
            reported in the range of 0 to 0.9. Any value
            above 0.9 is reported as 0.9001.
        search_rank_lost_impression_share (google.protobuf.wrappers_pb2.DoubleValue):
            The estimated percentage of impressions on
            the Search Network that your ads didn't receive
            due to poor Ad Rank. Note: Search rank lost
            impression share is reported in the range of 0
            to 0.9. Any value above 0.9 is reported as
            0.9001.
        search_rank_lost_top_impression_share (google.protobuf.wrappers_pb2.DoubleValue):
            The number estimating how often your ad
            didn't show anywhere above the organic search
            results due to poor Ad Rank. Note: Search rank
            lost top impression share is reported in the
            range of 0 to 0.9. Any value above 0.9 is
            reported as 0.9001.
        search_top_impression_share (google.protobuf.wrappers_pb2.DoubleValue):
            The impressions you've received in the top
            location (anywhere above the organic search
            results) compared to the estimated number of
            impressions you were eligible to receive in the
            top location. Note: Search top impression share
            is reported in the range of 0.1 to 1. Any value
            below 0.1 is reported as 0.0999.
        speed_score (google.protobuf.wrappers_pb2.Int64Value):
            A measure of how quickly your page loads
            after clicks on your mobile ads. The score is a
            range from 1 to 10, 10 being the fastest.
        top_impression_percentage (google.protobuf.wrappers_pb2.DoubleValue):
            The percent of your ad impressions that are
            shown anywhere above the organic search results.
        valid_accelerated_mobile_pages_clicks_percentage (google.protobuf.wrappers_pb2.DoubleValue):
            The percentage of ad clicks to Accelerated
            Mobile Pages (AMP) landing pages that reach a
            valid AMP page.
        value_per_all_conversions (google.protobuf.wrappers_pb2.DoubleValue):
            The value of all conversions divided by the
            number of all conversions.
        value_per_conversion (google.protobuf.wrappers_pb2.DoubleValue):
            The value of conversions divided by the number of
            conversions. This only includes conversion actions which
            include_in_conversions_metric attribute is set to true. If
            you use conversion-based bidding, your bid strategies will
            optimize for these conversions.
        value_per_current_model_attributed_conversion (google.protobuf.wrappers_pb2.DoubleValue):
            The value of current model attributed conversions divided by
            the number of the conversions. This only includes conversion
            actions which include_in_conversions_metric attribute is set
            to true. If you use conversion-based bidding, your bid
            strategies will optimize for these conversions.
        video_quartile_100_rate (google.protobuf.wrappers_pb2.DoubleValue):
            Percentage of impressions where the viewer
            watched all of your video.
        video_quartile_25_rate (google.protobuf.wrappers_pb2.DoubleValue):
            Percentage of impressions where the viewer
            watched 25% of your video.
        video_quartile_50_rate (google.protobuf.wrappers_pb2.DoubleValue):
            Percentage of impressions where the viewer
            watched 50% of your video.
        video_quartile_75_rate (google.protobuf.wrappers_pb2.DoubleValue):
            Percentage of impressions where the viewer
            watched 75% of your video.
        video_view_rate (google.protobuf.wrappers_pb2.DoubleValue):
            The number of views your TrueView video ad
            receives divided by its number of impressions,
            including thumbnail impressions for TrueView in-
            display ads.
        video_views (google.protobuf.wrappers_pb2.Int64Value):
            The number of times your video ads were
            viewed.
        view_through_conversions (google.protobuf.wrappers_pb2.Int64Value):
            The total number of view-through conversions.
            These happen when a customer sees an image or
            rich media ad, then later completes a conversion
            on your site without interacting with (e.g.,
            clicking on) another ad.
    """

    absolute_top_impression_percentage = proto.Field(
        proto.MESSAGE, number=95, message=wrappers.DoubleValue,
    )
    active_view_cpm = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.DoubleValue,
    )
    active_view_ctr = proto.Field(
        proto.MESSAGE, number=79, message=wrappers.DoubleValue,
    )
    active_view_impressions = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.Int64Value,
    )
    active_view_measurability = proto.Field(
        proto.MESSAGE, number=96, message=wrappers.DoubleValue,
    )
    active_view_measurable_cost_micros = proto.Field(
        proto.MESSAGE, number=3, message=wrappers.Int64Value,
    )
    active_view_measurable_impressions = proto.Field(
        proto.MESSAGE, number=4, message=wrappers.Int64Value,
    )
    active_view_viewability = proto.Field(
        proto.MESSAGE, number=97, message=wrappers.DoubleValue,
    )
    all_conversions_from_interactions_rate = proto.Field(
        proto.MESSAGE, number=65, message=wrappers.DoubleValue,
    )
    all_conversions_value = proto.Field(
        proto.MESSAGE, number=66, message=wrappers.DoubleValue,
    )
    all_conversions = proto.Field(
        proto.MESSAGE, number=7, message=wrappers.DoubleValue,
    )
    all_conversions_value_per_cost = proto.Field(
        proto.MESSAGE, number=62, message=wrappers.DoubleValue,
    )
    all_conversions_from_click_to_call = proto.Field(
        proto.MESSAGE, number=118, message=wrappers.DoubleValue,
    )
    all_conversions_from_directions = proto.Field(
        proto.MESSAGE, number=119, message=wrappers.DoubleValue,
    )
    all_conversions_from_interactions_value_per_interaction = proto.Field(
        proto.MESSAGE, number=67, message=wrappers.DoubleValue,
    )
    all_conversions_from_menu = proto.Field(
        proto.MESSAGE, number=120, message=wrappers.DoubleValue,
    )
    all_conversions_from_order = proto.Field(
        proto.MESSAGE, number=121, message=wrappers.DoubleValue,
    )
    all_conversions_from_other_engagement = proto.Field(
        proto.MESSAGE, number=122, message=wrappers.DoubleValue,
    )
    all_conversions_from_store_visit = proto.Field(
        proto.MESSAGE, number=123, message=wrappers.DoubleValue,
    )
    all_conversions_from_store_website = proto.Field(
        proto.MESSAGE, number=124, message=wrappers.DoubleValue,
    )
    average_cost = proto.Field(
        proto.MESSAGE, number=8, message=wrappers.DoubleValue,
    )
    average_cpc = proto.Field(
        proto.MESSAGE, number=9, message=wrappers.DoubleValue,
    )
    average_cpe = proto.Field(
        proto.MESSAGE, number=98, message=wrappers.DoubleValue,
    )
    average_cpm = proto.Field(
        proto.MESSAGE, number=10, message=wrappers.DoubleValue,
    )
    average_cpv = proto.Field(
        proto.MESSAGE, number=11, message=wrappers.DoubleValue,
    )
    average_page_views = proto.Field(
        proto.MESSAGE, number=99, message=wrappers.DoubleValue,
    )
    average_time_on_site = proto.Field(
        proto.MESSAGE, number=84, message=wrappers.DoubleValue,
    )
    benchmark_average_max_cpc = proto.Field(
        proto.MESSAGE, number=14, message=wrappers.DoubleValue,
    )
    benchmark_ctr = proto.Field(
        proto.MESSAGE, number=77, message=wrappers.DoubleValue,
    )
    bounce_rate = proto.Field(
        proto.MESSAGE, number=15, message=wrappers.DoubleValue,
    )
    clicks = proto.Field(proto.MESSAGE, number=19, message=wrappers.Int64Value,)
    combined_clicks = proto.Field(
        proto.MESSAGE, number=115, message=wrappers.Int64Value,
    )
    combined_clicks_per_query = proto.Field(
        proto.MESSAGE, number=116, message=wrappers.DoubleValue,
    )
    combined_queries = proto.Field(
        proto.MESSAGE, number=117, message=wrappers.Int64Value,
    )
    content_budget_lost_impression_share = proto.Field(
        proto.MESSAGE, number=20, message=wrappers.DoubleValue,
    )
    content_impression_share = proto.Field(
        proto.MESSAGE, number=21, message=wrappers.DoubleValue,
    )
    conversion_last_received_request_date_time = proto.Field(
        proto.MESSAGE, number=73, message=wrappers.StringValue,
    )
    conversion_last_conversion_date = proto.Field(
        proto.MESSAGE, number=74, message=wrappers.StringValue,
    )
    content_rank_lost_impression_share = proto.Field(
        proto.MESSAGE, number=22, message=wrappers.DoubleValue,
    )
    conversions_from_interactions_rate = proto.Field(
        proto.MESSAGE, number=69, message=wrappers.DoubleValue,
    )
    conversions_value = proto.Field(
        proto.MESSAGE, number=70, message=wrappers.DoubleValue,
    )
    conversions_value_per_cost = proto.Field(
        proto.MESSAGE, number=71, message=wrappers.DoubleValue,
    )
    conversions_from_interactions_value_per_interaction = proto.Field(
        proto.MESSAGE, number=72, message=wrappers.DoubleValue,
    )
    conversions = proto.Field(
        proto.MESSAGE, number=25, message=wrappers.DoubleValue,
    )
    cost_micros = proto.Field(
        proto.MESSAGE, number=26, message=wrappers.Int64Value,
    )
    cost_per_all_conversions = proto.Field(
        proto.MESSAGE, number=68, message=wrappers.DoubleValue,
    )
    cost_per_conversion = proto.Field(
        proto.MESSAGE, number=28, message=wrappers.DoubleValue,
    )
    cost_per_current_model_attributed_conversion = proto.Field(
        proto.MESSAGE, number=106, message=wrappers.DoubleValue,
    )
    cross_device_conversions = proto.Field(
        proto.MESSAGE, number=29, message=wrappers.DoubleValue,
    )
    ctr = proto.Field(proto.MESSAGE, number=30, message=wrappers.DoubleValue,)
    current_model_attributed_conversions = proto.Field(
        proto.MESSAGE, number=101, message=wrappers.DoubleValue,
    )
    current_model_attributed_conversions_from_interactions_rate = proto.Field(
        proto.MESSAGE, number=102, message=wrappers.DoubleValue,
    )
    current_model_attributed_conversions_from_interactions_value_per_interaction = proto.Field(
        proto.MESSAGE, number=103, message=wrappers.DoubleValue,
    )
    current_model_attributed_conversions_value = proto.Field(
        proto.MESSAGE, number=104, message=wrappers.DoubleValue,
    )
    current_model_attributed_conversions_value_per_cost = proto.Field(
        proto.MESSAGE, number=105, message=wrappers.DoubleValue,
    )
    engagement_rate = proto.Field(
        proto.MESSAGE, number=31, message=wrappers.DoubleValue,
    )
    engagements = proto.Field(
        proto.MESSAGE, number=32, message=wrappers.Int64Value,
    )
    hotel_average_lead_value_micros = proto.Field(
        proto.MESSAGE, number=75, message=wrappers.DoubleValue,
    )
    hotel_price_difference_percentage = proto.Field(
        proto.MESSAGE, number=129, message=wrappers.DoubleValue,
    )
    hotel_eligible_impressions = proto.Field(
        proto.MESSAGE, number=130, message=wrappers.Int64Value,
    )
    historical_creative_quality_score = proto.Field(
        proto.ENUM,
        number=80,
        enum=quality_score_bucket.QualityScoreBucketEnum.QualityScoreBucket,
    )
    historical_landing_page_quality_score = proto.Field(
        proto.ENUM,
        number=81,
        enum=quality_score_bucket.QualityScoreBucketEnum.QualityScoreBucket,
    )
    historical_quality_score = proto.Field(
        proto.MESSAGE, number=82, message=wrappers.Int64Value,
    )
    historical_search_predicted_ctr = proto.Field(
        proto.ENUM,
        number=83,
        enum=quality_score_bucket.QualityScoreBucketEnum.QualityScoreBucket,
    )
    gmail_forwards = proto.Field(
        proto.MESSAGE, number=85, message=wrappers.Int64Value,
    )
    gmail_saves = proto.Field(
        proto.MESSAGE, number=86, message=wrappers.Int64Value,
    )
    gmail_secondary_clicks = proto.Field(
        proto.MESSAGE, number=87, message=wrappers.Int64Value,
    )
    impressions_from_store_reach = proto.Field(
        proto.MESSAGE, number=125, message=wrappers.Int64Value,
    )
    impressions = proto.Field(
        proto.MESSAGE, number=37, message=wrappers.Int64Value,
    )
    interaction_rate = proto.Field(
        proto.MESSAGE, number=38, message=wrappers.DoubleValue,
    )
    interactions = proto.Field(
        proto.MESSAGE, number=39, message=wrappers.Int64Value,
    )
    interaction_event_types = proto.RepeatedField(
        proto.ENUM,
        number=100,
        enum=interaction_event_type.InteractionEventTypeEnum.InteractionEventType,
    )
    invalid_click_rate = proto.Field(
        proto.MESSAGE, number=40, message=wrappers.DoubleValue,
    )
    invalid_clicks = proto.Field(
        proto.MESSAGE, number=41, message=wrappers.Int64Value,
    )
    message_chats = proto.Field(
        proto.MESSAGE, number=126, message=wrappers.Int64Value,
    )
    message_impressions = proto.Field(
        proto.MESSAGE, number=127, message=wrappers.Int64Value,
    )
    message_chat_rate = proto.Field(
        proto.MESSAGE, number=128, message=wrappers.DoubleValue,
    )
    mobile_friendly_clicks_percentage = proto.Field(
        proto.MESSAGE, number=109, message=wrappers.DoubleValue,
    )
    organic_clicks = proto.Field(
        proto.MESSAGE, number=110, message=wrappers.Int64Value,
    )
    organic_clicks_per_query = proto.Field(
        proto.MESSAGE, number=111, message=wrappers.DoubleValue,
    )
    organic_impressions = proto.Field(
        proto.MESSAGE, number=112, message=wrappers.Int64Value,
    )
    organic_impressions_per_query = proto.Field(
        proto.MESSAGE, number=113, message=wrappers.DoubleValue,
    )
    organic_queries = proto.Field(
        proto.MESSAGE, number=114, message=wrappers.Int64Value,
    )
    percent_new_visitors = proto.Field(
        proto.MESSAGE, number=42, message=wrappers.DoubleValue,
    )
    phone_calls = proto.Field(
        proto.MESSAGE, number=43, message=wrappers.Int64Value,
    )
    phone_impressions = proto.Field(
        proto.MESSAGE, number=44, message=wrappers.Int64Value,
    )
    phone_through_rate = proto.Field(
        proto.MESSAGE, number=45, message=wrappers.DoubleValue,
    )
    relative_ctr = proto.Field(
        proto.MESSAGE, number=46, message=wrappers.DoubleValue,
    )
    search_absolute_top_impression_share = proto.Field(
        proto.MESSAGE, number=78, message=wrappers.DoubleValue,
    )
    search_budget_lost_absolute_top_impression_share = proto.Field(
        proto.MESSAGE, number=88, message=wrappers.DoubleValue,
    )
    search_budget_lost_impression_share = proto.Field(
        proto.MESSAGE, number=47, message=wrappers.DoubleValue,
    )
    search_budget_lost_top_impression_share = proto.Field(
        proto.MESSAGE, number=89, message=wrappers.DoubleValue,
    )
    search_click_share = proto.Field(
        proto.MESSAGE, number=48, message=wrappers.DoubleValue,
    )
    search_exact_match_impression_share = proto.Field(
        proto.MESSAGE, number=49, message=wrappers.DoubleValue,
    )
    search_impression_share = proto.Field(
        proto.MESSAGE, number=50, message=wrappers.DoubleValue,
    )
    search_rank_lost_absolute_top_impression_share = proto.Field(
        proto.MESSAGE, number=90, message=wrappers.DoubleValue,
    )
    search_rank_lost_impression_share = proto.Field(
        proto.MESSAGE, number=51, message=wrappers.DoubleValue,
    )
    search_rank_lost_top_impression_share = proto.Field(
        proto.MESSAGE, number=91, message=wrappers.DoubleValue,
    )
    search_top_impression_share = proto.Field(
        proto.MESSAGE, number=92, message=wrappers.DoubleValue,
    )
    speed_score = proto.Field(
        proto.MESSAGE, number=107, message=wrappers.Int64Value,
    )
    top_impression_percentage = proto.Field(
        proto.MESSAGE, number=93, message=wrappers.DoubleValue,
    )
    valid_accelerated_mobile_pages_clicks_percentage = proto.Field(
        proto.MESSAGE, number=108, message=wrappers.DoubleValue,
    )
    value_per_all_conversions = proto.Field(
        proto.MESSAGE, number=52, message=wrappers.DoubleValue,
    )
    value_per_conversion = proto.Field(
        proto.MESSAGE, number=53, message=wrappers.DoubleValue,
    )
    value_per_current_model_attributed_conversion = proto.Field(
        proto.MESSAGE, number=94, message=wrappers.DoubleValue,
    )
    video_quartile_100_rate = proto.Field(
        proto.MESSAGE, number=54, message=wrappers.DoubleValue,
    )
    video_quartile_25_rate = proto.Field(
        proto.MESSAGE, number=55, message=wrappers.DoubleValue,
    )
    video_quartile_50_rate = proto.Field(
        proto.MESSAGE, number=56, message=wrappers.DoubleValue,
    )
    video_quartile_75_rate = proto.Field(
        proto.MESSAGE, number=57, message=wrappers.DoubleValue,
    )
    video_view_rate = proto.Field(
        proto.MESSAGE, number=58, message=wrappers.DoubleValue,
    )
    video_views = proto.Field(
        proto.MESSAGE, number=59, message=wrappers.Int64Value,
    )
    view_through_conversions = proto.Field(
        proto.MESSAGE, number=60, message=wrappers.Int64Value,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
