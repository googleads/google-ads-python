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
from __future__ import annotations


import proto  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v25.enums",
    marshal="google.ads.googleads.v25",
    manifest={
        "SurveySubjectTypeEnum",
    },
)


class SurveySubjectTypeEnum(proto.Message):
    r"""Container for enum"""

    class SurveySubjectType(proto.Enum):
        r"""The enum

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Unknown value.
            GENERIC_BRAND (2):
                Generic Brand
            GENERIC_PRODUCT (3):
                Generic Product
            GENERIC_SERVICE (4):
                Generic Service
            APP (5):
                App
            APPS_DATING_SERVICES (6):
                Apps Dating Services
            APPS_PODCASTS (7):
                Apps Podcasts
            APPS_DIGITAL_COMICS (8):
                Apps Digital Comics
            AUTOMOTIVE_BATTERY (9):
                Automotive Battery
            AUTOMOTIVE_BRAND (10):
                Automotive Brand
            AUTOMOTIVE_CAR_RENTAL (11):
                Automotive Car Rental
            AUTOMOTIVE_CAR_SERVICE (12):
                Automotive Car Service
            AUTOMOTIVE_ELECTRIC_CAR_BRAND (13):
                Automotive Electric Car Brand
            AUTOMOTIVE_GAS_STATIONS (14):
                Automotive Gas Stations
            AUTOMOTIVE_MOTORCYCLE (15):
                Automotive Motorcycle
            AUTOMOTIVE_OIL (16):
                Automotive Oil
            AUTOMOTIVE_PRODUCT (17):
                Automotive Product
            AUTOMOTIVE_TIRES_BRAND (18):
                Automotive Tires Brand
            BIM_COMPANY (19):
                Bim Company
            BIM_ENTERPRISE_SERVICES_COMPANY (20):
                Bim Enterprise Services Company
            BIM_JOB (21):
                Bim Job
            BIM_MARKETING_COMPANY (22):
                Bim Marketing Company
            BIM_RECRUITING (23):
                Bim Recruiting
            BIM_SHIPPING (24):
                Bim Shipping
            CPG_BABY_CARE_BRAND (25):
                Cpg Baby Care Brand
            CPG_BABY_CARE_PRODUCT (26):
                Cpg Baby Care Product
            CPG_BEAUTY_BRAND (27):
                Cpg Beauty Brand
            CPG_BEAUTY_PRODUCT (28):
                Cpg Beauty Product
            CPG_BEAUTY_AND_PERSONAL_CARE_BRAND (29):
                Cpg Beauty And Personal Care Brand
            CPG_BEAUTY_AND_PERSONAL_CARE_PRODUCT (30):
                Cpg Beauty And Personal Care Product
            CPG_BODY_WASH_BRAND (31):
                Cpg Body Wash Brand
            CPG_BODY_WASH_PRODUCT (32):
                Cpg Body Wash Product
            CPG_DRAIN_CLEANERS (33):
                Cpg Drain Cleaners
            CPG_FRAGRANCE_BRAND (34):
                Cpg Fragrance Brand
            CPG_FRAGRANCE_PRODUCT (35):
                Cpg Fragrance Product
            CPG_HAIR_CARE_BRAND (36):
                Cpg Hair Care Brand
            CPG_HAIR_CARE_PRODUCT (37):
                Cpg Hair Care Product
            CPG_HOUSEHOLD_CLEANING_BRAND (38):
                Cpg Household Cleaning Brand
            CPG_HOUSEHOLD_CLEANING_PRODUCT (39):
                Cpg Household Cleaning Product
            CPG_LAUNDRY_BRAND (40):
                Cpg Laundry Brand
            CPG_MAKE_UP_BRAND (41):
                Cpg Make Up Brand
            CPG_MAKE_UP_PRODUCT (42):
                Cpg Make Up Product
            CPG_MOUTHWASH_BRAND (43):
                Cpg Mouthwash Brand
            CPG_OFFICE_SUPPLIES_BRAND (44):
                Cpg Office Supplies Brand
            CPG_OFFICE_SUPPLIES_PRODUCT (45):
                Cpg Office Supplies Product
            CPG_ORAL_CARE_BRAND (46):
                Cpg Oral Care Brand
            CPG_PERSONAL_CARE_BRAND (47):
                Cpg Personal Care Brand
            CPG_PERSONAL_CARE_PRODUCT (48):
                Cpg Personal Care Product
            CPG_SKIN_CARE_BRAND (49):
                Cpg Skin Care Brand
            CPG_SKIN_CARE_PRODUCT (50):
                Cpg Skin Care Product
            EDUCATION_BUSINESS_PROGRAMS (51):
                Education Business Programs
            EDUCATION_MASTERS_PROGRAMS (52):
                Education Masters Programs
            EDUCATION_NURSING_PROGRAMS (53):
                Education Nursing Programs
            EDUCATION_IT_PROGRAMS (54):
                Education It Programs
            EDUCATION_OFFLINE (55):
                Education Offline
            EDUCATION_ONLINE (56):
                Education Online
            EDUCATION_PROGRAM (57):
                Education Program
            EDUCATION_TEST_PREPARATION (58):
                Education Test Preparation
            FBR_BEER_BRAND (59):
                Fbr Beer Brand
            FBR_BEVERAGE_BRAND (60):
                Fbr Beverage Brand
            FBR_BEVERAGE_PRODUCT (61):
                Fbr Beverage Product
            FBR_BREAKFAST_FOOD_BRAND (62):
                Fbr Breakfast Food Brand
            FBR_BREAKFAST_FOOD_PRODUCT (63):
                Fbr Breakfast Food Product
            FBR_CANDY (64):
                Fbr Candy
            FBR_CHEESE (65):
                Fbr Cheese
            FBR_CHIPS_BRAND (66):
                Fbr Chips Brand
            FBR_CHIPS_PRODUCT (67):
                Fbr Chips Product
            FBR_CHOCOLATE_BRAND (68):
                Fbr Chocolate Brand
            FBR_CHOCOLATE_PRODUCT (69):
                Fbr Chocolate Product
            FBR_COFFEE_BRAND (70):
                Fbr Coffee Brand
            FBR_COFFEE_PRODUCT (71):
                Fbr Coffee Product
            FBR_COLD_DRINK_BRAND (72):
                Fbr Cold Drink Brand
            FBR_COLD_DRINK_PRODUCT (73):
                Fbr Cold Drink Product
            FBR_COOKIES (74):
                Fbr Cookies
            FBR_DOGFOOD_BRAND (75):
                Fbr Dogfood Brand
            FBR_DOGFOOD_PRODUCT (76):
                Fbr Dogfood Product
            FBR_DOG_TREATS_BRAND (77):
                Fbr Dog Treats Brand
            FBR_FOOD_BRAND (78):
                Fbr Food Brand
            FBR_FOOD_DELIVERY_BRAND (79):
                Fbr Food Delivery Brand
            FBR_FOOD_PRODUCT (80):
                Fbr Food Product
            FBR_ICE_CREAM_BRAND (81):
                Fbr Ice Cream Brand
            FBR_ICE_CREAM_PRODUCT (82):
                Fbr Ice Cream Product
            FBR_PET_FOOD_BRAND (83):
                Fbr Pet Food Brand
            FBR_PET_FOOD_PRODUCT (84):
                Fbr Pet Food Product
            FBR_PET_SUPPLY_BRAND (85):
                Fbr Pet Supply Brand
            FBR_PET_SUPPLY_PRODUCT (86):
                Fbr Pet Supply Product
            FBR_RESTAURANT (87):
                Fbr Restaurant
            FBR_RESTAURANT_DELIVERY_SERVICE_BRAND (88):
                Fbr Restaurant Delivery Service Brand
            FBR_RESTAURANT_DELIVERY_SERVICE_PRODUCT (89):
                Fbr Restaurant Delivery Service Product
            FBR_SNACKS_BRAND (90):
                Fbr Snacks Brand
            FBR_SNACKS_PRODUCT (91):
                Fbr Snacks Product
            FBR_SODA_BRAND (92):
                Fbr Soda Brand
            FBR_SODA_PRODUCT (93):
                Fbr Soda Product
            FBR_SPIRIT_BRAND (94):
                Fbr Spirit Brand
            FBR_SPIRIT_PRODUCT (95):
                Fbr Spirit Product
            FBR_WHEY_PROTEIN_BRAND (96):
                Fbr Whey Protein Brand
            FBR_WINE (97):
                Fbr Wine
            FINANCE_ACCOUNTING_BRAND (98):
                Finance Accounting Brand
            FINANCE_BANK (99):
                Finance Bank
            FINANCE_CREDIT_CARD_BRAND (100):
                Finance Credit Card Brand
            FINANCE_CREDIT_CARD_PRODUCT (101):
                Finance Credit Card Product
            FINANCE_FINANCIAL_SERVICES (102):
                Finance Financial Services
            FINANCE_INSURANCE (103):
                Finance Insurance
            FINANCE_INVESTMENT_SERVICES (104):
                Finance Investment Services
            FINANCE_LOAN_PROVIDER (105):
                Finance Loan Provider
            FINANCE_MORTGAGE_COMPANY (106):
                Finance Mortgage Company
            FINANCE_PAYMENTS_PROCESSING (107):
                Finance Payments Processing
            FINANCE_PAYMENTS_SYSTEMS (108):
                Finance Payments Systems
            FINANCE_TAXES_BRAND (109):
                Finance Taxes Brand
            FINANCE_TAXES_PRODUCT (110):
                Finance Taxes Product
            GAMBLING_CASINO (111):
                Gambling Casino
            GAMBLING_DAILY_FANTASY_SPORT (112):
                Gambling Daily Fantasy Sport
            GAMBLING_GAMBLING_SITE (113):
                Gambling Gambling Site
            GAMBLING_LOTTERY (114):
                Gambling Lottery
            GAMBLING_SPORTS_BETTING_SITE (115):
                Gambling Sports Betting Site
            GOVERNMENT_ANTI_SMOKING (116):
                Government Anti Smoking
            GOVERNMENT_MILITARY (117):
                Government Military
            GOVERNMENT_ORGANIZATION (118):
                Government Organization
            GOVERNMENT_PROGRAM (119):
                Government Program
            GOVERNMENT_PUBLIC_HEALTH_BEHAVIORS (120):
                Government Public Health Behaviors
            GOVERNMENT_PUBLIC_HEALTH_ISSUE (121):
                Government Public Health Issue
            GOVERNMENT_PUBLIC_HEALTH_TOPIC (122):
                Government Public Health Topic
            GOVERNMENT_SERVICE (123):
                Government Service
            HEALTHCARE_GYMS (124):
                Healthcare Gyms
            HEALTHCARE_HEALTH_INSURANCE_BRAND (125):
                Healthcare Health Insurance Brand
            HEALTHCARE_MULTIVITAMINS (126):
                Healthcare Multivitamins
            HEALTHCARE_SPORTS_SUPPLEMENTS (127):
                Healthcare Sports Supplements
            HEALTHCARE_WEIGHT_LOSS_BRAND (128):
                Healthcare Weight Loss Brand
            HEALTHCARE_WEIGHT_LOSS_PRODUCT (129):
                Healthcare Weight Loss Product
            HOME_SERVICES_CABLE_TV (130):
                Home Services Cable Tv
            HOME_SERVICES_ENERGY_BRAND (131):
                Home Services Energy Brand
            HOME_SERVICES_HOUSEHOLD_SERVICES_COMPANY (132):
                Home Services Household Services Company
            HOME_SERVICES_INTERNET_SERVICE (133):
                Home Services Internet Service
            HOME_SERVICES_MOBILE_PHONE (134):
                Home Services Mobile Phone
            HOME_SERVICES_PAY_TV_CHANNEL (135):
                Home Services Pay Tv Channel
            HOME_SERVICES_PAY_TV_NETWORK (136):
                Home Services Pay Tv Network
            LOCAL_CHARITY (137):
                Local Charity
            LOCAL_CLASSIFIEDS_SITE (138):
                Local Classifieds Site
            LOCAL_FLOWER_BRAND (139):
                Local Flower Brand
            LOCAL_JOB_CLASSIFIEDS_SITE (140):
                Local Job Classifieds Site
            LOCAL_LAW_FIRMS (141):
                Local Law Firms
            LOCAL_REAL_ESTATE_SITE (142):
                Local Real Estate Site
            MEDIA_AND_ENTERTAINMENT_DOWNLOAD_SITE (143):
                Media And Entertainment Download Site
            MEDIA_AND_ENTERTAINMENT_DVD (144):
                Media And Entertainment Dvd
            MEDIA_AND_ENTERTAINMENT_EVENT (145):
                Media And Entertainment Event
            MEDIA_AND_ENTERTAINMENT_GAME (146):
                Media And Entertainment Game
            MEDIA_AND_ENTERTAINMENT_GAMING_PRODUCTS (147):
                Media And Entertainment Gaming Products
            MEDIA_AND_ENTERTAINMENT_LIVE_EVENT (148):
                Media And Entertainment Live Event
            MEDIA_AND_ENTERTAINMENT_MOBILE_GAME (149):
                Media And Entertainment Mobile Game
            MEDIA_AND_ENTERTAINMENT_MOVIE (150):
                Media And Entertainment Movie
            MEDIA_AND_ENTERTAINMENT_MOVIE_DIGITAL_DOWNLOAD (151):
                Media And Entertainment Movie Digital
                Download
            MEDIA_AND_ENTERTAINMENT_MUSIC_ARTIST (152):
                Media And Entertainment Music Artist
            MEDIA_AND_ENTERTAINMENT_MUSIC_RELEASES (153):
                Media And Entertainment Music Releases
            MEDIA_AND_ENTERTAINMENT_PLAYLISTS (154):
                Media And Entertainment Playlists
            MEDIA_AND_ENTERTAINMENT_SHOW (155):
                Media And Entertainment Show
            MEDIA_AND_ENTERTAINMENT_SHOW_DIGITAL_DOWNLOAD (156):
                Media And Entertainment Show Digital Download
            MEDIA_AND_ENTERTAINMENT_SPORTS (157):
                Media And Entertainment Sports
            MEDIA_AND_ENTERTAINMENT_STREAMING_SITE (158):
                Media And Entertainment Streaming Site
            MEDIA_AND_ENTERTAINMENT_TITLE_DIGITAL_DOWNLOAD (159):
                Media And Entertainment Title Digital
                Download
            MEDIA_AND_ENTERTAINMENT_TV_CHANNEL (160):
                Media And Entertainment Tv Channel
            MEDIA_AND_ENTERTAINMENT_TV_SHOW (161):
                Media And Entertainment Tv Show
            MEDIA_AND_ENTERTAINMENT_TV_SHOW_DIGITAL_DOWNLOAD (162):
                Media And Entertainment Tv Show Digital
                Download
            MEDIA_AND_ENTERTAINMENT_VIDEO_GAME (163):
                Media And Entertainment Video Game
            MEDIA_AND_ENTERTAINMENT_VIDEO_GAME_DLC (164):
                Media And Entertainment Video Game Dlc
            MEDIA_AND_ENTERTAINMENT_WEB_SERIES (165):
                Media And Entertainment Web Series
            OFFER (166):
                Offer
            PHARMA_NON_MEDICAL_CONDITION_OTC_DRUG (167):
                Pharma Non Medical Condition Otc Drug
            POLITICS_CANDIDATE (168):
                Politics Candidate
            POLITICS_GET_OUT_THE_VOTE_NOVEMBER_ELECTIONS (169):
                Politics Get Out The Vote November Elections
            POLITICS_GET_OUT_THE_VOTE_PRIMARY_ELECTIONS (170):
                Politics Get Out The Vote Primary Elections
            POLITICS_ISSUE (171):
                Politics Issue
            POLITICS_UNFAVORABLE_CANDIDATE (172):
                Politics Unfavorable Candidate
            RETAIL_APPAREL (173):
                Retail Apparel
            RETAIL_BRICK_AND_MORTAR (174):
                Retail Brick And Mortar
            RETAIL_FURNITURE_BRAND (175):
                Retail Furniture Brand
            RETAIL_FURNITURE_PRODUCT (176):
                Retail Furniture Product
            RETAIL_GIFTS_BRAND (177):
                Retail Gifts Brand
            RETAIL_GIFTS_PRODUCT (178):
                Retail Gifts Product
            RETAIL_HOME_GOODS (179):
                Retail Home Goods
            RETAIL_JEWELRY_BRAND (180):
                Retail Jewelry Brand
            RETAIL_ONLINE_RETAILERS (181):
                Retail Online Retailers
            RETAIL_SHOE_BRAND (182):
                Retail Shoe Brand
            RETAIL_STORE (183):
                Retail Store
            RETAIL_TOY_SHOP (184):
                Retail Toy Shop
            TECHNOLOGY_ARTIFICIAL_INTELLIGENCE_BRAND (185):
                Technology Artificial Intelligence Brand
            TECHNOLOGY_ARTIFICIAL_INTELLIGENCE_PRODUCT (186):
                Technology Artificial Intelligence Product
            TECHNOLOGY_BRAND (187):
                Technology Brand
            TECHNOLOGY_FEATURE (188):
                Technology Feature
            TECHNOLOGY_PRODUCT (189):
                Technology Product
            TECHNOLOGY_CAMERA_BRAND (190):
                Technology Camera Brand
            TECHNOLOGY_CAMERA_PRODUCT (191):
                Technology Camera Product
            TECHNOLOGY_CONTROL_PLANS (192):
                Technology Control Plans
            TECHNOLOGY_GAMING_BRAND (193):
                Technology Gaming Brand
            TECHNOLOGY_HOME_APPLIANCE_BRAND (194):
                Technology Home Appliance Brand
            TECHNOLOGY_HOME_APPLIANCE_PRODUCT (195):
                Technology Home Appliance Product
            TECHNOLOGY_LAPTOP_BRAND (196):
                Technology Laptop Brand
            TECHNOLOGY_LAPTOP_PRODUCT (197):
                Technology Laptop Product
            TECHNOLOGY_MOBILE_PHONE_PLANS (198):
                Technology Mobile Phone Plans
            TECHNOLOGY_ONLINE_SAFETY_BRAND (199):
                Technology Online Safety Brand
            TECHNOLOGY_ONLINE_SAFETY_PRODUCT (200):
                Technology Online Safety Product
            TECHNOLOGY_OPERATING_SYSTEM (201):
                Technology Operating System
            TECHNOLOGY_POSTPAID_TELCO_PLAN (202):
                Technology Postpaid Telco Plan
            TECHNOLOGY_PREPAID_TELCO_PLAN (203):
                Technology Prepaid Telco Plan
            TECHNOLOGY_PRINTER_BRAND (204):
                Technology Printer Brand
            TECHNOLOGY_SEARCH_ENGINE (205):
                Technology Search Engine
            TECHNOLOGY_SMALL_HOME_APPLIANCE_BRAND (206):
                Technology Small Home Appliance Brand
            TECHNOLOGY_SMALL_HOME_APPLIANCE_PRODUCT (207):
                Technology Small Home Appliance Product
            TECHNOLOGY_SMART_HOME_DEVICE (208):
                Technology Smart Home Device
            TECHNOLOGY_SMARTPHONE_BRAND (209):
                Technology Mobile Phone Brand
            TECHNOLOGY_SMARTPHONE_PRODUCT (210):
                Technology Mobile Phone Product
            TECHNOLOGY_SOCIAL_MEDIA (211):
                Technology Social Media
            TECHNOLOGY_TABLET_BRAND (212):
                Technology Tablet Brand
            TECHNOLOGY_TABLET_PRODUCT (213):
                Technology Tablet Product
            TECHNOLOGY_TELECOM_FIBER_OPTIC_INTERNET (214):
                Technology Telecom Fiber Optic Internet
            TECHNOLOGY_TELECOM_SERVICE_PACK (215):
                Technology Telecom Service Pack
            TECHNOLOGY_TELCO_NETWORK (216):
                Technology Telco Network
            TECHNOLOGY_TV_BRAND (217):
                Technology Tv Brand
            TECHNOLOGY_TV_PRODUCT (218):
                Technology Tv Product
            TECHNOLOGY_VIDEO_ON_DEMAND (219):
                Technology Video On Demand
            TECHNOLOGY_WEARABLES_BRAND (220):
                Technology Wearables Brand
            TECHNOLOGY_WEBSITE (221):
                Technology Website
            TRAVEL_ACCOMMODATIONS (222):
                Travel Accommodations
            TRAVEL_AIRLINE (223):
                Travel Airline
            TRAVEL_BOOKING_SERVICE (224):
                Travel Booking Service
            TRAVEL_CRUISES (225):
                Travel Cruises
            TRAVEL_DESTINATION (226):
                Travel Destination
            TRAVEL_HOTEL (227):
                Travel Hotel
            TRAVEL_OPTION (228):
                Travel Option
            TRAVEL_VACATION_RENTAL_SERVICE (229):
                Travel Vacation Rental Service
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        GENERIC_BRAND = 2
        GENERIC_PRODUCT = 3
        GENERIC_SERVICE = 4
        APP = 5
        APPS_DATING_SERVICES = 6
        APPS_PODCASTS = 7
        APPS_DIGITAL_COMICS = 8
        AUTOMOTIVE_BATTERY = 9
        AUTOMOTIVE_BRAND = 10
        AUTOMOTIVE_CAR_RENTAL = 11
        AUTOMOTIVE_CAR_SERVICE = 12
        AUTOMOTIVE_ELECTRIC_CAR_BRAND = 13
        AUTOMOTIVE_GAS_STATIONS = 14
        AUTOMOTIVE_MOTORCYCLE = 15
        AUTOMOTIVE_OIL = 16
        AUTOMOTIVE_PRODUCT = 17
        AUTOMOTIVE_TIRES_BRAND = 18
        BIM_COMPANY = 19
        BIM_ENTERPRISE_SERVICES_COMPANY = 20
        BIM_JOB = 21
        BIM_MARKETING_COMPANY = 22
        BIM_RECRUITING = 23
        BIM_SHIPPING = 24
        CPG_BABY_CARE_BRAND = 25
        CPG_BABY_CARE_PRODUCT = 26
        CPG_BEAUTY_BRAND = 27
        CPG_BEAUTY_PRODUCT = 28
        CPG_BEAUTY_AND_PERSONAL_CARE_BRAND = 29
        CPG_BEAUTY_AND_PERSONAL_CARE_PRODUCT = 30
        CPG_BODY_WASH_BRAND = 31
        CPG_BODY_WASH_PRODUCT = 32
        CPG_DRAIN_CLEANERS = 33
        CPG_FRAGRANCE_BRAND = 34
        CPG_FRAGRANCE_PRODUCT = 35
        CPG_HAIR_CARE_BRAND = 36
        CPG_HAIR_CARE_PRODUCT = 37
        CPG_HOUSEHOLD_CLEANING_BRAND = 38
        CPG_HOUSEHOLD_CLEANING_PRODUCT = 39
        CPG_LAUNDRY_BRAND = 40
        CPG_MAKE_UP_BRAND = 41
        CPG_MAKE_UP_PRODUCT = 42
        CPG_MOUTHWASH_BRAND = 43
        CPG_OFFICE_SUPPLIES_BRAND = 44
        CPG_OFFICE_SUPPLIES_PRODUCT = 45
        CPG_ORAL_CARE_BRAND = 46
        CPG_PERSONAL_CARE_BRAND = 47
        CPG_PERSONAL_CARE_PRODUCT = 48
        CPG_SKIN_CARE_BRAND = 49
        CPG_SKIN_CARE_PRODUCT = 50
        EDUCATION_BUSINESS_PROGRAMS = 51
        EDUCATION_MASTERS_PROGRAMS = 52
        EDUCATION_NURSING_PROGRAMS = 53
        EDUCATION_IT_PROGRAMS = 54
        EDUCATION_OFFLINE = 55
        EDUCATION_ONLINE = 56
        EDUCATION_PROGRAM = 57
        EDUCATION_TEST_PREPARATION = 58
        FBR_BEER_BRAND = 59
        FBR_BEVERAGE_BRAND = 60
        FBR_BEVERAGE_PRODUCT = 61
        FBR_BREAKFAST_FOOD_BRAND = 62
        FBR_BREAKFAST_FOOD_PRODUCT = 63
        FBR_CANDY = 64
        FBR_CHEESE = 65
        FBR_CHIPS_BRAND = 66
        FBR_CHIPS_PRODUCT = 67
        FBR_CHOCOLATE_BRAND = 68
        FBR_CHOCOLATE_PRODUCT = 69
        FBR_COFFEE_BRAND = 70
        FBR_COFFEE_PRODUCT = 71
        FBR_COLD_DRINK_BRAND = 72
        FBR_COLD_DRINK_PRODUCT = 73
        FBR_COOKIES = 74
        FBR_DOGFOOD_BRAND = 75
        FBR_DOGFOOD_PRODUCT = 76
        FBR_DOG_TREATS_BRAND = 77
        FBR_FOOD_BRAND = 78
        FBR_FOOD_DELIVERY_BRAND = 79
        FBR_FOOD_PRODUCT = 80
        FBR_ICE_CREAM_BRAND = 81
        FBR_ICE_CREAM_PRODUCT = 82
        FBR_PET_FOOD_BRAND = 83
        FBR_PET_FOOD_PRODUCT = 84
        FBR_PET_SUPPLY_BRAND = 85
        FBR_PET_SUPPLY_PRODUCT = 86
        FBR_RESTAURANT = 87
        FBR_RESTAURANT_DELIVERY_SERVICE_BRAND = 88
        FBR_RESTAURANT_DELIVERY_SERVICE_PRODUCT = 89
        FBR_SNACKS_BRAND = 90
        FBR_SNACKS_PRODUCT = 91
        FBR_SODA_BRAND = 92
        FBR_SODA_PRODUCT = 93
        FBR_SPIRIT_BRAND = 94
        FBR_SPIRIT_PRODUCT = 95
        FBR_WHEY_PROTEIN_BRAND = 96
        FBR_WINE = 97
        FINANCE_ACCOUNTING_BRAND = 98
        FINANCE_BANK = 99
        FINANCE_CREDIT_CARD_BRAND = 100
        FINANCE_CREDIT_CARD_PRODUCT = 101
        FINANCE_FINANCIAL_SERVICES = 102
        FINANCE_INSURANCE = 103
        FINANCE_INVESTMENT_SERVICES = 104
        FINANCE_LOAN_PROVIDER = 105
        FINANCE_MORTGAGE_COMPANY = 106
        FINANCE_PAYMENTS_PROCESSING = 107
        FINANCE_PAYMENTS_SYSTEMS = 108
        FINANCE_TAXES_BRAND = 109
        FINANCE_TAXES_PRODUCT = 110
        GAMBLING_CASINO = 111
        GAMBLING_DAILY_FANTASY_SPORT = 112
        GAMBLING_GAMBLING_SITE = 113
        GAMBLING_LOTTERY = 114
        GAMBLING_SPORTS_BETTING_SITE = 115
        GOVERNMENT_ANTI_SMOKING = 116
        GOVERNMENT_MILITARY = 117
        GOVERNMENT_ORGANIZATION = 118
        GOVERNMENT_PROGRAM = 119
        GOVERNMENT_PUBLIC_HEALTH_BEHAVIORS = 120
        GOVERNMENT_PUBLIC_HEALTH_ISSUE = 121
        GOVERNMENT_PUBLIC_HEALTH_TOPIC = 122
        GOVERNMENT_SERVICE = 123
        HEALTHCARE_GYMS = 124
        HEALTHCARE_HEALTH_INSURANCE_BRAND = 125
        HEALTHCARE_MULTIVITAMINS = 126
        HEALTHCARE_SPORTS_SUPPLEMENTS = 127
        HEALTHCARE_WEIGHT_LOSS_BRAND = 128
        HEALTHCARE_WEIGHT_LOSS_PRODUCT = 129
        HOME_SERVICES_CABLE_TV = 130
        HOME_SERVICES_ENERGY_BRAND = 131
        HOME_SERVICES_HOUSEHOLD_SERVICES_COMPANY = 132
        HOME_SERVICES_INTERNET_SERVICE = 133
        HOME_SERVICES_MOBILE_PHONE = 134
        HOME_SERVICES_PAY_TV_CHANNEL = 135
        HOME_SERVICES_PAY_TV_NETWORK = 136
        LOCAL_CHARITY = 137
        LOCAL_CLASSIFIEDS_SITE = 138
        LOCAL_FLOWER_BRAND = 139
        LOCAL_JOB_CLASSIFIEDS_SITE = 140
        LOCAL_LAW_FIRMS = 141
        LOCAL_REAL_ESTATE_SITE = 142
        MEDIA_AND_ENTERTAINMENT_DOWNLOAD_SITE = 143
        MEDIA_AND_ENTERTAINMENT_DVD = 144
        MEDIA_AND_ENTERTAINMENT_EVENT = 145
        MEDIA_AND_ENTERTAINMENT_GAME = 146
        MEDIA_AND_ENTERTAINMENT_GAMING_PRODUCTS = 147
        MEDIA_AND_ENTERTAINMENT_LIVE_EVENT = 148
        MEDIA_AND_ENTERTAINMENT_MOBILE_GAME = 149
        MEDIA_AND_ENTERTAINMENT_MOVIE = 150
        MEDIA_AND_ENTERTAINMENT_MOVIE_DIGITAL_DOWNLOAD = 151
        MEDIA_AND_ENTERTAINMENT_MUSIC_ARTIST = 152
        MEDIA_AND_ENTERTAINMENT_MUSIC_RELEASES = 153
        MEDIA_AND_ENTERTAINMENT_PLAYLISTS = 154
        MEDIA_AND_ENTERTAINMENT_SHOW = 155
        MEDIA_AND_ENTERTAINMENT_SHOW_DIGITAL_DOWNLOAD = 156
        MEDIA_AND_ENTERTAINMENT_SPORTS = 157
        MEDIA_AND_ENTERTAINMENT_STREAMING_SITE = 158
        MEDIA_AND_ENTERTAINMENT_TITLE_DIGITAL_DOWNLOAD = 159
        MEDIA_AND_ENTERTAINMENT_TV_CHANNEL = 160
        MEDIA_AND_ENTERTAINMENT_TV_SHOW = 161
        MEDIA_AND_ENTERTAINMENT_TV_SHOW_DIGITAL_DOWNLOAD = 162
        MEDIA_AND_ENTERTAINMENT_VIDEO_GAME = 163
        MEDIA_AND_ENTERTAINMENT_VIDEO_GAME_DLC = 164
        MEDIA_AND_ENTERTAINMENT_WEB_SERIES = 165
        OFFER = 166
        PHARMA_NON_MEDICAL_CONDITION_OTC_DRUG = 167
        POLITICS_CANDIDATE = 168
        POLITICS_GET_OUT_THE_VOTE_NOVEMBER_ELECTIONS = 169
        POLITICS_GET_OUT_THE_VOTE_PRIMARY_ELECTIONS = 170
        POLITICS_ISSUE = 171
        POLITICS_UNFAVORABLE_CANDIDATE = 172
        RETAIL_APPAREL = 173
        RETAIL_BRICK_AND_MORTAR = 174
        RETAIL_FURNITURE_BRAND = 175
        RETAIL_FURNITURE_PRODUCT = 176
        RETAIL_GIFTS_BRAND = 177
        RETAIL_GIFTS_PRODUCT = 178
        RETAIL_HOME_GOODS = 179
        RETAIL_JEWELRY_BRAND = 180
        RETAIL_ONLINE_RETAILERS = 181
        RETAIL_SHOE_BRAND = 182
        RETAIL_STORE = 183
        RETAIL_TOY_SHOP = 184
        TECHNOLOGY_ARTIFICIAL_INTELLIGENCE_BRAND = 185
        TECHNOLOGY_ARTIFICIAL_INTELLIGENCE_PRODUCT = 186
        TECHNOLOGY_BRAND = 187
        TECHNOLOGY_FEATURE = 188
        TECHNOLOGY_PRODUCT = 189
        TECHNOLOGY_CAMERA_BRAND = 190
        TECHNOLOGY_CAMERA_PRODUCT = 191
        TECHNOLOGY_CONTROL_PLANS = 192
        TECHNOLOGY_GAMING_BRAND = 193
        TECHNOLOGY_HOME_APPLIANCE_BRAND = 194
        TECHNOLOGY_HOME_APPLIANCE_PRODUCT = 195
        TECHNOLOGY_LAPTOP_BRAND = 196
        TECHNOLOGY_LAPTOP_PRODUCT = 197
        TECHNOLOGY_MOBILE_PHONE_PLANS = 198
        TECHNOLOGY_ONLINE_SAFETY_BRAND = 199
        TECHNOLOGY_ONLINE_SAFETY_PRODUCT = 200
        TECHNOLOGY_OPERATING_SYSTEM = 201
        TECHNOLOGY_POSTPAID_TELCO_PLAN = 202
        TECHNOLOGY_PREPAID_TELCO_PLAN = 203
        TECHNOLOGY_PRINTER_BRAND = 204
        TECHNOLOGY_SEARCH_ENGINE = 205
        TECHNOLOGY_SMALL_HOME_APPLIANCE_BRAND = 206
        TECHNOLOGY_SMALL_HOME_APPLIANCE_PRODUCT = 207
        TECHNOLOGY_SMART_HOME_DEVICE = 208
        TECHNOLOGY_SMARTPHONE_BRAND = 209
        TECHNOLOGY_SMARTPHONE_PRODUCT = 210
        TECHNOLOGY_SOCIAL_MEDIA = 211
        TECHNOLOGY_TABLET_BRAND = 212
        TECHNOLOGY_TABLET_PRODUCT = 213
        TECHNOLOGY_TELECOM_FIBER_OPTIC_INTERNET = 214
        TECHNOLOGY_TELECOM_SERVICE_PACK = 215
        TECHNOLOGY_TELCO_NETWORK = 216
        TECHNOLOGY_TV_BRAND = 217
        TECHNOLOGY_TV_PRODUCT = 218
        TECHNOLOGY_VIDEO_ON_DEMAND = 219
        TECHNOLOGY_WEARABLES_BRAND = 220
        TECHNOLOGY_WEBSITE = 221
        TRAVEL_ACCOMMODATIONS = 222
        TRAVEL_AIRLINE = 223
        TRAVEL_BOOKING_SERVICE = 224
        TRAVEL_CRUISES = 225
        TRAVEL_DESTINATION = 226
        TRAVEL_HOTEL = 227
        TRAVEL_OPTION = 228
        TRAVEL_VACATION_RENTAL_SERVICE = 229


__all__ = tuple(sorted(__protobuf__.manifest))
