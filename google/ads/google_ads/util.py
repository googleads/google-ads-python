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
"""Common utilities for the Google Ads API client library."""


class ResourceName:

    # As of Google Ads API v1 composite resource names are
    # delimited by a "~" character.
    _COMPOSITE_DELIMITER = '~'

    @classmethod
    def format_composite(cls, *arg):
        """Formats any number of ID strings into a single composite string.

        Note: this utility does not construct an entire resource name string.
        It only formats the composite portion for IDs that are not globally
        unique, for example an ad_group_ad.

        Args:
            arg: Any number of str IDs for resources such as ad_groups or
            ad_group_ads.

        Returns:
            A str of all the given strs concatenated with the compsite
            delimiter.

        Raises:
           TypeError: If anything other than a string is passed in.
        """
        return cls._COMPOSITE_DELIMITER.join(arg)

