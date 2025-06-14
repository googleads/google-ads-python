#!/usr/bin/env python
# Copyright 2023 Google LLC
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
"""A set of helper functions for use in code examples."""

from datetime import datetime, timezone
import requests


def get_printable_datetime() -> str:
    """Generates a string for the current date and time in local time zone.

    The datetime string has the following format, where the trailing "sZ"
    represents three digits of milliseconds plus the timezone offset:
    %Y-%m-%dT%H:%M%S.sZ

    Here's an example output: "2023-03-23T15:45:25.211+04:00"

    Returns:
        a datetime string
    """
    return (
        datetime.now(timezone.utc)
        .astimezone()
        .isoformat(timespec="milliseconds")
    )


def get_image_bytes_from_url(url: str) -> bytes:
    """Retrieves the raw bytes of an image from a url.

    Args:
        url: The URL of the image to retrieve.

    Returns:
        Raw bytes of an image.
    """
    try:
        return requests.get(url).content
    except requests.exceptions.RequestException as e:
        print(f"Could not download image from url: {url}")
        raise e
