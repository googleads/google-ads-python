#!/usr/bin/env python
# Copyright 2020 Google LLC
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
"""This example shows use of the validateOnly header for an expanded text ad.

No objects will be created, but exceptions will still be thrown.
"""


import argparse
import sys

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException


def main(client, customer_id, ad_group_id):
    ad_group_ad_operation = client.get_type('AdGroupAdOperation', version='v2')
    ad_group_ad = ad_group_ad_operation.create
    ad_group_service = client.get_service('AdGroupService', version='v2')
    ad_group_ad.ad_group.value = ad_group_service.ad_group_path(customer_id,
        ad_group_id)
    ad_group_ad.status = client.get_type('AdGroupAdStatusEnum',
        version='v2').PAUSED

    # Create an expanded text ad.
    ad_group_ad.ad.expanded_text_ad.description.value = 'Luxury Cruise to Mars'
    ad_group_ad.ad.expanded_text_ad.headline_part1.value = (
        'Visit the Red Planet in style.')
    # Adds a headline that will trigger a policy violation to demonstrate error
    # handling.
    ad_group_ad.ad.expanded_text_ad.headline_part2.value = (
        'Low-gravity fun for everyone!!')
    final_url = ad_group_ad.ad.final_urls.add()
    final_url.value = 'http://www.example.com/'

    ad_group_ad_service = client.get_service('AdGroupAdService', version='v2')
    # Attempt the mutate with validate_only=True.
    try:
        response = ad_group_ad_service.mutate_ad_group_ads(customer_id,
            [ad_group_ad_operation], partial_failure=False, validate_only=True)
        print('"Expanded text ad validated successfully.')
    except GoogleAdsException as ex:
        # This will be hit if there is a validation error from the server.
        print(f'Request with ID "{ex.request_id}" failed with status '
              f'"{ex.error.code().name}".')
        print('There may have been validation error(s) while adding expanded '
              'text ad.')
        for error in ex.failure.errors:
            # Note: Depending on the ad type, you may get back policy violation
            # errors as either PolicyFindingError or PolicyViolationError.
            # ExpandedTextAds return errors as PolicyFindingError, so only this
            # case is illustrated here. For additional details, see
            # https://developers.google.com/google-ads/api/docs/policy-exemption/overview
            if (error.error_code.policy_finding_error ==
                client.get_type('PolicyFindingErrorEnum',
                                version='v2').POLICY_FINDING):
                if error.details.policy_finding_details:
                    count = 1
                    details = (error.details.policy_finding_details
                               .policy_topic_entries)
                    for entry in details:
                        print(f'{count}) Policy topic entry: \n{entry}\n')
                    count += 1
            else:
                print(f'\tNon-policy finding error with message '
                      f'"{error.message}".')
                if error.location:
                    for field_path_element in (
                        error.location.field_path_elements):
                        print(f'\t\tOn field: {field_path_element.field_name}')
        sys.exit(1)

if __name__ == '__main__':
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()

    parser = argparse.ArgumentParser(
        description='Shows how to use the ValidateOnly header.')

    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=str,
                        required=True, help='The Google Ads customer ID.')
    parser.add_argument('-a', '--ad_group_id', type=str,
                        required=True, help='The Ad Group ID.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, args.ad_group_id)
