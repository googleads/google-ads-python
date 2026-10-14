# -*- coding: utf-8 -*-
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.ads.googleads.v26 import gapic_version as package_version

import google.api_core as api_core

__version__ = package_version.__version__

# PEP 0810: Explicit Lazy Imports
# Python 3.15+ natively intercepts and defers these imports.
# Developers can disable this behavior and force eager imports.
# For more information, see:
# https://docs.python.org/3.15/library/sys.html#sys.set_lazy_imports_filter
# Older Python versions safely ignore this variable.
__lazy_modules__ = {
    "google.ads.googleads.v26.actions",
    "google.ads.googleads.v26.common",
    "google.ads.googleads.v26.enums",
    "google.ads.googleads.v26.errors",
    "google.ads.googleads.v26.resources",
    "google.ads.googleads.v26.services",
}

from . import actions
from . import common
from . import enums
from . import errors
from . import resources
from . import services


__all__ = (
    "actions",
    "common",
    "enums",
    "errors",
    "resources",
    "services",
)

api_core.check_python_version("google.ads.googleads.v26")
api_core.check_dependency_versions("google.ads.googleads.v26")
