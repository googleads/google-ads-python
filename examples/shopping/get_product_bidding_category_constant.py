#!/usr/bin/env python
# Copyright 2019 Google LLC
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
"""This example fetches the set of valid ProductBiddingCategories."""


import argparse
import collections
import sys
from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException

_DEFAULT_PAGE_SIZE = 1000


def display_categories(categories, prefix=''):
  for category in categories:
    print('{}{} [{}]'.format(prefix, category.name, category.id))
    if not category.children:
      display_categories(category.children, prefix=prefix + category.name)


def main(client, customer_id, page_size):
  ga_service = client.get_service('GoogleAdsService', version='v3')
  query = ('SELECT product_bidding_category_constant.localized_name, '
           'product_bidding_category_constant.product_bidding_category_constant_parent '
           'FROM product_bidding_category_constant WHERE '
           'product_bidding_category_constant.country_code IN ("US")')

  results = ga_service.search(customer_id, query=query, page_size=page_size)

  class Category:
    def __init__(self, name=None, id=None, children=[]):
      self.name = name
      self.id = id
      self.children = children

  all_categories = collections.defaultdict(lambda: Category())

  root_categories = []

  try:
    for row in results:
      product_bidding_category = row.product_bidding_category_constant

      category = Category(product_bidding_category.localized_name.value,
                          product_bidding_category.resource_name)

      all_categories[category.id] = category
      parent = product_bidding_category.product_bidding_category_constant_parent
      parent_id = getattr(parent, 'value', None)

      if parent_id:
        all_categories[parent_id].children.append(category)
      else:
        root_categories.append(category)

    display_categories(root_categories)
  except GoogleAdsException as ex:
      print('Request with ID "%s" failed with status "%s" and includes the '
            'following errors:' % (ex.request_id, ex.error.code().name))
      for error in ex.failure.errors:
          print('\tError with message "%s".' % error.message)
          if error.location:
              for field_path_element in error.location.field_path_elements:
                  print('\t\tOn field: %s' % field_path_element.field_name)
      sys.exit(1)

if __name__ == '__main__':
  google_ads_client = GoogleAdsClient.load_from_storage()
 
  parser = argparse.ArgumentParser(
      description='Get Product Bidding Category Constant')
  # The following argument(s) should be provided to run the example.
  parser.add_argument('-c', '--customer_id', type=str,
                      required=True, help='The Google Ads customer ID.')
  args = parser.parse_args()
 
  main(google_ads_client, args.customer_id, _DEFAULT_PAGE_SIZE)
