#!/usr/bin/env python
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
"""This demonstrates how to create a campaign experiment.

It requests the creation based on a draft and waits for completion.
"""


import argparse
import sys
import uuid

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException


def main(client, customer_id, campaign_draft_resource_name):
    # Create the campaign experiment.
    campaign_experiment = client.get_type('CampaignExperiment', version='v3')
    campaign_experiment.campaign_draft.value = campaign_draft_resource_name
    campaign_experiment.name.value = 'Campaign Experiment #{}'.format(
        uuid.uuid4())
    campaign_experiment.traffic_split_percent.value = 50
    campaign_experiment.traffic_split_type = client.get_type(
        'CampaignExperimentTrafficSplitTypeEnum', version='v3').RANDOM_QUERY

    try:
        campaign_experiment_service = client.get_service(
            'CampaignExperimentService', version='v3')

        # A Long Running Operation (LRO) is returned from this
        # asynchronous request by the API.
        campaign_experiment_lro = (
            campaign_experiment_service.create_campaign_experiment(
                customer_id, campaign_experiment))
    except GoogleAdsException as ex:
        print('Request with ID "{}" failed with status "{}" and includes the '
              'following errors:'.format(ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "{}".'.format(error.message))
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: {}'.format(field_path_element.field_name))
        sys.exit(1)

    print('Asynchronous request to create campaign experiment with '
          'resource name "{}" started.'.format(
              campaign_experiment_lro.metadata.campaign_experiment))
    print('Waiting until operation completes.')

    # Poll until the operation completes.
    campaign_experiment_lro.result()

    # Retrieve the campaign experiment that has been created.
    ga_service = client.get_service('GoogleAdsService', version='v3')
    query = (
        'SELECT campaign_experiment.experiment_campaign '
        'FROM campaign_experiment '
        'WHERE campaign_experiment.resource_name = "{}"'.format(
            campaign_experiment_lro.metadata.campaign_experiment))

    results = ga_service.search(customer_id, query=query, page_size=1)

    try:
        for row in results:
            print('Experiment campaign "{}" creation completed.'.format(
                row.campaign_experiment.experiment_campaign.value))
    except GoogleAdsException as ex:
        print('Request with ID "{}" failed with status "{}" and includes the '
              'following errors:'.format(ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "{}".'.format(error.message))
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: {}'.format(field_path_element.field_name))
        sys.exit(1)

if __name__ == '__main__':
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()

    parser = argparse.ArgumentParser(
        description=('Create a campaign experiment based on a campaign draft.'))
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=str,
                        required=True, help='The Google Ads customer ID.')
    parser.add_argument('-n', '--campaign_draft_resource_name',
                        type=str, required=True,
                        help='The campaign draft resource name.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, args.campaign_draft_resource_name)
