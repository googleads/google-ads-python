import unittest
from unittest import mock

# TODO: Ensure tests use Google Ads API v19, e.g., by mocking with
# GoogleAdsClient.load_from_storage(version='v19')
from examples.campaign_management import set_ad_parameters


class TestSetAdParameters(unittest.TestCase):
    @mock.patch("google.ads.googleads.client.GoogleAdsClient.load_from_storage")
    @mock.patch("examples.campaign_management.set_ad_parameters.main")
    def test_smoke(self, mock_main, mock_load_client):
        mock_load_client.return_value = mock.Mock()
        set_ad_parameters.main(
            mock_load_client, "TEST_CUSTOMER_ID", "TEST_AD_GROUP_ID", "TEST_CRITERION_ID"
        )
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
