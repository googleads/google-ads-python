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
"""Tests for the Google Ads API client util module."""

import mock
from unittest import TestCase

import google.ads.google_ads.util as util


class UtilsTest(TestCase):
    def test_patch_to_json_method_callable(self):
        self.assertTrue(callable(util.patch_to_json_method))

    def test_patch_to_json_method_augments(self):
        mock_obj = mock.Mock()
        util.patch_to_json_method(mock_obj)
        self.assertTrue(callable(mock_obj.ToJsonString))

    def test_patch_to_json_returns_string(self):
        mock_obj = mock.Mock()
        util.patch_to_json_method(mock_obj)
        self.assertIsInstance(mock_obj.ToJsonString(mock_obj), str)

    def test_patch_to_json_stringifies_paths(self):
        mock_obj = mock.Mock()
        mock_obj.paths = ['hello', 'goodbye']
        util.patch_to_json_method(mock_obj)
        self.assertEqual(mock_obj.ToJsonString(mock_obj), 'hello,goodbye')

    def test_patch_to_json_camel_cases_paths(self):
        mock_obj = mock.Mock()
        mock_obj.paths = ['hello', '_test_test_test']
        util.patch_to_json_method(mock_obj)
        self.assertEqual(mock_obj.ToJsonString(mock_obj), 'hello,TestTestTest')

    def test_path_to_json_camel_cases_digits(self):
        mock_obj = mock.Mock()
        mock_obj.paths = ['hello', '_test_25_test']
        util.patch_to_json_method(mock_obj)
        self.assertEqual(mock_obj.ToJsonString(mock_obj), 'hello,Test25Test')

