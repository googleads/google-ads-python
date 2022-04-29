# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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


__protobuf__ = proto.module(
    package="google.ads.googleads.v10.enums",
    marshal="google.ads.googleads.v10",
    manifest={"LeadFormFieldUserInputTypeEnum",},
)


class LeadFormFieldUserInputTypeEnum(proto.Message):
    r"""Describes the input type of a lead form field.
    """

    class LeadFormFieldUserInputType(proto.Enum):
        r"""Enum describing the input type of a lead form field."""
        UNSPECIFIED = 0
        UNKNOWN = 1
        FULL_NAME = 2
        EMAIL = 3
        PHONE_NUMBER = 4
        POSTAL_CODE = 5
        CITY = 9
        REGION = 10
        COUNTRY = 11
        WORK_EMAIL = 12
        COMPANY_NAME = 13
        WORK_PHONE = 14
        JOB_TITLE = 15
        GOVERNMENT_ISSUED_ID_CPF_BR = 16
        GOVERNMENT_ISSUED_ID_DNI_AR = 17
        GOVERNMENT_ISSUED_ID_DNI_PE = 18
        GOVERNMENT_ISSUED_ID_RUT_CL = 19
        GOVERNMENT_ISSUED_ID_CC_CO = 20
        GOVERNMENT_ISSUED_ID_CI_EC = 21
        GOVERNMENT_ISSUED_ID_RFC_MX = 22
        FIRST_NAME = 23
        LAST_NAME = 24
        VEHICLE_MODEL = 1001
        VEHICLE_TYPE = 1002
        PREFERRED_DEALERSHIP = 1003
        VEHICLE_PURCHASE_TIMELINE = 1004
        VEHICLE_OWNERSHIP = 1005
        VEHICLE_PAYMENT_TYPE = 1009
        VEHICLE_CONDITION = 1010
        COMPANY_SIZE = 1006
        ANNUAL_SALES = 1007
        YEARS_IN_BUSINESS = 1008
        JOB_DEPARTMENT = 1011
        JOB_ROLE = 1012
        EDUCATION_PROGRAM = 1013
        EDUCATION_COURSE = 1014
        PRODUCT = 1016
        SERVICE = 1017
        OFFER = 1018
        CATEGORY = 1019
        PREFERRED_CONTACT_METHOD = 1020
        PREFERRED_LOCATION = 1021
        PREFERRED_CONTACT_TIME = 1022
        PURCHASE_TIMELINE = 1023
        YEARS_OF_EXPERIENCE = 1048
        JOB_INDUSTRY = 1049
        LEVEL_OF_EDUCATION = 1050
        PROPERTY_TYPE = 1024
        REALTOR_HELP_GOAL = 1025
        PROPERTY_COMMUNITY = 1026
        PRICE_RANGE = 1027
        NUMBER_OF_BEDROOMS = 1028
        FURNISHED_PROPERTY = 1029
        PETS_ALLOWED_PROPERTY = 1030
        NEXT_PLANNED_PURCHASE = 1031
        EVENT_SIGNUP_INTEREST = 1033
        PREFERRED_SHOPPING_PLACES = 1034
        FAVORITE_BRAND = 1035
        TRANSPORTATION_COMMERCIAL_LICENSE_TYPE = 1036
        EVENT_BOOKING_INTEREST = 1038
        DESTINATION_COUNTRY = 1039
        DESTINATION_CITY = 1040
        DEPARTURE_COUNTRY = 1041
        DEPARTURE_CITY = 1042
        DEPARTURE_DATE = 1043
        RETURN_DATE = 1044
        NUMBER_OF_TRAVELERS = 1045
        TRAVEL_BUDGET = 1046
        TRAVEL_ACCOMMODATION = 1047


__all__ = tuple(sorted(__protobuf__.manifest))
