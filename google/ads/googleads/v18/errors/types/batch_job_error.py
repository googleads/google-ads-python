# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
    package="google.ads.googleads.v18.errors",
    marshal="google.ads.googleads.v18",
    manifest={
        "BatchJobErrorEnum",
    },
)


class BatchJobErrorEnum(proto.Message):
    r"""Container for enum describing possible batch job errors."""

    class BatchJobError(proto.Enum):
        r"""Enum describing possible request errors.

        Values:
            UNSPECIFIED (0):
                Enum unspecified.
            UNKNOWN (1):
                The received error code is not known in this
                version.
            CANNOT_MODIFY_JOB_AFTER_JOB_STARTS_RUNNING (2):
                The batch job cannot add more operations or
                run after it has started running.
            EMPTY_OPERATIONS (3):
                The operations for an AddBatchJobOperations
                request were empty.
            INVALID_SEQUENCE_TOKEN (4):
                The sequence token for an
                AddBatchJobOperations request was invalid.
            RESULTS_NOT_READY (5):
                Batch job results can only be retrieved once
                the job is finished.
            INVALID_PAGE_SIZE (6):
                The page size for ListBatchJobResults was
                invalid.
            CAN_ONLY_REMOVE_PENDING_JOB (7):
                The batch job cannot be removed because it
                has started running.
            CANNOT_LIST_RESULTS (8):
                The batch job cannot be listed due to
                unexpected errors such as duplicate checkpoints.
            ASSET_GROUP_AND_ASSET_GROUP_ASSET_TRANSACTION_FAILURE (9):
                The request contains interdependent
                AssetGroup and AssetGroupAsset operations that
                are treated atomically as a single transaction,
                and one or more of the operations in that
                transaction failed, which caused the entire
                transaction, and therefore this mutate
                operation, to fail. The operations that caused
                the transaction to fail can be found in the
                consecutive AssetGroup or AssetGroupAsset
                results with the same asset group id. The mutate
                operation will be successful once the remaining
                errors in the transaction are fixed.
            ASSET_GROUP_LISTING_GROUP_FILTER_TRANSACTION_FAILURE (10):
                The request contains interdependent
                AssetGroupListingGroupFilter operations that are
                treated atomically as a single transaction, and
                one or more of the operations in that
                transaction failed, which caused the entire
                transaction, and therefore this mutate
                operation, to fail. The operations that caused
                the transaction to fail can be found in the
                consecutive AssetGroupListingGroupFilter results
                with the same asset group id. The mutate
                operation will be successful once the remaining
                errors in the transaction are fixed.
            REQUEST_TOO_LARGE (11):
                The AddBatchJobOperationsRequest is too
                large. Split the request into smaller requests.
                The maximum allowed request size is 10484504
                bytes.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        CANNOT_MODIFY_JOB_AFTER_JOB_STARTS_RUNNING = 2
        EMPTY_OPERATIONS = 3
        INVALID_SEQUENCE_TOKEN = 4
        RESULTS_NOT_READY = 5
        INVALID_PAGE_SIZE = 6
        CAN_ONLY_REMOVE_PENDING_JOB = 7
        CANNOT_LIST_RESULTS = 8
        ASSET_GROUP_AND_ASSET_GROUP_ASSET_TRANSACTION_FAILURE = 9
        ASSET_GROUP_LISTING_GROUP_FILTER_TRANSACTION_FAILURE = 10
        REQUEST_TOO_LARGE = 11


__all__ = tuple(sorted(__protobuf__.manifest))
