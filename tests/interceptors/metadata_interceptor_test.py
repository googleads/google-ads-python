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

from google.ads.googleads.interceptors import MetadataInterceptor


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

    def test_intercept_updates_user_agent_add_pb(self):
        """Asserts that the protobuf version is included in the user agent.

        This test should be removed or updated once this functionality is
        incorporated into python-api-core per this feature request:
        https://github.com/googleapis/python-api-core/issues/416
        """
        interceptor = MetadataInterceptor(
            self.mock_developer_token,
            self.mock_login_customer_id,
            self.mock_linked_customer_id,
        )

        mock_request = mock.Mock()
        mock_client_call_details = mock.Mock()
        mock_client_call_details.method = "test/method"
        mock_client_call_details.timeout = 5
        mock_client_call_details.metadata = [
            ("apples", "oranges"),
            ("x-goog-api-client", "gl-python/3.7.0 grpc/1.45.0 gax/2.2.2"),
        ]
        # Create a simple function that just returns the client_call_details
        # so we can make assertions about what was modified in the _intercept
        # method.
        def mock_continuation(client_call_details, request):
            return client_call_details

        with mock.patch.object(
            interceptor,
            "_update_client_call_details_metadata",
            wraps=interceptor._update_client_call_details_metadata,
        ) as mock_updater:
            modified_client_call_details = interceptor._intercept(
                mock_continuation, mock_client_call_details, mock_request
            )

            user_agent = modified_client_call_details.metadata[1][1]
            self.assertEqual(user_agent.count("pb"), 1)

    def test_intercept_updates_user_agent_existing_pb(self):
        """Asserts that the protobuf version is not added if already present.

        This test should be removed or updated once this functionality is
        incorporated into python-api-core per this feature request:
        https://github.com/googleapis/python-api-core/issues/416
        """
        interceptor = MetadataInterceptor(
            self.mock_developer_token,
            self.mock_login_customer_id,
            self.mock_linked_customer_id,
        )

        mock_request = mock.Mock()
        mock_client_call_details = mock.Mock()
        mock_client_call_details.method = "test/method"
        mock_client_call_details.timeout = 5
        mock_client_call_details.metadata = [
            ("apples", "oranges"),
            ("x-goog-api-client", "gl-python/3.7.0 grpc/1.45.0 pb/3.21.0",),
        ]
        # Create a simple function that just returns the client_call_details
        # so we can make assertions about what was modified in the _intercept
        # method.
        def mock_continuation(client_call_details, request):
            return client_call_details

        with mock.patch.object(
            interceptor,
            "_update_client_call_details_metadata",
            wraps=interceptor._update_client_call_details_metadata,
        ) as mock_updater:
            modified_client_call_details = interceptor._intercept(
                mock_continuation, mock_client_call_details, mock_request
            )

            user_agent = modified_client_call_details.metadata[1][1]
            # We assert that the _intercept method did not add the "pb" key
            # value pair because it was already present when passed in.
            self.assertEqual(user_agent.count("pb"), 1)
