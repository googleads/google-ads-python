import unittest
from unittest import mock

# TODO: Ensure tests use Google Ads API v19, e.g., by mocking with
# GoogleAdsClient.load_from_storage(version='v19')
from examples.campaign_management import get_all_disapproved_ads


class TestGetAllDisapprovedAds(unittest.TestCase):
    @mock.patch("google.ads.googleads.client.GoogleAdsClient.load_from_storage")
    @mock.patch("examples.campaign_management.get_all_disapproved_ads.main")
    def test_smoke(self, mock_main, mock_load_client):
        mock_load_client.return_value = mock.Mock()
        get_all_disapproved_ads.main(
            mock_load_client, "TEST_CUSTOMER_ID"
        )
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
