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


from google.oauth2.service_account import Credentials as ServiceAccountCreds
from google.oauth2.credentials import Credentials as InstalledAppCredentials
from google.auth.transport.requests import Request

_SERVICE_ACCOUNT_SCOPES = ['https://www.googleapis.com/auth/adwords']
_DEFAULT_TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'

def get_installed_app_credentials(
    client_id, client_secret, refresh_token, token_uri=_DEFAULT_TOKEN_URI):
    """Creates and returns an instance of oauth2.credentials.Credentials.

    Args:
        client_id: A str of the oauth2 client_id from configuration.
        client_secret: A str of the oauth2 client_secret from configuration.
        refresh_token: A str of the oauth2 refresh_token from configuration.

    Returns:
        An instance of oauth2.credentials.Credentials
    """
    credentials = InstalledAppCredentials(
        None, client_id=client_id, client_secret=client_secret,
        refresh_token=refresh_token, token_uri=token_uri)

    credentials.refresh(Request())
    return credentials


def get_service_account_credentials(path_to_private_key_file, subject,
                                    scopes=_SERVICE_ACCOUNT_SCOPES):
    """Creates and returns an instance of oauth2.service_account.Credentials.

    Args:
        path_to_private_key_file: A str of the path to the private key file
            location.
        subject: A str of the email address of the delegated account.
        scopes: A list of additional scopes.

    Returns:
        An instance of oauth2.credentials.Credentials
    """
    credentials = ServiceAccountCreds.from_service_account_file(
        path_to_private_key_file,
        subject=subject,
        scopes=scopes)

    credentials.refresh(Request())
    return credentials
