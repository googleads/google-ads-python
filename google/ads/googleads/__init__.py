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

import sys
import warnings

import google.ads.googleads.client
import google.ads.googleads.errors
import google.ads.googleads.util

VERSION = "28.0.0.post1"

# Warns that this version of the library is intended as a temporary workaround
# for Python 3.8 users.
warnings.warn(
    "This version of google-ads-python (28.0.0.post1) is only intended for "
    "use by Python 3.8 users who cannot upgrade to a newer version of Python "
    "and are blocked from accessing the Google Ads API due to changes made to"
    "comply with European Union Political Ads Regulation. For more details, "
    "see: https://ads-developers.googleblog.com/2025/08/eu-par-google-ads-api-scripts.html. "
    "We recommend upgrading to Python >=3.10 and google-ads-python >=28.0.0 "
    "as soon as possible.",
    category=Warning,
)
