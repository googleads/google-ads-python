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
"""This example creates an account budget proposal.

To get account budget proposal, run get_account_budget_proposals.py
"""

from __future__ import absolute_import

import argparse
import sys

import six

import google.ads.google_ads.client


def main(client, customer_id, billing_setup_id):
    account_budget_proposal_service = client.get_service(
        'AccountBudgetProposalService')
    billing_setup_service = client.get_service('BillingSetupService',
                                               version='v2')

    account_budget_proposal_operation = client.get_type(
        'AccountBudgetProposalOperation')
    proposal = account_budget_proposal_operation.create

    proposal.proposal_type = client.get_type(
        'AccountBudgetProposalTypeEnum').CREATE
    proposal.billing_setup.value = billing_setup_service.billing_setup_path(
        customer_id, billing_setup_id)
    proposal.proposed_name.value = 'Account Budget Proposal (example)'

    # Specify the account budget starts immediately
    proposal.proposed_start_time_type = client.get_type('TimeTypeEnum',
                                                        version='v2').NOW
    # Alternatively you can specify a specific start time. Refer to the
    # AccountBudgetProposal resource documentation for allowed formats.
    #
    # proposal.proposed_start_date_time = '2020-01-02 03:04:05'

    # Specify that the budget runs forever
    proposal.proposed_end_time_type = client.get_type('TimeTypeEnum',
                                                      version='v2').FOREVER
    # Alternatively you can specify a specific end time. Allowed formats are as
    # above.
    #
    # proposal.proposed_end_date_time = '2021-01-02 03:04:05'

    # Optional: set notes for the budget. These are free text and do not effect
    # budget delivery.
    #
    # proposal.proposed_notes = client.wrapper
    #     .string('Received prepayment of $0.01')
    proposal.proposed_spending_limit_micros.value = 10000

    try:
        account_budget_proposal_response = (
          account_budget_proposal_service.mutate_account_budget_proposal(
              customer_id, account_budget_proposal_operation))
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)

    print('Created account budget proposal "%s".'
          % account_budget_proposal_response.result.resource_name)


if __name__ == '__main__':
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = (google.ads.google_ads.client.GoogleAdsClient
                         .load_from_storage())

    parser = argparse.ArgumentParser(
        description='Creates an account budget proposal.')
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=six.text_type,
                        required=True, help='The Ads customer ID.')
    parser.add_argument('-b', '--billing_setup_id', type=six.text_type,
                        required=True, help='The billing setup ID.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, args.billing_setup_id)
