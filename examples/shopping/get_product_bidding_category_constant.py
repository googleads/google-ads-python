from __future__ import absolute_import
 
import argparse
import six
import sys
import uuid
import collections
import google.ads.google_ads.client
from google.ads.google_ads.errors import GoogleAdsException
from google.ads.google_ads.client import GoogleAdsClient

_DEFAULT_PAGE_SIZE = 1000
 
 
def display_categories(categories,prefix=''):
  for c in categories:
    print("{}{} [{}]".format(prefix,c.name,c.id))
    if not c.children:
      display_categories(c.children, prefix=prefix + c.name)
 
 
def get_product_bidding_category_constant(client,customer_id,page_size):
  ga_service = client.get_service('GoogleAdsService', version='v1')
  query = ('SELECT product_bidding_category_constant.localized_name,'
  'product_bidding_category_constant.product_bidding_category_constant_parent '
  'FROM product_bidding_category_constant WHERE product_bidding_category_constant.country_code IN ("US")')
  
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
      
      parent_id = getattr(product_bidding_category.product_bidding_category_constant_parent, 'value', None)
      
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
  google_ads_client = (GoogleAdsClient
                        .load_from_storage())
 
  parser = argparse.ArgumentParser(
      description='Get Product Bidding Category Constant')
  # The following argument(s) should be provided to run the example.
  parser.add_argument('-c', '--customer_id', type=six.text_type,
                      required=True, help='The Google Ads customer ID.')
  args = parser.parse_args()
 
  get_product_bidding_category_constant(google_ads_client, args.customer_id, _DEFAULT_PAGE_SIZE)
