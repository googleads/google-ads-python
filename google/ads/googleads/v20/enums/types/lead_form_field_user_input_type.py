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
    package="google.ads.googleads.v20.enums",
    marshal="google.ads.googleads.v20",
    manifest={
        "LeadFormFieldUserInputTypeEnum",
    },
)


class LeadFormFieldUserInputTypeEnum(proto.Message):
    r"""Describes the input type of a lead form field."""

    class LeadFormFieldUserInputType(proto.Enum):
        r"""Enum describing the input type of a lead form field.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            FULL_NAME (2):
                The user will be asked to fill in their given and family
                name. This field cannot be set at the same time as
                GIVEN_NAME or FAMILY_NAME.
            EMAIL (3):
                The user will be asked to fill in their email
                address.
            PHONE_NUMBER (4):
                The user will be asked to fill in their phone
                number.
            POSTAL_CODE (5):
                The user will be asked to fill in their zip
                code.
            STREET_ADDRESS (8):
                The user will be asked to fill in their
                street address.
            CITY (9):
                The user will be asked to fill in their city.
            REGION (10):
                The user will be asked to fill in their
                region part of the address (for example, state
                for US, province for Canada).
            COUNTRY (11):
                The user will be asked to fill in their
                country.
            WORK_EMAIL (12):
                The user will be asked to fill in their work
                email address.
            COMPANY_NAME (13):
                The user will be asked to fill in their
                company name.
            WORK_PHONE (14):
                The user will be asked to fill in their work
                phone.
            JOB_TITLE (15):
                The user will be asked to fill in their job
                title.
            GOVERNMENT_ISSUED_ID_CPF_BR (16):
                The user will be asked to fill in their CPF
                for Brazil users.
            GOVERNMENT_ISSUED_ID_DNI_AR (17):
                The user will be asked to fill in their DNI
                for Argentina users.
            GOVERNMENT_ISSUED_ID_DNI_PE (18):
                The user will be asked to fill in their DNI
                for Peru users.
            GOVERNMENT_ISSUED_ID_RUT_CL (19):
                The user will be asked to fill in their RUT
                for Chile users.
            GOVERNMENT_ISSUED_ID_CC_CO (20):
                The user will be asked to fill in their CC
                for Colombia users.
            GOVERNMENT_ISSUED_ID_CI_EC (21):
                The user will be asked to fill in their CI
                for Ecuador users.
            GOVERNMENT_ISSUED_ID_RFC_MX (22):
                The user will be asked to fill in their RFC
                for Mexico users.
            FIRST_NAME (23):
                The user will be asked to fill in their first name. This
                field can not be set at the same time as FULL_NAME.
            LAST_NAME (24):
                The user will be asked to fill in their last name. This
                field can not be set at the same time as FULL_NAME.
            VEHICLE_MODEL (1001):
                Question: "Which model are you interested in?" Category:
                "Auto" This field is subject to a limit of 5 qualifying
                questions per form and cannot be used if values are set
                using custom_question_fields.
            VEHICLE_TYPE (1002):
                Question: "Which type of vehicle are you interested in?"
                Category: "Auto" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            PREFERRED_DEALERSHIP (1003):
                Question: "What is your preferred dealership?" Category:
                "Auto" This field is subject to a limit of 5 qualifying
                questions per form and cannot be used if values are set
                using custom_question_fields.
            VEHICLE_PURCHASE_TIMELINE (1004):
                Question: "When do you plan on purchasing a vehicle?"
                Category: "Auto" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            VEHICLE_OWNERSHIP (1005):
                Question: "Do you own a vehicle?" Category: "Auto" This
                field is subject to a limit of 5 qualifying questions per
                form and cannot be used if values are set using
                custom_question_fields.
            VEHICLE_PAYMENT_TYPE (1009):
                Question: "What vehicle ownership option are you interested
                in?" Category: "Auto" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            VEHICLE_CONDITION (1010):
                Question: "What type of vehicle condition are you interested
                in?" Category: "Auto" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            COMPANY_SIZE (1006):
                Question: "What size is your company?" Category: "Business"
                This field is subject to a limit of 5 qualifying questions
                per form and cannot be used if values are set using
                custom_question_fields.
            ANNUAL_SALES (1007):
                Question: "What is your annual sales volume?" Category:
                "Business" This field is subject to a limit of 5 qualifying
                questions per form and cannot be used if values are set
                using custom_question_fields.
            YEARS_IN_BUSINESS (1008):
                Question: "How many years have you been in business?"
                Category: "Business" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            JOB_DEPARTMENT (1011):
                Question: "What is your job department?" Category:
                "Business" This field is subject to a limit of 5 qualifying
                questions per form and cannot be used if values are set
                using custom_question_fields.
            JOB_ROLE (1012):
                Question: "What is your job role?" Category: "Business" This
                field is subject to a limit of 5 qualifying questions per
                form and cannot be used if values are set using
                custom_question_fields.
            OVER_18_AGE (1078):
                Question: "Are you over 18 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_19_AGE (1079):
                Question: "Are you over 19 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_20_AGE (1080):
                Question: "Are you over 20 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_21_AGE (1081):
                Question: "Are you over 21 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_22_AGE (1082):
                Question: "Are you over 22 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_23_AGE (1083):
                Question: "Are you over 23 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_24_AGE (1084):
                Question: "Are you over 24 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_25_AGE (1085):
                Question: "Are you over 25 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_26_AGE (1086):
                Question: "Are you over 26 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_27_AGE (1087):
                Question: "Are you over 27 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_28_AGE (1088):
                Question: "Are you over 28 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_29_AGE (1089):
                Question: "Are you over 29 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_30_AGE (1090):
                Question: "Are you over 30 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_31_AGE (1091):
                Question: "Are you over 31 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_32_AGE (1092):
                Question: "Are you over 32 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_33_AGE (1093):
                Question: "Are you over 33 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_34_AGE (1094):
                Question: "Are you over 34 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_35_AGE (1095):
                Question: "Are you over 35 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_36_AGE (1096):
                Question: "Are you over 36 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_37_AGE (1097):
                Question: "Are you over 37 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_38_AGE (1098):
                Question: "Are you over 38 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_39_AGE (1099):
                Question: "Are you over 39 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_40_AGE (1100):
                Question: "Are you over 40 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_41_AGE (1101):
                Question: "Are you over 41 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_42_AGE (1102):
                Question: "Are you over 42 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_43_AGE (1103):
                Question: "Are you over 43 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_44_AGE (1104):
                Question: "Are you over 44 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_45_AGE (1105):
                Question: "Are you over 45 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_46_AGE (1106):
                Question: "Are you over 46 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_47_AGE (1107):
                Question: "Are you over 47 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_48_AGE (1108):
                Question: "Are you over 48 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_49_AGE (1109):
                Question: "Are you over 49 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_50_AGE (1110):
                Question: "Are you over 50 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_51_AGE (1111):
                Question: "Are you over 51 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_52_AGE (1112):
                Question: "Are you over 52 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_53_AGE (1113):
                Question: "Are you over 53 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_54_AGE (1114):
                Question: "Are you over 54 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_55_AGE (1115):
                Question: "Are you over 55 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_56_AGE (1116):
                Question: "Are you over 56 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_57_AGE (1117):
                Question: "Are you over 57 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_58_AGE (1118):
                Question: "Are you over 58 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_59_AGE (1119):
                Question: "Are you over 59 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_60_AGE (1120):
                Question: "Are you over 60 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_61_AGE (1121):
                Question: "Are you over 61 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_62_AGE (1122):
                Question: "Are you over 62 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_63_AGE (1123):
                Question: "Are you over 63 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_64_AGE (1124):
                Question: "Are you over 64 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            OVER_65_AGE (1125):
                Question: "Are you over 65 years of age?" Category:
                "Demographics" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            EDUCATION_PROGRAM (1013):
                Question: "Which program are you interested in?" Category:
                "Education" This field is subject to a limit of 5 qualifying
                questions per form and cannot be used if values are set
                using custom_question_fields.
            EDUCATION_COURSE (1014):
                Question: "Which course are you interested in?" Category:
                "Education" This field is subject to a limit of 5 qualifying
                questions per form and cannot be used if values are set
                using custom_question_fields.
            PRODUCT (1016):
                Question: "Which product are you interested in?" Category:
                "General" This field is subject to a limit of 5 qualifying
                questions per form and cannot be used if values are set
                using custom_question_fields.
            SERVICE (1017):
                Question: "Which service are you interested in?" Category:
                "General" This field is subject to a limit of 5 qualifying
                questions per form and cannot be used if values are set
                using custom_question_fields.
            OFFER (1018):
                Question: "Which offer are you interested in?" Category:
                "General" This field is subject to a limit of 5 qualifying
                questions per form and cannot be used if values are set
                using custom_question_fields.
            CATEGORY (1019):
                Question: "Which category are you interested in?" Category:
                "General" This field is subject to a limit of 5 qualifying
                questions per form and cannot be used if values are set
                using custom_question_fields.
            PREFERRED_CONTACT_METHOD (1020):
                Question: "What is your preferred method of contact?"
                Category: "General" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            PREFERRED_LOCATION (1021):
                Question: "What is your preferred location?" Category:
                "General" This field is subject to a limit of 5 qualifying
                questions per form and cannot be used if values are set
                using custom_question_fields.
            PREFERRED_CONTACT_TIME (1022):
                Question: "What is the best time to contact you?" Category:
                "General" This field is subject to a limit of 5 qualifying
                questions per form and cannot be used if values are set
                using custom_question_fields.
            PURCHASE_TIMELINE (1023):
                Question: "When are you looking to make a purchase?"
                Category: "General" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            YEARS_OF_EXPERIENCE (1048):
                Question: "How many years of work experience do you have?"
                Category: "Jobs" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            JOB_INDUSTRY (1049):
                Question: "What industry do you work in?" Category: "Jobs"
                This field is subject to a limit of 5 qualifying questions
                per form and cannot be used if values are set using
                custom_question_fields.
            LEVEL_OF_EDUCATION (1050):
                Question: "What is your highest level of education?"
                Category: "Jobs" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            PROPERTY_TYPE (1024):
                Question: "What type of property are you looking for?"
                Category: "Real Estate" This field is subject to a limit of
                5 qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            REALTOR_HELP_GOAL (1025):
                Question: "What do you need a realtor's help with?"
                Category: "Real Estate" This field is subject to a limit of
                5 qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            PROPERTY_COMMUNITY (1026):
                Question: "What neighborhood are you interested in?"
                Category: "Real Estate" This field is subject to a limit of
                5 qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            PRICE_RANGE (1027):
                Question: "What price range are you looking for?" Category:
                "Real Estate" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            NUMBER_OF_BEDROOMS (1028):
                Question: "How many bedrooms are you looking for?" Category:
                "Real Estate" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            FURNISHED_PROPERTY (1029):
                Question: "Are you looking for a fully furnished property?"
                Category: "Real Estate" This field is subject to a limit of
                5 qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            PETS_ALLOWED_PROPERTY (1030):
                Question: "Are you looking for properties that allow pets?"
                Category: "Real Estate" This field is subject to a limit of
                5 qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            NEXT_PLANNED_PURCHASE (1031):
                Question: "What is the next product you plan to purchase?"
                Category: "Retail" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            EVENT_SIGNUP_INTEREST (1033):
                Question: "Would you like to sign up for an event?"
                Category: "Retail" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            PREFERRED_SHOPPING_PLACES (1034):
                Question: "Where are you interested in shopping?" Category:
                "Retail" This field is subject to a limit of 5 qualifying
                questions per form and cannot be used if values are set
                using custom_question_fields.
            FAVORITE_BRAND (1035):
                Question: "What is your favorite brand?" Category: "Retail"
                This field is subject to a limit of 5 qualifying questions
                per form and cannot be used if values are set using
                custom_question_fields.
            TRANSPORTATION_COMMERCIAL_LICENSE_TYPE (1036):
                Question: "Which type of valid commercial license do you
                have?" Category: "Transportation" This field is subject to a
                limit of 5 qualifying questions per form and cannot be used
                if values are set using custom_question_fields.
            EVENT_BOOKING_INTEREST (1038):
                Question: "Interested in booking an event?" Category:
                "Travel" This field is subject to a limit of 5 qualifying
                questions per form and cannot be used if values are set
                using custom_question_fields.
            DESTINATION_COUNTRY (1039):
                Question: "What is your destination country?" Category:
                "Travel" This field is subject to a limit of 5 qualifying
                questions per form and cannot be used if values are set
                using custom_question_fields.
            DESTINATION_CITY (1040):
                Question: "What is your destination city?" Category:
                "Travel" This field is subject to a limit of 5 qualifying
                questions per form and cannot be used if values are set
                using custom_question_fields.
            DEPARTURE_COUNTRY (1041):
                Question: "What is your departure country?" Category:
                "Travel" This field is subject to a limit of 5 qualifying
                questions per form and cannot be used if values are set
                using custom_question_fields.
            DEPARTURE_CITY (1042):
                Question: "What is your departure city?" Category: "Travel"
                This field is subject to a limit of 5 qualifying questions
                per form and cannot be used if values are set using
                custom_question_fields.
            DEPARTURE_DATE (1043):
                Question: "What is your departure date?" Category: "Travel"
                This field is subject to a limit of 5 qualifying questions
                per form and cannot be used if values are set using
                custom_question_fields.
            RETURN_DATE (1044):
                Question: "What is your return date?" Category: "Travel"
                This field is subject to a limit of 5 qualifying questions
                per form and cannot be used if values are set using
                custom_question_fields.
            NUMBER_OF_TRAVELERS (1045):
                Question: "How many people are you traveling with?"
                Category: "Travel" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
            TRAVEL_BUDGET (1046):
                Question: "What is your travel budget?" Category: "Travel"
                This field is subject to a limit of 5 qualifying questions
                per form and cannot be used if values are set using
                custom_question_fields.
            TRAVEL_ACCOMMODATION (1047):
                Question: "Where do you want to stay during your travel?"
                Category: "Travel" This field is subject to a limit of 5
                qualifying questions per form and cannot be used if values
                are set using custom_question_fields.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        FULL_NAME = 2
        EMAIL = 3
        PHONE_NUMBER = 4
        POSTAL_CODE = 5
        STREET_ADDRESS = 8
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
        OVER_18_AGE = 1078
        OVER_19_AGE = 1079
        OVER_20_AGE = 1080
        OVER_21_AGE = 1081
        OVER_22_AGE = 1082
        OVER_23_AGE = 1083
        OVER_24_AGE = 1084
        OVER_25_AGE = 1085
        OVER_26_AGE = 1086
        OVER_27_AGE = 1087
        OVER_28_AGE = 1088
        OVER_29_AGE = 1089
        OVER_30_AGE = 1090
        OVER_31_AGE = 1091
        OVER_32_AGE = 1092
        OVER_33_AGE = 1093
        OVER_34_AGE = 1094
        OVER_35_AGE = 1095
        OVER_36_AGE = 1096
        OVER_37_AGE = 1097
        OVER_38_AGE = 1098
        OVER_39_AGE = 1099
        OVER_40_AGE = 1100
        OVER_41_AGE = 1101
        OVER_42_AGE = 1102
        OVER_43_AGE = 1103
        OVER_44_AGE = 1104
        OVER_45_AGE = 1105
        OVER_46_AGE = 1106
        OVER_47_AGE = 1107
        OVER_48_AGE = 1108
        OVER_49_AGE = 1109
        OVER_50_AGE = 1110
        OVER_51_AGE = 1111
        OVER_52_AGE = 1112
        OVER_53_AGE = 1113
        OVER_54_AGE = 1114
        OVER_55_AGE = 1115
        OVER_56_AGE = 1116
        OVER_57_AGE = 1117
        OVER_58_AGE = 1118
        OVER_59_AGE = 1119
        OVER_60_AGE = 1120
        OVER_61_AGE = 1121
        OVER_62_AGE = 1122
        OVER_63_AGE = 1123
        OVER_64_AGE = 1124
        OVER_65_AGE = 1125
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
