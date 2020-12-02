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

import functools
import json
import logging.config
import os
import yaml


_logger = logging.getLogger(__name__)

_ENV_PREFIX = "GOOGLE_ADS_"
_REQUIRED_KEYS = ("developer_token",)
_OPTIONAL_KEYS = (
    "login_customer_id",
    "endpoint",
    "logging",
    "configuration_file_path",
)
_OAUTH2_INSTALLED_APP_KEYS = ("client_id", "client_secret", "refresh_token")
_OAUTH2_SERVICE_ACCOUNT_KEYS = ("path_to_private_key_file", "delegated_account")
# These keys are additional environment variables that can be used to specify
# some of the above configuration values.
_REDUNDANT_KEYS = ("json_key_file_path", "impersonated_email")
_KEYS_ENV_VARIABLES_MAP = {
    key: _ENV_PREFIX + key.upper()
    for key in list(_REQUIRED_KEYS)
    + list(_OPTIONAL_KEYS)
    + list(_OAUTH2_INSTALLED_APP_KEYS)
    + list(_OAUTH2_SERVICE_ACCOUNT_KEYS)
    + list(_REDUNDANT_KEYS)
}


def _config_validation_decorator(func):
    """A decorator used to easily run validations on configs loaded into dicts.

    Add this decorator to any method that returns the config as a dict.

    Raises:
        ValueError: If the configuration fails validation
    """

    @functools.wraps(func)
    def validation_wrapper(*args, **kwargs):
        config_dict = func(*args, **kwargs)
        validate_dict(config_dict)
        return config_dict

    return validation_wrapper


def _config_parser_decorator(func):
    """A decorator used to easily parse config values.

    Since configs can be loaded from different locations such as env vars or
    from YAML files it's possible that they may have inconsistent types that
    need to be parsed to a different type. Add this decorator to any method
    that returns the config as a dict.
    """

    @functools.wraps(func)
    def parser_wrapper(*args, **kwargs):
        config_dict = func(*args, **kwargs)
        parsed_config = convert_login_customer_id_to_str(config_dict)
        return parsed_config

    return parser_wrapper


def validate_dict(config_data):
    """Validates the given configuration dict.

    Validations that are performed include:
        1. Ensuring all required keys are present.
        2. If a login_customer_id is present ensure it's valid

    Args:
        config_data: a dict with configuration data.

    Raises:
        ValueError: If the dict does not contain all required config keys.
    """
    if not all(key in config_data for key in _REQUIRED_KEYS):
        raise ValueError(
            "A required field in the configuration data was not "
            "found. The required fields are: {}".format(str(_REQUIRED_KEYS))
        )

    if "login_customer_id" in config_data:
        validate_login_customer_id(config_data["login_customer_id"])


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
            raise ValueError(
                "The specified login customer ID is invalid. "
                "It must be a ten digit number represented "
                'as a string, i.e. "1234567890"'
            )


@_config_validation_decorator
@_config_parser_decorator
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
        path = os.path.join(os.path.expanduser("~"), "google-ads.yaml")

    if not os.path.isabs(path):
        path = os.path.expanduser(path)

    with open(path, "rb") as handle:
        yaml_doc = handle.read()

    return parse_yaml_document_to_dict(yaml_doc)


@_config_validation_decorator
@_config_parser_decorator
def load_from_dict(config_dict):
    """Check if the argument is dictionary or not. If successful it calls the parsing decorator,
    followed by validation decorator. This validates the keys used in the config_dict, before
    returning to its caller.

    Args:
        config_dict: a dict containing client configuration.

    Returns:
        The same input dictionary that is passed into the function.

    Raises:
        A value error if the argument (config_dict) is not a dict.
    """
    if isinstance(config_dict, dict):
        return config_dict
    else:
        raise ValueError(
            "The configuration object passed to function load_from_dict must be of type dict."
        )


@_config_validation_decorator
@_config_parser_decorator
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


@_config_validation_decorator
@_config_parser_decorator
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

    specified_variable_names = config_data.keys()

    # If configuration_file_path is set by the environment then configuration
    # is retrieved from the yaml file specified in the given path.
    if "configuration_file_path" in specified_variable_names:
        return load_from_yaml_file(config_data["configuration_file_path"])

    if "logging" in specified_variable_names:
        try:
            config_data["logging"] = json.loads(config_data["logging"])
            logging.config.dictConfig(config_data["logging"])
        except json.JSONDecodeError:
            raise ValueError(
                "GOOGLE_ADS_LOGGING env variable should be in JSON format."
            )

    if "path_to_private_key_file" in specified_variable_names:
        _logger.warning(
            "The 'GOOGLE_ADS_PATH_TO_PRIVATE_KEY_FILE' environment "
            "variable is deprecated. Please use "
            "'GOOGLE_ADS_JSON_KEY_FILE_PATH' instead."
        )

    if "delegated_account" in specified_variable_names:
        _logger.warning(
            "The 'GOOGLE_ADS_DELEGATED_ACCOUNT' environment "
            "variable is deprecated. Please use "
            "'GOOGLE_ADS_IMPERSONATED_EMAIL' instead."
        )

    # json_key_file_path is an alternate key that can be used in place of
    # path_to_private_key_file. It will always override the latter, but the
    # name will persist for compatibility purposes.
    if "json_key_file_path" in specified_variable_names:
        config_data["path_to_private_key_file"] = config_data[
            "json_key_file_path"
        ]
        del config_data["json_key_file_path"]

    # impersonated_email is an alternate key that can be used in placed of
    # delegated_account. It will always override the latter, but the name will
    # persist for compatibility purposes.
    if "impersonated_email" in specified_variable_names:
        config_data["delegated_account"] = config_data["impersonated_email"]
        del config_data["impersonated_email"]

    return config_data


def get_oauth2_installed_app_keys():
    """A getter that returns the required OAuth2 installed application keys.

    Returns:
        A tuple containing the required keys as strs.
    """
    return _OAUTH2_INSTALLED_APP_KEYS


def get_oauth2_service_account_keys():
    """A getter that returns the required OAuth2 service account keys.

    Returns:
        A tuple containing the required keys as strs.
    """
    return _OAUTH2_SERVICE_ACCOUNT_KEYS


def convert_login_customer_id_to_str(config_data):
    """Parses a config dict's login_customer_id attr value to a str.

    Like many values from YAML it's possible for login_customer_id to
    either be a str or an int. Since we actually run validations on this
    value before making requests it's important to parse it to a str.

    Args:
        config_data: A config dict object.

    Returns:
        The same config dict object with a mutated login_customer_id attr.
    """
    login_customer_id = config_data.get("login_customer_id")

    if login_customer_id:
        config_data["login_customer_id"] = str(login_customer_id)

    return config_data
