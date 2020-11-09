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
"""This example illustrates getting GeoTargetConstants by given location names.
"""


import sys

import google.ads.google_ads.client

# Locale is using ISO 639-1 format. If an invalid locale is given,
# 'en' is used by default.
LOCALE = "en"

# A list of country codes can be referenced here:
# https://developers.google.com/adwords/api/docs/appendix/geotargeting
COUNTRY_CODE = "FR"


def main(client):
    gtc_service = client.get_service("GeoTargetConstantService", version="v6")

    location_names = client.get_type(
        "SuggestGeoTargetConstantsRequest", version="v6"
    ).LocationNames()

    location_names.names.extend(["Paris", "Quebec", "Spain", "Deutschland"])

    results = gtc_service.suggest_geo_target_constants(
        LOCALE, COUNTRY_CODE, location_names=location_names
    )

    geo_target_constant_status_enum = client.get_type(
        "GeoTargetConstantStatusEnum"
    ).GeoTargetConstantStatus

    try:
        for suggestion in results.geo_target_constant_suggestions:
            geo_target_constant = suggestion.geo_target_constant
            print(
                "%s (%s, %s, %s, %s) is found in locale (%s) with reach (%d) "
                "from search term (%s)."
                % (
                    geo_target_constant.resource_name,
                    geo_target_constant.name,
                    geo_target_constant.country_code,
                    geo_target_constant.target_type,
                    geo_target_constant_status_enum.Name(
                        geo_target_constant.status
                    ),
                    suggestion.locale,
                    suggestion.reach,
                    suggestion.search_term,
                )
            )
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print(
            'Request with ID "%s" failed with status "%s" and includes the '
            "following errors:" % (ex.request_id, ex.error.code().name)
        )
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print("\t\tOn field: %s" % field_path_element.field_name)
        sys.exit(1)


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = (
        google.ads.google_ads.client.GoogleAdsClient.load_from_storage()
    )

    main(google_ads_client)
