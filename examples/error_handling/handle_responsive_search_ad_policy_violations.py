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
"""Requests an exemption for policy violations of a responsive search ad.

If the request somehow fails with exceptions that are not policy finding
errors, the example will stop instead of trying sending an exemption request.
"""

import argparse
import sys
import uuid

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id, ad_group_id):
    """Uses Customer Match to create and add users to a new user list.

    Args:
        client: The Google Ads client.
        customer_id: The customer ID for which to add the responsive search ad.
        ad_group_id: The ad group ID to which to add a responsive search ad.
    """
    ad_group_ad_service_client = client.get_service("AdGroupAdService")
    ad_group_ad_operation = create_responsive_search_ad(
        client, ad_group_ad_service_client, customer_id, ad_group_id
    )

    ignorable_policy_topics = []
    try:
        # Try sending a mutate request to add the ad group ad.
        ad_group_ad_service_client.mutate_ad_group_ads(
            customer_id=customer_id, operations=[ad_group_ad_operation]
        )
    except GoogleAdsException as googleads_exception:
        # The request will always fail due to the policy violation in the
        # ad's description.
        ignorable_policy_topics = fetch_ignorable_policy_topics(
            client, googleads_exception
        )

    request_exemption(
        customer_id,
        ad_group_ad_service_client,
        ad_group_ad_operation,
        ignorable_policy_topics,
    )


def create_responsive_search_ad(
    client, ad_group_ad_service_client, customer_id, ad_group_id
):
    """Create a responsive search ad that includes a policy violation.

    Args:
        client: The GoogleAds client instance.
        ad_group_ad_service_client: The AdGroupAdService client instance.
        customer_id: The customer ID for which to add the responsive search ad.
        ad_group_id: The ad group ID to which to add a responsive search ad.

    Returns:
        The attempted AdGroupAdOperation instance.
    """
    ad_group_resource_name = client.get_service("AdGroupService").ad_group_path(
        customer_id, ad_group_id
    )

    # Creates an operation and ad group ad to create and hold the above ad.
    ad_group_ad_operation = client.get_type("AdGroupAdOperation")
    ad_group_ad = ad_group_ad_operation.create
    ad_group_ad.ad_group = ad_group_resource_name
    # Set the ad group ad to PAUSED to prevent it from immediately serving.
    # Set to ENABLED once you've added targeting and the ad are ready to serve.
    ad_group_ad.status = client.enums.AdGroupAdStatusEnum.PAUSED
    # Sets the responsive search ad info on an ad.
    responsive_search_ad_info = ad_group_ad.ad.responsive_search_ad

    headline_1 = client.get_type("AdTextAsset")
    headline_1.text = f"Cruise to Mars #{str(uuid.uuid4())[0:13]}"
    headline_2 = client.get_type("AdTextAsset")
    headline_2.text = "Best Space Cruise Line"
    headline_3 = client.get_type("AdTextAsset")
    headline_3.text = "Experience the Stars"
    responsive_search_ad_info.headlines.extend(
        [headline_1, headline_2, headline_3]
    )

    # Intentionally use an ad text that violates policy by having too many
    # exclamation marks.
    description_1 = client.get_type("AdTextAsset")
    description_1.text = "Buy your tickets now!!!!!!!"
    description_2 = client.get_type("AdTextAsset")
    description_2.text = "Visit the Red Planet"
    responsive_search_ad_info.descriptions.extend(
        [description_1, description_2]
    )

    ad_group_ad.ad.final_urls.append("https://www.example.com")

    return ad_group_ad_operation


# [START handle_responsive_search_ad_policy_violations]
def fetch_ignorable_policy_topics(client, googleads_exception):
    """Collects all ignorable policy topics to be sent for exemption request.

    Args:
        client: The GoogleAds client instance.
        googleads_exception: The exception that contains the policy
            violation(s).

    Returns:
        A list of ignorable policy topics.
    """
    ignorable_policy_topics = []

    print("Google Ads failure details:")
    for error in googleads_exception.failure.errors:
        if (
            error.error_code.policy_finding_error
            != client.get_type(
                "PolicyFindingErrorEnum"
            ).PolicyFindingError.POLICY_FINDING
        ):
            print(
                "This example supports sending exemption request for the "
                "policy finding error only."
            )
            raise googleads_exception

        print(f"\t{error.error_code.policy_finding_error}: {error.message}")

        if (
            error.details is not None
            and error.details.policy_finding_details is not None
        ):
            policy_finding_details = error.details.policy_finding_details
            print("\tPolicy finding details:")

            for (
                policy_topic_entry
            ) in policy_finding_details.policy_topic_entries:
                ignorable_policy_topics.append(policy_topic_entry.topic)
                print(f"\t\tPolicy topic name: '{policy_topic_entry.topic}'")
                print(
                    f"\t\tPolicy topic entry type: '{policy_topic_entry.type_}'"
                )
                # For the sake of brevity, we exclude printing "policy topic
                # evidences" and "policy topic constraints" here. You can fetch
                # those data by calling:
                # - policy_topic_entry.evidences
                # - policy_topic_entry.constraints

    return ignorable_policy_topics
    # [END handle_responsive_search_ad_policy_violations]


# [START handle_responsive_search_ad_policy_violations_1]
def request_exemption(
    customer_id,
    ad_group_ad_service_client,
    ad_group_ad_operation,
    ignorable_policy_topics,
):
    """Sends exemption requests for creating a responsive search ad.

    Args:
        customer_id: The customer ID for which to add the responsive search ad.
        ad_group_ad_service_client: The AdGroupAdService client instance.
        ad_group_ad_operation: The AdGroupAdOperation that returned policy
            violation(s).
        ignorable_policy_topics: The extracted list of policy topic entries.
    """
    print(
        "Attempting to add a responsive search ad again by requesting "
        "exemption for its policy violations."
    )
    ad_group_ad_operation.policy_validation_parameter.ignorable_policy_topics.extend(
        ignorable_policy_topics
    )
    response = ad_group_ad_service_client.mutate_ad_group_ads(
        customer_id=customer_id, operations=[ad_group_ad_operation]
    )
    print(
        "Successfully added a responsive search ad with resource name "
        f"'{response.results[0].resource_name}' for policy violation "
        "exemption."
    )
    # [END handle_responsive_search_ad_policy_violations_1]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Requests an exemption for responsive search ad policy "
        "violations."
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )
    parser.add_argument(
        "-a",
        "--ad_group_id",
        type=str,
        required=True,
        help="The ad group ID to which to add a responsive search ad.",
    )
    args = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v20")

    try:
        main(googleads_client, args.customer_id, args.ad_group_id)
    except GoogleAdsException as ex:
        print(
            f"Request with ID '{ex.request_id}' failed with status "
            f"'{ex.error.code().name}' and includes the following errors:"
        )
        for error in ex.failure.errors:
            print(f"\tError with message '{error.message}'.")
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
