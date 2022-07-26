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

import mock
import os
import yaml
from pyfakefs.fake_filesystem_unittest import TestCase as FileTestCase

from google.ads.googleads import config


class ConfigTest(FileTestCase):
    def setUp(self):
        self.setUpPyfakefs()
        self.developer_token = "abc123"
        self.client_id = "client_id_123456789"
        self.client_secret = "client_secret_987654321"
        self.refresh_token = "refresh"
        self.login_customer_id = "1234567890"
        self.linked_customer_id = "0987654321"
        self.path_to_private_key_file = "/test/path/to/config.json"
        self.json_key_file_path = "/another/test/path/to/config.json"
        self.delegated_account = "delegated@account.com"
        self.endpoint = "www.testendpoint.com"
        self.configuration_file_path = "/usr/test/path/google-ads.yaml"
        self.impersonated_email = "impersonated@account.com"
        self.use_proto_plus = False
        # The below fields are defaults that include required keys.
        # They are merged with other keys in individual tests, and isolated
        # here so that new required keys don't need to be added to each test.
        self.default_dict_config = {
            "developer_token": self.developer_token,
            "use_proto_plus": self.use_proto_plus,
        }
        self.default_env_var_config = {
            "GOOGLE_ADS_DEVELOPER_TOKEN": self.developer_token,
            "GOOGLE_ADS_USE_PROTO_PLUS": self.use_proto_plus,
        }

    def _create_mock_yaml(
        self,
        additional_configs,
        file_path=os.path.join(os.path.expanduser("~"), "google-ads.yaml"),
    ):
        merged = {**self.default_dict_config, **additional_configs}
        self.fs.create_file(
            file_path,
            contents=yaml.safe_dump(merged),
        )

    def test_load_from_yaml_file_logging(self):
        """Should load logging config from yaml if provided."""
        self._create_mock_yaml(
            {
                "developer_token": self.developer_token,
                "logging": {
                    "version": 1,
                    "disable_existing_loggers": False,
                    "formatters": {
                        "default_fmt": {
                            "format": "[%(asctime)s - %(levelname)s]",
                            "datefmt": "%Y-%m-%d %H:%M:%S",
                        }
                    },
                    "handlers": {
                        "default_handler": {
                            "class": "logging.StreamHandler",
                            "formatter": "default_fmt",
                        }
                    },
                    "loggers": {
                        "": {
                            "handlers": ["default_handler"],
                            "level": "DEBUG",
                        }
                    },
                },
            }
        )

        result = config.load_from_yaml_file()

        self.assertEqual(result["developer_token"], self.developer_token)
        self.assertIsInstance(result["logging"], dict)

    def test_load_from_yaml_file_logging_invalid_json(self):
        """Should raise ValueError if logging config is not valid JSON."""
        self._create_mock_yaml({"logging": "not JSON"})
        self.assertRaises(ValueError, config.load_from_yaml_file)

    def test_load_from_yaml_file(self):
        """Should load config from a yaml file in the root directory."""
        self._create_mock_yaml(
            {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self.refresh_token,
            }
        )

        result = config.load_from_yaml_file()

        self.assertEqual(result["developer_token"], self.developer_token)
        self.assertEqual(result["use_proto_plus"], self.use_proto_plus)
        self.assertEqual(result["client_id"], self.client_id)
        self.assertEqual(result["client_secret"], self.client_secret)
        self.assertEqual(result["refresh_token"], self.refresh_token)

    def test_load_from_yaml_file_missing_developer_token(self):
        """Should raise ValueError if developer_token key is missing."""
        file_path = os.path.join(os.path.expanduser("~"), "google-ads.yaml")
        # save a YAML file without a required developer_token key
        self.fs.create_file(
            file_path,
            contents=yaml.safe_dump(
                {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "refresh_token": self.refresh_token,
                    "use_proto_plus": self.use_proto_plus,
                }
            ),
        )

        self.assertRaises(ValueError, config.load_from_yaml_file)

    def test_load_from_yaml_file_missing_use_proto_plus_key(self):
        """Should raise ValueError if use_proto_plus key is missing."""
        file_path = os.path.join(os.path.expanduser("~"), "google-ads.yaml")
        # save a YAML file without a required use_proto_plus key
        self.fs.create_file(
            file_path,
            contents=yaml.safe_dump(
                {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "refresh_token": self.refresh_token,
                    "developer_token": self.developer_token,
                }
            ),
        )

        self.assertRaises(ValueError, config.load_from_yaml_file)

    def test_load_from_yaml_file_with_path(self):
        """Should load yaml file from a given path passed in directly."""
        custom_path = os.path.expanduser("/test/custom/path")
        file_path = os.path.join(custom_path, "google-ads.yaml")
        self._create_mock_yaml(
            {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self.refresh_token,
            },
            file_path=file_path,
        )

        result = config.load_from_yaml_file(path=file_path)

        self.assertEqual(result["developer_token"], self.developer_token)
        self.assertEqual(result["use_proto_plus"], self.use_proto_plus)
        self.assertEqual(result["client_id"], self.client_id)
        self.assertEqual(result["client_secret"], self.client_secret)
        self.assertEqual(result["refresh_token"], self.refresh_token)

    def test_load_from_yaml_file_from_env_var(self):
        """Should load yaml file from env var path if defined."""
        env_var_path = os.path.expanduser("/test/from/env/var")
        file_path = os.path.join(env_var_path, "google-ads.yaml")
        self._create_mock_yaml({}, file_path=file_path)

        environ = {"GOOGLE_ADS_CONFIGURATION_FILE_PATH": file_path}
        with mock.patch("os.environ", environ):
            result = config.load_from_yaml_file()
            self.assertEqual(result["developer_token"], self.developer_token)
            self.assertEqual(result["use_proto_plus"], self.use_proto_plus)

    def test_load_from_yaml_file_with_path_and_env_var(self):
        """Should load yaml file from passed-in path if both are defined."""
        env_var_path = os.path.join(
            os.path.expanduser("/test/from/env/var"), "google-ads.yaml"
        )
        passed_in_path = os.path.join(
            os.path.expanduser("/test/given/path"), "google-ads.yaml"
        )
        # Create yaml file in location defined by path passed to method
        self._create_mock_yaml(
            {"location": "passed in"}, file_path=passed_in_path
        )
        # Create yaml file in location defined by environment variable
        self._create_mock_yaml({"location": "env var"}, file_path=env_var_path)

        environ = {"GOOGLE_ADS_CONFIGURATION_FILE_PATH": env_var_path}
        with mock.patch("os.environ", environ):
            # Load config and check that it came from path passed to method
            result = config.load_from_yaml_file(path=passed_in_path)
            self.assertEqual(result["location"], "passed in")

    def test_load_from_yaml_file_login_cid_number(self):
        """Should load login_customer_id key if value is defined as a number."""
        login_cid_num = int(self.login_customer_id)
        self._create_mock_yaml({"login_customer_id": login_cid_num})

        result = config.load_from_yaml_file()

        self.assertEqual(result["login_customer_id"], self.login_customer_id)

    def test_load_from_yaml_file_linked_cid(self):
        """Should load liked_customer_id config from yaml."""
        self._create_mock_yaml({"linked_customer_id": self.linked_customer_id})

        result = config.load_from_yaml_file()

        self.assertEqual(result["linked_customer_id"], self.linked_customer_id)

    def test_load_from_yaml_file_secondary_service_account_keys(self):
        """Should convert secondary keys to primary keys.

        This test should be removed once the secondary service account keys
        are deprecated.
        """
        self._create_mock_yaml(
            {
                "path_to_private_key_file": self.json_key_file_path,
                "delegated_account": self.impersonated_email,
            }
        )

        result = config.load_from_yaml_file()

        self.assertEqual(result["json_key_file_path"], self.json_key_file_path)
        self.assertEqual(result["impersonated_email"], self.impersonated_email)

    def test_parse_yaml_document_to_dict(self):
        """Should parse configuration from a yaml string"""
        yaml_doc = f"""
            client_id: {self.client_id}\n
            client_secret: {self.client_secret}\n
            developer_token: {self.developer_token}\n
            use_proto_plus: {self.use_proto_plus}\n
            refresh_token: {self.refresh_token}\n
            """

        result = config.parse_yaml_document_to_dict(yaml_doc)

        self.assertEqual(result["developer_token"], self.developer_token)
        self.assertEqual(result["use_proto_plus"], self.use_proto_plus)
        self.assertEqual(result["client_id"], self.client_id)
        self.assertEqual(result["client_secret"], self.client_secret)
        self.assertEqual(result["refresh_token"], self.refresh_token)

    def test_parse_yaml_document_to_dict_missing_required_key(self):
        """Should raise ValueError if yaml string is missing a required key."""
        # YAML document is missing the required developer_token key
        yaml_doc = f"""
            client_id: {self.client_id}\n
            client_secret: {self.client_secret}\n
            use_proto_plus: {self.use_proto_plus}\n
            refresh_token: {self.refresh_token}\n
            """

        self.assertRaises(
            ValueError, config.parse_yaml_document_to_dict, yaml_doc
        )

    def test_load_from_dict(self):
        """Can load config from a dict."""
        config_data = {
            **self.default_dict_config,
            **{
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self.refresh_token,
            },
        }
        self.assertEqual(config.load_from_dict(config_data), config_data)

    def test_load_from_dict_logging(self):
        """Should load logging config from dict."""
        config_data = {
            **self.default_dict_config,
            **{
                "logging": {
                    "version": 1,
                    "disable_existing_loggers": False,
                    "formatters": {
                        "default_fmt": {
                            "format": "[%(asctime)s - %(levelname)s]",
                            "datefmt": "%Y-%m-%d %H:%M:%S",
                        }
                    },
                    "handlers": {
                        "default_handler": {
                            "class": "logging.StreamHandler",
                            "formatter": "default_fmt",
                        }
                    },
                    "loggers": {
                        "": {
                            "handlers": ["default_handler"],
                            "level": "DEBUG",
                        }
                    },
                },
            },
        }
        self.assertEqual(config.load_from_dict(config_data), config_data)

    def test_load_from_dict_secondary_service_account_keys(self):
        """Should convert secondary keys to primary keys."""
        config_data = {
            **self.default_dict_config,
            **{
                "path_to_private_key_file": self.json_key_file_path,
                "delegated_account": self.impersonated_email,
            },
        }

        result = config.load_from_dict(config_data)
        self.assertEqual(result["json_key_file_path"], self.json_key_file_path)
        self.assertEqual(result["impersonated_email"], self.impersonated_email)

    def test_load_from_dict_error(self):
        """Should raise ValueError if invalid dict is given."""
        config_data = 111
        self.assertRaises(ValueError, config.load_from_dict, config_data)

    @mock.patch.object(config, "_logger", mock.Mock())
    @mock.patch("logging.config.dictConfig")
    def test_load_from_env(self, config_spy):
        """Should load config from environment variables."""
        environ = {
            **self.default_env_var_config,
            **{
                "GOOGLE_ADS_CLIENT_ID": self.client_id,
                "GOOGLE_ADS_CLIENT_SECRET": self.client_secret,
                "GOOGLE_ADS_REFRESH_TOKEN": self.refresh_token,
                "GOOGLE_ADS_LOGGING": '{"test": true}',
                "GOOGLE_ADS_ENDPOINT": self.endpoint,
                "GOOGLE_ADS_LOGIN_CUSTOMER_ID": self.login_customer_id,
                "GOOGLE_ADS_LINKED_CUSTOMER_ID": self.linked_customer_id,
                "GOOGLE_ADS_LINKED_CUSTOMER_ID": self.linked_customer_id,
                "GOOGLE_ADS_JSON_KEY_FILE_PATH": self.json_key_file_path,
                "GOOGLE_ADS_IMPERSONATED_EMAIL": self.impersonated_email,
            },
        }

        with mock.patch("os.environ", environ):
            result = config.load_from_env()
            self.assertEqual(
                result,
                {
                    "developer_token": self.developer_token,
                    "use_proto_plus": self.use_proto_plus,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "refresh_token": self.refresh_token,
                    "logging": {"test": True},
                    "endpoint": self.endpoint,
                    "login_customer_id": self.login_customer_id,
                    "linked_customer_id": self.linked_customer_id,
                    "json_key_file_path": self.json_key_file_path,
                    "impersonated_email": self.impersonated_email,
                },
            )
            config_spy.assert_called_once()

    @mock.patch.object(config, "_logger", mock.Mock())
    def test_load_from_env_missing_required_key(self):
        """Should raise ValueError if missing required env var.."""
        # environ is missing required developer_token key
        environ = {
            "GOOGLE_ADS_CLIENT_ID": self.client_id,
            "GOOGLE_ADS_CLIENT_SECRET": self.client_secret,
            "GOOGLE_ADS_REFRESH_TOKEN": self.refresh_token,
            "GOOGLE_ADS_LOGGING": '{"test": true}',
            "GOOGLE_ADS_ENDPOINT": self.endpoint,
            "GOOGLE_ADS_LOGIN_CUSTOMER_ID": self.login_customer_id,
            "GOOGLE_ADS_JSON_KEY_FILE_PATH": self.json_key_file_path,
            "GOOGLE_ADS_IMPERSONATED_EMAIL": self.impersonated_email,
        }

        with mock.patch("os.environ", environ):
            self.assertRaises(ValueError, config.load_from_env)

    def test_load_from_env_config_file_path(self):
        """Should delegate to load_from_yaml_file method."""
        environ = {
            "GOOGLE_ADS_CONFIGURATION_FILE_PATH": self.configuration_file_path
        }

        with mock.patch("os.environ", environ):
            with mock.patch.object(
                config,
                "load_from_yaml_file",
                # Return basic config to pass validation.
                return_value=self.default_dict_config,
            ) as spy:
                config.load_from_env()
                spy.assert_called_once()

    def test_load_from_env_linked_cid(self):
        """Should load linked CID from environment when specified"""
        environ = {
            **self.default_env_var_config,
            **{
                "GOOGLE_ADS_LINKED_CUSTOMER_ID": self.linked_customer_id,
            },
        }

        with mock.patch("os.environ", environ):
            results = config.load_from_env()
            self.assertEqual(
                results["linked_customer_id"], self.linked_customer_id
            )

    def test_load_from_env_config_file_path_added_vars(self):
        """Should use config from yaml when config file path env var exists.

        If a configuration file path is defined via an environment variable
        then the yaml file at that location will be loaded and any other
        environment variable configuration will be ignored.
        """
        env_dev_token = "123456"
        environ = {
            **self.default_env_var_config,
            **{
                "GOOGLE_ADS_CONFIGURATION_FILE_PATH": self.configuration_file_path,
                "GOOGLE_ADS_DEVELOPER_TOKEN": env_dev_token,
            },
        }

        with mock.patch("os.environ", environ), mock.patch.object(
            # Mock load_from_yaml_file return value so it returns
            # a default dict config that passes validation
            config,
            "load_from_yaml_file",
            return_value=self.default_dict_config,
        ) as spy:
            # Assert that the config values were retrieved from the yaml
            # file and not from environment variables.
            result = config.load_from_env()
            self.assertEqual(result["developer_token"], self.developer_token)
            self.assertEqual(result["use_proto_plus"], self.use_proto_plus)

    @mock.patch.object(config, "_logger", mock.Mock())
    def test_load_from_env_redundant_file_path(self):
        """JSON_KEY_FILE_PATH takes precedent if both exist."""
        environ = {
            **self.default_env_var_config,
            # The two below variables represent the same key, and this test
            # checks that JSON_KEY_FILE_PATH takes precedent and overwrites
            # the path_to_private_key_file_path key in the returned dict.
            **{
                "GOOGLE_ADS_PATH_TO_PRIVATE_KEY_FILE": self.path_to_private_key_file,
                "GOOGLE_ADS_JSON_KEY_FILE_PATH": self.json_key_file_path,
            },
        }

        with mock.patch("os.environ", environ):
            result = config.load_from_env()
            self.assertEqual(
                result["json_key_file_path"], self.json_key_file_path
            )

    @mock.patch.object(config, "_logger", mock.Mock())
    def test_load_from_env_secondary_file_path(self):
        """JSON_KEY_FILE_PATH is used instead of secondary var name."""
        environ = {
            **self.default_env_var_config,
            **{
                "GOOGLE_ADS_PATH_TO_PRIVATE_KEY_FILE": self.path_to_private_key_file,
            },
        }

        with mock.patch("os.environ", environ):
            result = config.load_from_env()
            self.assertEqual(
                result["json_key_file_path"], self.path_to_private_key_file
            )

    @mock.patch.object(config, "_logger", mock.Mock())
    def test_load_from_env_redundant_delegated_email(self):
        """IMPERSONATED_EMAIL takes precedent if both exist."""
        environ = {
            **self.default_env_var_config,
            **{
                # The two below variables represent the same key, and this test
                # checks that IMPERSONATED_EMAIL takes precedent and overwrites
                # the delegate_account key in the returned dict.
                "GOOGLE_ADS_DELEGATED_ACCOUNT": self.delegated_account,
                "GOOGLE_ADS_IMPERSONATED_EMAIL": self.impersonated_email,
            },
        }

        with mock.patch("os.environ", environ):
            result = config.load_from_env()
            self.assertEqual(
                result["impersonated_email"], self.impersonated_email
            )

    @mock.patch.object(config, "_logger", mock.Mock())
    def test_load_from_env_secondary_delegated_email(self):
        """IMPERSONATED_EMAIL is used instead of secondary var name."""
        environ = {
            **self.default_env_var_config,
            **{
                "GOOGLE_ADS_DELEGATED_ACCOUNT": self.delegated_account,
            },
        }

        with mock.patch("os.environ", environ):
            result = config.load_from_env()
            self.assertEqual(
                result["impersonated_email"], self.delegated_account
            )

    def test_validate_dict(self):
        config_data = {"invalid": "config"}
        self.assertRaises(ValueError, config.validate_dict, config_data)

    def test_validate_dict(self):
        config_data = {key: "test" for key in config._REQUIRED_KEYS}
        try:
            config.validate_dict(config_data)
        except ValueError as ex:
            self.fail("test_validate_dict failed unexpectedly: {}".format(ex))

    def test_validate_dict_with_invalid_login_cid(self):
        config_data = {key: "test" for key in config._REQUIRED_KEYS}
        config_data["login_customer_id"] = "123-456-5789"
        self.assertRaises(ValueError, config.validate_dict, config_data)

    def test_validate_dict_with_invalid_linked_cid(self):
        config_data = {key: "test" for key in config._REQUIRED_KEYS}
        config_data["linked_customer_id"] = "123-456-5789"
        self.assertRaises(ValueError, config.validate_dict, config_data)

    def test_validate_dict_with_valid_login_cid(self):
        config_data = {key: "test" for key in config._REQUIRED_KEYS}
        config_data["login_customer_id"] = "1234567893"
        try:
            config.validate_dict(config_data)
        except ValueError as ex:
            self.fail(
                "test_validate_dict_with_login_cid failed unexpectedly: "
                "{}".format(ex)
            )

    def test_validate_dict_with_valid_linked_cid(self):
        config_data = {key: "test" for key in config._REQUIRED_KEYS}
        config_data["linked_customer_id"] = "1234567893"
        try:
            config.validate_dict(config_data)
        except ValueError as ex:
            self.fail(
                "test_validate_dict_with_linked_cid failed unexpectedly: "
                "{}".format(ex)
            )

    def test_validate_login_customer_id_invalid(self):
        self.assertRaises(
            ValueError, config.validate_login_customer_id, "123-456-7890"
        )

    def test_validate_login_customer_id_unicode(self):
        self.assertRaises(
            ValueError, config.validate_login_customer_id, "1230\u00B2"
        )

    def test_validate_login_customer_id_embedded(self):
        self.assertRaises(
            ValueError, config.validate_login_customer_id, "abc1234567890def"
        )

    def test_validate_login_customer_id_negative(self):
        self.assertRaises(
            ValueError, config.validate_login_customer_id, "-1234567890"
        )

    def test_validate_login_customer_id_too_short(self):
        self.assertRaises(ValueError, config.validate_login_customer_id, "123")

    def test_validate_linked_customer_id_too_short(self):
        self.assertRaises(ValueError, config.validate_linked_customer_id, "123")

    def test_get_oauth2_installed_app_keys(self):
        self.assertEqual(
            config.get_oauth2_installed_app_keys(),
            config._OAUTH2_INSTALLED_APP_KEYS,
        )

    def test_get_oauth2_service_account_keys(self):
        self.assertEqual(
            config.get_oauth2_service_account_keys(),
            config._OAUTH2_SERVICE_ACCOUNT_KEYS,
        )

    def test_convert_login_customer_id_to_str_with_int(self):
        config_data = {"login_customer_id": 1234567890}
        expected = {"login_customer_id": "1234567890"}
        self.assertEqual(
            config.convert_login_customer_id_to_str(config_data), expected
        )

    def test_parse_login_customer_id_with_str(self):
        config_data = {"login_customer_id": "1234567890"}
        self.assertEqual(
            config.convert_login_customer_id_to_str(config_data), config_data
        )

    def test_parse_login_customer_id_with_none(self):
        config_data = {"not_login_customer_id": 1234567890}
        self.assertEqual(
            config.convert_login_customer_id_to_str(config_data), config_data
        )

    def test_convert_linked_customer_id_to_str_with_int(self):
        config_data = {"linked_customer_id": 1234567890}
        expected = {"linked_customer_id": "1234567890"}
        self.assertEqual(
            config.convert_linked_customer_id_to_str(config_data), expected
        )

    def test_parse_linked_customer_id_with_str(self):
        config_data = {"linked_customer_id": "1234567890"}
        self.assertEqual(
            config.convert_linked_customer_id_to_str(config_data), config_data
        )

    def test_parse_linked_customer_id_with_none(self):
        config_data = {"not_linked_customer_id": 1234567890}
        self.assertEqual(
            config.convert_linked_customer_id_to_str(config_data), config_data
        )

    def test_disambiguate_string_bool(self):
        self.assertEqual(config.disambiguate_string_bool(True), True)

    def test_disambiguate_string_bool_with_str(self):
        self.assertEqual(config.disambiguate_string_bool("True"), True)

    def test_disambiguate_string_bool_raises_value_error(self):
        self.assertRaises(
            ValueError, config.disambiguate_string_bool, "invalid"
        )

    def test_disambiguate_string_bool_raises_type_error(self):
        self.assertRaises(TypeError, config.disambiguate_string_bool, {})
