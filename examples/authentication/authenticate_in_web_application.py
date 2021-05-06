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
"""This example creates an OAuth2 refresh token using the Web application flow.

This example will start a basic server that listens for requests at
http://localhost:PORT, where PORT is passed into the example via a command line
argument.

Note: You must add `http://localhost/oauth2callback` to the "Authorize redirect
URIs" list in your Google Cloud Console project before running this example.
"""


import argparse

from google_auth_oauthlib.flow import InstalledAppFlow


SCOPE = "https://www.googleapis.com/auth/adwords"


def main(client_secrets_path, scopes):
    flow = InstalledAppFlow.from_client_secrets_file(
        client_secrets_path, scopes=scopes
    )

    flow.run_local_server()

    print(f"Access token: {flow.credentials.token}")
    print(f"Refresh token: {flow.credentials.refresh_token}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Generates OAuth2 refresh token using the Web application flow. "
            "To retrieve the necessary tokens, generate a client ID and client "
            "secret in the Google Cloud Console "
            "(https://console.cloud.google.com) by creating credentials for a "
            "Web application. Set the 'Authorized redirect URIs' "
            "to: http://localhost:[PORT]"
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "--client_secrets_path",
        required=True,
        type=str,
        help=(
            "Path to the client secrets JSON file from the "
            "Google Developers Console that contains your "
            "client ID and client secret."
        ),
    )
    parser.add_argument(
        "--additional_scopes",
        default=None,
        type=str,
        nargs="+",
        help=("Additional scopes to apply when generating the refresh token."),
    )
    args = parser.parse_args()

    configured_scopes = [SCOPE]

    if args.additional_scopes:
        configured_scopes.extend(args.additional_scopes)

    main(args.client_secrets_path, configured_scopes)
