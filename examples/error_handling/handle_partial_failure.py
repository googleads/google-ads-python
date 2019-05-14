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
"""This shows how to handle responses that may include partial_failure errors.
"""

from __future__ import absolute_import

import argparse
import six
import sys
import uuid

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException


def main(client, customer_id, campaign_id):
    ad_group_service = client.get_service('AdGroupService', version='v1')
    campaign_service = client.get_service('CampaignService', version='v1')
    resource_name = campaign_service.campaign_path(customer_id, campaign_id)
    invalid_resource_name = campaign_service.campaign_path(customer_id, 0)
    ad_group_operations = []

    # This AdGroup should be created successfully - assuming the campaign in
    # the params exists.
    ad_group_op1 = client.get_type('AdGroupOperation', version='v1')
    ad_group_op1.create.name.value = 'Valid AdGroup: %s' % uuid.uuid4()
    ad_group_op1.create.campaign.value = resource_name
    ad_group_operations.append(ad_group_op1)

    # This AdGroup will always fail - campaign ID 0 in resource names is
    # never valid.
    ad_group_op2 = client.get_type('AdGroupOperation', version='v1')
    ad_group_op2.create.name.value = 'Broken AdGroup: %s' % (uuid.uuid4())
    ad_group_op2.create.campaign.value = invalid_resource_name
    ad_group_operations.append(ad_group_op2)

    # This AdGroup will always fail - duplicate ad group names are not allowed.
    ad_group_op3 = client.get_type('AdGroupOperation', version='v1')
    ad_group_op3.create.name.value = (ad_group_op1.create.name.value)
    ad_group_op3.create.campaign.value = resource_name
    ad_group_operations.append(ad_group_op3)

    try:
        # Issue a mutate request, setting partial_failure=True.
        ad_group_response = ad_group_service.mutate_ad_groups(
            customer_id, ad_group_operations, partial_failure=True)
    except GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)
    else:
        # Check for existence of any partial failures in the response.
        if ad_group_response.partial_failure_error:
            print('Partial failures occurred. Details will be shown below.\n')
            partial_failures = get_partial_failure_messages(
                client, ad_group_response)

            for error in partial_failures:
                # Construct and print a string that details which element in
                # the above ad_group_operations list failed (by index number)
                # as well as the error message and error code.
                print('A partial failure at index %d occured.\n'
                      'Error message: %s\nError code: %s' % (
                          error.location.field_path_elements[0].index.value,
                          error.message, error.error_code))
        else:
            print('All operations completed successfully. No partial failure '
                  'to show.')

        # In the list of results, operations from the ad_group_operation list
        # that failed will be represented as empty messages. This loop detects
        # such empty messages and ignores them, while printing information about
        # successful operations.
        for message in ad_group_response.results:
            # Empty messages will have a byte size of zero.
            if message.ByteSize() == 0:
                continue

            print('Created ad group with resource_name: %s.' % (
                message.resource_name))


def get_partial_failure_messages(client, response):
    """Get a list of all partial failure error objects for a given response.

    Shows how to retrieve partial_failure errors from a response message (in
    the case of this example the message will be of type MutateAdGroupsResponse)
    and how to unpack those errors to GoogleAdsError instances. As an example,
    a GoogleAdsError object from this example will be structured similar to:

    error_code {
      range_error: TOO_LOW
    }
    message: "Too low."
    trigger {
      string_value: ""
    }
    location {
      field_path_elements {
        field_name: "operations"
        index {
          value: 1
        }
      }
      field_path_elements {
        field_name: "create"
      }
      field_path_elements {
        field_name: "campaign"
      }
    }

    Args:
        client: an initialized GoogleAdsClient.
        response: a MutateAdGroupsResponse instance.
    Returns:
        A list of GoogleAdsError instances each relating to an individual
        failure from the given list of partial failures.
    """
    # Retrieve the serialized list of errors off of the response message.
    error_detail = response.partial_failure_error.details[0].value
    # Retrieve the GoogleAdsFailure class from the client
    google_ads_failure = client.get_type('GoogleAdsFailure', version='v1')
    # Parse the string into a GoogleAdsFailure message instance.
    err_object = google_ads_failure.FromString(error_detail)
    return err_object.errors


if __name__ == '__main__':
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()

    parser = argparse.ArgumentParser(
        description='Adds an ad group for specified customer and campaign id.')
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=six.text_type,
                        required=True, help='The Google Ads customer ID.')
    parser.add_argument('-i', '--campaign_id', type=six.text_type,
                        required=True, help='The campaign ID.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, args.campaign_id)
