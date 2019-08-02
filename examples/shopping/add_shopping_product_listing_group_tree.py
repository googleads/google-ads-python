from __future__ import absolute_import
import argparse
import collections
import sys
import six
from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException
from google.ads.google_ads.util import ResourceName
import google.ads.google_ads.client


PAGE_SIZE=1000 
last_criterion_id = 0
    
def next_id():
    global last_criterion_id
    last_criterion_id -= 1
    return str(last_criterion_id)


def main(client,customer_id, ad_group_id, should_replace_existing_tree): 

    if should_replace_existing_tree:
        remove_listing_group_tree(client, customer_id, ad_group_id)

    operations= []
    ad_group_service = client.get_service('AdGroupCriterionService')
    operation = client.get_type("AdGroupCriterionOperation")
    criterion=operation.create
    resource_name = ad_group_service.ad_group_criteria_path(customer_id, ResourceName.format_composite(ad_group_id, next_id()))
    criterion.resource_name = resource_name
    criterion.status=client.get_type("AdGroupCriterionStatusEnum").ENABLED
    criterion.listing_group.type = client.get_type("ListingGroupTypeEnum").SUBDIVISION

    operations.append(operation)

    ad_group_criterion_root_resource_name = criterion.resource_name


    operation = create_listing_group_unit_biddable(client, customer_id, ad_group_id, ad_group_criterion_root_resource_name, \
                                                'NEW',200_000)
    operations.append(operation)


    operation = create_listing_group_unit_biddable(client, customer_id, ad_group_id, ad_group_criterion_root_resource_name, \
                                                'USED',100_000)
    operations.append(operation)

    operation, resource_name = create_listing_group_subdivision(client, customer_id, ad_group_id, ad_group_criterion_root_resource_name )
    operations.append(operation)

   
    operation = create_listing_group_unit_biddable(client, customer_id, ad_group_id, resource_name, \
                                                cpc_bid_micros = 900_000, brand= "CoolBrand")
    operations.append(operation)



    operation = create_listing_group_unit_biddable(client, customer_id, ad_group_id, resource_name, \
                                                cpc_bid_micros = 10_000, brand= "CheapBrand")
    operations.append(operation)


    operation = create_listing_group_unit_biddable(client, customer_id, ad_group_id, resource_name, \
                                                cpc_bid_micros = 50_000)
    operations.append(operation)

    total_count=0


    agc_service = client.get_service("AdGroupCriterionService")
    print(operations)
    response = agc_service.mutate_ad_group_criteria(customer_id, operations)

    total_count=0
    for row in operations.results:
        print("Added ad group criterion with name: {}".format(row.resource_name))
        total_count+=1
    print("{} criteria added in total.".format(total_count))
    
    




def create_listing_group_unit_biddable(client, customer_id, ad_group_id, ad_group_criterion_root_resource_name, \
                                        listing_dimension_info= None, cpc_bid_micros= None,brand= None):
    ad_group_service = client.get_service('AdGroupService')
    operation = client.get_type("AdGroupCriterionOperation")

    criterion = operation.create
    resource_name = ad_group_service.ad_group_path(customer_id, ad_group_id)
    criterion.ad_group.value = resource_name
    criterion.status = client.get_type('AdGroupCriterionStatusEnum').ENABLED
    criterion.cpc_bid_micros.value = cpc_bid_micros


    listing_group = criterion.listing_group
    listing_group.type = client.get_type('ListingGroupTypeEnum').UNIT
    listing_group.parent_ad_group_criterion.value = ad_group_criterion_root_resource_name
    if listing_dimension_info=='NEW':
        listing_group.case_value.product_condition.condition = client.get_type("ProductConditionEnum").NEW
    elif listing_dimension_info=='USED':
        listing_group.case_value.product_condition.condition = client.get_type("ProductConditionEnum").USED

    if brand:
        criterion.listing_group.case_value.listing_brand.value.value = brand
    else:
        pass      
    return operation


def create_listing_group_subdivision(client, customer_id, ad_group_id, parent_ad_group_criterion_name=None):

    ad_group_service = client.get_service('AdGroupCriterionService')
    operation = client.get_type('AdGroupCriterionOperation')
    criterion = operation.create
    resource_name = ad_group_service.ad_group_criteria_path(customer_id, ResourceName.format_composite(ad_group_id, next_id()))
    criterion.resource_name = resource_name
    criterion.status=client.get_type("AdGroupCriterionStatusEnum").ENABLED

    listing_group = criterion.listing_group
    listing_group.type = client.get_type("ListingGroupTypeEnum").SUBDIVISION
    listing_group.parent_ad_group_criterion.value = parent_ad_group_criterion_name
    listing_group.case_value.product_condition.condition = client.get_type("ProductConditionEnum").UNSPECIFIED


    return operation, resource_name



def remove_listing_group_tree(client, customer_id, ad_group_id):
    ga_service = client.get_service('GoogleAdsService', version='v1')
    query = ('SELECT ad_group_criterion.resource_name FROM  '
           'ad_group_criterion  WHERE ad_group_criterion.type = LISTING_GROUP '
           'AND ad_group_criterion.listing_group.parent_ad_group_criterion IS NULL ')
    query = '%s AND ad_group.id = %s' % (query, ad_group_id)
    results = ga_service.search(customer_id, query=query, page_size=PAGE_SIZE)
    res=[]
    for row in results: 
        criterion = row.ad_group_criterion
        print("Found an ad group criterion with resource name: {}".format(criterion.resouce_name))
        operation = client.get_type('AdGroupCriterionOperation', version='v1')
        operation.remove = criterion.resource_name
        res.append(ad_group_criterion_root)

    if res:
        agc_service= client.get_service('AdGroupCriterionService', version='v1')
        response = agc_service.mutate_ad_group_criteria(customer_id, operations)
        print("Removed {} as group criteria".format(response.results.count))
    return res


if __name__ == '__main__':
    google_ads_client = GoogleAdsClient.load_from_storage()

    parser = argparse.ArgumentParser(
      description='Get Product Bidding Category Constant')
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=six.text_type,
                      required=True, help='The Google Ads customer ID.')
    parser.add_argument('-a', '--adgroup_id', type=six.text_type,
                      required=True, help='The Google Ad Group Id')

    args = parser.parse_args()

    main(google_ads_client, args.customer_id,args.adgroup_id, False)


