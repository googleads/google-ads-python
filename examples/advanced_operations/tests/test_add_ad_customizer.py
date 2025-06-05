# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for add_ad_customizer.py."""

from unittest import mock
from unittest import TestCase

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

from examples.advanced_operations.add_ad_customizer import main
from examples.advanced_operations.add_ad_customizer import create_text_customizer_attribute
from examples.advanced_operations.add_ad_customizer import create_price_customizer_attribute
from examples.advanced_operations.add_ad_customizer import link_customizer_attributes
from examples.advanced_operations.add_ad_customizer import create_ad_with_customizations


_CUSTOMER_ID = "1234567890"
_AD_GROUP_ID = "9876543210"
_TEXT_CUSTOMIZER_NAME = "Planet_test"
_PRICE_CUSTOMIZER_NAME = "Price_test"
_TEXT_CUSTOMIZER_RESOURCE_NAME = "customers/1234567890/customizerAttributes/1"
_PRICE_CUSTOMIZER_RESOURCE_NAME = "customers/1234567890/customizerAttributes/2"


@mock.patch("examples.advanced_operations.add_ad_customizer.GoogleAdsClient.load_from_storage")
class AddAdCustomizerTest(TestCase):
    def setUp(self):
        self.client_mock = mock.MagicMock(spec=GoogleAdsClient)
        # Mock the enums attribute
        self.client_mock.enums = mock.MagicMock()
        self.client_mock.enums.CustomizerAttributeTypeEnum = mock.MagicMock()
        self.client_mock.enums.ServedAssetFieldTypeEnum = mock.MagicMock()
        # It's also good practice to assign specific mock objects or values
        # if the code relies on specific enum members, for example:
        # self.client_mock.enums.CustomizerAttributeTypeEnum.TEXT = "TEXT_ENUM_VALUE"
        # self.client_mock.enums.CustomizerAttributeTypeEnum.PRICE = "PRICE_ENUM_VALUE"
        # self.client_mock.enums.ServedAssetFieldTypeEnum.HEADLINE_1 = "HEADLINE_1_ENUM_VALUE"
        # However, for now, MagicMock should suffice as the code seems to only access them.

        self.googleads_service_mock = self.client_mock.get_service("GoogleAdsService")
        self.customizer_attribute_service_mock = self.client_mock.get_service("CustomizerAttributeService")
        self.ad_group_customizer_service_mock = self.client_mock.get_service("AdGroupCustomizerService")
        self.ad_group_ad_service_mock = self.client_mock.get_service("AdGroupAdService")

        # Mock successful responses for service calls
        # This will be the default return value for mutate_customizer_attributes.
        # Individual tests that call it once will need to adjust this.
        self.customizer_attribute_service_mock.mutate_customizer_attributes.return_value.results = [
            mock.Mock(resource_name=_TEXT_CUSTOMIZER_RESOURCE_NAME),
            mock.Mock(resource_name=_PRICE_CUSTOMIZER_RESOURCE_NAME)
        ]
        self.ad_group_customizer_service_mock.mutate_ad_group_customizers.return_value.results = [
            mock.Mock(resource_name="adGroupCustomizer1"),
            mock.Mock(resource_name="adGroupCustomizer2")
        ]
        self.ad_group_ad_service_mock.mutate_ad_group_ads.return_value.results = [
            mock.Mock(resource_name="adGroupAd1")
        ]

        self.googleads_service_mock.ad_group_path.return_value = f"customers/{_CUSTOMER_ID}/adGroups/{_AD_GROUP_ID}"


    def test_create_text_customizer_attribute(self, mock_load_client):
        mock_load_client.return_value = self.client_mock
        # Adjust return_value for a single call to mutate_customizer_attributes
        self.customizer_attribute_service_mock.mutate_customizer_attributes.return_value.results = [
            mock.Mock(resource_name=_TEXT_CUSTOMIZER_RESOURCE_NAME)
        ]

        resource_name = create_text_customizer_attribute(
            self.client_mock, _CUSTOMER_ID, _TEXT_CUSTOMIZER_NAME
        )
        self.assertEqual(resource_name, _TEXT_CUSTOMIZER_RESOURCE_NAME)
        self.customizer_attribute_service_mock.mutate_customizer_attributes.assert_called_once()


    def test_create_price_customizer_attribute(self, mock_load_client):
        mock_load_client.return_value = self.client_mock
        # Adjust return_value for a single call to mutate_customizer_attributes
        self.customizer_attribute_service_mock.mutate_customizer_attributes.return_value.results = [
            mock.Mock(resource_name=_PRICE_CUSTOMIZER_RESOURCE_NAME)
        ]

        resource_name = create_price_customizer_attribute(
            self.client_mock, _CUSTOMER_ID, _PRICE_CUSTOMIZER_NAME
        )
        self.assertEqual(resource_name, _PRICE_CUSTOMIZER_RESOURCE_NAME)
        self.customizer_attribute_service_mock.mutate_customizer_attributes.assert_called_once()


    def test_link_customizer_attributes(self, mock_load_client):
        mock_load_client.return_value = self.client_mock
        link_customizer_attributes(
            self.client_mock,
            _CUSTOMER_ID,
            _AD_GROUP_ID,
            _TEXT_CUSTOMIZER_RESOURCE_NAME,
            _PRICE_CUSTOMIZER_RESOURCE_NAME,
        )
        self.ad_group_customizer_service_mock.mutate_ad_group_customizers.assert_called_once()


    def test_create_ad_with_customizations(self, mock_load_client):
        mock_load_client.return_value = self.client_mock
        create_ad_with_customizations(
            self.client_mock,
            _CUSTOMER_ID,
            _AD_GROUP_ID,
            _TEXT_CUSTOMIZER_NAME,
            _PRICE_CUSTOMIZER_NAME,
        )
        self.ad_group_ad_service_mock.mutate_ad_group_ads.assert_called_once()


    @mock.patch("examples.advanced_operations.add_ad_customizer.create_text_customizer_attribute")
    @mock.patch("examples.advanced_operations.add_ad_customizer.create_price_customizer_attribute")
    @mock.patch("examples.advanced_operations.add_ad_customizer.link_customizer_attributes")
    @mock.patch("examples.advanced_operations.add_ad_customizer.create_ad_with_customizations")
    def test_main_success(
        self,
        mock_create_ad,
        mock_link_attributes,
        mock_create_price_attr,
        mock_create_text_attr,
        mock_load_client
    ):
        mock_load_client.return_value = self.client_mock
        mock_create_text_attr.return_value = _TEXT_CUSTOMIZER_RESOURCE_NAME
        mock_create_price_attr.return_value = _PRICE_CUSTOMIZER_RESOURCE_NAME

        main(self.client_mock, _CUSTOMER_ID, _AD_GROUP_ID)

        mock_create_text_attr.assert_called_once_with(
            self.client_mock, _CUSTOMER_ID, mock.ANY
        )
        mock_create_price_attr.assert_called_once_with(
            self.client_mock, _CUSTOMER_ID, mock.ANY
        )
        mock_link_attributes.assert_called_once_with(
            self.client_mock,
            _CUSTOMER_ID,
            _AD_GROUP_ID,
            _TEXT_CUSTOMIZER_RESOURCE_NAME,
            _PRICE_CUSTOMIZER_RESOURCE_NAME,
        )
        mock_create_ad.assert_called_once_with(
            self.client_mock,
            _CUSTOMER_ID,
            _AD_GROUP_ID,
            mock.ANY,
            mock.ANY,
        )

    @mock.patch("examples.advanced_operations.add_ad_customizer.create_text_customizer_attribute")
    def test_main_google_ads_exception(
        self, mock_create_text_attr, mock_load_client
    ):
        # We don't need mock_load_client here as main directly uses the passed client
        # However, it's included by the class-level decorator, so we accept it.
        mock_failure = mock.Mock()
        mock_failure.errors = [mock.Mock(message="Test Error")]
        # Add a mock for the 'call' attribute if it's accessed by GoogleAdsException
        mock_call = mock.Mock()

        mock_create_text_attr.side_effect = GoogleAdsException(
            error=mock.Mock(),
            failure=mock_failure,
            call=mock_call,  # Add the missing 'call' argument
            request_id="test_request_id"
        )

        # The main function in the script catches the exception and calls sys.exit(1)
        # and prints to stdout. For this test, we'll assert that the exception is raised
        # when calling main with our mock client.
        with self.assertRaises(GoogleAdsException):
            main(self.client_mock, _CUSTOMER_ID, _AD_GROUP_ID)

# It's good practice to also create an __init__.py in the tests directory
# if it doesn't exist, to make it a Python package.
# This subtask will also create that file.
# Create the file examples/advanced_operations/tests/__init__.py if it doesn't exist.
# If it exists, leave it as is.
