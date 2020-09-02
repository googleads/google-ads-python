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
"""This example creates an OAuth 2.0 refresh token for the Google Ads API.

This illustrates how to step through the OAuth 2.0 native / installed
application flow.

It is intended to be run from the command line and requires user input.
"""


import argparse

from google_auth_oauthlib.flow import InstalledAppFlow


SCOPE = "https://www.googleapis.com/auth/adwords"


def main(client_secrets_path, scopes):
    flow = InstalledAppFlow.from_client_secrets_file(
        client_secrets_path, scopes=scopes
    )

    flow.run_console()

    print("Access token: %s" % flow.credentials.token)
    print("Refresh token: %s" % flow.credentials.refresh_token)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generates OAuth 2.0 credentials with the specified "
        "client secrets file."
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "--client_secrets_path",
        required=True,
        help=(
            "Path to the client secrets JSON file from the "
            "Google Developers Console that contains your "
            "client ID and client secret."
        ),
    )
    parser.add_argument(
        "--additional_scopes",
        default=None,
        help=(
            "Additional scopes to apply when generating the "
            "refresh token. Each scope should be separated "
            "by a comma."
        ),
    )
    args = parser.parse_args()

    configured_scopes = [SCOPE]

    if args.additional_scopes:
        configured_scopes.extend(
            args.additional_scopes.replace(" ", "").split(",")
        )

    main(args.client_secrets_path, configured_scopes)
