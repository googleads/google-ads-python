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
"""This example creates  an OAuth2 refresh token using the Web application flow.

To retrieve the necessary client_secrets JSON file, first generate an OAuth 2.0
client ID of type 'Web application' in the Google Cloud Console:

https://console.cloud.google.com

Make sure 'http://localhost:8080' is included the list of authorized redirect
URIs for this client ID.

Once complete, download the credentials and save the file path so it can be
passed into this example.
"""


import argparse
import hashlib
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import os

from google_auth_oauthlib.flow import Flow


_SCOPE = "https://www.googleapis.com/auth/adwords"
_REDIRECT_URI = "http://localhost:8080"


def main(client_secrets_path, scopes):
    """The main method, starts a basic server and initializes an auth request.

    Args:
        client_secrets_path: a path to where the client secrete JSON file is
            located on the machine running this example.
        scopes: a list of API scopes to include in the auth request, see:
            https://developers.google.com/identity/protocols/oauth2/scopes
    """
    flow = Flow.from_client_secrets_file(client_secrets_path, scopes=scopes)
    flow.redirect_uri = _REDIRECT_URI

    # Create an anti-forgery state token as described here:
    # https://developers.google.com/identity/protocols/OpenIDConnect#createxsrftoken
    passthrough_val = hashlib.sha256(os.urandom(1024)).hexdigest()

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        state=passthrough_val,
        include_granted_scopes='true'
    )

    print(authorization_url)
    _get_authorization_code()


class rootHttpHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        query_params = parse_qs(urlparse(self.path).query)
        code = query_params["code"]


def _get_authorization_code():
    """Initializes a basic http server to listen for auth requests."""
    server = socketserver.TCPServer(("", 8080), rootHttpHandler)
    server.handle_request()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Generates OAuth2 refresh token using the Web application flow. "
            "To retrieve the necessary client_secrets JSON file, first "
            "generate an OAuth 2.0 client ID of type Web application in the "
            "Google Cloud Console (https://console.cloud.google.com). "
            "Make sure 'http://localhost:8080' is included the list of "
            "'Authorized redirect URIs' for this client ID."
        ),
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "--client_secrets_path",
        required=True,
        type=str,
        help=(
            "Path to the client secrets JSON file from the Google Developers "
            "Console that contains your client ID, client secret, and "
            "redirect URIs."
        ),
    )
    parser.add_argument(
        "--additional_scopes",
        default=None,
        type=str,
        nargs="+",
        help="Additional scopes to apply when generating the refresh token.",
    )
    args = parser.parse_args()

    configured_scopes = [_SCOPE]

    if args.additional_scopes:
        configured_scopes.extend(args.additional_scopes)

    main(args.client_secrets_path, configured_scopes)
