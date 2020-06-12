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
"""This example illustrates adding a custom audience.

Custom audiences help you reach your ideal audience by entering relevant
keywords, URLs, and apps. For more information about custom audiences, see:
https://support.google.com/google-ads/answer/9805516
"""


import argparse
import sys
from uuid import uuid4

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
    """
    custom_audience_service = client.get_service("CustomAudienceService")

    # Create a custom audience operation.
    custom_audience_operation = client.get_type("CustomAudienceOperation")

    # Create a custom audience
    custom_audience = custom_audience_operation.create
    custom_audience.name = f"Example CustomAudience #{uuid4()}"
    custom_audience.description = (
        "Custom audiences who have searched specific terms on Google Search."
    )
    # Match customers by what they searched on Google Search. Note: "INTEREST"
    # or "PURCHASE_INTENT" is not allowed for the type field of a newly
    # created custom audience. Use "AUTO" instead of these two options when
    # creating a new custom audience.
    custom_audience.type_ = client.get_type(
        "CustomAudienceTypeEnum"
    ).CustomAudienceType.SEARCH
    custom_audience.status = client.get_type(
        "CustomAudienceStatusEnum"
    ).CustomAudienceStatus.ENABLED
    # List of members that this custom audience is composed of. Customers that
    # meet any of the membership conditions will be reached.
    member_type_enum = client.get_type(
        "CustomAudienceMemberTypeEnum"
    ).CustomAudienceMemberType
    member1 = client.get_type("CustomAudienceMember")
    member1.member_type = member_type_enum.KEYWORD
    member1.keyword = "mars cruise"
    member2 = client.get_type("CustomAudienceMember")
    member2.member_type = member_type_enum.KEYWORD
    member2.keyword = "jupiter cruise"
    member3 = client.get_type("CustomAudienceMember")
    member3.member_type = member_type_enum.URL
    member3.keyword = "http://www.example.com/locations/mars"
    member4 = client.get_type("CustomAudienceMember")
    member4.member_type = member_type_enum.URL
    member4.keyword = "http://www.example.com/locations/jupiter"
    custom_audience.members.extend([member1, member2, member3, member4])

    # Add the custom audience.
    custom_audience_response = (
        custom_audience_service.mutate_custom_audiences(
            customer_id=customer_id, operations=[custom_audience_operation]
        )
    )

    print(
        "New custom audience added with resource name: "
        f"'{custom_audience_response.results[0].resource_name}'"
    )


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v6")

    parser = argparse.ArgumentParser(
        description="Adds a custom audience for a specified customer."
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )
    args = parser.parse_args()

    try:
        main(googleads_client, args.customer_id)
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'	Error with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
