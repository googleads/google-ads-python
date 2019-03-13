# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This example generates keyword ideas from a list of seed keywords."""

from __future__ import absolute_import

import argparse
import six
import sys
from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException

_DEFAULT_LOCATION_IDS = '1023191' # location ID for New York, NY
_DEFAULT_LANGUAGE_ID = '1000' # language ID for English


def main(client, customer_id, location_ids, language_id, keywords, page_url):
    keyword_plan_idea_service = client.get_service('KeywordPlanIdeaService',
                                                   version='v1')
    keyword_competition_level_enum = (
        client.get_type('KeywordPlanCompetitionLevelEnum', version='v1')
            .KeywordPlanCompetitionLevel)
    keyword_plan_network = client.get_type(
        'KeywordPlanNetworkEnum', version='v1').GOOGLE_SEARCH_AND_PARTNERS
    locations = map_locations_to_string_values(client, location_ids)
    language = map_language_to_string_value(client, language_id)

    # Only one of these values will be passed to the KeywordPlanIdeaService
    # depending on whether keywords, a page_url or both were given.
    url_seed = None
    keyword_seed = None
    keyword_url_seed = None

    if (not len(keywords) and not page_url):
        raise ValueError('At least one of keywords or page URL is required, '
                         'but neither was specified.')
    elif (not len(keywords) and page_url):
        url_seed = client.get_type('UrlSeed', version='v1')
        url_seed.url.value = page_url
    elif (len(keywords) and not page_url):
        keyword_seed = client.get_type('KeywordSeed', version='v1')
        keyword_protos = map_keywords_to_string_values(client, keywords)
        keyword_seed.keywords.extend(keyword_protos)
    else:
        keyword_url_seed = client.get_type('KeywordAndUrlSeed', version='v1')
        keyword_url_seed.url.value = page_url
        keyword_protos = map_keywords_to_string_values(client, keywords)
        keyword_url_seed.keywords.extend(keyword_protos)

    try:
        keyword_ideas = keyword_plan_idea_service.generate_keyword_ideas(
            customer_id, language, locations, keyword_plan_network,
            url_seed=url_seed, keyword_seed=keyword_seed,
            keyword_and_url_seed=keyword_url_seed)

        for idea in keyword_ideas.results:
            competition_value = keyword_competition_level_enum.Name(
                idea.keyword_idea_metrics.competition)
            print('Keyword idea text "%s" has %d average monthly searches and '
                  '"%s" competition.\n' % (
                      idea.text.value,
                      idea.keyword_idea_metrics.avg_monthly_searches.value,
                      competition_value))
    except GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)


def map_keywords_to_string_values(client, keywords):
    keyword_protos = []
    for keyword in keywords:
        string_val = client.get_type('StringValue')
        string_val.value = keyword
        keyword_protos.append(string_val)
    return keyword_protos


def map_locations_to_string_values(client, location_ids):
    gtc_service = client.get_service('GeoTargetConstantService', version='v1')
    locations = []
    for location_id in location_ids:
        location = client.get_type('StringValue')
        location.value = gtc_service.geo_target_constant_path(location_id)
        locations.append(location)
    return locations


def map_language_to_string_value(client, language_id):
    language = client.get_type('StringValue')
    language.value = client.get_service('LanguageConstantService',
                                        version='v1').language_constant_path(
                                            language_id)
    return language


if __name__ == '__main__':
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()

    parser = argparse.ArgumentParser(
        description='Generates keyword ideas from a list of seed keywords.')

    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=six.text_type,
                        required=True, help='The Google Ads customer ID.')
    # For more information on determining location IDs, see:
    parser.add_argument('-k', '--keywords', type=six.text_type, required=False,
                        help='Comma-separated starter keywords')
    # https://developers.google.com/adwords/api/docs/appendix/geotargeting.
    parser.add_argument('-l', '--location_ids', type=six.text_type,
                        required=False, help='Comma-delimited list of location '
                                             'criteria IDs')
    # A language criterion ID. For example, specify 1000 for English. For more
    # information on determining this value, see the below link:
    # https://developers.google.com/adwords/api/docs/appendix/codes-formats#languages.
    parser.add_argument('-i', '--language_id', type=six.text_type,
                        required=False, help='Comma-delimited list of language '
                                             'criterion IDs')
    # Optional: Specify a URL string related to your business to generate ideas.
    parser.add_argument('-p', '--page_url', type=six.text_type, required=False,
                        help='A URL string related to your business')

    parser.set_defaults(location_ids=_DEFAULT_LOCATION_IDS,
                        language_id=_DEFAULT_LANGUAGE_ID, keywords='')

    args = parser.parse_args()

    main(google_ads_client, args.customer_id,
         filter(None, args.location_ids.split(',')), args.language_id,
         filter(None, args.keywords.split(',')), args.page_url)
