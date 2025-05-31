import unittest
from unittest import mock

# TODO: Ensure tests use Google Ads API v19, e.g., by mocking with
# GoogleAdsClient.load_from_storage(version='v19')
from examples.campaign_management import validate_ad


class TestValidateAd(unittest.TestCase):
    @mock.patch("google.ads.googleads.client.GoogleAdsClient.load_from_storage")
    @mock.patch("examples.campaign_management.validate_ad.main")
    def test_smoke(self, mock_main, mock_load_client):
        mock_load_client.return_value = mock.Mock()
        validate_ad.main(
            mock_load_client, "TEST_CUSTOMER_ID", "TEST_AD_GROUP_ID"
        )
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
