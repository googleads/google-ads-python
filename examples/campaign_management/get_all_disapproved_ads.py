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
"""This illustrates how to retrieve disapproved ads in a given campaign."""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.services.services.google_ads_service import (
    GoogleAdsServiceClient,
)
from google.ads.googleads.v22.services.types.google_ads_service import (
    SearchGoogleAdsRequest,
    SearchGoogleAdsResponse,
)
from google.ads.googleads.v22.resources.types.ad_group_ad import AdGroupAd
from google.ads.googleads.v22.resources.types.ad import Ad
from google.ads.googleads.v22.enums.types.policy_approval_status import (
    PolicyApprovalStatusEnum,
)


def main(client: GoogleAdsClient, customer_id: str, campaign_id: str) -> None:
    ga_service: GoogleAdsServiceClient = client.get_service("GoogleAdsService")

    query: str = f"""
        SELECT
          ad_group_ad.ad.id,
          ad_group_ad.ad.type,
          ad_group_ad.policy_summary.approval_status,
          ad_group_ad.policy_summary.policy_topic_entries
        FROM ad_group_ad
        WHERE
          campaign.id = {campaign_id}
          AND ad_group_ad.policy_summary.approval_status = DISAPPROVED"""

    request: SearchGoogleAdsRequest = client.get_type("SearchGoogleAdsRequest")
    request.customer_id = customer_id
    request.search_settings.return_total_results_count = True
    request.query = query

    results: SearchGoogleAdsResponse = ga_service.search(request=request)

    disapproved_enum: PolicyApprovalStatusEnum.PolicyApprovalStatus = (
        client.enums.PolicyApprovalStatusEnum.DISAPPROVED
    )

    print("Disapproved ads:")

    # Iterate over all ads in all rows returned and count disapproved ads.
    for result_row in results:
        # result_row: GoogleAdsRow = result_row <- Removed type hint
        ad_group_ad: AdGroupAd = result_row.ad_group_ad
        ad: Ad = ad_group_ad.ad
        policy_summary = ad_group_ad.policy_summary

        if not policy_summary.approval_status == disapproved_enum:
            continue

        print(
            f'Ad with ID "{ad.id}" and type "{ad.type_.name}" was '
            "disapproved with the following policy topic entries:"
        )

        # Display the policy topic entries related to the ad disapproval.
        for pol_entry in policy_summary.policy_topic_entries:
            # pol_entry: PolicyTopicEntry = pol_entry <- Removed type hint
            print(
                f'\ttopic: "{pol_entry.topic}", type "{pol_entry.type_.name}"'
            )

            # Display the attributes and values that triggered the policy
            # topic.
            for pol_evidence in pol_entry.evidences:
                # pol_evidence: PolicyTopicEvidence = pol_evidence <- Removed type hint
                for index, ev_text in enumerate(pol_evidence.text_list.texts):
                    # ev_text: str = ev_text <- Removed type hint
                    print(f"\t\tevidence text[{index}]: {ev_text}")

    print(f"\nNumber of disapproved ads found: {results.total_results_count}")


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description=(
            "Lists disapproved ads for a given customer's specified "
            "campaign."
        )
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
        "-i", "--campaign_id", type=str, required=True, help="The campaign ID."
    )
    args: argparse.Namespace = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v22"
    )

    try:
        main(
            googleads_client,
            args.customer_id,
            args.campaign_id,
        )
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
