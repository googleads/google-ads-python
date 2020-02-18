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
"""Updates a campaign criterion with a new bid modifier."""

import argparse
import sys

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException
from google.api_core import protobuf_helpers


def main(client, customer_id, campaign_id, criterion_id, bid_modifier):
    campaign_criterion_service = client.get_service(
        'CampaignCriterionService', version='v2')

    criterion_rname = campaign_criterion_service.campaign_criteria_path(
        customer_id, f'{campaign_id}~{criterion_id}')

    campaign_criterion_operation = client.get_type(
        'CampaignCriterionOperation', version='v2')
    campaign_criterion = campaign_criterion_operation.update
    campaign_criterion.resource_name = criterion_rname
    campaign_criterion.bid_modifier.value = bid_modifier
    fm = protobuf_helpers.field_mask(None, campaign_criterion)
    campaign_criterion_operation.update_mask.CopyFrom(fm)

    try:
        campaign_criterion_response = (
            campaign_criterion_service.mutate_campaign_criteria(
                customer_id, [campaign_criterion_operation]))
    except GoogleAdsException as ex:
        print(f'Request with ID "{ex.request_id}" failed with status '
              f'"{ex.error.code().name}" and includes the following errors:')
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f'\t\tOn field: {field_path_element.field_name}')
        sys.exit(1)

    print('Campaign criterion with resource name '
          f'"{campaign_criterion_response.results[0].resource_name}" was '
          'modified.')


if __name__ == '__main__':
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()

    parser = argparse.ArgumentParser(
        description=('Updates the bid modifier and device type for the given '
                     'customer ID and campaign criterion ID.'))
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=str,
                        required=True, help='The Google Ads customer ID.')
    parser.add_argument('--campaign_id', type=str, required=True,
                        help='The campaign ID.')
    parser.add_argument('--criterion_id', type=str, required=True,
                        help='The criterion ID.')
    parser.add_argument('-b', '--bid_modifier', type=float, default=1.5,
                        help='The desired campaign criterion bid modifier.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, args.campaign_id,
         args.criterion_id, args.bid_modifier)
