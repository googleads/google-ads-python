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
"""Demonstrates how to request an exemption for policy violations of a keyword.

Note that the example uses an exemptible policy-violating keyword by default.
If you use a keyword that contains non-exemptible policy violations, they will
not be sent for exemption request and you will still fail to create a keyword.
If you specify a keyword that doesn't violate any policies, this example will
just add the keyword as usual, similar to what the AddKeywords example does.

Note that once you've requested policy exemption for a keyword, when you send
a request for adding it again, the request will pass like when you add a
non-violating keyword.
"""

import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id, ad_group_id, keyword_text):
    """Demonstrates how to request an exemption for keyword policy violations.

    Args:
        client: The Google Ads client.
        customer_id: The customer ID for which to add the keyword.
        ad_group_id: The ad group ID to which to add keyword.
        keyword_text: The keyword text to add.
    """

    ad_group_criterion_service = client.get_service("AdGroupCriterionService")

    (
        googleads_exception,
        ad_group_criterion_operation,
    ) = _create_keyword_criterion(
        client,
        ad_group_criterion_service,
        customer_id,
        ad_group_id,
        keyword_text,
    )

    try:
        # Try sending exemption requests for creating a keyword. However, if
        # your keyword contains many policy violations, but not all of them are
        # exemptible, the request will not be sent.
        if googleads_exception is not None:
            exempt_policy_violation_keys = _fetch_exempt_policy_violation_keys(
                googleads_exception
            )
            _request_exemption(
                customer_id,
                ad_group_criterion_service,
                ad_group_criterion_operation,
                exempt_policy_violation_keys,
            )
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


def _create_keyword_criterion(
    client, ad_group_criterion_service, customer_id, ad_group_id, keyword_text
):
    """Attempts to add a keyword criterion to an ad group.

    Args:
        client: The GoogleAds client instance.
        ad_group_criterion_service: The AdGroupCriterionService client instance.
        customer_id: The customer ID for which to add the expanded text ad.
        ad_group_id: The ad group ID to which to add an expanded text ad.
        keyword_text: The keyword text to add.

    Returns:
        The GoogleAdsException that occurred (or None if the operation was
        successful) and the modified operation.
    """
    # Constructs an ad group criterion using the keyword text provided.
    ad_group_criterion_operation = client.get_type("AdGroupCriterionOperation")
    ad_group_criterion = ad_group_criterion_operation.create
    ad_group_criterion.ad_group = client.get_service(
        "AdGroupService"
    ).ad_group_path(customer_id, ad_group_id)
    ad_group_criterion.status = client.get_type(
        "AdGroupCriterionStatusEnum"
    ).AdGroupCriterionStatus.ENABLED
    ad_group_criterion.keyword.text = keyword_text
    ad_group_criterion.keyword.match_type = client.get_type(
        "KeywordMatchTypeEnum"
    ).KeywordMatchType.EXACT

    try:
        # Try sending a mutate request to add the keyword.
        response = ad_group_criterion_service.mutate_ad_group_criteria(
            customer_id=customer_id, operations=[ad_group_criterion_operation]
        )
    except GoogleAdsException as googleads_exception:
        # Return the exception in order to extract keyword violation details.
        return googleads_exception, ad_group_criterion_operation

    # Report that the mutate request was completed successfully.
    print(
        "Added a keyword with resource name "
        f"'{response.results[0].resource_name}'."
    )

    return None, ad_group_criterion_operation


# [START handle_keyword_policy_violations]
def _fetch_exempt_policy_violation_keys(googleads_exception):
    """Collects all policy violation keys that can be exempted.

    Args:
        googleads_exception: The exception to check for policy violation(s).

    Returns:
        A list of policy violation keys.
    """
    exempt_policy_violation_keys = []

    print("Google Ads failure details:")
    for error in googleads_exception.failure.errors:
        print(f"\t{error.error_code}: {error.message}")

        if (
            error.details is not None
            and error.details.policy_violation_details is not None
        ):
            policy_violation_details = error.details.policy_violation_details
            print(
                "\tPolicy violation details:\n"
                f"\t\tExternal policy name: '{policy_violation_details}'\n"
                "\t\tExternal policy description: "
                f"'{policy_violation_details.external_policy_description}'\n"
                f"\t\tIs exemptible? '{policy_violation_details.is_exemptible}'"
            )

            if (
                policy_violation_details.is_exemptible
                and policy_violation_details.key is not None
            ):
                exempt_policy_violation_keys.append(
                    policy_violation_details.key
                )
                print(
                    f"\t\tPolicy violation key: {policy_violation_details.key}"
                )
                print(
                    f"\t\t\tName: '{policy_violation_details.key.policy_name}'"
                    "\t\t\tViolating text: "
                    f"'{policy_violation_details.key.violating_text}'"
                )
            else:
                print(
                    "No exemption request is sent because your keyword "
                    "contained some non-exemptible policy violations."
                )
                raise googleads_exception
        else:
            print(
                "No exemption request is sent because there are non-policy "
                "related errors thrown."
            )
            raise googleads_exception

    return exempt_policy_violation_keys
    # [END handle_keyword_policy_violations]


# [START handle_keyword_policy_violations_1]
def _request_exemption(
    customer_id,
    ad_group_criterion_service,
    ad_group_criterion_operation,
    exempt_policy_violation_keys,
):
    """Sends exemption requests for creating a keyword.

    Args:
        customer_id: The customer ID for which to add the expanded text ad.
        ad_group_criterion_service: The AdGroupCriterionService client instance.
        ad_group_criterion_operation: The AdGroupCriterionOperation for which
            to request exemption.
        exempt_policy_violation_keys: The exemptible policy violation keys.
    """
    print(
        "Attempting to add a keyword again by requesting exemption for its "
        "policy violations."
    )
    ad_group_criterion_operation.exempt_policy_violation_keys.extend(
        exempt_policy_violation_keys
    )
    response = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id, operations=[ad_group_criterion_operation]
    )
    print(
        "Successfully added a keyword with resource name "
        f"'{response.results[0].resource_name}' by requesting a policy "
        "violation exemption."
    )
    # [END handle_keyword_policy_violations_1]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Demonstrates how to request an exemption for policy "
        "violations of a keyword."
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
        help="The ad group ID to which to add an expanded text ad.",
    )
    parser.add_argument(
        "-k",
        "--keyword_text",
        type=str,
        required=False,
        default="medication",
        help="Specify the keyword text here or use the default keyword "
        "'medication'.",
    )
    args = parser.parse_args()

    main(
        googleads_client, args.customer_id, args.ad_group_id, args.keyword_text
    )
