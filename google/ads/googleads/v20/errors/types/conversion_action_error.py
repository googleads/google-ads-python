# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
from __future__ import annotations


import proto  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v20.errors",
    marshal="google.ads.googleads.v20",
    manifest={
        "ConversionActionErrorEnum",
    },
)


class ConversionActionErrorEnum(proto.Message):
    r"""Container for enum describing possible conversion action
    errors.

    """

    class ConversionActionError(proto.Enum):
        r"""Enum describing possible conversion action errors.

        Values:
            UNSPECIFIED (0):
                Enum unspecified.
            UNKNOWN (1):
                The received error code is not known in this
                version.
            DUPLICATE_NAME (2):
                The specified conversion action name already
                exists.
            DUPLICATE_APP_ID (3):
                Another conversion action with the specified
                app id already exists.
            TWO_CONVERSION_ACTIONS_BIDDING_ON_SAME_APP_DOWNLOAD (4):
                Android first open action conflicts with
                Google play codeless download action tracking
                the same app.
            BIDDING_ON_SAME_APP_DOWNLOAD_AS_GLOBAL_ACTION (5):
                Android first open action conflicts with
                Google play codeless download action tracking
                the same app.
            DATA_DRIVEN_MODEL_WAS_NEVER_GENERATED (6):
                The attribution model cannot be set to DATA_DRIVEN because a
                data-driven model has never been generated.
            DATA_DRIVEN_MODEL_EXPIRED (7):
                The attribution model cannot be set to DATA_DRIVEN because
                the data-driven model is expired.
            DATA_DRIVEN_MODEL_STALE (8):
                The attribution model cannot be set to DATA_DRIVEN because
                the data-driven model is stale.
            DATA_DRIVEN_MODEL_UNKNOWN (9):
                The attribution model cannot be set to DATA_DRIVEN because
                the data-driven model is unavailable or the conversion
                action was newly added.
            CREATION_NOT_SUPPORTED (10):
                Creation of this conversion action type isn't
                supported by Google Ads API.
            UPDATE_NOT_SUPPORTED (11):
                Update of this conversion action isn't
                supported by Google Ads API.
            CANNOT_SET_RULE_BASED_ATTRIBUTION_MODELS (12):
                Rule-based attribution models are deprecated
                and not allowed to be set by conversion action.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        DUPLICATE_NAME = 2
        DUPLICATE_APP_ID = 3
        TWO_CONVERSION_ACTIONS_BIDDING_ON_SAME_APP_DOWNLOAD = 4
        BIDDING_ON_SAME_APP_DOWNLOAD_AS_GLOBAL_ACTION = 5
        DATA_DRIVEN_MODEL_WAS_NEVER_GENERATED = 6
        DATA_DRIVEN_MODEL_EXPIRED = 7
        DATA_DRIVEN_MODEL_STALE = 8
        DATA_DRIVEN_MODEL_UNKNOWN = 9
        CREATION_NOT_SUPPORTED = 10
        UPDATE_NOT_SUPPORTED = 11
        CANNOT_SET_RULE_BASED_ATTRIBUTION_MODELS = 12


__all__ = tuple(sorted(__protobuf__.manifest))
