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
"""Tests the configuration helper module."""

import os
import yaml
from pyfakefs.fake_filesystem_unittest import TestCase as FileTestCase

from google.ads.google_ads import config

class ConfigTest(FileTestCase):
    def setUp(self):
        self.setUpPyfakefs()
        self.developer_token = 'abc123'
        self.client_id = 'client_id_123456789'
        self.client_secret = 'client_secret_987654321'
        self.refresh_token = 'refresh'
        self.login_customer_id = '1234567890'
        self.path_to_private_key_file = '/test/path/to/config.json'
        self.delegated_account = 'delegated@account.com'


    def test_load_from_yaml_file(self):
        file_path = os.path.join(os.path.expanduser('~'), 'google-ads.yaml')
        self.fs.create_file(file_path, contents=yaml.safe_dump({
            'developer_token': self.developer_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token}))

        result = config.load_from_yaml_file()

        self.assertEqual(result['developer_token'], self.developer_token)
        self.assertEqual(result['client_id'], self.client_id)
        self.assertEqual(result['client_secret'], self.client_secret)
        self.assertEqual(result['refresh_token'], self.refresh_token)

    def test_load_from_yaml_file_with_path(self):
        custom_path = os.path.expanduser('/test/custom/path')
        file_path = os.path.join(custom_path, 'google-ads.yaml')
        self.fs.create_file(file_path, contents=yaml.safe_dump({
            'developer_token': self.developer_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token}))

        result = config.load_from_yaml_file(path=file_path)

        self.assertEqual(result['developer_token'], self.developer_token)
        self.assertEqual(result['client_id'], self.client_id)
        self.assertEqual(result['client_secret'], self.client_secret)
        self.assertEqual(result['refresh_token'], self.refresh_token)