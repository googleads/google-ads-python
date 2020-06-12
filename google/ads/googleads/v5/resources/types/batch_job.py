# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
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

import proto  # type: ignore


from google.ads.googleads.v5.enums.types import batch_job_status
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v5.resources",
    marshal="google.ads.googleads.v5",
    manifest={"BatchJob",},
)


class BatchJob(proto.Message):
    r"""A list of mutates being processed asynchronously. The mutates
    are uploaded by the user. The mutates themselves aren't readable
    and the results of the job can only be read using
    BatchJobService.ListBatchJobResults.

    Attributes:
        resource_name (str):
            Immutable. The resource name of the batch job. Batch job
            resource names have the form:

            ``customers/{customer_id}/batchJobs/{batch_job_id}``
        id (google.protobuf.wrappers_pb2.Int64Value):
            Output only. ID of this batch job.
        next_add_sequence_token (google.protobuf.wrappers_pb2.StringValue):
            Output only. The next sequence token to use
            when adding operations. Only set when the batch
            job status is PENDING.
        metadata (google.ads.googleads.v5.resources.types.BatchJob.BatchJobMetadata):
            Output only. Contains additional information
            about this batch job.
        status (google.ads.googleads.v5.enums.types.BatchJobStatusEnum.BatchJobStatus):
            Output only. Status of this batch job.
        long_running_operation (google.protobuf.wrappers_pb2.StringValue):
            Output only. The resource name of the long-
            unning operation that can be used to poll for
            completion. Only set when the batch job status
            is RUNNING or DONE.
    """

    class BatchJobMetadata(proto.Message):
        r"""Additional information about the batch job. This message is
        also used as metadata returned in batch job Long Running
        Operations.

        Attributes:
            creation_date_time (google.protobuf.wrappers_pb2.StringValue):
                Output only. The time when this batch job was
                created. Formatted as yyyy-mm-dd hh:mm:ss.
                Example: "2018-03-05 09:15:00".
            start_date_time (str):
                Output only. The time when this batch job
                started running. Formatted as yyyy-mm-dd
                hh:mm:ss. Example: "2018-03-05 09:15:30".
            completion_date_time (google.protobuf.wrappers_pb2.StringValue):
                Output only. The time when this batch job was
                completed. Formatted as yyyy-MM-dd HH:mm:ss.
                Example: "2018-03-05 09:16:00".
            estimated_completion_ratio (google.protobuf.wrappers_pb2.DoubleValue):
                Output only. The fraction (between 0.0 and
                1.0) of mutates that have been processed. This
                is empty if the job hasn't started running yet.
            operation_count (google.protobuf.wrappers_pb2.Int64Value):
                Output only. The number of mutate operations
                in the batch job.
            executed_operation_count (google.protobuf.wrappers_pb2.Int64Value):
                Output only. The number of mutate operations
                executed by the batch job. Present only if the
                job has started running.
        """

        creation_date_time = proto.Field(
            proto.MESSAGE, number=1, message=wrappers.StringValue,
        )
        start_date_time = proto.Field(proto.STRING, number=7, optional=True)
        completion_date_time = proto.Field(
            proto.MESSAGE, number=2, message=wrappers.StringValue,
        )
        estimated_completion_ratio = proto.Field(
            proto.MESSAGE, number=3, message=wrappers.DoubleValue,
        )
        operation_count = proto.Field(
            proto.MESSAGE, number=4, message=wrappers.Int64Value,
        )
        executed_operation_count = proto.Field(
            proto.MESSAGE, number=5, message=wrappers.Int64Value,
        )

    resource_name = proto.Field(proto.STRING, number=1)
    id = proto.Field(proto.MESSAGE, number=2, message=wrappers.Int64Value,)
    next_add_sequence_token = proto.Field(
        proto.MESSAGE, number=3, message=wrappers.StringValue,
    )
    metadata = proto.Field(proto.MESSAGE, number=4, message=BatchJobMetadata,)
    status = proto.Field(
        proto.ENUM,
        number=5,
        enum=batch_job_status.BatchJobStatusEnum.BatchJobStatus,
    )
    long_running_operation = proto.Field(
        proto.MESSAGE, number=6, message=wrappers.StringValue,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
