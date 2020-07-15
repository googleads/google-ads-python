#!/usr/bin/env python
#
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This example gets the changes in the account made in the last 7 days."""


import argparse
import sys


import google.ads.google_ads.client


ADS_PAGE_SIZE = 1000


def resource_name_for_resource_type(resource_type, row):
  """Return the resource name for the resource type.

  Each returned row contains all possible changed fields. This function
  returns the resource name of the changed field based on the
  resource type. The changed field's parent is also populated but is not used.
  
  Args:
    resource_type: the string equivalent of the resource type
    row: a single row returned from the service

  Returns:
    The resource name of the field that changed.
  """
  resource_name = ''  # default for UNSPECIFIED or UNKNOWN
  if resource_type == 'AD_GROUP':
    resource_name = row.change_status.ad_group.value
  elif resource_type == 'AD_GROUP_AD':
    resource_name = row.change_status.ad_group_ad.value
  elif resource_type == 'AD_GROUP_CRITERION':
    resource_name = row.change_status.ad_group_criterion.value
  elif resource_type == 'CAMPAIGN':
    resource_name = row.change_status.campaign.value
  elif resource_type == 'CAMPAIGN_CRITERION':
    resource_name = row.change_status.campaign_criterion.value
  return resource_name


def main(client, customer_id):
  ads_service = client.get_service('GoogleAdsService', version='v4')
  query = ('SELECT change_status.resource_name, '
           'change_status.last_change_date_time, '
           'change_status.resource_type, '
           'change_status.campaign, '
           'change_status.ad_group, '
           'change_status.resource_status, '
           'change_status.ad_group_ad, '
           'change_status.ad_group_criterion, '
           'change_status.campaign_criterion '
           'FROM change_status '
           'WHERE change_status.last_change_date_time DURING LAST_7_DAYS '
           'ORDER BY change_status.last_change_date_time')

  response = ads_service.search(customer_id, query=query,
                                page_size=ADS_PAGE_SIZE)

  resource_type_enum = (client.get_type(
      'ChangeStatusResourceTypeEnum', version='v4').ChangeStatusResourceType)
  change_status_operation_enum = (client.get_type(
      'ChangeStatusOperationEnum', version='v4').ChangeStatusOperation)

  try:
    for row in response:
      resource_type = (resource_type_enum.Name(row.change_status
                                               .resource_type))
      resource_status = (change_status_operation_enum
                         .Name(row.change_status.resource_status))
      print ('On "%s", change status "%s" shows a resource type of "%s" '
             'with resource name "%s" was "%s".'
             % (row.change_status.last_change_date_time.value,
                row.change_status.resource_name,
                resource_type,
                resource_name_for_resource_type(resource_type, row),
                resource_status))
  except google.ads.google_ads.errors.GoogleAdsException as ex:
    print('Request with ID "%s" failed with status "%s" and includes the '
          'following errors:' % (ex.request_id, ex.error.code().name))
    for error in ex.failure.errors:
      print('\tError with message "%s".' % error.message)
      if error.location:
        for field_path_element in error.location.field_path_elements:
          print('\t\tOn field: %s' % field_path_element.field_name)
    sys.exit(1)


if __name__ == '__main__':
  # GoogleAdsClient will read a google-ads.yaml configuration file in the
  # home directory if none is specified.
  google_ads_client = (google.ads.google_ads.client.GoogleAdsClient
                       .load_from_storage())

  parser = argparse.ArgumentParser(
     description=('Displays account changes that occurred in the last 7 days.'))
  # The following argument(s) should be provided to run the example.
  parser.add_argument('-c', '--customer_id', type=str,
                      required=True, help='The Google Ads customer ID.')
  args = parser.parse_args()

  main(google_ads_client, args.customer_id)
