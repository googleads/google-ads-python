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

_DEFAULT_PAGE_SIZE = 100
_DEFAULT_LOCATION_ID = '1023191' # location ID for New York, NY
_DEFAULT_LANGUAGE_ID = '1000' # language ID for English


def main(client, customer_id, location_ids, language_id, keywords, page_url,
         page_size):
    if (not len(keywords) and not page_url):
        raise ValueError('At least one of keywords or page URL is required, '
                         'but neither was specified.')
    keyword_plan_idea_service = client.get_service('KeywordPlanIdeaService',
                                                   version='v1')
    language_constant_service = client.get_service('LanguageConstantService',
                                                   version='v1')
    geo_target_constant_service = client.get_service('GeoTargetConstantService',
                                                     version='v1')
    keyword_plan_network = client.get_type(
        'KeywordPlanNetworkEnum').GOOGLE_SEARCH_AND_PARTNERS
    keyword_protos = build_keyword_protos(client, keywords)
    location_protos = build_geo_target_protos(client, location_ids,
                                              geo_target_constant_service)
    language_proto = build_language_proto(client, language_id,
                                          language_constant_service)

    if (not len(keywords) and page_url):
        url_seed = client.get_type('UrlSeed', version='v1')
        url_seed.url.value = str(page_url)
        keyword_ideas = keyword_plan_idea_service.generate_keyword_ideas(
            customer_id, language_proto, location_ids, keyword_plan_network,
            url_seed=url_seed)
    elif (len(keywords) and not page_url):
        keyword_seed = client.get_type('KeywordSeed', version='v1')
        keyword_seed.keywords.extend(keyword_protos)
        keyword_ideas = keyword_plan_idea_service.generate_keyword_ideas(
            customer_id, language_proto,
            location_protos, keyword_plan_network,
            keyword_seed=keyword_seed)
    else:
        keyword_and_url_seed = client.get_type('KeywordAndUrlSeed',
                                               version='v1')
        keyword_and_url_seed.url.value = page_url
        keyword_and_url_seed.keywords.extend(keyword_protos)
        keyword_ideas = keyword_plan_idea_service.generate_keyword_ideas(
            customer_id, language_id, location_ids, keyword_plan_network,
            keyword_and_url_seed=keyword_and_url_seed)


def build_keyword_protos(client, keywords):
    keyword_protos = []
    for keyword in keywords:
        string_val = client.get_type('StringValue')
        string_val.value = keyword
        keyword_protos.append(string_val)
    return keyword_protos


def build_geo_target_protos(client, location_ids, geo_target_constant_service):
    location_protos = []
    for location_id in location_ids:
        location = client.get_type('StringValue')
        location.value = geo_target_constant_service.geo_target_constant_path(
            location_id)
        location_protos.append(location)
    return location_protos


def build_language_proto(client, language_id, language_constant_service):
    language_proto = client.get_type('StringValue')
    language_proto.value = language_constant_service.language_constant_path(
        language_id)
    return language_proto


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
                        required=False, help='Comma-separated location criteria '
                                            'IDs')
    # A language criterion ID. For example, specify 1000 for English. For more
    # information on determining this value, see the below link:
    # https://developers.google.com/adwords/api/docs/appendix/codes-formats#languages.
    parser.add_argument('-i', '--language_id', type=six.text_type,
                        required=False, help='A language criterion ID')
    # Optional: Specify a URL string related to your business to generate ideas.
    parser.add_argument('-p', '--page_url', type=six.text_type, required=False,
                        help='A URL string related to your business')

    parser.set_defaults(location_ids=_DEFAULT_LOCATION_ID,
                        language_id=_DEFAULT_LANGUAGE_ID)

    args = parser.parse_args()

    main(google_ads_client, args.customer_id, args.location_ids.split(','),
         args.language_id, args.keywords.split(','), args.page_url,
         _DEFAULT_PAGE_SIZE)
