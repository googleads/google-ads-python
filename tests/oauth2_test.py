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
"""Tests for the OAuth2 helper module."""

import mock
from unittest import TestCase

from google.ads.googleads import oauth2


class OAuth2Tests(TestCase):
    def setUp(self):
        self.client_id = "client_id_123456789"
        self.client_secret = "client_secret_987654321"
        self.refresh_token = "refresh"
        self.json_key_file_path = "/path/to/file"
        self.subject = "test@test.com"
        self.token_uri = oauth2._DEFAULT_TOKEN_URI
        self.scopes = oauth2._SERVICE_ACCOUNT_SCOPES

    def test_get_installed_app_credentials(self):
        mock_credentials = mock.Mock()
        mock_request = mock.Mock()
        with mock.patch.object(
            oauth2, "InstalledAppCredentials", return_value=mock_credentials
        ) as mock_initializer, mock.patch.object(
            oauth2, "Request", return_value=mock_request
        ) as mock_request_class:
            result = oauth2.get_installed_app_credentials(
                self.client_id, self.client_secret, self.refresh_token
            )

            mock_initializer.assert_called_once_with(
                None,
                client_id=self.client_id,
                client_secret=self.client_secret,
                refresh_token=self.refresh_token,
                token_uri=self.token_uri,
            )
            mock_request_class.assert_called_once()
            result.refresh.assert_called_once_with(mock_request)

    def test_get_service_account_credentials(self):
        mock_credentials = mock.Mock()
        mock_request = mock.Mock()
        with mock.patch.object(
            oauth2.ServiceAccountCreds,
            "from_service_account_file",
            return_value=mock_credentials,
        ) as mock_initializer, mock.patch.object(
            oauth2, "Request", return_value=mock_request
        ) as mock_request_class:
            result = oauth2.get_service_account_credentials(
                self.json_key_file_path, self.subject
            )

            mock_initializer.assert_called_once_with(
                self.json_key_file_path,
                subject=self.subject,
                scopes=self.scopes,
            )
            mock_request_class.assert_called_once()
            result.refresh.assert_called_once_with(mock_request)

    def test_get_credentials_installed_application(self):
        mock_config = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
        }

        with mock.patch.object(
            oauth2, "get_installed_app_credentials", return_value=None
        ) as mock_initializer:
            oauth2.get_credentials(mock_config)
            mock_initializer.assert_called_once_with(
                self.client_id, self.client_secret, self.refresh_token
            )

    def test_get_credentials_installed_application_bad_config(self):
        # using a config that is missing the refresh_token key
        mock_config = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        self.assertRaises(ValueError, oauth2.get_credentials, mock_config)

    def test_get_credentials_installed_application(self):
        mock_config = {
            "json_key_file_path": self.json_key_file_path,
            "impersonated_email": self.subject,
        }

        with mock.patch.object(
            oauth2, "get_service_account_credentials", return_value=None
        ) as mock_initializer:
            oauth2.get_credentials(mock_config)
            mock_initializer.assert_called_once_with(
                self.json_key_file_path, self.subject, http_proxy=None,
            )

    def test_get_credentials_with_proxy(self):
        http_proxy = "https://localhost:8000"
        mock_request = mock.Mock()
        mock_session = mock.Mock()
        mock_config = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "http_proxy": http_proxy,
        }

        with mock.patch.object(
            oauth2, "get_installed_app_credentials", return_value=None
        ) as mock_initializer:
            oauth2.get_credentials(mock_config)

            mock_initializer.assert_called_once_with(
                self.client_id,
                self.client_secret,
                self.refresh_token,
                http_proxy=http_proxy,
            )

    def test_get_installed_app_credentials_with_proxy(self):
        http_proxy = "https://localhost:8000"
        mock_request = mock.Mock()
        mock_session = mock.Mock()
        mock_credentials = mock.Mock()

        with mock.patch.object(
            oauth2, "InstalledAppCredentials", return_value=mock_credentials
        ) as mock_initializer, mock.patch.object(
            oauth2, "Request", return_value=mock_request
        ) as mock_request_class, mock.patch.object(
            oauth2, "Session", return_value=mock_session
        ) as mock_session_initializer:

            oauth2.get_installed_app_credentials(
                self.client_id,
                self.client_secret,
                self.refresh_token,
                http_proxy=http_proxy,
            )
            mock_request_class.assert_called_once_with(session=mock_session)

    def test_get_installed_app_credentials_without_proxy(self):
        mock_request = mock.Mock()
        mock_session = mock.Mock()
        mock_credentials = mock.Mock()

        with mock.patch.object(
            oauth2, "InstalledAppCredentials", return_value=mock_credentials
        ) as mock_initializer, mock.patch.object(
            oauth2, "Request", return_value=mock_request
        ) as mock_request_class:

            oauth2.get_installed_app_credentials(
                self.client_id, self.client_secret, self.refresh_token
            )
            mock_request_class.assert_called_once_with()
