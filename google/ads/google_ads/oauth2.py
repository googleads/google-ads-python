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
"""A set of functions to help initialize OAuth2 credentials."""

from google.oauth2.credentials import Credentials as InstalledAppCredentials
from google.auth.transport.requests import Request

def get_installed_app_credentials(
    client_id, client_secret, refresh_token, token_uri):
    credentials = InstalledAppCredentials(
        None, client_id=client_id, client_secret=client_secret,
        refresh_token=refresh_token, token_uri=token_uri)

    credentials.refresh(Request())
    return credentials
