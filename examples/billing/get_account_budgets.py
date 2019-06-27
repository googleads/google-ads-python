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
"""This illustrates how to get all account budgets for a Google Ads customer."""

from __future__ import absolute_import

import argparse
import sys

import six

import google.ads.google_ads.client


_DEFAULT_PAGE_SIZE = 1000


def main(client, customer_id, page_size):
    ga_service = client.get_service('GoogleAdsService', version='v2')

    query = ('SELECT account_budget.status, '
             'account_budget.billing_setup, '
             'account_budget.approved_spending_limit_micros, '
             'account_budget.approved_spending_limit_type, '
             'account_budget.proposed_spending_limit_micros, '
             'account_budget.proposed_spending_limit_type, '
             'account_budget.approved_start_date_time, '
             'account_budget.proposed_start_date_time, '
             'account_budget.approved_end_date_time, '
             'account_budget.approved_end_time_type, '
             'account_budget.proposed_end_date_time, '
             'account_budget.proposed_end_time_type '
             'FROM account_budget')

    results = ga_service.search(customer_id, query=query, page_size=page_size)

    try:
        # Use the enum type to determine the enum names from the values.
        budget_status_enum = client.get_type(
            'AccountBudgetStatusEnum').AccountBudgetStatus

        for row in results:
            budget = row.account_budget
            approved_spending_limit = (
                micros_to_currency(budget.approved_spending_limit_micros.value)
                if budget.approved_spending_limit_micros
                else budget.approved_spending_limit_type.name)
            proposed_spending_limit = (
                micros_to_currency(budget.proposed_spending_limit_micros.value)
                if budget.proposed_spending_limit_micros
                else budget.proposed_spending_limit_type.name)
            approved_end_date_time = (
                budget.approved_end_date_time.value
                if budget.approved_end_date_time
                else budget.approved_end_date_time_type)
            proposed_end_date_time = (
                budget.proposed_end_date_time.value
                if budget.proposed_end_date_time
                else budget.proposed_end_date_time_type)

            print('Account budget "%s", with status "%s", billing setup "%s", '
                  'amount served %.2f, total adjustments %.2f, '
                  'approved spending limit "%s" (proposed "%s"), '
                  'approved start time "%s" (proposed "%s"), '
                  'approved end time "%s" (proposed "%s").'
                  % (budget.resource_name,
                     budget_status_enum.Name(budget.status),
                     budget.billing_setup.value,
                     micros_to_currency(budget.amount_served_micros.value),
                     micros_to_currency(budget.total_adjustments_micros.value),
                     approved_spending_limit,
                     proposed_spending_limit,
                     budget.approved_start_date_time,
                     budget.proposed_start_date_time,
                     approved_end_date_time,
                     proposed_end_date_time))
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)


def micros_to_currency(micros):
    return micros / 1000000.0


if __name__ == '__main__':
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = (google.ads.google_ads.client.GoogleAdsClient
                         .load_from_storage())

    parser = argparse.ArgumentParser(
        description=('Lists all account budgets for given Google Ads customer '
                     'ID.'))
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=six.text_type,
                        required=True, help='The Google Ads customer ID.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, _DEFAULT_PAGE_SIZE)
