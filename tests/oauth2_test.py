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

from google.ads.google_ads import oauth2


class OAuth2Tests(TestCase):

    def setUp(self):
        self.client_id = 'client_id_123456789'
        self.client_secret = 'client_secret_987654321'
        self.refresh_token = 'refresh'
        self.token_uri = 'www.tokenuri.com'

    def test_get_installed_app_credentials(self):
        mock_credentials = mock.Mock()
        mock_request = mock.Mock()
        with mock.patch.object(
            oauth2,
            'InstalledAppCredentials',
            return_value=mock_credentials
        ) as mock_initializer, mock.patch.object(
            oauth2,
            'Request',
            return_value = mock_request
        ) as mock_request_class:
            result = oauth2.get_installed_app_credentials(
                self.client_id, self.client_secret, self.refresh_token,
                self.token_uri)

            mock_initializer.assert_called_once_with(
                None,
                client_id=self.client_id,
                client_secret=self.client_secret,
                refresh_token=self.refresh_token,
                token_uri=self.token_uri)
            mock_request_class.assert_called_once()
            result.refresh.assert_called_once_with(mock_request)
