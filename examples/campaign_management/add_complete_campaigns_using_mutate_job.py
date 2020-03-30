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
"""Adds complete campaigns using MutateJobService.

Complete campaigns include campaign budgets, campaigns, ad groups and keywords.
"""


import argparse
import sys
from uuid import uuid4

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException

NUMBER_OF_CAMPAIGNS_TO_ADD = 2
NUMBER_OF_AD_GROUPS_TO_ADD = '2'
NUMBER_OF_KEYWORDS_TO_ADD = '5'
POLL_FREQUENCY_SECONDS = '1'
MAX_TOTAL_POLL_INTERVAL_SECONDS = '60'

PAGE_SIZE = 1000


def get_next_temporary_id():
    """Returns the next temporary ID to use in mutate job operations.

    If temporary ID has not been defined, i.e. if this function has not been
    called before, we set the initial value as -1 and return it. Subsequent
    calls will decrement the value by 1 before returning.

    Returns: an int of the next temporary ID.
    """
    global temporary_id

    try:
        temporary_id -= 1
        return temporary_id
    except NameError:
        temporary_id = -1
        return temporary_id


def handle_google_ads_exception(exception):
    """Prints the details of a GoogleAdsException object.

    Args:
        exception: an instance of GoogleAdsException.
    """
    print(f'Request with ID "{exception.request_id}" failed with status '
          f'"{exception.error.code().name}" and includes the following errors:')
    for error in exception.failure.errors:
        print(f'\tError with message "{error.message}".')
        if error.location:
            for field_path_element in error.location.field_path_elements:
                print(f'\t\tOn field: {field_path_element.field_name}')
    sys.exit(1)


def build_mutate_operation(client, operation_type, operation):
    """Builds a mutate operation with the given operation type and operation.

    Args:
        client: an initialized GoogleAdsClient instance.
        operation_type: a str of the operation type corresponding to a field on
            the MutateOperation message class.
        operation: an operation instance.

    Returns: a MutateOperation instance
    """
    mutate_operation = client.get_type('MutateOperation', version='v3')
    getattr(mutate_operation, operation_type).CopyFrom(operation)
    return mutate_operation


def main(client, customer_id):
    """Main function that runs the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a str of a customer ID.
    """
    mutate_job_service = client.get_service('MutateJobService', version='v3')
    resource_name = create_mutate_job(mutate_job_service, customer_id)
    operations = build_all_operations(client, customer_id)
    add_all_mutate_job_operations(mutate_job_service, operations, resource_name)


def create_mutate_job(mutate_job_service, customer_id):
    """Creates a mutate job for the specified customer ID.

    Args:
        mutate_job_service: an instance of the MutateJobService message class.
        customer_id: a str of a customer ID.

    Returns: a str of a resource name for a mutate job.
    """
    try:
        response = mutate_job_service.create_mutate_job(customer_id)
        resource_name = response.resource_name
        print(f'Created a mutate job with resource name "{resource_name}"')
        return resource_name
    except GoogleAdsException as exception:
        handle_google_ads_exception(exception)


def add_all_mutate_job_operations(mutate_job_service, operations,
                                  resource_name):
    """Adds all mutate job operations to the mutate job.

    As this is the first time for this mutate job, we pass null as a sequence
    token. The response will contain the next sequence token that we can use
    to upload more operations in the future.

    Args:
        mutate_job_service: an instance of the MutateJobService message class.
        operations: a list of a mutate operations.
        resource_name: a str of a resource name for a mutate job.
    """
    operations = build_all_operations(customer_id)
    response = mutate_job_service.add_mutate_job_operations(resource_name,
                                                            None, operations)


def build_all_operations(client, customer_id):
    """Builds all operations for creating a complete campaign.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a str of a customer ID.

    Returns: a list of operations of various types.
    """
    operations = []

    # Creates a new campaign budget operation and adds it to the list of
    # mutate operations.
    campaign_budget_op = build_campaign_budget_operation(client, customer_id)
    operations.append(build_mutate_operation(
        client, 'campaign_budget_operation', campaign_budget_op))

    # Creates new campaign operations and adds them to the list of
    # mutate operations.
    campaign_operations = build_campaign_operations(
        client, customer_id, campaign_budget_op.create.resource_name)
    operations = operations + [
        build_mutate_operation(client, 'campaign_operation', operation) \
        for operation in campaign_operations]

    # Creates new campaign criterion operations and adds them to the array of
    # mutate operations.
    campaign_criterion_operations = build_campaign_criterion_operations(
        client, campaign_operations)
    operations = operations + [
        build_mutate_operation(
            client, 'campaign_criterion_operation', operation) \
        for operation in campaign_criterion_operations]
    breakpoint()


def build_campaign_budget_operation(client, customer_id):
    """Builds a new campaign budget operation for the given customer ID.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a str of a customer ID.

    Returns: a CampaignBudgetOperation instance.
    """
    campaign_budget_service = client.get_service('CampaignBudgetService',
                                              version='v3')
    campaign_budget_operation = client.get_type('CampaignBudgetOperation',
                                                version='v3')
    campaign_budget = campaign_budget_operation.create
    resource_name = campaign_budget_service.campaign_budget_path(
        customer_id, get_next_temporary_id())
    campaign_budget.resource_name = resource_name
    campaign_budget.name.value = f'Interplanetary Cruise Budget #{uuid4()}'
    campaign_budget.delivery_method = client.get_type(
        'BudgetDeliveryMethodEnum', version='v3').STANDARD
    campaign_budget.amount_micros.value = 5000000

    return campaign_budget_operation


def build_campaign_operations(client, customer_id,
                              campaign_budget_resource_name):
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
            client, customer_id, campaign_budget_resource_name) \
        for i in range(NUMBER_OF_CAMPAIGNS_TO_ADD)]


def build_campaign_operation(client, customer_id,
                             campaign_budget_resource_name):
    """Builds new campaign operation for the specified customer ID.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a str of a customer ID.
        campaign_budget_resource_name: a str resource name for a campaign
            budget.

    Returns: a CampaignOperation instance.
    """
    campaign_operation = client.get_type('CampaignOperation', version='v3')
    campaign_service = client.get_service('CampaignService', version='v3')
    # Creates a campaign.
    campaign = campaign_operation.create
    campaign_id = get_next_temporary_id()
    # Creates a resource name using the temporary ID.
    campaign.resource_name = campaign_service.campaign_path(customer_id,
                                                            campaign_id)
    campaign.name.value = f'Mutate job campaign #{customer_id}.{campaign_id}'
    campaign.advertising_channel_type = client.get_type(
        'AdvertisingChannelTypeEnum', version='v3').SEARCH
    # Recommendation: Set the campaign to PAUSED when creating it to prevent
    # the ads from immediately serving. Set to ENABLED once you've added
    # targeting and the ads are ready to serve.
    campaign.status = client.get_type('CampaignStatusEnum', version='v3').PAUSED
    # Set the bidding strategy and type.
    campaign.manual_cpc.CopyFrom(client.get_type('ManualCpc', version='v3'))
    campaign.campaign_budget.value = campaign_budget_resource_name

    return campaign_operation


def build_campaign_criterion_operations(client, campaign_operations):
    """Builds new campaign criterion operations for negative keyword criteria.

    Args:
        client: an initialized GoogleAdsClient instance.
        campaign_operations: a list of CampaignOperation instances.

    Returns: a list of CampaignCriterionOperation instances.
    """
    return [
        build_campaign_criterion_operation(client, campaign_operation) \
        for campaign_operation in campaign_operations]


def build_campaign_criterion_operation(client, campaign_operation):
    """Builds a new campaign criterion operation for negative keyword criterion.

    Args:
        client: an initialized GoogleAdsClient instance.
        campaign_operation: a CampaignOperation instance.

    Returns: a CampaignCriterionOperation instance.
    """
    campaign_criterion_operation = client.get_type(
        'CampaignCriterionOperation', version='v3')
    # Creates a campaign criterion.
    campaign_criterion = campaign_criterion_operation.create
    campaign_criterion.keyword.text.value = 'venus'
    campaign_criterion.keyword.match_type = client.get_type(
        'KeywordMatchTypeEnum', version='v3').BROAD
    # Sets the campaign criterion as a negative criterion.
    campaign_criterion.negative.value = True
    campaign_criterion.campaign.value = campaign_operation.create.resource_name

    return campaign_criterion_operation


if __name__ == '__main__':
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()

    parser = argparse.ArgumentParser(
        description=('Adds a bid modifier to the specified campaign ID, for '
                     'the given customer ID.'))

    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=str, required=True,
                        help='The Google Ads customer ID.')

    args = parser.parse_args()

    main(google_ads_client, args.customer_id)
