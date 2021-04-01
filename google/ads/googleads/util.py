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
_RE_FIND_CHARS_TO_UPPERCASE = re.compile(r"(?:_|^)([a-z])")


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

    return functools.reduce(_getattr, [obj] + attr.split("."))


def set_nested_message_field(message, field_path, value):
    """Sets the value of a nested attribute on a protobuf message instance.

    This method uses "setattr" to update a given field on a protobuf message
    instance, which means it can only be used to set fields that are of a
    primitive type, (i.e. "string" or "int64"). Additionally the given value
    must be of the same type as the target field.

    For example, consider the following Campaign message instance:

    campaign {
        app_campaign_setting {
            app_id: "123"
        }
    }

    The field "app_campaign_setting" has the type AppCampaignSetting and cannot
    be set with this method, however the field "app_campaign_setting.app_id"
    has the type "string" and thus can be set with this method, assuming that
    the given value is also a "string".

    The given field path can either be a dot-delimited string, such as
    "app_campaign_setting.app_id" or a list of strings, for example
    ["app_campaign_setting", "app_id"].

    Args:
        message: A protobuf message instance to set an attribute value on.
        field_path: The attribute path, either a dot-delimited string of field
            names or a list of strings.
        value: The value that the nested attribute should be set to.
    """
    if type(field_path) == str:
        field_path = field_path.split(".")

    if len(field_path) == 1:
        setattr(message, field_path[0], value)
    else:
        set_nested_message_field(
            getattr(message, field_path[0]), field_path[1:], value
        )


def convert_upper_case_to_snake_case(string):
    """Converts a string from UpperCase to snake_case.

    Primarily used to translate module names when retrieving them from version
    modules' __init__.py files.

    Args:
        string: an arbitrary string to convert.

    Returns:
        A new snake_case representation of the given string.
    """
    new_string = ""
    index = 0

    for char in string:
        if index == 0:
            new_string += char.lower()
        elif char.isupper():
            new_string += f"_{char.lower()}"
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
        return match.group().replace("_", "").upper()

    return _RE_FIND_CHARS_TO_UPPERCASE.sub(converter, string)
