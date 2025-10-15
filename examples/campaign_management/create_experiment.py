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
"""This example creates a new experiment and experiment arms.

It also demonstrates how to modify the draft campaign as well as begin the
experiment.
"""

import argparse
import sys
import uuid
from typing import List, Any

from google.api_core import protobuf_helpers

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.services.types.experiment_service import (
    ExperimentOperation,
    MutateExperimentsResponse,
)
from google.ads.googleads.v22.services.types.experiment_arm_service import (
    ExperimentArmOperation,
    MutateExperimentArmsRequest,
    MutateExperimentArmsResponse,
)
from google.ads.googleads.v22.resources.types.experiment import Experiment
from google.ads.googleads.v22.resources.types.experiment_arm import (
    ExperimentArm,
)
from google.ads.googleads.v22.services.services.experiment_service import (
    ExperimentServiceClient,
)
from google.ads.googleads.v22.services.services.experiment_arm_service import (
    ExperimentArmServiceClient,
)
from google.ads.googleads.v22.services.services.campaign_service import (
    CampaignServiceClient,
)
from google.ads.googleads.v22.services.types.campaign_service import (
    CampaignOperation,
)
from google.ads.googleads.v22.resources.types.campaign import Campaign


def main(
    client: GoogleAdsClient, customer_id: str, base_campaign_id: str
) -> None:
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        base_campaign_id: the campaign ID to associate with the control arm of
          the experiment.
    """
    experiment: str = create_experiment_resource(client, customer_id)
    draft_campaign: str = create_experiment_arms(
        client, customer_id, base_campaign_id, experiment
    )

    modify_draft_campaign(client, customer_id, draft_campaign)

    # When you're done setting up the experiment and arms and modifying the
    # draft campaign, this will begin the experiment.
    experiment_service: ExperimentServiceClient = client.get_service(
        "ExperimentService"
    )
    experiment_service.schedule_experiment(resource_name=experiment)


# [START create_experiment_1]
def create_experiment_resource(
    client: GoogleAdsClient, customer_id: str
) -> str:
    """Creates a new experiment resource.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.

    Returns:
        the resource name for the new experiment.
    """
    experiment_operation: ExperimentOperation = client.get_type(
        "ExperimentOperation"
    )
    experiment: Experiment = experiment_operation.create

    experiment.name = f"Example Experiment #{uuid.uuid4()}"
    experiment.type_ = client.enums.ExperimentTypeEnum.SEARCH_CUSTOM
    experiment.suffix = "[experiment]"
    experiment.status = client.enums.ExperimentStatusEnum.SETUP

    experiment_service: ExperimentServiceClient = client.get_service(
        "ExperimentService"
    )
    response: MutateExperimentsResponse = experiment_service.mutate_experiments(
        customer_id=customer_id, operations=[experiment_operation]
    )

    experiment_resource_name: str = response.results[0].resource_name
    print(f"Created experiment with resource name {experiment_resource_name}")

    return experiment_resource_name
    # [END create_experiment_1]


# [START create_experiment_2]
def create_experiment_arms(
    client: GoogleAdsClient,
    customer_id: str,
    base_campaign_id: str,
    experiment: str,
) -> str:
    """Creates a control and treatment experiment arms.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        base_campaign_id: the campaign ID to associate with the control arm of
          the experiment.
        experiment: the resource name for an experiment.

    Returns:
        the resource name for the new treatment experiment arm.
    """
    operations: List[ExperimentArmOperation] = []

    campaign_service: CampaignServiceClient = client.get_service(
        "CampaignService"
    )

    # The "control" arm references an already-existing campaign.
    operation_1: ExperimentArmOperation = client.get_type(
        "ExperimentArmOperation"
    )
    exa_1: ExperimentArm = operation_1.create
    exa_1.control = True
    exa_1.campaigns.append(
        campaign_service.campaign_path(customer_id, base_campaign_id)
    )
    exa_1.experiment = experiment
    exa_1.name = "control arm"
    exa_1.traffic_split = 40
    operations.append(operation_1)

    # The non-"control" arm, also called a "treatment" arm, will automatically
    # generate draft campaigns that you can modify before starting the
    # experiment.
    operation_2: ExperimentArmOperation = client.get_type(
        "ExperimentArmOperation"
    )
    exa_2: ExperimentArm = operation_2.create
    exa_2.control = False
    exa_2.experiment = experiment
    exa_2.name = "experiment arm"
    exa_2.traffic_split = 60
    operations.append(operation_2)

    experiment_arm_service: ExperimentArmServiceClient = client.get_service(
        "ExperimentArmService"
    )
    request: MutateExperimentArmsRequest = client.get_type(
        "MutateExperimentArmsRequest"
    )
    request.customer_id = customer_id
    request.operations = operations
    # We want to fetch the draft campaign IDs from the treatment arm, so the
    # easiest way to do that is to have the response return the newly created
    # entities.
    request.response_content_type = (
        client.enums.ResponseContentTypeEnum.MUTABLE_RESOURCE
    )
    response: MutateExperimentArmsResponse = (
        experiment_arm_service.mutate_experiment_arms(request=request)
    )

    # Results always return in the order that you specify them in the request.
    # Since we created the treatment arm second, it will be the second result.
    control_arm_result: Any = response.results[0]
    treatment_arm_result: Any = response.results[1]

    print(
        f"Created control arm with resource name {control_arm_result.resource_name}"
    )
    print(
        f"Created treatment arm with resource name {treatment_arm_result.resource_name}"
    )

    return treatment_arm_result.experiment_arm.in_design_campaigns[0]
    # [END create_experiment_2]


def modify_draft_campaign(
    client: GoogleAdsClient, customer_id: str, draft_campaign: str
) -> None:
    """Modifies the given in-design campaign.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        draft_campaign: the resource name for an in-design campaign.
    """
    campaign_service: CampaignServiceClient = client.get_service(
        "CampaignService"
    )
    campaign_operation: CampaignOperation = client.get_type("CampaignOperation")
    campaign: Campaign = campaign_operation.update
    campaign.resource_name = draft_campaign

    # You can change anything you like about the campaign. These are the changes
    # you're testing by doing this experiment. Here we just change the name for
    # illustrative purposes, but generally you may want to change more
    # meaningful parts of the campaign.
    campaign.name = f"Modified Campaign Name #{uuid.uuid4()}"

    client.copy_from(
        campaign_operation.update_mask,
        protobuf_helpers.field_mask(None, campaign._pb),
    )

    campaign_service.mutate_campaigns(
        customer_id=customer_id, operations=[campaign_operation]
    )

    print(f"Updated name for campaign {draft_campaign}")


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description=("Create a campaign experiment based on a campaign draft.")
    )
    # The following argument(s) need to be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )
    parser.add_argument(
        "-i",
        "--base_campaign_id",
        type=str,
        required=True,
        help="The campaign id.",
    )
    args: argparse.Namespace = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v22"
    )

    try:
        main(googleads_client, args.customer_id, args.base_campaign_id)
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
