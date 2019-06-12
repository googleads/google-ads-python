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

import os
import yaml

def load_from_yaml_file(path=None):
    """Creates a GoogleAdsClient with data stored in the specified file.

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
