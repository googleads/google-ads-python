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
    package="google.ads.googleads.v22.errors",
    marshal="google.ads.googleads.v22",
    manifest={
        "AssetGenerationErrorEnum",
    },
)


class AssetGenerationErrorEnum(proto.Message):
    r"""Container for enum describing GenAI asset generation errors."""

    class AssetGenerationError(proto.Enum):
        r"""Enum describing GenAI asset generation errors.

        Values:
            UNSPECIFIED (0):
                Enum unspecified.
            UNKNOWN (1):
                The received error code is not known in this
                version.
            NO_ASSETS_GENERATED (2):
                No assets were generated for the given
                request.
            FINAL_URL_REQUIRED (3):
                A final URL is required but was not provided,
                and could not be sourced from the existing
                generation context because no existing
                generation context was provided.
            GENERATION_CONTEXT_MISSING_FINAL_URL (4):
                A final URL is required but was not provided,
                and could not be sourced from the provided
                existing generation context.
            FINAL_URL_SENSITIVE (5):
                The provided final URL is considered
                sensitive, and assets cannot be generated.
            FINAL_URL_UNSUPPORTED_LANGUAGE (6):
                The language of the provided final URL is not
                supported.
            FINAL_URL_UNAVAILABLE (7):
                The provided final URL was not indexed or
                could otherwise not be processed.
            CAMPAIGN_TYPE_REQUIRED (8):
                Campaign type is required but was not
                provided, and could not be sourced from the
                existing generation context because no existing
                generation context was provided.
            UNSUPPORTED_CAMPAIGN_TYPE (9):
                The provided campaign type is not supported
                for this asset generation operation.
            UNSUPPORTED_FIELD_TYPE (10):
                The provided field type is not supported for
                this asset generation operation.
            UNSUPPORTED_FIELD_TYPE_FOR_CAMPAIGN_TYPE (11):
                The provided field type is not supported for
                the given campaign type.
            FREEFORM_PROMPT_UNSUPPORTED_LANGUAGE (12):
                The language of the provided freeform prompt
                is not supported.
            FREEFORM_PROMPT_SENSITIVE (13):
                The provided freeform prompt is considered
                sensitive, and assets cannot be generated.
            INPUT_IMAGE_FILE_SIZE_TOO_LARGE (14):
                The provided image file size exceeds the
                limit.
            INPUT_IMAGE_EMPTY (15):
                The provided image is empty.
            GENERATION_TYPE_REQUIRED (16):
                Exactly one generation type must be provided.
            TOO_MANY_KEYWORDS (17):
                Too many keywords provided in request.
            KEYWORD_INVALID_LENGTH (18):
                A provided keyword does not have a valid
                length.
            NO_VALID_KEYWORDS (19):
                All keywords were filtered out.
            FREEFORM_PROMPT_INVALID_LENGTH (20):
                The provided freeform prompt does not have a
                valid length.
            FREEFORM_PROMPT_REFERENCES_CHILDREN (21):
                The provided freeform prompt references
                children.
            FREEFORM_PROMPT_REFERENCES_SPECIFIC_PEOPLE (22):
                The provided freeform prompt references
                specific people.
            FREEFORM_PROMPT_VIOLATES_ADS_POLICY (23):
                The provided freeform prompt violates Ads
                Policy.
            FREEFORM_PROMPT_BRAND_CONTENT (24):
                The provided freeform prompt contains brand
                content.
            INPUT_IMAGE_DEPICTS_CHILDREN (25):
                The provided image depicts children.
            INPUT_IMAGE_CONTAINS_BRAND_CONTENT (26):
                The provided image contains brand content.
            INPUT_IMAGE_SENSITIVE (27):
                The provided image contains sensitive subject
                matter.
            INPUT_IMAGE_VIOLATES_POLICY (28):
                The provided image may violate Google Ads
                policies.
            ALL_OUTPUT_IMAGES_FILTERED_OUT_CHILDREN_DEPICTION (29):
                All output images were filtered out because
                they included depictions of children.
            ALL_OUTPUT_IMAGES_FILTERED_OUT_SPECIFIC_PEOPLE (30):
                All output images were filtered out because
                they included depictions of specific people.
            ALL_OUTPUT_IMAGES_FILTERED_OUT (31):
                All output images were filtered out for a
                reason not covered by a more specific error
                code.
            INPUT_IMAGE_REQUIRED (32):
                At least one input image is required for
                certain requests.
            INPUT_IMAGE_UNSUPPORTED_IMAGE_TYPE (33):
                The provided image is of an unsupported type.
            CONTEXT_ASSET_GROUP_NOT_FOUND (34):
                Asset Group could not be found with the
                provided ID.
            CONTEXT_AD_GROUP_AD_NOT_FOUND (35):
                Ad Group Ad could not be found with the
                provided ID combination.
            CONTEXT_CAMPAIGN_NOT_FOUND (36):
                Could not find Campaign associated with the
                provided generation context.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        NO_ASSETS_GENERATED = 2
        FINAL_URL_REQUIRED = 3
        GENERATION_CONTEXT_MISSING_FINAL_URL = 4
        FINAL_URL_SENSITIVE = 5
        FINAL_URL_UNSUPPORTED_LANGUAGE = 6
        FINAL_URL_UNAVAILABLE = 7
        CAMPAIGN_TYPE_REQUIRED = 8
        UNSUPPORTED_CAMPAIGN_TYPE = 9
        UNSUPPORTED_FIELD_TYPE = 10
        UNSUPPORTED_FIELD_TYPE_FOR_CAMPAIGN_TYPE = 11
        FREEFORM_PROMPT_UNSUPPORTED_LANGUAGE = 12
        FREEFORM_PROMPT_SENSITIVE = 13
        INPUT_IMAGE_FILE_SIZE_TOO_LARGE = 14
        INPUT_IMAGE_EMPTY = 15
        GENERATION_TYPE_REQUIRED = 16
        TOO_MANY_KEYWORDS = 17
        KEYWORD_INVALID_LENGTH = 18
        NO_VALID_KEYWORDS = 19
        FREEFORM_PROMPT_INVALID_LENGTH = 20
        FREEFORM_PROMPT_REFERENCES_CHILDREN = 21
        FREEFORM_PROMPT_REFERENCES_SPECIFIC_PEOPLE = 22
        FREEFORM_PROMPT_VIOLATES_ADS_POLICY = 23
        FREEFORM_PROMPT_BRAND_CONTENT = 24
        INPUT_IMAGE_DEPICTS_CHILDREN = 25
        INPUT_IMAGE_CONTAINS_BRAND_CONTENT = 26
        INPUT_IMAGE_SENSITIVE = 27
        INPUT_IMAGE_VIOLATES_POLICY = 28
        ALL_OUTPUT_IMAGES_FILTERED_OUT_CHILDREN_DEPICTION = 29
        ALL_OUTPUT_IMAGES_FILTERED_OUT_SPECIFIC_PEOPLE = 30
        ALL_OUTPUT_IMAGES_FILTERED_OUT = 31
        INPUT_IMAGE_REQUIRED = 32
        INPUT_IMAGE_UNSUPPORTED_IMAGE_TYPE = 33
        CONTEXT_ASSET_GROUP_NOT_FOUND = 34
        CONTEXT_AD_GROUP_AD_NOT_FOUND = 35
        CONTEXT_CAMPAIGN_NOT_FOUND = 36


__all__ = tuple(sorted(__protobuf__.manifest))
