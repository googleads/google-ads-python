# Encoding: utf-8
#
# Copyright 2022 Google LLC
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
""" This example creates a new experiment, experiment arms, and demonstrates
 how to modify the draft campaign as well as begin the experiment.
"""
import argparse
import sys
import uuid
from venv import create

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id, campaign_id):
    experiment = create_experiment_resource(client, customer_id)
    treatment_arm = create_experiment_arms(
        client, customer_id, campaign_id, experiment
    )
    draft_campaign = fetch_draft_campaign(client, customer_id, treatment_arm)

    modify_draft_campaign(client, customer_id, draft_campaign)

    # When you're done setting up the experiment and arms and modifying the draft
    # campaign, this will begin the experiment.
    experiment_service = client.get_service("ExperimentService")

    experiment_service.schedule_experiment(resource_name=experiment)


# [START create_experiment_1]
def create_experiment_resource(client, customer_id):
    experiment_operation = client.get_type("ExperimentOperation")
    experiment = experiment_operation.create

    experiment.name = f"Example Experiment #{uuid.uuid4()}"
    experiment.type = client.enums.ExperimentTypeEnum.SEARCH_CUSTOM
    experiment.suffix = "[experiment]"
    experiment.status = client.enums.ExperimentStatusEnum.SETUP

    try:
        experiment_service = client.get_service("ExperimentService")
        response = experiment_service.mutate_experiments(
            customer_id=customer_id, operations=[experiment_operation]
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

    experiment_resource_name = response.results[0].resource_name
    print(f"Created experiment with resource name {experiment_resource_name}")

    return experiment_resource_name


# [END create_experiment_1]


# [START create_experiment_2]
def create_experiment_arms(client, customer_id, campaign_id, experiment):
    operations = []

    campaign_service = client.get_service("CampaignService")

    # The "control" arm references an already-existing campaign.
    exa = client.get_type("ExperimentArm")
    exa.control = True
    exa.campaigns = campaign_service.campaign_path(customer_id, campaign_id)
    exa.trial = experiment
    exa.name = "control arm"
    exa.traffic_split = 40
    operations.append(exa)

    # The non-"control" arm, also called a "treatment" arm, will automatically
    # generate draft campaigns that you can modify before starting the
    # experiment.
    exa = client.get_type("ExperimentArm")
    exa.control = False
    exa.trial = experiment
    exa.name = "experiment arm"
    exa.traffic_split = 60
    operations.append(exa)

    try:
        experiment_arm_service = client.get_service("ExperimentArmService")
        response = experiment_arm_service.mutate_experiment_arms(
            customer_id, operations
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

    # Results always return in the order that you specify them in the request.
    # Since we created the treatment arm last, it will be the last result.  If
    # you don't remember which arm is the treatment arm, you can always filter
    # the query in the next section with `experiment_arm.control = false`.
    control_arm = response.results[0].resource_name
    treatment_arm = response.results[1].resource_name

    print(f"Created control arm with resource name {control_arm}")
    print(f"Created treatment arm with resource name {treatment_arm}")

    return treatment_arm


# [END create_experiment_2]


# [START create_experiment_3]
def fetch_draft_campaign(client, customer_id, treatment_arm):
    # The `in_design_campaigns` represent campaign drafts, which you can modify
    # before starting the experiment.

    ga_service = client.get_service("GoogleAdsService")

    query = f"""
    SELECT experiment_arm.in_design_campaigns
    FROM experiment_arm
    WHERE experiment_arm.resource_name = {treatment_arm}"""

    request = client.get_type("SearchGoogleAdsRequest")
    request.customer_id = customer_id
    request.query = query

    results = ga_service.search(request=request)

    # In design campaigns returns as a list, but for now it can only ever
    # contain a single ID, so we just grab the first one.
    draft_campaign = results[0].experiment_arm.in_design_campaigns[0]

    print(f"Found draft campaign with resource name {draft_campaign}")

    return draft_campaign


# [END create_experiment_3]


def modify_draft_campaign(client, customer_id, draft_campaign):

    campaign_service = client.get_service("CampaignService")
    campaign_operation = client.get_type("CampaignOperation")
    campaign = campaign_operation.update

    # You can change anything you like about the campaign. These are the changes you're testing
    # by doing this experiment. Here we just change the name for illustrative purposes, but
    # generally you may want to change more meaningful parts of the campaign.
    campaign.name = f"Modified Campaign Name #{uuid.uuid4()}"

    try:
        response = campaign_service.mutate_campaigns(
            customer_id=customer_id, operations=[campaign_operation]
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

    print(f"Updated name for campaign {draft_campaign}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=("Create a campaign experiment based on a campaign draft.")
    )
    # The following argument(s) need to be provided to run the example.
    parser.add_argument(
        "-a",
        "--api_version",
        type=int,
        required=True,
        help="The version of the Google Ads API`.",
    )
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )
    parser.add_argument(
        "-i",
        "--campaign_id",
        type=str,
        required=True,
        help="The campaign id.",
    )
    args = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(
        version=args.api_version
    )

    main(googleads_client, args.customer_id, args.campaign_id)
