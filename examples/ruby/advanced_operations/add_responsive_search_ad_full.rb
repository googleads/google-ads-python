#!/usr/bin/env ruby
# Copyright 2024 Google LLC
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

# This example shows how to create a complete Responsive Search ad.
#
# Includes creation of: budget, campaign, ad group, ad group ad,
# keywords, and geo targeting.
#
# More details on Responsive Search ads can be found here:
# https://support.google.com/google-ads/answer/7684791

require 'google/ads/google_ads'
require 'optimist'
require 'securerandom' # For UUIDs

# Keywords from user.
KEYWORD_TEXT_EXACT = "example of exact match"
KEYWORD_TEXT_PHRASE = "example of phrase match"
KEYWORD_TEXT_BROAD = "example of broad match"

# Geo targeting from user.
GEO_LOCATION_1 = "Buenos aires"
GEO_LOCATION_2 = "San Isidro"
GEO_LOCATION_3 = "Mar del Plata"

# LOCALE and COUNTRY_CODE are used for geo targeting.
# LOCALE is using ISO 639-1 format. If an invalid LOCALE is given,
# 'es' is used by default.
LOCALE = "es"

# A list of country codes can be referenced here:
# https://developers.google.com/google-ads/api/reference/data/geotargets
COUNTRY_CODE = "AR"

# Helper function to create an AdTextAsset.
#
# Args:
#   client: An initialized GoogleAdsClient instance.
#   text: Text for headlines and descriptions.
#   pinned_field: To pin a text asset so it always shows in the ad.
#
# Returns:
#   An AdTextAsset.
def create_ad_text_asset(client, text, pinned_field = nil)
  client.resource.ad_text_asset do |ad_text_asset|
    ad_text_asset.text = text
    unless pinned_field.nil?
      ad_text_asset.pinned_field = pinned_field
    end
  end
end

# Helper function to create an AdTextAsset with a customizer.
#
# Args:
#   client: An initialized GoogleAdsClient instance.
#   customizer_attribute_resource_name: The resource name of the customizer attribute.
#
# Returns:
#   An AdTextAsset.
def create_ad_text_asset_with_customizer(client, customizer_attribute_resource_name)
  client.resource.ad_text_asset do |ad_text_asset|
    # Create this particular description using the ad customizer. Visit
    # https://developers.google.com/google-ads/api/docs/ads/customize-responsive-search-ads#ad_customizers_in_responsive_search_ads
    # for details about the placeholder format. The ad customizer replaces the
    # placeholder with the value we previously created and linked to the
    # customer using CustomerCustomizer.
    ad_text_asset.text = "Just {CUSTOMIZER.#{customizer_attribute_resource_name}:10USD}"
  end
end

# Creates a customizer attribute with the given customizer attribute name.
#
# Args:
#   client: An initialized GoogleAdsClient instance.
#   customer_id: A client customer ID.
#   customizer_attribute_name: The name for the customizer attribute.
#
# Returns:
#   A resource name for a customizer attribute.
def create_customizer_attribute(client, customer_id, customizer_attribute_name)
  # Create a customizer attribute operation for creating a customizer attribute.
  operation = client.operation.create_customizer_attribute do |ca|
    ca.name = customizer_attribute_name
    # Specify the type to be 'PRICE' so that we can dynamically customize the
    # part of the ad's description that is a price of a product/service we
    # advertise.
    ca.type = :PRICE
  end

  # Issue a mutate request to add the customizer attribute and print its
  # information.
  customizer_attribute_service = client.service.customizer_attribute
  response = customizer_attribute_service.mutate_customizer_attributes(
    customer_id: customer_id,
    operations: [operation],
  )
  resource_name = response.results.first.resource_name

  puts "Added a customizer attribute with resource name: '#{resource_name}'"

  resource_name
end

# Links the customizer attribute to the customer.
#
# Args:
#   client: An initialized GoogleAdsClient instance.
#   customer_id: A client customer ID.
#   customizer_attribute_resource_name: A resource name for a customizer attribute.
def link_customizer_attribute_to_customer(client, customer_id, customizer_attribute_resource_name)
  # Create a customer customizer operation.
  operation = client.operation.create_customer_customizer do |cc|
    cc.customizer_attribute = customizer_attribute_resource_name
    cc.value = client.resource.customizer_value do |val|
      val.type = :PRICE
      # The ad customizer will dynamically replace the placeholder with this value
      # when the ad serves.
      val.string_value = "100USD"
    end
  end

  customer_customizer_service = client.service.customer_customizer
  # Issue a mutate request to create the customer customizer and prints its
  # information.
  response = customer_customizer_service.mutate_customer_customizers(
    customer_id: customer_id,
    operations: [operation],
  )
  resource_name = response.results.first.resource_name

  puts "Added a customer customizer to the customer with resource name: '#{resource_name}'"
end

# Creates a campaign budget resource.
#
# Args:
#   client: An initialized GoogleAdsClient instance.
#   customer_id: A client customer ID.
#
# Returns:
#   Campaign budget resource name.
def create_campaign_budget(client, customer_id)
  # Create a budget, which can be shared by multiple campaigns.
  campaign_budget_service = client.service.campaign_budget
  operation = client.operation.create_campaign_budget do |cb|
    cb.name = "Campaign budget \#{SecureRandom.uuid}"
    cb.delivery_method = :STANDARD
    cb.amount_micros = 500_000 # 500,000
    # cb.explicitly_shared = false # Not setting this, as per Python version for non-MCC
  end

  # Add budget.
  response = campaign_budget_service.mutate_campaign_budgets(
    customer_id: customer_id,
    operations: [operation],
  )
  resource_name = response.results.first.resource_name
  puts "Created campaign budget #{resource_name}"
  resource_name
end

# Creates a campaign resource.
#
# Args:
#   client: An initialized GoogleAdsClient instance.
#   customer_id: A client customer ID.
#   campaign_budget_resource_name: A budget resource name.
#
# Returns:
#   Campaign resource name.
def create_campaign(client, customer_id, campaign_budget_resource_name)
  campaign_service = client.service.campaign
  operation = client.operation.create_campaign do |campaign|
    campaign.name = "Testing RSA via API \#{SecureRandom.uuid}"
    campaign.advertising_channel_type = :SEARCH

    # Recommendation: Set the campaign to PAUSED when creating it to prevent
    # the ads from immediately serving. Set to ENABLED once you've added
    # targeting and the ads are ready to serve.
    campaign.status = :PAUSED

    # Set the bidding strategy and budget.
    # The bidding strategy for Maximize Clicks is TargetSpend.
    # The target_spend_micros is deprecated so don't put any value.
    # See other bidding strategies you can select in the link below.
    # https://developers.google.com/google-ads/api/reference/rpc/latest/Campaign#campaign_bidding_strategy
    # Based on Python: campaign.target_spend.target_spend_micros = 0
    # This means we are using TargetSpend bidding strategy.
    campaign.bidding_strategy_type = :TARGET_SPEND
    campaign.target_spend = client.resource.target_spend do |ts|
      # ts.target_spend_micros = 0 # Python sets this, but comment says it's deprecated.
                                 # Let's try omitting it first, relying on the TargetSpend type itself.
                                 # If campaign creation fails, this might need to be added.
                                 # Or, more accurately, Python's client.get_type("Campaign") creates the target_spend field
                                 # automatically. Ruby's block syntax might need explicit creation.
                                 # Let's try with explicit creation and setting micros to 0 as in Python.
      ts.target_spend_micros = 0
    end

    campaign.campaign_budget = campaign_budget_resource_name

    # Set the campaign network options.
    campaign.network_settings = client.resource.network_settings do |ns|
      ns.target_google_search = true
      ns.target_search_network = true
      ns.target_partner_search_network = false
      # Enable Display Expansion on Search campaigns. For more details see:
      # https://support.google.com/google-ads/answer/7193800
      ns.target_content_network = true
    end

    # Optional: Set the start and end dates (omitted as in Python example)
  end

  # Add the campaign.
  response = campaign_service.mutate_campaigns(
    customer_id: customer_id,
    operations: [operation],
  )
  resource_name = response.results.first.resource_name
  puts "Created campaign #{resource_name}."
  resource_name
end

# Creates an ad group.
#
# Args:
#   client: An initialized GoogleAdsClient instance.
#   customer_id: A client customer ID.
#   campaign_resource_name: A campaign resource name.
#
# Returns:
#   Ad group resource name.
def create_ad_group(client, customer_id, campaign_resource_name)
  ad_group_service = client.service.ad_group

  operation = client.operation.create_ad_group do |ag|
    ag.name = "Testing RSA via API \#{SecureRandom.uuid}"
    ag.status = :ENABLED
    ag.campaign = campaign_resource_name
    ag.type = :SEARCH_STANDARD
    # If you want to set up a max CPC bid uncomment line below.
    # ag.cpc_bid_micros = 1_000_000 # 1,000,000
  end

  # Add the ad group.
  response = ad_group_service.mutate_ad_groups(
    customer_id: customer_id,
    operations: [operation],
  )
  ad_group_resource_name = response.results.first.resource_name
  puts "Created ad group #{ad_group_resource_name}."
  ad_group_resource_name
end

# Creates an ad group ad (Responsive Search Ad).
#
# Args:
#   client: An initialized GoogleAdsClient instance.
#   customer_id: A client customer ID.
#   ad_group_resource_name: An ad group resource name.
#   customizer_attribute_resource_name: (optional) If present, indicates the resource
#     name of the customizer attribute to use in one of the descriptions.
#
# Returns:
#   Ad group ad resource name.
def create_ad_group_ad(client, customer_id, ad_group_resource_name, customizer_attribute_resource_name)
  ad_group_ad_service = client.service.ad_group_ad

  operation = client.operation.create_ad_group_ad do |aga|
    aga.status = :ENABLED
    aga.ad_group = ad_group_resource_name

    # Set responsive search ad info.
    # https://developers.google.com/google-ads/api/reference/rpc/latest/ResponsiveSearchAdInfo
    aga.ad = client.resource.ad do |ad|
      ad.final_urls << "https://www.example.com/"

      # Headline 1 (pinned)
      pinned_headline = create_ad_text_asset(
        client,
        "Headline 1 testing",
        client.enum.served_asset_field_type.HEADLINE_1,
      )

      # Headlines
      ad.responsive_search_ad = client.resource.responsive_search_ad_info do |rsa|
        rsa.headlines << pinned_headline
        rsa.headlines << create_ad_text_asset(client, "Headline 2 testing")
        rsa.headlines << create_ad_text_asset(client, "Headline 3 testing")

        # Descriptions
        description_1 = create_ad_text_asset(client, "Desc 1 testing")
        description_2 = if customizer_attribute_resource_name
          create_ad_text_asset_with_customizer(client, customizer_attribute_resource_name)
        else
          create_ad_text_asset(client, "Desc 2 testing")
        end
        rsa.descriptions << description_1
        rsa.descriptions << description_2

        # Paths
        rsa.path1 = "all-inclusive"
        rsa.path2 = "deals"
      end
    end
  end

  # Send a request to the server to add a responsive search ad.
  response = ad_group_ad_service.mutate_ad_group_ads(
    customer_id: customer_id,
    operations: [operation],
  )

  response.results.each do |result|
    puts "Created responsive search ad with resource name "#{result.resource_name}"."
  end
end

# Creates keywords.
#
# Creates 3 keyword match types: EXACT, PHRASE, and BROAD.
#
# Args:
#   client: An initialized GoogleAdsClient instance.
#   customer_id: A client customer ID.
#   ad_group_resource_name: An ad group resource name.
def add_keywords(client, customer_id, ad_group_resource_name)
  ad_group_criterion_service = client.service.ad_group_criterion

  keywords_to_add = [
    { text: KEYWORD_TEXT_EXACT, match_type: :EXACT },
    { text: KEYWORD_TEXT_PHRASE, match_type: :PHRASE },
    { text: KEYWORD_TEXT_BROAD, match_type: :BROAD },
  ]

  operations = keywords_to_add.map do |keyword_info|
    client.operation.create_ad_group_criterion do |agc|
      agc.ad_group = ad_group_resource_name
      agc.status = :ENABLED
      agc.keyword = client.resource.keyword_info do |ki|
        ki.text = keyword_info[:text]
        ki.match_type = keyword_info[:match_type]
      end
      # Optional: agc.negative = true
      # Optional: agc.final_urls << 'https://www.example.com'
    end
  end

  # Add keywords
  response = ad_group_criterion_service.mutate_ad_group_criteria(
    customer_id: customer_id,
    operations: operations,
  )
  response.results.each do |result|
    puts "Created keyword #{result.resource_name}."
  end
end

# Creates geo targets.
#
# Args:
#   client: An initialized GoogleAdsClient instance.
#   customer_id: A client customer ID.
#   campaign_resource_name: A campaign resource name.
def add_geo_targeting(client, customer_id, campaign_resource_name)
  geo_target_constant_service = client.service.geo_target_constant

  # Search by location names from
  # GeoTargetConstantService.suggest_geo_target_constants() and directly
  # apply GeoTargetConstant.resource_name.
  gtc_request = client.request.suggest_geo_target_constants do |req|
    req.locale = LOCALE
    req.country_code = COUNTRY_CODE
    # The location names to get suggested geo target constants.
    req.location_names = client.resource.location_names do |ln|
      ln.names << GEO_LOCATION_1
      ln.names << GEO_LOCATION_2
      ln.names << GEO_LOCATION_3
    end
  end

  response = geo_target_constant_service.suggest_geo_target_constants(gtc_request)

  operations = response.geo_target_constant_suggestions.map do |suggestion|
    puts "geo_target_constant: #{suggestion.geo_target_constant.resource_name} "          "is found in LOCALE (#{suggestion.locale}) "          "with reach (#{suggestion.reach}) "          "from search term (#{suggestion.search_term})."

    # Create the campaign criterion for location targeting.
    client.operation.create_campaign_criterion do |cc|
      cc.campaign = campaign_resource_name
      cc.location = client.resource.location_info do |li|
        li.geo_target_constant = suggestion.geo_target_constant.resource_name
      end
    end
  end

  unless operations.empty?
    campaign_criterion_service = client.service.campaign_criterion
    response = campaign_criterion_service.mutate_campaign_criteria(
      customer_id: customer_id,
      operations: operations, # Note: Python script sends this as [*operations] which is a way to unpack. Ruby passes array directly.
    )

    response.results.each do |result|
      puts "Added campaign criterion "#{result.resource_name}"."
    end
  else
    puts "No geo target suggestions found for the given locations. Skipping campaign criteria creation."
  end
end

# Main function that creates all necessary entities for the example.
#
# Args:
#   client: An initialized GoogleAdsClient instance.
#   customer_id: A client customer ID.
#   customizer_attribute_name: The name of the customizer attribute to be created.
def main_function(client, customer_id, customizer_attribute_name = nil)
  customizer_attribute_resource_name = nil
  if customizer_attribute_name
    customizer_attribute_resource_name = create_customizer_attribute(
      client,
      customer_id,
      customizer_attribute_name,
    )

    link_customizer_attribute_to_customer(
      client,
      customer_id,
      customizer_attribute_resource_name,
    )
  end

  # Create a budget, which can be shared by multiple campaigns.
  campaign_budget_resource_name = create_campaign_budget(client, customer_id)

  campaign_resource_name = create_campaign(
    client,
    customer_id,
    campaign_budget_resource_name,
  )

  ad_group_resource_name = create_ad_group(
    client,
    customer_id,
    campaign_resource_name,
  )

  create_ad_group_ad(
    client,
    customer_id,
    ad_group_resource_name,
    customizer_attribute_resource_name, # Pass the resource name here
  )

  add_keywords(client, customer_id, ad_group_resource_name)

  add_geo_targeting(client, customer_id, campaign_resource_name)
end

# Entry point of the script
if __FILE__ == $0
  options = Optimist.options do
    opt :customer_id, "The Google Ads customer ID.", type: :string, required: true, short: "-c"
    opt :customizer_attribute_name,
        "The name of the customizer attribute to be created. The name must "         "be unique across a client account, so be sure not to use "         "the same value more than once.",
        type: :string,
        short: "-n"
  end

  # GoogleAdsClient will read the google-ads.yaml configuration file in the
  # home directory if none is specified.
  client = Google::Ads::GoogleAds::GoogleAdsClient.new

  begin
    main_function(
      client,
      options[:customer_id],
      options[:customizer_attribute_name_given] ? options[:customizer_attribute_name] : nil,
    )
  rescue Google::Ads::GoogleAds::Errors::GoogleAdsError => e
    STDERR.puts "Request with ID '#{e.request_id}' failed with status "                  "'#{e.error.code}' and includes the following errors:"
    e.failure.errors.each do |error|
      STDERR.puts "	Error with message '#{error.message}'."
      if error.location
        error.location.field_path_elements.each do |field_path_element|
          STDERR.puts "		On field: #{field_path_element.field_name}"
        end
      end
    end
    exit 1
  rescue Google::Gax::RetryError => e
    STDERR.puts "RetryError: #{e}"
    exit 1
  end
end
