import unittest
from unittest import mock
import sys

sys.path.insert(0, '/app') # For subtask environment

# Key import to mock
from examples.advanced_operations import add_display_upload_ad

class TestAddDisplayUploadAd(unittest.TestCase):

    @mock.patch('examples.advanced_operations.add_display_upload_ad.requests.get')
    def test_main_functional(self, mock_requests_get):
        mock_google_ads_client = mock.Mock()
        mock_google_ads_client.version = "v19"

        # Mock the response from requests.get
        mock_response = mock.Mock()
        mock_response.content = b'dummy_zip_data'
        mock_requests_get.return_value = mock_response

        # Mock services
        mock_asset_service = mock.Mock()
        mock_ad_group_ad_service = mock.Mock()
        mock_ad_group_service = mock.Mock() # For ad_group_path

        def get_service_side_effect(service_name, version=None):
            self.assertEqual("v19", version if version else mock_google_ads_client.version)
            if service_name == "AssetService":
                return mock_asset_service
            elif service_name == "AdGroupAdService":
                return mock_ad_group_ad_service
            elif service_name == "AdGroupService":
                return mock_ad_group_service
            self.fail(f"Unexpected service: {service_name}")
        mock_google_ads_client.get_service.side_effect = get_service_side_effect

        # Mock types
        # For AssetOperation
        mock_asset_operation_obj = mock.Mock(name="AssetOperation")
        mock_asset_create_obj = mock.Mock(name="Asset_Create") # This is what operation.create returns
        # The Asset message has a field media_bundle_asset of type MediaBundleAsset
        mock_asset_create_obj.media_bundle_asset = mock.Mock(name="MediaBundleAsset_On_Asset")
        mock_asset_operation_obj.create = mock_asset_create_obj

        # For AdGroupAdOperation
        mock_ad_group_ad_operation_obj = mock.Mock(name="AdGroupAdOperation")
        mock_ad_group_ad_create_obj = mock.Mock(name="AdGroupAd_Create") # This is operation.create
        # AdGroupAd has a field 'ad' of type Ad
        ad_data_mock = mock.Mock(name="Ad_On_AdGroupAd")
        # Ad has a field 'display_upload_ad' of type DisplayUploadAdInfo
        display_upload_ad_info_mock = mock.Mock(name="DisplayUploadAdInfo_On_Ad")
        # DisplayUploadAdInfo has a field 'media_bundle' of type AdMediaBundleAsset
        display_upload_ad_info_mock.media_bundle = mock.Mock(name="AdMediaBundleAsset_On_DisplayUploadAdInfo")
        ad_data_mock.display_upload_ad = display_upload_ad_info_mock
        ad_data_mock.final_urls = [] # Initialize as list for append
        mock_ad_group_ad_create_obj.ad = ad_data_mock
        mock_ad_group_ad_operation_obj.create = mock_ad_group_ad_create_obj


        def get_type_side_effect(type_name, version=None):
            # Version is not typically passed by client.get_type
            if type_name == "AssetOperation":
                return mock_asset_operation_obj
            elif type_name == "AdGroupAdOperation":
                return mock_ad_group_ad_operation_obj
            self.fail(f"Unexpected type: {type_name}")
        mock_google_ads_client.get_type.side_effect = get_type_side_effect

        # Mock enums
        mock_google_ads_client.enums.AssetTypeEnum.MEDIA_BUNDLE = "MEDIA_BUNDLE_ENUM"
        mock_google_ads_client.enums.AdGroupAdStatusEnum.PAUSED = "PAUSED_ENUM"
        mock_google_ads_client.enums.DisplayUploadProductTypeEnum.HTML5_UPLOAD_AD = "HTML5_UPLOAD_AD_ENUM"

        # Mock service responses
        mock_asset_service.mutate_assets.return_value = mock.Mock(results=[mock.Mock(resource_name="test_asset_rn")])
        mock_ad_group_ad_service.mutate_ad_group_ads.return_value = mock.Mock(results=[mock.Mock(resource_name="test_ad_rn")])
        mock_ad_group_service.ad_group_path.return_value = "test_ad_group_path"

        customer_id = "cust123"
        ad_group_id = "ag123"

        add_display_upload_ad.main(mock_google_ads_client, customer_id, ad_group_id)

        # Assertions
        mock_requests_get.assert_called_once_with(add_display_upload_ad.BUNDLE_URL)

        # AssetService assertions
        mock_asset_service.mutate_assets.assert_called_once()
        asset_kwargs = mock_asset_service.mutate_assets.call_args[1] # Use kwargs from call_args
        self.assertEqual(asset_kwargs['customer_id'], customer_id)
        self.assertEqual(asset_kwargs['operations'][0], mock_asset_operation_obj) # Check the operation obj
        # Check attributes on the Asset object (mock_asset_create_obj)
        self.assertEqual(mock_asset_create_obj.type_, "MEDIA_BUNDLE_ENUM")
        self.assertEqual(mock_asset_create_obj.name, "Ad Media Bundle")
        # Check attributes on the nested MediaBundleAsset object
        self.assertEqual(mock_asset_create_obj.media_bundle_asset.data, b'dummy_zip_data')

        # AdGroupAdService assertions
        mock_ad_group_ad_service.mutate_ad_group_ads.assert_called_once()
        ad_kwargs = mock_ad_group_ad_service.mutate_ad_group_ads.call_args[1]
        self.assertEqual(ad_kwargs['customer_id'], customer_id)
        self.assertEqual(ad_kwargs['operations'][0], mock_ad_group_ad_operation_obj) # Check the operation obj
        # Check attributes on AdGroupAd object (mock_ad_group_ad_create_obj)
        self.assertEqual(mock_ad_group_ad_create_obj.status, "PAUSED_ENUM")
        self.assertEqual(mock_ad_group_ad_create_obj.ad_group, "test_ad_group_path")
        # Check attributes on nested Ad object (ad_data_mock)
        self.assertIn("http://example.com/html5", ad_data_mock.final_urls) # Script uses http
        # Check attributes on nested DisplayUploadAdInfo object (display_upload_ad_info_mock)
        self.assertEqual(display_upload_ad_info_mock.display_upload_product_type, "HTML5_UPLOAD_AD_ENUM")
        # Check attributes on nested AdMediaBundleAsset object (display_upload_ad_info_mock.media_bundle)
        self.assertEqual(display_upload_ad_info_mock.media_bundle.asset, "test_asset_rn")

if __name__ == '__main__':
    unittest.main()
