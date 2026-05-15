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
"""This example shows how to create an OPTIMIZE_ASSETS experiment.

Asset optimization experiments are used to test different asset combinations
within Performance Max campaigns.
"""

import argparse
import sys
from typing import List, Tuple, Any
from uuid import uuid4

from examples.utils.example_helpers import get_image_bytes_from_url
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v24.services.types.google_ads_service import (
    MutateOperation,
)


def main(
    client: GoogleAdsClient, customer_id: str, asset_group_id: str
) -> None:
    """Creates an OPTIMIZE_ASSETS experiment.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: The Google Ads customer ID.
        asset_group_id: The base asset group ID to run the experiment on.
    """
    googleads_service = client.get_service("GoogleAdsService")

    # Query the asset group to find the associated campaign resource name.
    query = f"""
        SELECT asset_group.campaign
        FROM asset_group
        WHERE asset_group.id = {asset_group_id}
    """
    search_response = googleads_service.search(
        customer_id=customer_id, query=query
    )
    if len(search_response):
        campaign_resource_name = search_response[0].asset_group.campaign
    else:
        print(f"Asset group with ID {asset_group_id} not found.")
        sys.exit(1)

    # Temp IDs
    ASSET_1_TEMP_ID = "-1"
    EXPERIMENT_TEMP_ID = "-2"
    ASSET_2_TEMP_ID = "-3"

    # [START create_asset_optimization_experiment_1]
    # 1. Create Assets with temporary resource names.
    # We create a text asset and an image asset to showcase different types.
    asset_operation_1 = create_text_asset_operation(
        client,
        customer_id,
        ASSET_1_TEMP_ID,
        "Fly to Mars!",
    )
    asset_operation_2 = create_image_asset_operation(
        client,
        customer_id,
        ASSET_2_TEMP_ID,
        "https://gaagl.page.link/Eit5",
        "Mars Landscape View",
    )

    # 2. Create an Experiment with a temporary resource name.
    experiment_operation = client.get_type("MutateOperation")
    experiment = experiment_operation.experiment_operation.create
    experiment.resource_name = googleads_service.experiment_path(
        customer_id, EXPERIMENT_TEMP_ID
    )
    experiment.name = f"Interstellar Asset Experiment #{uuid4()}"
    experiment.type_ = client.enums.ExperimentTypeEnum.OPTIMIZE_ASSETS
    # Set the optimize assets experiment subtype to COMPARE_ASSETS.
    experiment.optimize_assets_experiment.optimize_assets_experiment_subtype = (
        client.enums.OptimizeAssetsExperimentSubtypeEnum.COMPARE_ASSETS
    )

    # 3. Create two ExperimentArm resources.
    treatment_assets = [
        (ASSET_1_TEMP_ID, client.enums.AssetFieldTypeEnum.HEADLINE),
        (ASSET_2_TEMP_ID, client.enums.AssetFieldTypeEnum.MARKETING_IMAGE),
    ]
    arm_operations = create_arms_operations(
        client,
        customer_id,
        EXPERIMENT_TEMP_ID,
        campaign_resource_name,
        asset_group_id,
        treatment_assets,
    )

    # 4. Create AssetGroupAssets linking the assets to the asset group.
    asset_group_asset_operation_1 = create_asset_group_asset_operation(
        client,
        customer_id,
        asset_group_id,
        ASSET_1_TEMP_ID,
        client.enums.AssetFieldTypeEnum.HEADLINE,
    )
    asset_group_asset_operation_2 = create_asset_group_asset_operation(
        client,
        customer_id,
        asset_group_id,
        ASSET_2_TEMP_ID,
        client.enums.AssetFieldTypeEnum.MARKETING_IMAGE,
    )

    # Send all operations in a single Mutate request.
    # The operations must be in this specific order.
    mutate_operations = [
        asset_operation_1,
        asset_operation_2,
        experiment_operation,
        *arm_operations,
        asset_group_asset_operation_1,
        asset_group_asset_operation_2,
    ]

    response = googleads_service.mutate(
        customer_id=customer_id,
        mutate_operations=mutate_operations,
    )
    # [END create_asset_optimization_experiment_1]

    # Print the results.
    print(
        "Created headline asset:"
        f" {response.mutate_operation_responses[0].asset_result.resource_name}"
    )
    print(
        "Created image asset:"
        f" {response.mutate_operation_responses[1].asset_result.resource_name}"
    )
    print(
        "Created experiment:"
        f" {response.mutate_operation_responses[2].experiment_result.resource_name}"
    )
    print(
        "Created control arm:"
        f" {response.mutate_operation_responses[3].experiment_arm_result.resource_name}"
    )
    print(
        "Created treatment arm:"
        f" {response.mutate_operation_responses[4].experiment_arm_result.resource_name}"
    )
    print(
        "Created asset group asset for headline:"
        f" {response.mutate_operation_responses[5].asset_group_asset_result.resource_name}"
    )
    print(
        "Created asset group asset for image:"
        f" {response.mutate_operation_responses[6].asset_group_asset_result.resource_name}"
    )


def create_text_asset_operation(
    client: GoogleAdsClient, customer_id: str, temp_id: str, text: str
) -> MutateOperation:
    """Creates a mutate operation for a text asset."""
    googleads_service = client.get_service("GoogleAdsService")
    operation = client.get_type("MutateOperation")
    asset = operation.asset_operation.create
    asset.resource_name = googleads_service.asset_path(customer_id, temp_id)
    asset.text_asset.text = text
    return operation


def create_image_asset_operation(
    client: GoogleAdsClient,
    customer_id: str,
    temp_id: str,
    url: str,
    name: str,
) -> MutateOperation:
    """Creates a mutate operation for an image asset."""
    googleads_service = client.get_service("GoogleAdsService")
    operation = client.get_type("MutateOperation")
    asset = operation.asset_operation.create
    asset.resource_name = googleads_service.asset_path(customer_id, temp_id)
    asset.name = name
    asset.type_ = client.enums.AssetTypeEnum.IMAGE
    asset.image_asset.data = get_image_bytes_from_url(url)
    return operation


def create_arms_operations(
    client: GoogleAdsClient,
    customer_id: str,
    experiment_temp_id: str,
    campaign_resource_name: str,
    asset_group_id: str,
    treatment_assets: List[Tuple[str, Any]],
) -> List[MutateOperation]:
    """Creates mutate operations for control and treatment arms."""
    googleads_service = client.get_service("GoogleAdsService")
    experiment_arm_type = client.get_type("ExperimentArm")
    operations = []

    # Control arm
    control_operation = client.get_type("MutateOperation")
    control = control_operation.experiment_arm_operation.create
    control.experiment = googleads_service.experiment_path(
        customer_id, experiment_temp_id
    )
    control.name = "Base Assets (Control)"
    control.control = True
    control.traffic_split = 50
    control.campaigns.append(campaign_resource_name)

    asset_group_info_control = experiment_arm_type.AssetGroupInfo()
    asset_group_info_control.asset_group = googleads_service.asset_group_path(
        customer_id, asset_group_id
    )
    control.asset_groups.append(asset_group_info_control)
    operations.append(control_operation)

    # Treatment arm
    treatment_operation = client.get_type("MutateOperation")
    treatment = treatment_operation.experiment_arm_operation.create
    treatment.experiment = googleads_service.experiment_path(
        customer_id, experiment_temp_id
    )
    treatment.name = "New Assets (Treatment)"
    treatment.control = False
    treatment.traffic_split = 50
    treatment.campaigns.append(campaign_resource_name)

    asset_group_info_treatment = experiment_arm_type.AssetGroupInfo()
    asset_group_info_treatment.asset_group = googleads_service.asset_group_path(
        customer_id, asset_group_id
    )

    for asset_temp_id, field_type in treatment_assets:
        asset_group_asset_info = experiment_arm_type.AssetGroupAssetInfo()
        asset_group_asset_info.asset = googleads_service.asset_path(
            customer_id, asset_temp_id
        )
        asset_group_asset_info.field_type = field_type
        asset_group_info_treatment.asset_group_assets.append(
            asset_group_asset_info
        )

    treatment.asset_groups.append(asset_group_info_treatment)
    operations.append(treatment_operation)

    return operations


def create_asset_group_asset_operation(
    client: GoogleAdsClient,
    customer_id: str,
    asset_group_id: str,
    asset_temp_id: str,
    field_type: Any,
) -> MutateOperation:
    """Creates a mutate operation for an asset group asset."""
    googleads_service = client.get_service("GoogleAdsService")
    operation = client.get_type("MutateOperation")
    aga = operation.asset_group_asset_operation.create
    aga.asset_group = googleads_service.asset_group_path(
        customer_id, asset_group_id
    )
    aga.asset = googleads_service.asset_path(customer_id, asset_temp_id)
    aga.field_type = field_type
    return operation


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Creates an OPTIMIZE_ASSETS experiment."
    )
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )
    parser.add_argument(
        "-a",
        "--asset_group_id",
        type=str,
        required=True,
        help="The base asset group ID to run the experiment on.",
    )
    args = parser.parse_args()

    googleads_client = GoogleAdsClient.load_from_storage(version="v24")

    try:
        main(googleads_client, args.customer_id, args.asset_group_id)
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
