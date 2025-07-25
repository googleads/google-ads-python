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
"""Adds complete campaigns using BatchJobService.

Complete campaigns include campaign budgets, campaigns, ad groups and keywords.
"""


import argparse
import asyncio
import sys
from uuid import uuid4
from typing import Any, List, Coroutine

from google.api_core.operation import Operation

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v20.services.services.batch_job_service import (
    BatchJobServiceClient,
)
from google.ads.googleads.v20.services.types.batch_job_service import (
    MutateBatchJobResponse,
    AddBatchJobOperationsResponse,
    ListBatchJobResultsRequest,
    ListBatchJobResultsResponse,
)
from google.ads.googleads.v20.services.types.google_ads_service import (
    MutateOperation,
)
from google.ads.googleads.v20.resources.types.batch_job import BatchJob
from google.ads.googleads.v20.services.types.campaign_budget_service import (
    CampaignBudgetOperation,
)
from google.ads.googleads.v20.services.types.campaign_service import (
    CampaignOperation,
)
from google.ads.googleads.v20.services.types.campaign_criterion_service import (
    CampaignCriterionOperation,
)
from google.ads.googleads.v20.services.types.ad_group_service import (
    AdGroupOperation,
)
from google.ads.googleads.v20.services.types.ad_group_criterion_service import (
    AdGroupCriterionOperation,
)
from google.ads.googleads.v20.services.types.ad_group_ad_service import (
    AdGroupAdOperation,
)
from google.ads.googleads.v20.services.types.batch_job_service import (
    BatchJobOperation,
)


NUMBER_OF_CAMPAIGNS_TO_ADD: int = 2
NUMBER_OF_AD_GROUPS_TO_ADD: int = 2
NUMBER_OF_KEYWORDS_TO_ADD: int = 4

_temporary_id: int = 0


def get_next_temporary_id() -> int:
    """Returns the next temporary ID to use in batch job operations.

    Decrements the temporary ID by one before returning it. The first value
    returned for the ID is -1.

    Returns: an int of the next temporary ID.
    """
    global _temporary_id
    _temporary_id -= 1
    return _temporary_id


def build_mutate_operation(
    client: GoogleAdsClient, operation_type: str, operation: Any
) -> MutateOperation:
    """Builds a mutate operation with the given operation type and operation.

    Args:
        client: an initialized GoogleAdsClient instance.
        operation_type: a str of the operation type corresponding to a field on
            the MutateOperation message class.
        operation: an operation instance.

    Returns: a MutateOperation instance
    """
    mutate_operation: MutateOperation = client.get_type("MutateOperation")
    # Retrieve the nested operation message instance using getattr then copy the
    # contents of the given operation into it using the client.copy_from method.
    client.copy_from(getattr(mutate_operation, operation_type), operation)
    return mutate_operation


async def main(client: GoogleAdsClient, customer_id: str) -> None:
    """Main function that runs the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a str of a customer ID.
    """
    batch_job_service: BatchJobServiceClient = client.get_service(
        "BatchJobService"
    )
    batch_job_operation: BatchJobOperation = create_batch_job_operation(client)
    resource_name: str = create_batch_job(
        batch_job_service, customer_id, batch_job_operation
    )
    operations: List[MutateOperation] = build_all_operations(
        client, customer_id
    )
    add_all_batch_job_operations(batch_job_service, operations, resource_name)
    operations_response: Operation = run_batch_job(
        batch_job_service, resource_name
    )

    # Create an asyncio.Event instance to control execution during the
    # asynchronous steps in _poll_batch_job. Note that this is not important
    # for polling asynchronously, it simply helps with execution control, so we
    # can run _fetch_and_print_results after the asynchronous operations have
    # completed.
    done_event: asyncio.Event = asyncio.Event()
    poll_batch_job(operations_response, done_event)
    # Execution will stop here and wait for the asynchronous steps in
    # _poll_batch_job to complete before proceeding.
    await done_event.wait()

    fetch_and_print_results(client, batch_job_service, resource_name)


def create_batch_job_operation(client: GoogleAdsClient) -> BatchJobOperation:
    """Created a BatchJobOperation and sets an empty BatchJob instance to
    the "create" property in order to tell the Google Ads API that we're
    creating a new BatchJob.

    Args:
        client: an initialized GoogleAdsClient instance.

    Returns: a BatchJobOperation with a BatchJob instance set in the "create"
        property.
    """
    batch_job_operation: BatchJobOperation = client.get_type(
        "BatchJobOperation"
    )
    batch_job: BatchJob = client.get_type("BatchJob")
    client.copy_from(batch_job_operation.create, batch_job)
    return batch_job_operation


# [START add_complete_campaigns_using_batch_job]
def create_batch_job(
    batch_job_service: BatchJobServiceClient,
    customer_id: str,
    batch_job_operation: BatchJobOperation,
) -> str:
    """Creates a batch job for the specified customer ID.

    Args:
        batch_job_service: an instance of the BatchJobService message class.
        customer_id: a str of a customer ID.
        batch_job_operation: a BatchJobOperation instance set to "create"

    Returns: a str of a resource name for a batch job.
    """
    try:
        response: MutateBatchJobResponse = batch_job_service.mutate_batch_job(
            customer_id=customer_id, operation=batch_job_operation
        )
        resource_name: str = response.result.resource_name
        print(f'Created a batch job with resource name "{resource_name}"')
        return resource_name
    except GoogleAdsException as exception:
        handle_googleads_exception(exception)
        # This line will likely not be reached due to sys.exit(1) in handle_googleads_exception
        # but to satisfy the type checker, we add a return statement.
        return ""  # Or raise an exception
        # [END add_complete_campaigns_using_batch_job]


# [START add_complete_campaigns_using_batch_job_1]
def add_all_batch_job_operations(
    batch_job_service: BatchJobServiceClient,
    operations: List[MutateOperation],
    resource_name: str,
) -> None:
    """Adds all mutate operations to the batch job.

    As this is the first time for this batch job, we pass null as a sequence
    token. The response will contain the next sequence token that we can use
    to upload more operations in the future.

    Args:
        batch_job_service: an instance of the BatchJobService message class.
        operations: a list of a mutate operations.
        resource_name: a str of a resource name for a batch job.
    """
    try:
        response: AddBatchJobOperationsResponse = (
            batch_job_service.add_batch_job_operations(
                resource_name=resource_name,
                sequence_token=None,  # type: ignore
                mutate_operations=operations,
            )
        )

        print(
            f"{response.total_operations} mutate operations have been "
            "added so far."
        )

        # You can use this next sequence token for calling
        # add_batch_job_operations() next time.
        print(
            "Next sequence token for adding next operations is "
            f"{response.next_sequence_token}"
        )
    except GoogleAdsException as exception:
        handle_googleads_exception(exception)
        # [END add_complete_campaigns_using_batch_job_1]


def build_all_operations(
    client: GoogleAdsClient, customer_id: str
) -> List[MutateOperation]:
    """Builds all operations for creating a complete campaign.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a str of a customer ID.

    Returns: a list of operations of various types.
    """
    operations: List[MutateOperation] = []

    # Creates a new campaign budget operation and adds it to the list of
    # mutate operations.
    campaign_budget_op: CampaignBudgetOperation = (
        build_campaign_budget_operation(client, customer_id)
    )
    operations.append(
        build_mutate_operation(
            client, "campaign_budget_operation", campaign_budget_op
        )
    )

    # Creates new campaign operations and adds them to the list of
    # mutate operations.
    campaign_operations: List[CampaignOperation] = build_campaign_operations(
        client, customer_id, campaign_budget_op.create.resource_name
    )
    operations.extend(
        build_mutate_operation(client, "campaign_operation", operation)
        for operation in campaign_operations
    )

    # Creates new campaign criterion operations and adds them to the list of
    # mutate operations.
    campaign_criterion_operations: List[CampaignCriterionOperation] = (
        build_campaign_criterion_operations(client, campaign_operations)
    )
    operations.extend(
        build_mutate_operation(
            client, "campaign_criterion_operation", operation
        )
        for operation in campaign_criterion_operations
    )

    # Creates new ad group operations and adds them to the list of
    # mutate operations.
    ad_group_operations: List[AdGroupOperation] = build_ad_group_operations(
        client, customer_id, campaign_operations
    )
    operations.extend(
        build_mutate_operation(client, "ad_group_operation", operation)
        for operation in ad_group_operations
    )

    # Creates new ad group criterion operations and add them to the list of
    # mutate operations.
    ad_group_criterion_operations: List[AdGroupCriterionOperation] = (
        build_ad_group_criterion_operations(client, ad_group_operations)
    )
    operations.extend(
        build_mutate_operation(
            client, "ad_group_criterion_operation", operation
        )
        for operation in ad_group_criterion_operations
    )

    # Creates new ad group ad operations and adds them to the list of
    # mutate operations.
    ad_group_ad_operations: List[AdGroupAdOperation] = (
        build_ad_group_ad_operations(client, ad_group_operations)
    )
    operations.extend(
        build_mutate_operation(client, "ad_group_ad_operation", operation)
        for operation in ad_group_ad_operations
    )

    return operations


def build_campaign_budget_operation(
    client: GoogleAdsClient, customer_id: str
) -> CampaignBudgetOperation:
    """Builds a new campaign budget operation for the given customer ID.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a str of a customer ID.

    Returns: a CampaignBudgetOperation instance.
    """
    campaign_budget_service = client.get_service("CampaignBudgetService")
    campaign_budget_operation: CampaignBudgetOperation = client.get_type(
        "CampaignBudgetOperation"
    )
    campaign_budget = campaign_budget_operation.create
    resource_name: str = campaign_budget_service.campaign_budget_path(
        customer_id, get_next_temporary_id()
    )
    campaign_budget.resource_name = resource_name
    campaign_budget.name = f"Interplanetary Cruise Budget #{uuid4()}"
    campaign_budget.delivery_method = (
        client.enums.BudgetDeliveryMethodEnum.STANDARD
    )
    campaign_budget.amount_micros = 5000000

    return campaign_budget_operation


def build_campaign_operations(
    client: GoogleAdsClient,
    customer_id: str,
    campaign_budget_resource_name: str,
) -> List[CampaignOperation]:
    """Builds new campaign operations for the specified customer ID.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a str of a customer ID.
        campaign_budget_resource_name: a str resource name for a campaign
            budget.

    Returns: a list of CampaignOperation instances.
    """
    return [
        build_campaign_operation(
            client, customer_id, campaign_budget_resource_name
        )
        for _ in range(NUMBER_OF_CAMPAIGNS_TO_ADD)
    ]


def build_campaign_operation(
    client: GoogleAdsClient,
    customer_id: str,
    campaign_budget_resource_name: str,
) -> CampaignOperation:
    """Builds new campaign operation for the specified customer ID.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a str of a customer ID.
        campaign_budget_resource_name: a str resource name for a campaign
            budget.

    Returns: a CampaignOperation instance.
    """
    campaign_operation: CampaignOperation = client.get_type("CampaignOperation")
    campaign_service = client.get_service("CampaignService")
    # Creates a campaign.
    campaign = campaign_operation.create
    campaign_id: int = get_next_temporary_id()
    # Creates a resource name using the temporary ID.
    campaign.resource_name = campaign_service.campaign_path(
        customer_id, campaign_id
    )
    campaign.name = f"Batch job campaign #{customer_id}.{campaign_id}"
    campaign.advertising_channel_type = (
        client.enums.AdvertisingChannelTypeEnum.SEARCH
    )
    # Recommendation: Set the campaign to PAUSED when creating it to prevent
    # the ads from immediately serving. Set to ENABLED once you've added
    # targeting and the ads are ready to serve.
    campaign.status = client.enums.CampaignStatusEnum.PAUSED
    # Set the bidding strategy and type by setting manual_cpc equal to an empty
    # ManualCpc instance.
    client.copy_from(campaign.manual_cpc, client.get_type("ManualCpc"))
    campaign.campaign_budget = campaign_budget_resource_name

    return campaign_operation


def build_campaign_criterion_operations(
    client: GoogleAdsClient, campaign_operations: List[CampaignOperation]
) -> List[CampaignCriterionOperation]:
    """Builds new campaign criterion operations for negative keyword criteria.

    Args:
        client: an initialized GoogleAdsClient instance.
        campaign_operations: a list of CampaignOperation instances.

    Returns: a list of CampaignCriterionOperation instances.
    """
    return [
        build_campaign_criterion_operation(client, campaign_operation)
        for campaign_operation in campaign_operations
    ]


def build_campaign_criterion_operation(
    client: GoogleAdsClient, campaign_operation: CampaignOperation
) -> CampaignCriterionOperation:
    """Builds a new campaign criterion operation for negative keyword criterion.

    Args:
        client: an initialized GoogleAdsClient instance.
        campaign_operation: a CampaignOperation instance.

    Returns: a CampaignCriterionOperation instance.
    """
    campaign_criterion_operation: CampaignCriterionOperation = client.get_type(
        "CampaignCriterionOperation"
    )
    # Creates a campaign criterion.
    campaign_criterion = campaign_criterion_operation.create
    campaign_criterion.keyword.text = "venus"
    campaign_criterion.keyword.match_type = (
        client.enums.KeywordMatchTypeEnum.BROAD
    )
    # Sets the campaign criterion as a negative criterion.
    campaign_criterion.negative = True
    campaign_criterion.campaign = campaign_operation.create.resource_name

    return campaign_criterion_operation


def build_ad_group_operations(
    client: GoogleAdsClient,
    customer_id: str,
    campaign_operations: List[CampaignOperation],
) -> List[AdGroupOperation]:
    """Builds new ad group operations for the specified customer ID.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a str of a customer ID.
        campaign_operations: a list of CampaignOperation instances.

    Return: a list of AdGroupOperation instances.
    """
    operations: List[AdGroupOperation] = []

    for campaign_operation in campaign_operations:
        for _ in range(NUMBER_OF_AD_GROUPS_TO_ADD):
            operations.append(
                build_ad_group_operation(
                    client, customer_id, campaign_operation
                )
            )

    return operations


def build_ad_group_operation(
    client: GoogleAdsClient,
    customer_id: str,
    campaign_operation: CampaignOperation,
) -> AdGroupOperation:
    """Builds a new ad group operation for the specified customer ID.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a str of a customer ID.
        campaign_operation: a CampaignOperation instance.

    Return: an AdGroupOperation instance.
    """
    ad_group_operation: AdGroupOperation = client.get_type("AdGroupOperation")
    ad_group_service = client.get_service("AdGroupService")
    # Creates an ad group.
    ad_group = ad_group_operation.create
    ad_group_id: int = get_next_temporary_id()
    # Creates a resource name using the temporary ID.
    ad_group.resource_name = ad_group_service.ad_group_path(
        customer_id, ad_group_id
    )
    ad_group.name = f"Batch job ad group #{uuid4()}.{ad_group_id}"
    ad_group.campaign = campaign_operation.create.resource_name
    ad_group.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
    ad_group.cpc_bid_micros = 10000000

    return ad_group_operation


def build_ad_group_criterion_operations(
    client: GoogleAdsClient, ad_group_operations: List[AdGroupOperation]
) -> List[AdGroupCriterionOperation]:
    """Builds new ad group criterion operations for creating keywords.

    50% of keywords are created with some invalid characters to demonstrate
    how BatchJobService returns information about such errors.

    Args:
        client: an initialized GoogleAdsClient instance.
        ad_group_operations: a list of AdGroupOperation instances.

    Returns a list of AdGroupCriterionOperation instances.
    """
    operations: List[AdGroupCriterionOperation] = []

    for i, ad_group_operation in enumerate(ad_group_operations):
        for j in range(NUMBER_OF_KEYWORDS_TO_ADD):
            operations.append(
                build_ad_group_criterion_operation(
                    # Create a keyword text by making 50% of keywords invalid
                    # to demonstrate error handling.
                    client,
                    ad_group_operation,
                    j,  # Pass j as the number for keyword text
                    (i * NUMBER_OF_KEYWORDS_TO_ADD + j) % 2 == 0,
                )
            )

    return operations


def build_ad_group_criterion_operation(
    client: GoogleAdsClient,
    ad_group_operation: AdGroupOperation,
    number: int,
    is_valid: bool = True,
) -> AdGroupCriterionOperation:
    """Builds new ad group criterion operation for creating keywords.

    Takes an optional param that dictates whether the keyword text should
    intentionally generate an error with invalid characters.

    Args:
        client: an initialized GoogleAdsClient instance.
        ad_group_operation: an AdGroupOperation instance.
        number: an int of the number to assign to the name of the criterion.
        is_valid: a bool of whether the keyword text should be invalid.

    Returns: an AdGroupCriterionOperation instance.
    """
    ad_group_criterion_operation: AdGroupCriterionOperation = client.get_type(
        "AdGroupCriterionOperation"
    )
    # Creates an ad group criterion.
    ad_group_criterion = ad_group_criterion_operation.create
    ad_group_criterion.keyword.text = f"mars{number}"

    # If keyword should be invalid we add exclamation points, which will
    # generate errors when sent to the API.
    if not is_valid:
        ad_group_criterion.keyword.text += "!!!"

    ad_group_criterion.keyword.match_type = (
        client.enums.KeywordMatchTypeEnum.BROAD
    )
    ad_group_criterion.ad_group = ad_group_operation.create.resource_name
    # Keyword criteria do not have a status field.
    # ad_group_criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED

    return ad_group_criterion_operation


def build_ad_group_ad_operations(
    client: GoogleAdsClient, ad_group_operations: List[AdGroupOperation]
) -> List[AdGroupAdOperation]:
    """Builds new ad group ad operations.

    Args:
        client: an initialized GoogleAdsClient instance.
        ad_group_operations: a list of AdGroupOperation instances.

    Returns: a list of AdGroupAdOperation instances.
    """
    return [
        build_ad_group_ad_operation(client, ad_group_operation)
        for ad_group_operation in ad_group_operations
    ]


def build_ad_group_ad_operation(
    client: GoogleAdsClient, ad_group_operation: AdGroupOperation
) -> AdGroupAdOperation:
    """Builds a new ad group ad operation.

    Args:
        client: an initialized GoogleAdsClient instance.
        ad_group_operation: an AdGroupOperation instance.

    Returns: an AdGroupAdOperation instance.
    """
    ad_group_ad_operation: AdGroupAdOperation = client.get_type(
        "AdGroupAdOperation"
    )
    # Creates an ad group ad.
    ad_group_ad = ad_group_ad_operation.create
    # Creates the expanded text ad info.
    text_ad = ad_group_ad.ad.expanded_text_ad
    text_ad.headline_part1 = f"Cruise to Mars #{uuid4()}"
    text_ad.headline_part2 = "Best Space Cruise Line"
    text_ad.description = "Buy your tickets now!"

    ad_group_ad.ad.final_urls.append("http://www.example.com")
    ad_group_ad.ad_group = ad_group_operation.create.resource_name
    ad_group_ad.status = client.enums.AdGroupAdStatusEnum.PAUSED

    return ad_group_ad_operation


# [START add_complete_campaigns_using_batch_job_2]
def run_batch_job(
    batch_job_service: BatchJobServiceClient, resource_name: str
) -> Operation:
    """Runs the batch job for executing all uploaded mutate operations.

    Args:
        batch_job_service: an instance of the BatchJobService message class.
        resource_name: a str of a resource name for a batch job.

    Returns: a google.api_core.operation.Operation instance.
    """
    try:
        response: Operation = batch_job_service.run_batch_job(
            resource_name=resource_name
        )
        print(
            f'Batch job with resource name "{resource_name}" has been '
            "executed."
        )
        return response
    except GoogleAdsException as exception:
        handle_googleads_exception(exception)
        # This line will likely not be reached due to sys.exit(1) in handle_googleads_exception
        # but to satisfy the type checker, we add a return statement.
        # In a real application, you might want to return a dummy Operation or raise an error.
        return Operation(
            op_type_name="type.googleapis.com/google.protobuf.Empty",
            complete=True,
            done_callbacks=[],
            metadata_type=None,
            result_type=None,
        )  # type: ignore
        # [END add_complete_campaigns_using_batch_job_2]


# [START add_complete_campaigns_using_batch_job_3]
def poll_batch_job(
    operations_response: Operation, event: asyncio.Event
) -> None:
    """Polls the server until the batch job execution finishes.

    Sets the initial poll delay time and the total time to wait before time-out.

    Args:
        operations_response: a google.api_core.operation.Operation instance.
        event: an instance of asyncio.Event to invoke once the operations have
            completed, alerting the awaiting calling code that it can proceed.
    """
    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

    def done_callback(future: Coroutine[Any, Any, Any]) -> None:
        # The operations_response object will call callbacks from a daemon
        # thread so we must use a threadsafe method of setting the event here
        # otherwise it will not trigger the awaiting code.
        loop.call_soon_threadsafe(event.set)

    # operations_response represents a Long-Running Operation or LRO. The class
    # provides an interface for polling the API to check when the operation is
    # complete. Below we use the asynchronous interface, but there's also a
    # synchronous interface that uses the Operation.result method.
    # See: https://googleapis.dev/python/google-api-core/latest/operation.html
    operations_response.add_done_callback(done_callback)  # type: ignore
    # [END add_complete_campaigns_using_batch_job_3]


# [START add_complete_campaigns_using_batch_job_4]
def fetch_and_print_results(
    client: GoogleAdsClient,
    batch_job_service: BatchJobServiceClient,
    resource_name: str,
) -> None:
    """Prints all the results from running the batch job.

    Args:
        client: an initialized GoogleAdsClient instance.
        batch_job_service: an instance of the BatchJobService message class.
        resource_name: a str of a resource name for a batch job.
    """
    print(
        f'Batch job with resource name "{resource_name}" has finished. '
        "Now, printing its results..."
    )

    list_results_request: ListBatchJobResultsRequest = client.get_type(
        "ListBatchJobResultsRequest"
    )
    list_results_request.resource_name = resource_name
    list_results_request.page_size = 1000
    # Gets all the results from running batch job and prints their information.
    batch_job_results: ListBatchJobResultsResponse = (
        batch_job_service.list_batch_job_results(request=list_results_request)
    )

    for batch_job_result in batch_job_results:
        status: str = batch_job_result.status.message
        status = status if status else "N/A"
        result: Any = batch_job_result.mutate_operation_response
        result = result or "N/A"
        print(
            f"Batch job #{batch_job_result.operation_index} "
            f'has a status "{status}" and response type "{result}"'
        )
        # [END add_complete_campaigns_using_batch_job_4]


def handle_googleads_exception(exception: GoogleAdsException) -> None:
    """Prints the details of a GoogleAdsException object.

    Args:
        exception: an instance of GoogleAdsException.
    """
    print(
        f'Request with ID "{exception.request_id}" failed with status '
        f'"{exception.error.code().name}" and includes the following errors:'
    )
    for error in exception.failure.errors:
        print(f'\tError with message "{error.message}".')
        if error.location:
            for field_path_element in error.location.field_path_elements:
                print(f"\t\tOn field: {field_path_element.field_name}")
    sys.exit(1)


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description=(
            "Adds complete campaigns, including campaign budgets, "
            "campaigns, ad groups and keywords for the given "
            "customer ID using BatchJobService."
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

    args: argparse.Namespace = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v20"
    )

    asyncio.run(main(googleads_client, args.customer_id))
