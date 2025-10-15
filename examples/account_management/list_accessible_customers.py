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
"""This example lists the resource names for the customers that the
authenticating user has access to.

The customer IDs retrieved from the resource names can be used to set
the login-customer-id configuration. For more information see this
documentation: https://developers.google.com/google-ads/api/docs/concepts/call-structure#cid
"""


import sys
from typing import List

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.services.services.customer_service.client import (
    CustomerServiceClient,
)
from google.ads.googleads.v22.services.types.customer_service import (
    ListAccessibleCustomersResponse,
)


# [START list_accessible_customers]
def main(client: GoogleAdsClient) -> None:
    customer_service: CustomerServiceClient = client.get_service(
        "CustomerService"
    )

    accessible_customers: ListAccessibleCustomersResponse = (
        customer_service.list_accessible_customers()
    )
    result_total: int = len(accessible_customers.resource_names)
    print(f"Total results: {result_total}")

    resource_names: List[str] = accessible_customers.resource_names
    for resource_name in resource_names:  # resource_name is implicitly str
        print(f'Customer resource name: "{resource_name}"')
    # [END list_accessible_customers]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v22")

    try:
        main(googleads_client)
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
