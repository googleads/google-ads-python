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
"""This code example gets all image assets."""


import argparse
import sys
from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException

_DEFAULT_PAGE_SIZE = 1000


def main(client, customer_id, page_size):
    """Main method, to run this code example as a standalone application."""
    ga_service = client.get_service('GoogleAdsService', version='v2')

    query = ('SELECT asset.name, asset.image_asset.file_size, '
             'asset.image_asset.full_size.width_pixels, '
             'asset.image_asset.full_size.height_pixels, '
             'asset.image_asset.full_size.url FROM asset '
             'WHERE asset.type = \'IMAGE\'')

    results = ga_service.search(customer_id, query=query, page_size=page_size)

    try:
        count = 0
        for row in results:
            asset = row.asset
            image_asset = asset.image_asset
            count += 1
            print(f'Image with name "{asset.name}" found:\n'
                  f'\tfile size {image_asset.file_size.value} bytes\n'
                  f'\twidth {image_asset.full_size.width_pixels.value}px\n'
                  f'\theight {image_asset.full_size.height_pixels.value}px\n'
                  f'\turl "{image_asset.full_size.url.value}"')

        print(f'Total of {count} image(s) found.')
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
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()

    parser = argparse.ArgumentParser(
        description='List all image assets for specified customer.')
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=str,
                        required=True, help='The Google Ads customer ID.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, _DEFAULT_PAGE_SIZE)
