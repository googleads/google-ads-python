import unittest
from unittest.mock import MagicMock, patch

from examples.planning import get_ad_group_criterion_cpc_bid_simulations

class TestGetAdGroupCriterionCpcBidSimulations(unittest.TestCase):

    @patch('examples.planning.get_ad_group_criterion_cpc_bid_simulations.GoogleAdsClient.load_from_storage')
    def test_main_get_ad_group_criterion_cpc_bid_simulations(self, mock_load_from_storage):
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_google_ads_service = MagicMock()
        mock_google_ads_client.get_service.return_value = mock_google_ads_service

        # Mock the response from search_stream
        mock_row = MagicMock()
        simulation = mock_row.ad_group_criterion_simulation
        simulation.ad_group_id = 12345
        simulation.criterion_id = 67890
        simulation.start_date = "2023-01-01"
        simulation.end_date = "2023-01-31"

        point1 = MagicMock()
        point1.cpc_bid_micros = 1000000
        point1.clicks = 150.0
        point1.cost_micros = 75000000
        point1.impressions = 5000
        point1.biddable_conversions = 10.0
        point1.biddable_conversions_value = 200.0

        point2 = MagicMock()
        point2.cpc_bid_micros = 2000000
        point2.clicks = 250.0
        point2.cost_micros = 150000000
        point2.impressions = 7000
        point2.biddable_conversions = 20.0
        point2.biddable_conversions_value = 400.0

        simulation.cpc_bid_point_list.points = [point1, point2]

        # search_stream returns an iterator of batches, each batch has results
        mock_batch = MagicMock()
        mock_batch.results = [mock_row]
        mock_google_ads_service.search_stream.return_value = iter([mock_batch])

        test_customer_id = "1234567890"
        test_ad_group_id = "12345" # Matches the ad_group_id in the mock response

        with patch('sys.stdout', new_callable=MagicMock) as mock_stdout:
            get_ad_group_criterion_cpc_bid_simulations.main(
                mock_google_ads_client, test_customer_id, test_ad_group_id
            )

        # mock_load_from_storage.assert_called_once_with(version="v19") # This is removed as client is injected
        mock_google_ads_client.get_service.assert_called_once_with("GoogleAdsService")

        # Construct the expected query
        expected_query = f"""
        SELECT
          ad_group_criterion_simulation.ad_group_id,
          ad_group_criterion_simulation.criterion_id,
          ad_group_criterion_simulation.start_date,
          ad_group_criterion_simulation.end_date,
          ad_group_criterion_simulation.cpc_bid_point_list.points
        FROM ad_group_criterion_simulation
        WHERE
          ad_group_criterion_simulation.type = CPC_BID
          AND ad_group_criterion_simulation.ad_group_id = {test_ad_group_id}"""
        mock_google_ads_service.search_stream.assert_called_once_with(
            customer_id=test_customer_id, query=expected_query
        )

        output = "".join(call_args[0][0] for call_args in mock_stdout.write.call_args_list if call_args[0])

        self.assertIn(f"ad group ID {simulation.ad_group_id}", output)
        self.assertIn(f"criterion ID {simulation.criterion_id}", output)
        self.assertIn(f"start date {simulation.start_date}", output)
        self.assertIn(f"end date {simulation.end_date}", output)

        self.assertIn(f"bid: {point1.cpc_bid_micros} => clicks: {point1.clicks}", output)
        self.assertIn(f"cost: {point1.cost_micros}", output)
        self.assertIn(f"impressions: {point1.impressions}", output)
        self.assertIn(f"biddable conversions: {point1.biddable_conversions}", output)
        self.assertIn(f"biddable conversions value: {point1.biddable_conversions_value}", output)

        self.assertIn(f"bid: {point2.cpc_bid_micros} => clicks: {point2.clicks}", output)

if __name__ == "__main__":
    unittest.main()
