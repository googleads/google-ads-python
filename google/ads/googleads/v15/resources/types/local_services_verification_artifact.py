# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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

from google.ads.googleads.v15.common.types import local_services
from google.ads.googleads.v15.enums.types import (
    local_services_insurance_rejection_reason,
)
from google.ads.googleads.v15.enums.types import (
    local_services_license_rejection_reason,
)
from google.ads.googleads.v15.enums.types import (
    local_services_verification_artifact_status,
)
from google.ads.googleads.v15.enums.types import (
    local_services_verification_artifact_type,
)


__protobuf__ = proto.module(
    package="google.ads.googleads.v15.resources",
    marshal="google.ads.googleads.v15",
    manifest={
        "LocalServicesVerificationArtifact",
        "BackgroundCheckVerificationArtifact",
        "InsuranceVerificationArtifact",
        "LicenseVerificationArtifact",
    },
)


class LocalServicesVerificationArtifact(proto.Message):
    r"""A local services verification resource.
    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        resource_name (str):
            Immutable. The resource name of the Local Services
            Verification. Local Services Verification resource names
            have the form:

            ``customers/{customer_id}/localServicesVerificationArtifacts/{verification_artifact_id}``
        id (int):
            Output only. The ID of the verification
            artifact.

            This field is a member of `oneof`_ ``_id``.
        creation_date_time (str):
            Output only. The timestamp when this
            verification artifact was created. The format is
            "YYYY-MM-DD HH:MM:SS" in the Google Ads
            account's timezone. Examples: "2018-03-05
            09:15:00" or "2018-02-01 14:34:30".
        status (google.ads.googleads.v15.enums.types.LocalServicesVerificationArtifactStatusEnum.LocalServicesVerificationArtifactStatus):
            Output only. The status of the verification
            artifact.
        artifact_type (google.ads.googleads.v15.enums.types.LocalServicesVerificationArtifactTypeEnum.LocalServicesVerificationArtifactType):
            Output only. The type of the verification
            artifact.
        background_check_verification_artifact (google.ads.googleads.v15.resources.types.BackgroundCheckVerificationArtifact):
            Output only. A background check verification
            artifact.

            This field is a member of `oneof`_ ``artifact_data``.
        insurance_verification_artifact (google.ads.googleads.v15.resources.types.InsuranceVerificationArtifact):
            Output only. An insurance verification
            artifact.

            This field is a member of `oneof`_ ``artifact_data``.
        license_verification_artifact (google.ads.googleads.v15.resources.types.LicenseVerificationArtifact):
            Output only. A license verification artifact.

            This field is a member of `oneof`_ ``artifact_data``.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    id: int = proto.Field(
        proto.INT64,
        number=2,
        optional=True,
    )
    creation_date_time: str = proto.Field(
        proto.STRING,
        number=3,
    )
    status: local_services_verification_artifact_status.LocalServicesVerificationArtifactStatusEnum.LocalServicesVerificationArtifactStatus = proto.Field(
        proto.ENUM,
        number=4,
        enum=local_services_verification_artifact_status.LocalServicesVerificationArtifactStatusEnum.LocalServicesVerificationArtifactStatus,
    )
    artifact_type: local_services_verification_artifact_type.LocalServicesVerificationArtifactTypeEnum.LocalServicesVerificationArtifactType = proto.Field(
        proto.ENUM,
        number=5,
        enum=local_services_verification_artifact_type.LocalServicesVerificationArtifactTypeEnum.LocalServicesVerificationArtifactType,
    )
    background_check_verification_artifact: "BackgroundCheckVerificationArtifact" = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="artifact_data",
        message="BackgroundCheckVerificationArtifact",
    )
    insurance_verification_artifact: "InsuranceVerificationArtifact" = (
        proto.Field(
            proto.MESSAGE,
            number=7,
            oneof="artifact_data",
            message="InsuranceVerificationArtifact",
        )
    )
    license_verification_artifact: "LicenseVerificationArtifact" = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="artifact_data",
        message="LicenseVerificationArtifact",
    )


class BackgroundCheckVerificationArtifact(proto.Message):
    r"""A proto holding information specific to local services
    background check.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        case_url (str):
            Output only. URL to access background case.

            This field is a member of `oneof`_ ``_case_url``.
        final_adjudication_date_time (str):
            Output only. The timestamp when this
            background check case result was adjudicated.
            The format is "YYYY-MM-DD HH:MM:SS" in the
            Google Ads account's timezone. Examples:
            "2018-03-05 09:15:00" or "2018-02-01 14:34:30".

            This field is a member of `oneof`_ ``_final_adjudication_date_time``.
    """

    case_url: str = proto.Field(
        proto.STRING,
        number=1,
        optional=True,
    )
    final_adjudication_date_time: str = proto.Field(
        proto.STRING,
        number=2,
        optional=True,
    )


class InsuranceVerificationArtifact(proto.Message):
    r"""A proto holding information specific to a local services
    insurance.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        amount_micros (int):
            Output only. Insurance amount. This is
            measured in "micros" of the currency mentioned
            in the insurance document.

            This field is a member of `oneof`_ ``_amount_micros``.
        rejection_reason (google.ads.googleads.v15.enums.types.LocalServicesInsuranceRejectionReasonEnum.LocalServicesInsuranceRejectionReason):
            Output only. Insurance document's rejection
            reason.

            This field is a member of `oneof`_ ``_rejection_reason``.
        insurance_document_readonly (google.ads.googleads.v15.common.types.LocalServicesDocumentReadOnly):
            Output only. The readonly field containing
            the information for an uploaded insurance
            document.

            This field is a member of `oneof`_ ``_insurance_document_readonly``.
    """

    amount_micros: int = proto.Field(
        proto.INT64,
        number=1,
        optional=True,
    )
    rejection_reason: local_services_insurance_rejection_reason.LocalServicesInsuranceRejectionReasonEnum.LocalServicesInsuranceRejectionReason = proto.Field(
        proto.ENUM,
        number=2,
        optional=True,
        enum=local_services_insurance_rejection_reason.LocalServicesInsuranceRejectionReasonEnum.LocalServicesInsuranceRejectionReason,
    )
    insurance_document_readonly: local_services.LocalServicesDocumentReadOnly = proto.Field(
        proto.MESSAGE,
        number=3,
        optional=True,
        message=local_services.LocalServicesDocumentReadOnly,
    )


class LicenseVerificationArtifact(proto.Message):
    r"""A proto holding information specific to a local services
    license.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        license_type (str):
            Output only. License type / name.

            This field is a member of `oneof`_ ``_license_type``.
        license_number (str):
            Output only. License number.

            This field is a member of `oneof`_ ``_license_number``.
        licensee_first_name (str):
            Output only. First name of the licensee.

            This field is a member of `oneof`_ ``_licensee_first_name``.
        licensee_last_name (str):
            Output only. Last name of the licensee.

            This field is a member of `oneof`_ ``_licensee_last_name``.
        rejection_reason (google.ads.googleads.v15.enums.types.LocalServicesLicenseRejectionReasonEnum.LocalServicesLicenseRejectionReason):
            Output only. License rejection reason.

            This field is a member of `oneof`_ ``_rejection_reason``.
        license_document_readonly (google.ads.googleads.v15.common.types.LocalServicesDocumentReadOnly):
            Output only. The readonly field containing
            the information for an uploaded license
            document.

            This field is a member of `oneof`_ ``_license_document_readonly``.
    """

    license_type: str = proto.Field(
        proto.STRING,
        number=1,
        optional=True,
    )
    license_number: str = proto.Field(
        proto.STRING,
        number=2,
        optional=True,
    )
    licensee_first_name: str = proto.Field(
        proto.STRING,
        number=3,
        optional=True,
    )
    licensee_last_name: str = proto.Field(
        proto.STRING,
        number=4,
        optional=True,
    )
    rejection_reason: local_services_license_rejection_reason.LocalServicesLicenseRejectionReasonEnum.LocalServicesLicenseRejectionReason = proto.Field(
        proto.ENUM,
        number=5,
        optional=True,
        enum=local_services_license_rejection_reason.LocalServicesLicenseRejectionReasonEnum.LocalServicesLicenseRejectionReason,
    )
    license_document_readonly: local_services.LocalServicesDocumentReadOnly = (
        proto.Field(
            proto.MESSAGE,
            number=6,
            optional=True,
            message=local_services.LocalServicesDocumentReadOnly,
        )
    )


__all__ = tuple(sorted(__protobuf__.manifest))
