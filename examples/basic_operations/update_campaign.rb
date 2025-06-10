#!/usr/bin/env ruby
# Encoding: utf-8
#
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
#
# This example updates a campaign.
# To get campaigns, run get_campaigns.rb.

require 'optparse'
require 'google/ads/google_ads'

def update_campaign(customer_id, campaign_id)
  # GoogleAdsClient will read a config file from
  # ENV['HOME']/google_ads_config.rb when called without arguments.
  client = Google::Ads::GoogleAds::GoogleAdsClient.new

  campaign_service = client.service(:Campaign)

  # Create campaign operation.
  campaign_operation = client.operation(:Campaign)
  campaign = campaign_operation.update
  campaign.resource_name = client.path.campaign(customer_id, campaign_id)

  campaign.status = :PAUSED

  campaign.network_settings = client.resource(:NetworkSettings) do |ns|
    ns.target_search_network = false
  end

  # Retrieve a FieldMask for the fields configured in the campaign.
  campaign_operation.update_mask = Google::Protobuf::FieldMask.new(
    paths: campaign.to_h.keys.map { |key| Google::Ads::GoogleAds::Utils.snake_case(key.to_s) }
  )

  response = campaign_service.mutate_campaigns(
    customer_id: customer_id,
    operations: [campaign_operation],
  )

  puts "Updated campaign #{response.results.first.resource_name}."
end

if __FILE__ == $0
  options = {}
  # The following parameter(s) should be provided to run the example. You can
  # either specify these by changing the INSERT_XXX_ID_HERE values below, or on
  # the command line.
  #
  # Parameters passed on the command line will override any parameters set in
  # code.
  #
  # Running the example with -h will print the command line usage.
  options[:customer_id] = 'INSERT_CUSTOMER_ID_HERE'
  options[:campaign_id] = 'INSERT_CAMPAIGN_ID_HERE'

  OptionParser.new do |opts|
    opts.banner = sprintf('Usage: %s [options]', File.basename(__FILE__))

    opts.separator ''
    opts.separator 'Required parameters:'

    opts.on('-C', '--customer-id CUSTOMER-ID', String, 'Customer ID') do |v|
      options[:customer_id] = v
    end

    opts.on('-c', '--campaign-id CAMPAIGN-ID', String, 'Campaign ID') do |v|
      options[:campaign_id] = v
    end

    opts.separator ''
    opts.separator 'Help:'

    opts.on_tail('-h', '--help', 'Show this message') do
      puts opts
      exit
    end
  end.parse!

  begin
    update_campaign(options.fetch(:customer_id).tr("-", ""), options.fetch(:campaign_id))
  rescue Google::Ads::GoogleAds::Errors::GoogleAdsError => e
    e.failure.errors.each do |error|
      STDERR.printf("Error with message: %s
", error.message)
      if error.location
        error.location.field_path_elements.each do |field_path_element|
          STDERR.printf("	On field: %s
", field_path_element.field_name)
        end
      end
    end
    STDERR.printf("Error: %s
", e.inspect)
  rescue Google::Gax::RetryError => e
    STDERR.printf("Error: %s
", e.inspect)
  end
end
