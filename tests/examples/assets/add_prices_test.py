import unittest
from unittest.mock import MagicMock, patch, call, PropertyMock
import sys
import argparse
import os
from uuid import UUID  # For checking UUID patch

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")),
)

from examples.assets import add_prices

try:
    from google.ads.googleads.client import (
        GoogleAdsClient as RealGoogleAdsClient,
    )
except ImportError:
    RealGoogleAdsClient = MagicMock()


class TestAddPrices(unittest.TestCase):

    @patch("examples.assets.add_prices.uuid4")
    @patch(
        "examples.assets.add_prices.create_price_offering"
    )  # Mock the helper
    @patch("examples.assets.add_prices.GoogleAdsClient")
    def test_create_price_asset(
        self,
        mock_google_ads_client_constructor,
        mock_create_price_offering_helper,
        mock_uuid4,
    ):
        mock_client_instance = mock_google_ads_client_constructor.return_value
        mock_asset_service = MagicMock()
        mock_client_instance.get_service.return_value = mock_asset_service

        mock_asset_operation = MagicMock()
        mock_client_instance.get_type.return_value = mock_asset_operation
        mock_created_asset = mock_asset_operation.create
        mock_created_asset.price_asset = MagicMock()
        mock_created_asset.price_asset.price_offerings = MagicMock(spec=list)
        mock_created_asset.price_asset.price_offerings.extend = MagicMock()

        mock_client_instance.enums.PriceExtensionTypeEnum.SERVICES = (
            "SERVICES_ENUM"
        )
        mock_client_instance.enums.PriceExtensionPriceQualifierEnum.FROM = (
            "FROM_ENUM"
        )

        fake_uuid = UUID("abcdef12-1234-5678-1234-567812345678")
        mock_uuid4.return_value = fake_uuid
        customer_id = "test_customer_123"
        expected_asset_name = f"Price Asset #{fake_uuid}"

        mock_offering1 = MagicMock(name="Offering1")
        mock_offering2 = MagicMock(name="Offering2")
        mock_offering3 = MagicMock(name="Offering3")
        mock_create_price_offering_helper.side_effect = [
            mock_offering1,
            mock_offering2,
            mock_offering3,
        ]

        mock_asset_service.mutate_assets.return_value.results = [
            MagicMock(resource_name="price_asset_rn")
        ]

        resource_name = add_prices.create_price_asset(
            mock_client_instance, customer_id
        )

        self.assertEqual(resource_name, "price_asset_rn")
        mock_uuid4.assert_called_once()
        mock_client_instance.get_service.assert_called_once_with("AssetService")
        mock_client_instance.get_type.assert_called_once_with("AssetOperation")

        self.assertEqual(mock_created_asset.name, expected_asset_name)
        self.assertEqual(
            mock_created_asset.tracking_url_template,
            "http://tracker.example.com/?u={lpurl}",
        )

        price_asset_mock = mock_created_asset.price_asset
        self.assertEqual(price_asset_mock.type_, "SERVICES_ENUM")
        self.assertEqual(price_asset_mock.price_qualifier, "FROM_ENUM")
        self.assertEqual(price_asset_mock.language_code, "en")

        price_asset_mock.price_offerings.extend.assert_called_once_with(
            [mock_offering1, mock_offering2, mock_offering3]
        )

        self.assertEqual(mock_create_price_offering_helper.call_count, 3)
        mock_create_price_offering_helper.assert_any_call(
            mock_client_instance,
            "Scrubs",
            "Body Scrub, Salt Scrub",
            "http://www.example.com/scrubs",
            "http://m.example.com/scrubs",
            60000000,
            "USD",
            mock_client_instance.enums.PriceExtensionPriceUnitEnum.PER_HOUR,
        )
        mock_asset_service.mutate_assets.assert_called_once_with(
            customer_id=customer_id, operations=[mock_asset_operation]
        )

    def test_create_price_offering_helper(self):
        mock_client_instance = MagicMock()

        # Case 1: final_mobile_url is provided
        mock_price_offering_obj1 = MagicMock()
        mock_price_offering_obj1.price = MagicMock()
        # Replace final_mobile_url with a PropertyMock to track assignments
        # We need to attach it to the type of the mock object
        prop_mock1 = PropertyMock()
        type(mock_price_offering_obj1).final_mobile_url = (
            prop_mock1  # type() is important
        )

        mock_client_instance.get_type.return_value = mock_price_offering_obj1

        header = "Test Header"
        description = "Test Desc"
        final_url = "http://example.com/final"
        final_mobile_url_val = "http://m.example.com/final"  # Actual value
        price_in_micros = 10000000
        currency_code = "USD"
        unit_enum = "PER_DAY_ENUM"

        offering1 = add_prices.create_price_offering(
            mock_client_instance,
            header,
            description,
            final_url,
            final_mobile_url_val,
            price_in_micros,
            currency_code,
            unit_enum,
        )

        mock_client_instance.get_type.assert_called_once_with("PriceOffering")
        self.assertIs(offering1, mock_price_offering_obj1)
        self.assertEqual(offering1.header, header)
        self.assertEqual(offering1.description, description)
        self.assertEqual(offering1.final_url, final_url)
        prop_mock1.assert_called_once_with(
            final_mobile_url_val
        )  # Check it was set
        self.assertEqual(offering1.price.amount_micros, price_in_micros)
        self.assertEqual(offering1.price.currency_code, currency_code)
        self.assertEqual(offering1.unit, unit_enum)

        # Case 2: final_mobile_url is None
        mock_client_instance.reset_mock()  # Reset client mock for fresh get_type call
        mock_price_offering_obj2 = MagicMock()
        mock_price_offering_obj2.price = MagicMock()
        prop_mock2 = PropertyMock()
        type(mock_price_offering_obj2).final_mobile_url = prop_mock2

        mock_client_instance.get_type.return_value = mock_price_offering_obj2

        offering2 = add_prices.create_price_offering(
            mock_client_instance,
            header,
            description,
            final_url,
            None,  # final_mobile_url is None
            price_in_micros,
            currency_code,
            unit_enum,
        )
        self.assertIs(offering2, mock_price_offering_obj2)
        prop_mock2.assert_not_called()  # Check it was NOT set

    @patch("examples.assets.add_prices.GoogleAdsClient")
    def test_add_asset_to_account(self, mock_google_ads_client_constructor):
        mock_client_instance = mock_google_ads_client_constructor.return_value
        mock_customer_asset_service = MagicMock()
        mock_client_instance.get_service.return_value = (
            mock_customer_asset_service
        )

        mock_customer_asset_operation = MagicMock()
        mock_client_instance.get_type.return_value = (
            mock_customer_asset_operation
        )
        mock_created_customer_asset = mock_customer_asset_operation.create

        mock_client_instance.enums.AssetFieldTypeEnum.PRICE = "PRICE_ENUM"

        customer_id = "test_customer_123"
        price_asset_rn = "price_asset_rn_test"

        mock_customer_asset_service.mutate_customer_assets.return_value.results = [
            MagicMock(resource_name="cust_asset_rn")
        ]

        add_prices.add_asset_to_account(
            mock_client_instance, customer_id, price_asset_rn
        )

        mock_client_instance.get_service.assert_called_once_with(
            "CustomerAssetService"
        )
        mock_client_instance.get_type.assert_called_once_with(
            "CustomerAssetOperation"
        )

        self.assertEqual(mock_created_customer_asset.asset, price_asset_rn)
        self.assertEqual(mock_created_customer_asset.field_type, "PRICE_ENUM")

        mock_customer_asset_service.mutate_customer_assets.assert_called_once_with(
            customer_id=customer_id, operations=[mock_customer_asset_operation]
        )

    @patch("examples.assets.add_prices.add_asset_to_account")
    @patch("examples.assets.add_prices.create_price_asset")
    def test_main_function_logic(self, mock_create_asset, mock_add_to_account):
        mock_client = MagicMock()
        customer_id = "cust_main_logic"
        price_asset_rn = "price_asset_main_rn"
        mock_create_asset.return_value = price_asset_rn

        add_prices.main(mock_client, customer_id)

        mock_create_asset.assert_called_once_with(mock_client, customer_id)
        mock_add_to_account.assert_called_once_with(
            mock_client, customer_id, price_asset_rn
        )


# TestMainExecution class removed.

if __name__ == "__main__":
    unittest.main()
