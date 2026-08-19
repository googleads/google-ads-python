# Copyright 2026 Google LLC
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
"""Creates an ADOPT_AI_MAX intra-campaign experiment for a Search campaign.

Intra-campaign experiments split traffic *within* the campaign, based on whether
the feature (in this case, AI Max) is enabled or not.
"""

import argparse
import sys
from uuid import uuid4

from google.api_core import protobuf_helpers

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client: GoogleAdsClient, customer_id: str, campaign_id: str) -> None:
    """Creates an ADOPT_AI_MAX intra-campaign experiment for a Search campaign.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: The Google Ads customer ID.
        campaign_id: The campaign ID to run the experiment on.
    """
    googleads_service = client.get_service("GoogleAdsService")

    # [START create_search_adopt_ai_max_experiment_1]
    # Create the experiment resource name using a temporary ID.
    experiment_resource_name = googleads_service.experiment_path(
        customer_id, "-1"
    )

    # Create the experiment.
    experiment_operation = client.get_type("MutateOperation")
    experiment = experiment_operation.experiment_operation.create
    experiment.resource_name = experiment_resource_name
    experiment.name = f"ADOPT_AI_MAX Experiment #{uuid4()}"
    experiment.type_ = client.enums.ExperimentTypeEnum.ADOPT_AI_MAX

    # Create the control arm. Both arms in an intra-campaign experiment
    # reference the same base campaign.
    control_arm_operation = client.get_type("MutateOperation")
    control_arm = control_arm_operation.experiment_arm_operation.create
    control_arm.experiment = experiment_resource_name
    control_arm.name = "Control Arm"
    control_arm.control = True
    control_arm.traffic_split = 50
    control_arm.campaigns.append(
        googleads_service.campaign_path(customer_id, campaign_id)
    )

    # Create the treatment arm.
    treatment_arm_operation = client.get_type("MutateOperation")
    treatment_arm = treatment_arm_operation.experiment_arm_operation.create
    treatment_arm.experiment = experiment_resource_name
    treatment_arm.name = "Treatment Arm"
    treatment_arm.control = False
    treatment_arm.traffic_split = 50
    treatment_arm.campaigns.append(
        googleads_service.campaign_path(customer_id, campaign_id)
    )

    # Create a campaign operation with an update mask to enable AI Max and
    # configure asset automation settings.
    # Note: For intra-campaign experiments, these settings are applied to the
    # base campaign but are only active for the treatment traffic split.
    campaign_operation = client.get_type("MutateOperation")
    campaign = campaign_operation.campaign_operation.update
    campaign.resource_name = googleads_service.campaign_path(
        customer_id, campaign_id
    )
    campaign.ai_max_setting.enable_ai_max = True

    for asset_automation_type_enum in [
        client.enums.AssetAutomationTypeEnum.TEXT_ASSET_AUTOMATION,
        client.enums.AssetAutomationTypeEnum.FINAL_URL_EXPANSION_TEXT_ASSET_AUTOMATION,
    ]:
        asset_automation_setting = client.get_type(
            "Campaign"
        ).AssetAutomationSetting()
        asset_automation_setting.asset_automation_type = (
            asset_automation_type_enum
        )
        asset_automation_setting.asset_automation_status = (
            client.enums.AssetAutomationStatusEnum.OPTED_IN
        )
        campaign.asset_automation_settings.append(asset_automation_setting)

    client.copy_from(
        campaign_operation.campaign_operation.update_mask,
        protobuf_helpers.field_mask(None, campaign._pb),
    )

    # Send all mutate operations in a single Mutate request.
    mutate_operations = [
        experiment_operation,
        control_arm_operation,
        treatment_arm_operation,
        campaign_operation,
    ]

    response = googleads_service.mutate(
        customer_id=customer_id,
        mutate_operations=mutate_operations,
    )
    # [END create_search_adopt_ai_max_experiment_1]

    # Print the results.
    # The results will be returned in the same order as the mutate operations.
    experiment_result = response.mutate_operation_responses[0].experiment_result
    control_arm_result = response.mutate_operation_responses[
        1
    ].experiment_arm_result
    treatment_arm_result = response.mutate_operation_responses[
        2
    ].experiment_arm_result
    campaign_result = response.mutate_operation_responses[3].campaign_result

    print(f"Created experiment: {experiment_result.resource_name}")
    print(f"Created control arm: {control_arm_result.resource_name}")
    print(f"Created treatment arm: {treatment_arm_result.resource_name}")
    print(f"Updated campaign to enable AI Max: {campaign_result.resource_name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Adds an ADOPT_AI_MAX intra-campaign experiment."
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
        "-i",
        "--campaign_id",
        type=str,
        required=True,
        help="The campaign ID to run the experiment on.",
    )
    args = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v24")

    try:
        main(googleads_client, args.customer_id, args.campaign_id)
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
