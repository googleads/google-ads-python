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

import functools
import re

# This regex matches characters preceded by start of line or an underscore.
_RE_FIND_CHARS_TO_UPPERCASE = re.compile(r'(?:_|^)([a-z])')


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


def get_nested_attr(obj, attr, *args):
    """Gets the value of a nested attribute from an object.

    Args:
      obj: an object to retrieve an attribute value from.
      attr: a string of the attribute separated by dots.

    Returns:
      The object attribute value or the given *args if the attr isn't present.
    """
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)

    return functools.reduce(_getattr, [obj] + attr.split('.'))


def convert_upper_case_to_snake_case(string):
    """Converts a string from UpperCase to snake_case.

    Primarily used to translate module names when retrieving them from version
    modules' __init__.py files.

    Args:
        string: an arbitrary string to convert.
    """
    new_string = ''
    index = 0

    for char in string:
        if index == 0:
            new_string += char.lower()
        elif char.isupper():
            new_string += f'_{char.lower()}'
        else:
            new_string += char

        index += 1

    return new_string


def convert_snake_case_to_upper_case(string):
    """Converts a string from snake_case to UpperCase.

    Primarily used to translate module names when retrieving them from version
    modules' __init__.py files.

    Args:
        string: an arbitrary string to convert.
    """
    def converter(match):
        """Convert a string to strip underscores then uppercase it."""
        return match.group().replace('_', '').upper()

    return _RE_FIND_CHARS_TO_UPPERCASE.sub(converter, string)
