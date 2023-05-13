#!/usr/bin/env python
# Copyright 2023 Google LLC
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
"""This example illustrates how to get basic campaigns stats by label text.

Campaign IDs are retrieved by using the label text. Another query is performed
to query the performance metrics of all campaigns containing that retrieved
label ID.
"""

import argparse
import sys
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id, label_text):
    ga_service = client.get_service("GoogleAdsService")

    query_labels = f"""
        SELECT
          campaign.id
        FROM
          campaign_label
        WHERE
          label.name = '{label_text}'
    """

    search_request = client.get_type("SearchGoogleAdsStreamRequest")
    search_request.customer_id = customer_id
    search_request.query = query_labels

    stream = ga_service.search_stream(search_request)

    campaign_ids = []
    for batch in stream:
        for row in batch.results:
            campaign_ids.append(row.campaign.id)

    if not campaign_ids:
        print(f"No campaigns found with label: {label_text}")
        return

    query_metrics = f"""
        SELECT
          campaign.id,
          campaign.name,
          metrics.clicks,
          metrics.cost_micros,
          metrics.conversions,
          metrics.conversions_value
        FROM
          campaign
        WHERE
          campaign.id IN ({','.join(map(str, campaign_ids))})
        AND
          segments.date DURING LAST_30_DAYS
    """

    search_request.query = query_metrics
    stream = ga_service.search_stream(search_request)

    for batch in stream:
        for row in batch.results:
            print(f'Campaign with ID "{row.campaign.id}" and name '
                  f'"{row.campaign.name}" had {row.metrics.clicks} clicks, '
                  f'cost {row.metrics.cost_micros / 1e6}, '
                  f'and had {row.metrics.conversions} conversions '
                  f'at a {row.metrics.conversions_value} conversion value '
                  f'over the last 30 days.')


if __name__ == "__main__":
    googleads_client = GoogleAdsClient.load_from_storage(version="v13")

    parser = argparse.ArgumentParser(
        description="Retrieves campaigns stats associated with a specified "
                    "label text."
    )
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )
    parser.add_argument(
        "-l",
        "--label_text",
        type=str,
        required=True,
        help="The text of the label to filter campaigns by.",
    )
    args = parser.parse_args()

    try:
        main(googleads_client, args.customer_id, args.label_text)
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

