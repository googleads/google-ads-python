#!/usr/bin/env python
# Copyright 2018 Google LLC
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
"""This example adds campaign targeting criteria."""

from __future__ import absolute_import

import argparse
import six
import sys

import google.ads.google_ads.client


def main(client, customer_id, campaign_id, keyword, location_id):
    campaign_criterion_service = client.get_service('CampaignCriterionService',
                                                    version='v1')

    operations = [
        create_location_op(client, customer_id, campaign_id, location_id),
        create_negative_keyword_op(client, customer_id, campaign_id, keyword),
        create_proximity_op(client, customer_id, campaign_id)
    ]

    try:
        campaign_criterion_response = (
            campaign_criterion_service.mutate_campaign_criteria(
                customer_id, operations))
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)

    for result in campaign_criterion_response.results:
        print('Added campaign criterion "%s".' % result.resource_name)


def create_location_op(client, customer_id, campaign_id, location_id):
    campaign_service = client.get_service('CampaignService', version='v1')
    geo_target_constant_service = client.get_service('GeoTargetConstantService',
                                                     version='v1')

    # Create the campaign criterion.
    campaign_criterion_operation = client.get_type('CampaignCriterionOperation',
                                                   version='v1')
    campaign_criterion = campaign_criterion_operation.create
    campaign_criterion.campaign.value = campaign_service.campaign_path(
        customer_id, campaign_id)

    # Besides using location_id, you can also search by location names from
    # GeoTargetConstantService.suggest_geo_target_constants() and directly
    # apply GeoTargetConstant.resource_name here. An example can be found
    # in get_geo_target_constant_by_names.py.
    campaign_criterion.location.geo_target_constant.value = (
        geo_target_constant_service.geo_target_constant_path(location_id))

    return campaign_criterion_operation


def create_negative_keyword_op(client, customer_id, campaign_id, keyword):
    campaign_service = client.get_service('CampaignService', version='v1')

    # Create the campaign criterion.
    campaign_criterion_operation = client.get_type('CampaignCriterionOperation',
                                                   version='v1')
    campaign_criterion = campaign_criterion_operation.create
    campaign_criterion.campaign.value = campaign_service.campaign_path(
        customer_id, campaign_id)
    campaign_criterion.negative.value = True
    criterion_keyword = campaign_criterion.keyword
    criterion_keyword.text.value = keyword
    criterion_keyword.match_type = client.get_type('KeywordMatchTypeEnum',
                                                   version='v1').BROAD

    return campaign_criterion_operation


def create_proximity_op(client, customer_id, campaign_id):
    campaign_service = client.get_service('CampaignService', version='v1')

    # Create the campaign criterion.
    campaign_criterion_operation = client.get_type('CampaignCriterionOperation',
                                                   version='v1')
    campaign_criterion = campaign_criterion_operation.create
    campaign_criterion.campaign.value = campaign_service.campaign_path(
        customer_id, campaign_id)
    campaign_criterion.proximity.address.street_address.value = (
        '38 avenue de l\'Opera')
    campaign_criterion.proximity.address.city_name.value = 'Paris'
    campaign_criterion.proximity.address.postal_code.value = '75002'
    campaign_criterion.proximity.address.country_code.value = 'FR'
    campaign_criterion.proximity.radius.value = 10
    # Default is kilometers.
    campaign_criterion.proximity.radius_units = client.get_type(
        'ProximityRadiusUnitsEnum').MILES

    return campaign_criterion_operation


if __name__ == '__main__':
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = (google.ads.google_ads.client.GoogleAdsClient
                         .load_from_storage())

    parser = argparse.ArgumentParser(
        description=('Adds campaign targeting criteria for the specified '
                     'campaign under the given customer ID.'))
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=six.text_type,
                        required=True, help='The Google Ads customer ID.')
    parser.add_argument('-i', '--campaign_id', type=six.text_type,
                        required=True, help='The campaign ID.')
    parser.add_argument('-k', '--keyword', type=six.text_type, required=True,
                        help='The keyword to be added to the campaign.')
    parser.add_argument(
        '-l', '--location_id', type=six.text_type, required=False,
        default='21167',  # New York
        help=('A location criterion ID, this field is optional. If not '
              'specified, will default to New York. For more information on '
              'determining this value, see: '
              'https://developers.google.com/adwords/api/docs/appendix/'
              'geotargeting.'))
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, args.campaign_id, args.keyword,
         args.location_id)
