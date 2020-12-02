# Copyright 2020 Google LLC
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
"""Tests for the Metadata gRPC Interceptor."""

from unittest import TestCase

import mock

from google.ads.google_ads.interceptors import MetadataInterceptor


class MetadataInterceptorTest(TestCase):
    def setUp(self):
        self.mock_developer_token = "1234567890"
        self.mock_login_customer_id = "0987654321"
        self.mock_linked_customer_id = "5555555555"
        super(MetadataInterceptorTest, self).setUp()

    def test_init(self):
        interceptor = MetadataInterceptor(
            self.mock_developer_token, self.mock_login_customer_id
        )

        self.assertEqual(
            interceptor.developer_token_meta,
            ("developer-token", self.mock_developer_token),
        )

        self.assertEqual(
            interceptor.login_customer_id_meta,
            ("login-customer-id", self.mock_login_customer_id),
        )

    def test_init_no_login_customer_id(self):
        interceptor = MetadataInterceptor(self.mock_developer_token, None)

        self.assertEqual(
            interceptor.developer_token_meta,
            ("developer-token", self.mock_developer_token),
        )

        self.assertEqual(interceptor.login_customer_id_meta, None)

    def test_init_no_linked_customer_id(self):
        interceptor = MetadataInterceptor(self.mock_developer_token, None, None)

        self.assertEqual(
            interceptor.developer_token_meta,
            ("developer-token", self.mock_developer_token),
        )

        self.assertEqual(interceptor.linked_customer_id_meta, None)

    def test_update_client_call_details_metadata(self):
        interceptor = MetadataInterceptor(
            self.mock_developer_token, self.mock_login_customer_id
        )

        mock_metadata = list([("test-key", "test-value")])
        mock_client_call_details = mock.Mock()

        client_call_details = interceptor._update_client_call_details_metadata(
            mock_client_call_details, mock_metadata
        )

        self.assertEqual(client_call_details.metadata, mock_metadata)

    def test_intercept_unary_unary(self):
        interceptor = MetadataInterceptor(
            self.mock_developer_token,
            self.mock_login_customer_id,
            self.mock_linked_customer_id,
        )

        mock_continuation = mock.Mock(return_value=None)
        mock_client_call_details = mock.Mock()
        mock_client_call_details.method = "test/method"
        mock_client_call_details.timeout = 5
        mock_client_call_details.metadata = [("apples", "oranges")]
        mock_request = mock.Mock()

        with mock.patch.object(
            interceptor,
            "_update_client_call_details_metadata",
            wraps=interceptor._update_client_call_details_metadata,
        ) as mock_updater:
            interceptor.intercept_unary_unary(
                mock_continuation, mock_client_call_details, mock_request
            )

            mock_updater.assert_called_once_with(
                mock_client_call_details,
                [
                    mock_client_call_details.metadata[0],
                    interceptor.developer_token_meta,
                    interceptor.login_customer_id_meta,
                    interceptor.linked_customer_id_meta,
                ],
            )

            mock_continuation.assert_called_once()

    def test_intercept_unary_stream(self):
        interceptor = MetadataInterceptor(
            self.mock_developer_token,
            self.mock_login_customer_id,
            self.mock_linked_customer_id,
        )

        mock_continuation = mock.Mock(return_value=None)
        mock_client_call_details = mock.Mock()
        mock_client_call_details.method = "test/method"
        mock_client_call_details.timeout = 5
        mock_client_call_details.metadata = [("apples", "oranges")]
        mock_request = mock.Mock()

        with mock.patch.object(
            interceptor,
            "_update_client_call_details_metadata",
            wraps=interceptor._update_client_call_details_metadata,
        ) as mock_updater:
            interceptor.intercept_unary_stream(
                mock_continuation, mock_client_call_details, mock_request
            )

            mock_updater.assert_called_once_with(
                mock_client_call_details,
                [
                    mock_client_call_details.metadata[0],
                    interceptor.developer_token_meta,
                    interceptor.login_customer_id_meta,
                    interceptor.linked_customer_id_meta,
                ],
            )

            mock_continuation.assert_called_once()
