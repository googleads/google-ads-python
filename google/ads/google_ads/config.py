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
"""A set of functions to help load configuration from various locations."""

import json
import os
import yaml

_ENV_PREFIX = 'GOOGLE_ADS_'
_REQUIRED_KEYS = ('developer_token',)
_OPTIONAL_KEYS = ('login_customer_id', 'endpoint', 'logging')
_OAUTH2_INSTALLED_APP_KEYS = ('client_id', 'client_secret', 'refresh_token')
_OAUTH2_SERVICE_ACCOUNT_KEYS = ('path_to_private_key_file', 'delegated_account')
_KEYS_ENV_VARIABLES_MAP = {
    key: _ENV_PREFIX + key.upper() for key in
    list(_REQUIRED_KEYS) +
    list(_OPTIONAL_KEYS) +
    list(_OAUTH2_INSTALLED_APP_KEYS) +
    list(_OAUTH2_SERVICE_ACCOUNT_KEYS)}
_MISSING_CONFIG_ERROR_MESSAGE = ('A required field in the configuration data '
                                 'was not found. The required fields are: {}'
                                 ''.format(str(_REQUIRED_KEYS)))

def load_from_yaml_file(path=None):
    """Loads configuration data from a YAML file and returns it as a dict.

    Args:
        path: a str indicating the path to a YAML file containing
            configuration data used to initialize a GoogleAdsClient.

    Returns:
        A dict with configuration from the specified YAML file.

    Raises:
        FileNotFoundError: If the specified configuration file doesn't exist.
        IOError: If the configuration file can't be loaded.
    """
    if path is None:
        path = os.path.join(os.path.expanduser('~'), 'google-ads.yaml')

    if not os.path.isabs(path):
        path = os.path.expanduser(path)

    with open(path, 'rb') as handle:
        yaml_doc = handle.read()

    return parse_yaml_document_to_dict(yaml_doc)


def parse_yaml_document_to_dict(yaml_doc):
    """Parses a YAML document to a dict.

    Args:
        yaml_doc: a str (in Python 2) or bytes (in Python 3) containing YAML
            configuration data.

    Returns:
        A dict of the key/value pairs from the given YAML document.

    Raises:
        yaml.YAMLError: If there is a problem parsing the YAML document.
    """
    return yaml.safe_load(yaml_doc) or {}


def load_from_env():
    """Loads configuration data from the environment and returns it as a dict.

    Returns:
        A dict with configuration from the environment.

    Raises:
        ValueError: If the configuration
    """
    config_data = {
        key: os.environ[env_variable]
        for key, env_variable in _KEYS_ENV_VARIABLES_MAP.items()
        if env_variable in os.environ
    }
    if 'logging' in config_data.keys():
        try:
            config_data['logging'] = json.loads(config_data['logging'])
        except json.JSONDecodeError:
            raise ValueError(
                'GOOGLE_ADS_LOGGING env variable should be in JSON format.')

    return config_data


def validate_dict(config_data,
                  required_keys_error_message=_MISSING_CONFIG_ERROR_MESSAGE):
    """Validates the given configuration dict.

    Validations that are performed include:
        1. Ensuring all required keys are present.
        2. If a login_customer_id is present ensure it's valid

    Args:
        config_data: a dict with configuration data.
        required_keys_error_message: an optional error message str to raise if
            the given config does not contain all required keys. This is
            configurable so that error messages can be more specific since key
            names may vary depending on where config values are retrieved. For
            example "client_id" is "GOOGLE_ADS_CLIENT_ID" when retrieved from
            env.

    Raises:
        ValueError: If the dict does not contain all required config keys.
    """
    if not all(key in config_data for key in _REQUIRED_KEYS):
        raise ValueError(required_keys_error_message)

    if 'login_customer_id' in config_data:
        validate_login_customer_id(config_data['login_customer_id'])


def validate_login_customer_id(login_customer_id):
    """Validates a login customer ID.

    Args:
        login_customer_id: a str from config indicating a login customer ID.

    Raises:
        ValueError: If the login customer ID is not an int in the
            range 0 - 9999999999.
    """
    if login_customer_id is not None:
        if not login_customer_id.isdigit() or len(login_customer_id) != 10:
            raise ValueError('The specified login customer ID is invalid. '
                             'It must be a ten digit number represented '
                             'as a string, i.e. "1234567890"')