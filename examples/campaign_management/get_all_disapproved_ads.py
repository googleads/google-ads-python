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
import google.ads.google_ads.client


_DEFAULT_PAGE_SIZE = 1000


def main(client, customer_id, campaign_id, page_size):
    ga_service = client.get_service("GoogleAdsService", version="v5")

    query = f"""
        SELECT
          ad_group_ad.ad.id,
          ad_group_ad.ad.type,
          ad_group_ad.policy_summary.approval_status,
          ad_group_ad.policy_summary.policy_topic_entries
        FROM ad_group_ad
        WHERE
          campaign.id = {campaign_id}
          AND ad_group_ad.policy_summary.approval_status = DISAPPROVED"""

    try:
        results = ga_service.search(
            customer_id, query=query, page_size=page_size,
        )

        ad_type_enum = client.get_type("AdTypeEnum", version="v5").AdType
        policy_topic_entry_type_enum = client.get_type(
            "PolicyTopicEntryTypeEnum"
        ).PolicyTopicEntryType

        print("Disapproved ads:")

        approval_status_enum = client.get_type(
            "PolicyApprovalStatusEnum", version="v5"
        )

        # Iterate over all ads in all rows returned and count disapproved ads.
        for row in results:
            ad_group_ad = row.ad_group_ad
            ad = ad_group_ad.ad
            approval_status = ad_group_ad.policy_summary.approval_status

            print(
                'Ad with ID "%s" and type "%s" was disapproved with the '
                "following policy topic entries:"
                % (ad.id, ad_type_enum.Name(ad.type))
            )

            # Display the policy topic entries related to the ad disapproval.
            for entry in ad_group_ad.policy_summary.policy_topic_entries:
                print(
                    '\ttopic: "%s", type "%s"'
                    % (
                        entry.topic,
                        policy_topic_entry_type_enum.Name(entry.type),
                    )
                )

                # Display the attributes and values that triggered the policy
                # topic.
                for evidence in entry.evidences:
                    for index, text in enumerate(evidence.text_list.texts):
                        print("\t\tevidence text[%s]: %s" % (index, text.value))

        # The "num_results" field returns the number of items that have been
        # iterated in the results not the total number of rows returned by the
        # search query.
        print("\nNumber of disapproved ads found: %d" % results.num_results)
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print(
            'Request with ID "%s" failed with status "%s" and includes the '
            "following errors:" % (ex.request_id, ex.error.code().name)
        )
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print("\t\tOn field: %s" % field_path_element.field_name)
        sys.exit(1)


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = (
        google.ads.google_ads.client.GoogleAdsClient.load_from_storage()
    )

    parser = argparse.ArgumentParser(
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
    args = parser.parse_args()

    main(
        google_ads_client,
        args.customer_id,
        args.campaign_id,
        _DEFAULT_PAGE_SIZE,
    )
