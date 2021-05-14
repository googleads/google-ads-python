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

from google.ads.googleads.v7.common.types import offline_user_data
from google.ads.googleads.v7.enums.types import (
    offline_user_data_job_failure_reason,
)
from google.ads.googleads.v7.enums.types import offline_user_data_job_status
from google.ads.googleads.v7.enums.types import offline_user_data_job_type


__protobuf__ = proto.module(
    package="google.ads.googleads.v7.resources",
    marshal="google.ads.googleads.v7",
    manifest={"OfflineUserDataJob",},
)


class OfflineUserDataJob(proto.Message):
    r"""A job containing offline user data of store visitors, or user
    list members that will be processed asynchronously. The uploaded
    data isn't readable and the processing results of the job can
    only be read using
    OfflineUserDataJobService.GetOfflineUserDataJob.

    Attributes:
        resource_name (str):
            Immutable. The resource name of the offline user data job.
            Offline user data job resource names have the form:

            ``customers/{customer_id}/offlineUserDataJobs/{offline_user_data_job_id}``
        id (int):
            Output only. ID of this offline user data
            job.
        external_id (int):
            Immutable. User specified job ID.
        type_ (google.ads.googleads.v7.enums.types.OfflineUserDataJobTypeEnum.OfflineUserDataJobType):
            Immutable. Type of the job.
        status (google.ads.googleads.v7.enums.types.OfflineUserDataJobStatusEnum.OfflineUserDataJobStatus):
            Output only. Status of the job.
        failure_reason (google.ads.googleads.v7.enums.types.OfflineUserDataJobFailureReasonEnum.OfflineUserDataJobFailureReason):
            Output only. Reason for the processing
            failure, if status is FAILED.
        customer_match_user_list_metadata (google.ads.googleads.v7.common.types.CustomerMatchUserListMetadata):
            Immutable. Metadata for data updates to a
            CRM-based user list.
        store_sales_metadata (google.ads.googleads.v7.common.types.StoreSalesMetadata):
            Immutable. Metadata for store sales data
            update.
    """

    resource_name = proto.Field(proto.STRING, number=1,)
    id = proto.Field(proto.INT64, number=9, optional=True,)
    external_id = proto.Field(proto.INT64, number=10, optional=True,)
    type_ = proto.Field(
        proto.ENUM,
        number=4,
        enum=offline_user_data_job_type.OfflineUserDataJobTypeEnum.OfflineUserDataJobType,
    )
    status = proto.Field(
        proto.ENUM,
        number=5,
        enum=offline_user_data_job_status.OfflineUserDataJobStatusEnum.OfflineUserDataJobStatus,
    )
    failure_reason = proto.Field(
        proto.ENUM,
        number=6,
        enum=offline_user_data_job_failure_reason.OfflineUserDataJobFailureReasonEnum.OfflineUserDataJobFailureReason,
    )
    customer_match_user_list_metadata = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="metadata",
        message=offline_user_data.CustomerMatchUserListMetadata,
    )
    store_sales_metadata = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="metadata",
        message=offline_user_data.StoreSalesMetadata,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
