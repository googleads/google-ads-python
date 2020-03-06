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
"""This example shows how to link a manager customer to a client customer."""


import argparse
import sys
import uuid
from datetime import datetime, timedelta
from google.api_core import protobuf_helpers

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException


def main(client, customer_id, manager_customer_id):
    # This example assumes that the same credentials will work for both
    # customers, but that may not be the case. If you need to use different
    # credentials for each customer, then you may either update the client
    # configuration or instantiate two clients, where at least one points to
    # a specific configuration file so that both clients don't read the same
    # file located in the $HOME dir.

    # Extend an invitation to the client while authenticating as the manager.
    client_link_operation = client.get_type(
        'CustomerClientLinkOperation', version='v3')
    client_link = client_link_operation.create
    client_link.client_customer.value = 'customers/{}'.format(customer_id)
    client_link.status = client.get_type(
        'ManagerLinkStatusEnum').PENDING

    customer_client_link_service = client.get_service(
        'CustomerClientLinkService', version='v3')
    response = customer_client_link_service.mutate_customer_client_link(
        manager_customer_id, client_link_operation)
    resource_name = response.results[0].resource_name

    print('Extended an invitation from customer #{} to customer #{} with '
          'client link resource_name #{}'.format(
              manager_customer_id, customer_id, resource_name))

    # Find the manager_link_id of the link we just created, so we can construct
    # the resource name for the link from the client side. Note that since we
    # are filtering by resource_name, a unique identifier, only one
    # customer_client_link resource will be returned in the response
    query = '''
        SELECT
            customer_client_link.manager_link_id
        FROM
            customer_client_link
        WHERE
            customer_client_link.resource_name = "{}"
    '''.format(resource_name)

    ga_service = client.get_service('GoogleAdsService', version='v3')
    response = ga_service.search(manager_customer_id, query=query)

    # Since the google_ads_service.search method returns an iterator we need
    # to initialize an iteration in order to retrieve results, even though
    # we know the query will only return a single row.
    for row in response.result:
        manager_link_id = row.customer_client_link.manager_link_id

    manager_link_operation = client.get_type(
        'CustomerManagerLinkOperation', version='v3')
    manager_link = manager_link_operation.update
    manager_link.resource_name.value = (
        'customers/{}/customerManagerLinks/{}~{}'.format(
              customer_id, manager_customer_id, manager_link_id))

    manager_link.status = client.get_type('ManagerLinkStatusEnum', version='v3')
    field_mask = protobuf_helpers.field_mask(None, manager_link)
    manager_link_operation.update_mask.CopyFrom(field_mask)

    manager_link_service = client.get_service('ManagerLinkService',
                                              version='v3')
    response = manager_link_service.mutate_manager_links(
        manager_customer_id, [manager_link_operation])
    resource_name = response.results[0].resource_name

    print('Client accepted invitation with resource_name: #{}'.format(
        resource_name))

if __name__ == '__main__':
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()

    parser = argparse.ArgumentParser(
        description= ('Links and existing manager customer to an existing'
                      'client customer'))
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=str,
                        required=True, help='The customer ID.')
    parser.add_argument('-m', '--manager_customer_id', type=str,
                        required=True, help='The manager customer ID.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, args.manager_customer_id)
