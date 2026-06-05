#!/usr/bin/env python
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
"""Retrieves performance metrics for an experiment, evaluates the performance,
and takes action on the experiment accordingly.

It shows how to query statistical significance metrics for the experiment,
and how to execute actions such as promoting, ending, or graduating an experiment.
"""

import argparse
import sys
import uuid

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v24.services.services.google_ads_service import (
    GoogleAdsServiceClient,
)
from google.ads.googleads.v24.services.types.google_ads_service import (
    SearchGoogleAdsRequest,
    SearchGoogleAdsResponse,
    GoogleAdsRow,
)
from google.ads.googleads.v24.services.services.experiment_service import (
    ExperimentServiceClient,
)
from google.ads.googleads.v24.services.services.campaign_budget_service import (
    CampaignBudgetServiceClient,
)
from google.ads.googleads.v24.services.types.experiment_service import (
    CampaignBudgetMapping,
)

# Constants for decision making
# Choose a confidence level based on your specific needs.
# - The p-value (probability value) is the probability that the observed performance
#   difference between control and treatment occurred by random chance rather than due
#   to the changes in the experiment. A lower p-value represents higher confidence.
# - For example, a p-value threshold of 0.05 corresponds to a 95% confidence level
#   (the academic standard for statistical significance).
P_VALUE_THRESHOLD = 0.05  # 95% confidence level


def main(client: GoogleAdsClient, customer_id: str, experiment_id: str) -> None:
    """Queries experiment performance, evaluates the performance metrics, and updates
    the experiment accordingly (graduates, promotes, ends, or allows to continue running).

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        experiment_id: the experiment ID.
    """
    ga_service: GoogleAdsServiceClient = client.get_service("GoogleAdsService")

    # Query to retrieve the experiment.
    # Notice that we request the statistical metrics (for example, p-value, point estimate,
    # margin of error) which are populated based on the treatment arm.
    query = f"""
        SELECT
          experiment.resource_name,
          experiment.name,
          experiment.experiment_id,
          experiment.type,
          metrics.conversions_absolute_change_p_value,
          metrics.conversions_absolute_change_point_estimate,
          metrics.conversions_absolute_change_margin_of_error,
          metrics.clicks_p_value,
          metrics.clicks_point_estimate,
          metrics.clicks_margin_of_error
        FROM experiment
        WHERE experiment.experiment_id = {experiment_id}
    """

    # Issues a search request.
    search_request: SearchGoogleAdsRequest = client.get_type(
        "SearchGoogleAdsRequest"
    )
    search_request.customer_id = customer_id
    search_request.query = query

    results: SearchGoogleAdsResponse = ga_service.search(request=search_request)

    experiment_found = False
    row: GoogleAdsRow
    # There should be at most one row.
    for row in results:
        experiment_found = True
        print(f"Found experiment: {row.experiment.name}")
        print(f"  Resource Name: {row.experiment.resource_name}")

        evaluate_experiment(client, customer_id, row)
    if not experiment_found:
        print(f"No experiment found for experiment ID: {experiment_id}")


# [START evaluate_and_update_experiment_1]
def evaluate_experiment(
    client: GoogleAdsClient, customer_id: str, row: GoogleAdsRow
) -> None:
    """Evaluates the performance of the experiment and updates it accordingly
    (for example, promotes, ends, or graduates).

    Checks conversion and click metrics against statistical significance thresholds
    to determine the appropriate action to take on the experiment.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        row: a GoogleAdsRow containing the experiment and metrics.
    """
    # This function evaluates performance metrics and immediately takes action
    # to update the experiment's status (promote, end, or graduate) if
    # statistical significance thresholds are met.
    metrics = row.metrics
    experiment_resource_name = row.experiment.resource_name

    has_conv_metrics = (
        "conversions_absolute_change_p_value" in metrics
        and "conversions_absolute_change_point_estimate" in metrics
        and "conversions_absolute_change_margin_of_error" in metrics
    )
    has_click_metrics = (
        "clicks_p_value" in metrics
        and "clicks_point_estimate" in metrics
        and "clicks_margin_of_error" in metrics
    )

    # 1. Evaluate conversion success as a primary success signal if available.
    # - Point Estimate: Represents the estimated average lift or difference in conversions.
    # - Margin of Error: Outlines the confidence interval bounds. Note that the margin_of_error provided by the API is calculated for a preset confidence level which is set based on the experiment type.
    # - Lower Bound: (Point Estimate - Margin of Error). If this value is above 0,
    #   we have statistical significance that performance has improved.
    if has_conv_metrics:
        conv_p_value = metrics.conversions_absolute_change_p_value
        conv_lift = metrics.conversions_absolute_change_point_estimate
        conv_error = metrics.conversions_absolute_change_margin_of_error
        conv_lower_bound = conv_lift - conv_error

        if conv_p_value <= P_VALUE_THRESHOLD:
            if conv_lower_bound > 0:
                print(
                    "Significant Success: Conversions increased. Even at the lower"
                    f" bound, the lift is {conv_lower_bound:.2f}. Promoting"
                    " changes."
                )
                promote_experiment(
                    client, customer_id, experiment_resource_name
                )
                return
            elif (conv_lift + conv_error) < 0:
                print(
                    "Significant Decline: Even the upper bound"
                    f" ({conv_lift + conv_error:.2f}) is below zero. Ending"
                    " experiment."
                )
                end_experiment(client, customer_id, experiment_resource_name)
                return

        # 2. Evaluate click volume as a secondary signal.
        # This is helpful as an early indicator or for lower-volume accounts.
        click_p_value = metrics.clicks_p_value
        click_lift = metrics.clicks_point_estimate
        click_error = metrics.clicks_margin_of_error
        click_lower_bound = click_lift - click_error

        if click_p_value <= P_VALUE_THRESHOLD and click_lower_bound > 0:
            # We have a directional winner: high confidence in more traffic,
            # but not enough data to confirm conversion impact yet.
            print(f"Click volume is significantly up (+{click_lift*100:.1f}%).")

            # Graduation is only supported for separate campaign experiments, not
            # intra-campaign experiments where there is no separate treatment campaign.
            experiment_type_name = row.experiment.type_.name
            if (
                experiment_type_name != "ADOPT_BROAD_MATCH_KEYWORDS"
                and experiment_type_name != "ADOPT_AI_MAX"
            ):
                print(
                    "Graduating treatment campaign for further manual analysis."
                )
                graduate_experiment(
                    client, customer_id, experiment_resource_name
                )
            else:
                print(
                    "Intra-campaign trial detected: graduation is not supported. "
                    "Continuing to run the experiment to gather more conversion data."
                )
            return

    # 3. Print status if no action was taken.
    if has_conv_metrics or has_click_metrics:
        conv_status = (
            f"Conversions (p={metrics.conversions_absolute_change_p_value:.2f}, "
            f"lift={metrics.conversions_absolute_change_point_estimate:.2f} +/- "
            f"{metrics.conversions_absolute_change_margin_of_error:.2f})"
            if has_conv_metrics
            else "Conversions (not populated)"
        )
        click_status = (
            f"Clicks (p={metrics.clicks_p_value:.2f}, "
            f"lift={metrics.clicks_point_estimate:.2f} +/- "
            f"{metrics.clicks_margin_of_error:.2f})"
            if has_click_metrics
            else "Clicks (not populated)"
        )
        print(
            f"Inconclusive: No significant action taken. {conv_status}, {click_status}."
            " Allowing the experiment to continue running."
        )
    else:
        print(
            "Conversion and click performance metrics are not yet populated. "
            "Allowing the experiment to continue running."
        )
        # [END evaluate_and_update_experiment_1]


def promote_experiment(
    client: GoogleAdsClient, customer_id: str, experiment_resource_name: str
) -> None:
    """Promotes the experiment trial campaign to the base campaign.

    Promotion is an asynchronous long-running process that copies the trial
    campaign's settings and creatives back to the base campaign and subsequently
    ends the experiment.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        experiment_resource_name: the resource name of the experiment to promote.
    """
    experiment_service: ExperimentServiceClient = client.get_service(
        "ExperimentService"
    )
    # This method returns a long running operation (LRO).
    # - To block until the operation is complete: call operation.result()
    # - For non-blocking status checks: use operation.done()
    # - For manual polling or persistent tracking: store operation.operation.name
    #
    # For more information on handling LROs, see:
    # https://developers.google.com/google-ads/api/docs/concepts/long-running-operations
    operation = experiment_service.promote_experiment(
        resource_name=experiment_resource_name
    )
    print(f"Started promotion for experiment: {experiment_resource_name}")
    print(
        "The promotion is running asynchronously. You can track its progress"
        f" using the long-running operation: {operation.operation.name}"
    )
    print(
        "Best Practice: If the promotion fails, you can retrieve the full list"
        " of errors by calling ExperimentService.ListExperimentAsyncErrors."
    )


def end_experiment(
    client: GoogleAdsClient, customer_id: str, experiment_resource_name: str
) -> None:
    """Immediately ends the experiment.

    Terminates the traffic split and sets the end date to the current time.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        experiment_resource_name: the resource name of the experiment to end.
    """
    experiment_service: ExperimentServiceClient = client.get_service(
        "ExperimentService"
    )
    experiment_service.end_experiment(experiment=experiment_resource_name)
    print(f"Successfully ended experiment: {experiment_resource_name}")


def graduate_experiment(
    client: GoogleAdsClient, customer_id: str, experiment_resource_name: str
) -> None:
    """Graduates the experiment to a full standalone campaign.

    This process involves creating a new budget and mapping the treatment campaign to it.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        experiment_resource_name: the resource name of the experiment to graduate.
    """
    # 1. Create a new campaign budget for the graduating campaign.
    campaign_budget_service: CampaignBudgetServiceClient = client.get_service(
        "CampaignBudgetService"
    )
    campaign_budget_operation = client.get_type("CampaignBudgetOperation")
    campaign_budget = campaign_budget_operation.create
    campaign_budget.name = f"Graduated Experiment Budget #{uuid.uuid4()}"
    campaign_budget.amount_micros = 50_000_000  # $50.00/day budget
    campaign_budget.delivery_method = (
        client.enums.BudgetDeliveryMethodEnum.STANDARD
    )

    response = campaign_budget_service.mutate_campaign_budgets(
        customer_id=customer_id, operations=[campaign_budget_operation]
    )
    budget_resource_name = response.results[0].resource_name
    print(
        "Created new standalone campaign budget with resource name:"
        f" {budget_resource_name}"
    )

    # 2. Query the experiment_arm to retrieve the treatment campaign's resource name.
    # The treatment arm has control set to False.
    ga_service: GoogleAdsServiceClient = client.get_service("GoogleAdsService")
    # Query for the campaigns associated with the treatment arm of the experiment.
    query = f"""
        SELECT
          experiment_arm.campaigns
        FROM experiment_arm
        WHERE experiment_arm.experiment = '{experiment_resource_name}'
          AND experiment_arm.control = FALSE
    """
    search_response = ga_service.search(customer_id=customer_id, query=query)

    # Find the resource name of the treatment campaign.
    treatment_campaign_resource_name = None
    for row in search_response:
        if row.experiment_arm.campaigns:
            treatment_campaign_resource_name = row.experiment_arm.campaigns[0]
            break

    # Verify that a treatment campaign was found.
    if not treatment_campaign_resource_name:
        print(
            "Could not find the treatment campaign associated with this"
            " experiment."
        )
        return

    # 3. Build the budget mapping and execute the graduation request.
    experiment_service: ExperimentServiceClient = client.get_service(
        "ExperimentService"
    )
    budget_mapping: CampaignBudgetMapping = client.get_type(
        "CampaignBudgetMapping"
    )
    budget_mapping.experiment_campaign = treatment_campaign_resource_name
    budget_mapping.campaign_budget = budget_resource_name

    experiment_service.graduate_experiment(
        experiment=experiment_resource_name,
        campaign_budget_mappings=[budget_mapping],
    )
    print(
        "Successfully graduated experiment campaign"
        f" {treatment_campaign_resource_name} with new budget"
        f" {budget_resource_name}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Retrieves performance metrics for an experiment, evaluates the"
            " performance and takes action on the experiment accordingly."
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
        "-e",
        "--experiment_id",
        type=str,
        required=True,
        help="The experiment ID.",
    )
    args: argparse.Namespace = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v24"
    )

    try:
        main(
            googleads_client,
            args.customer_id,
            args.experiment_id,
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
