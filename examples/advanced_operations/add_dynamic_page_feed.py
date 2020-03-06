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
"""This example adds a page feed with URLs for a Dynamic Search Ads Campaign.

The page feed specifies precisely which URLs to use with the campaign. To use
a Dynamic Search Ads Campaign run add_dynamic_search_ads_campaign.py. To get
campaigns run basic_operations/get_campaigns.py.
"""


import argparse
import sys
import uuid
from datetime import datetime, timedelta
from google.api_core import protobuf_helpers

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException


# Class to keep track of page feed details.
class FeedDetails(object):
    def __init__(self, resource_name, url_attribute_id, label_attribute_id):
        self.resource_name = resource_name
        self.url_attribute_id = url_attribute_id
        self.label_attribute_id = label_attribute_id


def main(client, customer_id, campaign_id, ad_group_id):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
        campaign_id: a campaign ID str.
        ad_group_id: an ad group ID str.
    """
    dsa_page_url_label = 'discounts'

    try:
        # Get the page feed resource name. This code example creates a new feed,
        # but you can fetch and re-use an existing feed.
        feed_resource_name = create_feed(client, customer_id)

        # We need to look up the attribute name and ID for the feed we just
        # created so that we can give them back to the API for construction of
        # feed mappings in the next function.
        feed_details = get_feed_details(client, customer_id, feed_resource_name)
        create_feed_mapping(client, customer_id, feed_details)
        create_feed_items(client, customer_id, feed_details, dsa_page_url_label)

        # Associate the page feed with the campaign.
        update_campaign_dsa_setting(client, customer_id, campaign_id,
                                    feed_details)
        ad_group_service = client.get_service('AdGroupService', version='v3')
        ad_group_resource_name = ad_group_service.ad_group_path(customer_id,
                                                                ad_group_id)

        # Optional: Target web pages matching the feed's label in the ad group.
        add_dsa_targeting(client, customer_id, ad_group_resource_name,
                          dsa_page_url_label)
    except GoogleAdsException as ex:
        print('Request with ID "{}" failed with status "{}" and includes the '
              'following errors:'.format(ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "{}".'.format(error.message))
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: {}'.format(
                        field_path_element.field_name))
        sys.exit(1)


def create_feed(client, customer_id):
    """Creates a page feed with URLs

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.

    Returns:
        A FeedDetails instance with information about the newly created feed.
    """
    # Retrieve a new feed operation object.
    feed_operation = client.get_type('FeedOperation', version='v3')
    # Create a new feed.
    feed = feed_operation.create
    feed.name.value = 'DSA Feed #{}'.format(uuid.uuid4())
    feed.origin = client.get_type('FeedOriginEnum', version='v3').USER

    feed_attribute_type_enum = client.get_type('FeedAttributeTypeEnum',
                                               version='v3')

    # Create the feed's attributes.
    feed_attribute_url = feed.attributes.add()
    feed_attribute_url.type = feed_attribute_type_enum.URL_LIST
    feed_attribute_url.name.value = 'Page URL'

    feed_attribute_label = feed.attributes.add()
    feed_attribute_label.type = feed_attribute_type_enum.STRING_LIST
    feed_attribute_label.name.value = 'Label'

    # Retrieve the feed service.
    feed_service = client.get_service('FeedService', version='v3')
    # Send the feed operation and add the feed.
    response = feed_service.mutate_feeds(customer_id, [feed_operation])

    return response.results[0].resource_name


def get_feed_details(client, customer_id, resource_name):
    """Makes a search request to retrieve the attributes of a single feed.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
        resource_name: the str resource_name of a feed.

    Returns:
        A FeedDetails instance with information about the feed that was
        retrieved in the search request.
    """
    query = '''
        SELECT
            feed.attributes
        FROM
            feed
        WHERE
            feed.resource_name = "{}"
        LIMIT 1
    '''.format(resource_name)

    ga_service = client.get_service('GoogleAdsService', version='v3')
    response = ga_service.search(customer_id, query=query)

    # Maps specific fields in each row in the response to a dict. This would
    # overwrite the same fields in the dict for each row, but we know we'll
    # only one row will be returned.
    for row in response:
        attribute_lookup = {
            attribute.name.value:
                attribute.id.value for attribute in row.feed.attributes}

    return FeedDetails(resource_name, attribute_lookup['Page URL'],
                       attribute_lookup['Label'])


def create_feed_mapping(client, customer_id, feed_details):
    """Creates feed mapping using the given feed details

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
        feed_details: a FeedDetails instance with feed attribute information
    """
    # Retrieve a new feed mapping operation object.
    feed_mapping_operation = client.get_type('FeedMappingOperation',
                                             version='v3')
    # Create a new feed mapping.
    feed_mapping = feed_mapping_operation.create
    feed_mapping.criterion_type = client.get_type(
        'FeedMappingCriterionTypeEnum', version='v3').DSA_PAGE_FEED
    feed_mapping.feed.value = feed_details.resource_name
    dsa_page_feed_field_enum = client.get_type('DsaPageFeedCriterionFieldEnum',
                                               version='v3')

    url_field_mapping = feed_mapping.attribute_field_mappings.add()
    url_field_mapping.feed_attribute_id.value = feed_details.url_attribute_id
    url_field_mapping.dsa_page_feed_field = dsa_page_feed_field_enum.PAGE_URL

    label_field_mapping = feed_mapping.attribute_field_mappings.add()
    label_field_mapping.feed_attribute_id.value = (
        feed_details.label_attribute_id)
    label_field_mapping.dsa_page_feed_field = dsa_page_feed_field_enum.LABEL

    # Retrieve the feed mapping service.
    feed_mapping_service = client.get_service('FeedMappingService',
                                              version='v3')
    # Submit the feed mapping operation and add the feed mapping.
    response = feed_mapping_service.mutate_feed_mappings(
        customer_id, [feed_mapping_operation])
    resource_name = response.results[0].resource_name

    # Display the results.
    print('Feed mapping created with resource_name: # {}'.format(resource_name))


def create_feed_items(client, customer_id, feed_details, label):
    """Creates feed items with the given feed_details and label

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
        feed_details: a FeedDetails instance with feed attribute information
        label: a Dynamic Search Ad URL label str.
    """
    # See https://support.google.com/adwords/answer/7166527 for page feed URL
    # recommendations and rules.
    urls = ["http://www.example.com/discounts/rental-cars",
        "http://www.example.com/discounts/hotel-deals",
        "http://www.example.com/discounts/flight-deals"]

    def map_feed_urls(url):
        feed_item_operation = client.get_type('FeedItemOperation', version='v3')
        feed_item = feed_item_operation.create
        feed_item.feed.value = feed_details.resource_name

        url_attribute_value = feed_item.attribute_values.add()
        url_attribute_value.feed_attribute_id.value = (
            feed_details.url_attribute_id)
        url_string_val = url_attribute_value.string_values.add()
        url_string_val.value = url

        label_attribute_value = feed_item.attribute_values.add()
        label_attribute_value.feed_attribute_id.value = (
            feed_details.label_attribute_id)
        label_string_val = label_attribute_value.string_values.add()
        label_string_val.value = label

        return feed_item_operation

    # Create a new feed item operation for each of the URLs in the url list.
    feed_item_operations = list(map(map_feed_urls, urls))

    # Retrieve the feed item service.
    feed_item_service = client.get_service('FeedItemService', version='v3')
    # Submit the feed item operations and add the feed items.
    response = feed_item_service.mutate_feed_items(customer_id,
                                                   feed_item_operations)

    # Display the results.
    for feed_item in response.results:
        print('Created feed item with resource_name: # {}'.format(
            feed_item.resource_name))


def update_campaign_dsa_setting(client, customer_id, campaign_id, feed_details):
    """Updates the given campaign with the given feed details

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
        campaign_id: a campaign ID str;
        feed_details: a FeedDetails instance with feed attribute information.
    """
    query = '''
        SELECT
            campaign.id,
            campaign.name,
            campaign.dynamic_search_ads_setting.domain_name
        FROM
            campaign
        WHERE
            campaign.id = {}
        LIMIT 1
    '''.format(campaign_id)

    ga_service = client.get_service('GoogleAdsService', version='v3')
    results = ga_service.search(customer_id, query=query)

    for row in results:
        campaign = row.campaign

    if not campaign:
        raise ValueError('Campaign with id #{} not found'.format(campaign_id))

    if not campaign.dynamic_search_ads_setting.domain_name:
        raise ValueError(
            'Campaign id #{} is not set up for Dynamic Search Ads.'.format(
                campaign_id))

    # Retrieve a new campaign operation
    campaign_operation = client.get_type('CampaignOperation', version='v3')
    # Copy the retrieved campaign onto the new campaign operation.
    campaign_operation.update.CopyFrom(campaign)
    updated_campaign = campaign_operation.update
    feed = updated_campaign.dynamic_search_ads_setting.feeds.add()
    # Use a page feed to specify precisely which URLs to use with your Dynamic
    # Search ads.
    feed.value = feed_details.resource_name
    field_mask = protobuf_helpers.field_mask(campaign, updated_campaign)
    campaign_operation.update_mask.CopyFrom(field_mask)

    # Retrieve the campaign service.
    campaign_service = client.get_service('CampaignService', version='v3')
    # Submit the campaign operation and update the campaign.
    response = campaign_service.mutate_campaigns(customer_id,
                                                 [campaign_operation])
    resource_name = response.results[0].resource_name

    # Display the results.
    print('Updated campaign #{}'.format(resource_name))


def add_dsa_targeting(client, customer_id, ad_group_resource_name, label):
    """Adds Dynamic Search Ad targeting criteria to the given ad group

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
        ad_group_resource_name: a resource_name str for an Ad Group.
        label: a Dynamic Search Ad URL label str.
    """
    # Retrieve a new ad group criterion operation object.
    ad_group_criterion_operation = client.get_type(
        'AdGroupCriterionOperation', version='v3')
    # Create a new ad group criterion.
    ad_group_criterion = ad_group_criterion_operation.create
    ad_group_criterion.ad_group.value = ad_group_resource_name
    # Set the custom bid for this criterion.
    ad_group_criterion.cpc_bid_micros.value = 1500000
    ad_group_criterion.webpage.criterion_name.value = 'Test criterion'
    # Add a condition for label=specified_label_name
    webpage_criterion_info = ad_group_criterion.webpage.conditions.add()
    webpage_criterion_info.argument.value = label
    webpage_criterion_info.operand = client.get_type(
        'WebpageConditionOperandEnum', version='v3').CUSTOM_LABEL

    # Retrieve the ad group criterion service.
    ad_group_criterion_service = client.get_service('AdGroupCriterionService',
                                                    version='v3')
    response = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id, [ad_group_criterion_operation])
    resource_name = response.results[0].resource_name

    # Display the results.
    print('Created ad group criterion with resource_name: # {}'.format(
        resource_name))


if __name__ == '__main__':
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()

    parser = argparse.ArgumentParser(
        description= ('Adds a page feed with URLs for a Dynamic Search Ads '
                      'Campaign.'))
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=str,
                        required=True, help='The Google Ads customer ID.')
    parser.add_argument('-i', '--campaign_id', type=str,
                        required=True, help='The campaign ID.')
    parser.add_argument('-a', '--ad_group_id', type=str,
                        required=True, help='The ad group ID.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, args.campaign_id,
         args.ad_group_id)
