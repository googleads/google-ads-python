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
"""This example illustrates how to retrieve artifact metadata.

The metadata retrieved can provide additional context about the artifact,
such as whether it is selectable, filterable, or sortable. The artifact can be
either a resource (such as customer, or campaign) or a field (such as
metrics.impressions, campaign.id). It also shows the data type and artifacts
that are selectable with the artifact.
"""

from __future__ import absolute_import

import argparse
import six
import sys
import google.ads.google_ads.client


_DEFAULT_PAGE_SIZE = 1000


def _is_or_is_not(bool_value):
    """Produces display text for whether metadata is applicable to artifact.

    Args:
        bool_value: a BoolValue instance.

    Returns:
        A str with value "is" if bool_value is True, else "is not".
    """
    return 'is' if bool_value.value else 'isn\'t'


def main(client, artifact_name, page_size):
    gaf_service = client.get_service('GoogleAdsFieldService')

    # Searches for an artifact with the specified name.
    query = ('SELECT name, category, selectable, filterable, sortable, '
             'selectable_with, data_type, is_repeated '
             'WHERE name = \'%s\'') % artifact_name

    response = gaf_service.search_google_ads_fields(
        query=query, page_size=page_size)

    # Iterates over all rows and prints out the metadata of the returned
    # artifacts.
    try:
        for google_ads_field in response:
            # Note that the category and data type printed below are enum
            # values. For example, a value of 2 will be returned when the
            # category is "RESOURCE".
            #
            # A mapping of enum names to values can be found in
            # GoogleAdsFieldCategoryEnum for the category and
            # GoogleAdsFieldDataTypeEnum for the data type.
            selectable = _is_or_is_not(google_ads_field.selectable)
            filterable = _is_or_is_not(google_ads_field.filterable)
            sortable = _is_or_is_not(google_ads_field.sortable)
            is_repeated = _is_or_is_not(google_ads_field.is_repeated)

            print('An artifact named "%s" with category %d and data type %d %s '
                  'selectable, %s filterable, %s sortable, and %s repeated.'
                  % (google_ads_field.name.value, google_ads_field.category,
                     google_ads_field.data_type, selectable, filterable,
                     sortable, is_repeated))

            if len(google_ads_field.selectable_with) > 0:
                selectable_artifacts = [
                    wrapped_selectable_artifact.value
                    for wrapped_selectable_artifact
                    in google_ads_field.selectable_with]

                print('')
                print('The artifact can be selected with the following '
                      'artifacts:')
                for artifact in selectable_artifacts:
                    print(artifact)
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)


if __name__ == '__main__':
    # GoogleAdsClient will read a google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = (google.ads.google_ads.client.GoogleAdsClient
                         .load_from_storage())

    parser = argparse.ArgumentParser(
        description='Lists metadata for the specified artifact.')
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-a', '--artifact_name', type=six.text_type,
                        required=True,
                        help='The name of the artifact for which we are '
                        'retrieving metadata.')
    args = parser.parse_args()

    main(google_ads_client, args.artifact_name, _DEFAULT_PAGE_SIZE)
