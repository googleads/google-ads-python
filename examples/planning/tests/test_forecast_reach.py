import unittest
from unittest.mock import MagicMock, patch

# Assuming forecast_reach.py is structured to be importable and its main logic is in functions.
# We might need to adjust this if the script's structure is different.
# For example, if main() directly calls other functions, we might patch those.
from examples.planning import forecast_reach

class TestForecastReach(unittest.TestCase):

    @patch('examples.planning.forecast_reach.GoogleAdsClient.load_from_storage')
    def test_main_forecast_reach(self, mock_load_from_storage):
        # Mock the GoogleAdsClient and its services
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client

        # Mock the ReachPlanService
        mock_reach_plan_service = MagicMock()
        mock_google_ads_client.get_service.return_value = mock_reach_plan_service

        # Mock the responses from ReachPlanService
        # list_plannable_locations response
        mock_plannable_locations_response = MagicMock()
        mock_plannable_locations_response.plannable_locations = [
            MagicMock(name="Location1", id="123", parent_country_id="321"),
            MagicMock(name="Location2", id="456", parent_country_id="654")
        ]
        # list_plannable_products response
        mock_plannable_products_response = MagicMock()
        mock_product_metadata = MagicMock()
        mock_product_metadata.plannable_product_code = "YOUTUBE_REACH"
        mock_product_metadata.plannable_product_name = "YouTube Reach"
        mock_product_metadata.plannable_targeting.age_ranges = [MagicMock(name="AGE_RANGE_18_24")]
        mock_product_metadata.plannable_targeting.genders = [MagicMock(type_=MagicMock(name="GENDER_FEMALE"))]
        mock_product_metadata.plannable_targeting.devices = [MagicMock(type_=MagicMock(name="DEVICE_MOBILE"))]
        mock_plannable_products_response.product_metadata = [mock_product_metadata]
        # generate_reach_forecast response
        mock_reach_forecast_response = MagicMock()
        mock_reach_curve = MagicMock()
        mock_forecast_point = MagicMock()
        mock_forecast_point.cost_micros = 10000000 # e.g., 10 units of currency
        mock_forecast_point.forecast.on_target_reach = 100000
        mock_forecast_point.forecast.on_target_impressions = 150000
        mock_forecast_point.forecast.total_reach = 120000
        mock_forecast_point.forecast.total_impressions = 180000
        mock_planned_product_reach_forecast = MagicMock()
        mock_planned_product_reach_forecast.plannable_product_code = "YOUTUBE_REACH"
        mock_planned_product_reach_forecast.cost_micros = 10000000
        mock_forecast_point.planned_product_reach_forecasts = [mock_planned_product_reach_forecast]
        mock_reach_curve.reach_forecasts = [mock_forecast_point]
        mock_reach_forecast_response.reach_curve = mock_reach_curve

        # Configure side_effects or return_values for service calls
        mock_reach_plan_service.list_plannable_locations.return_value = mock_plannable_locations_response
        mock_reach_plan_service.list_plannable_products.return_value = mock_plannable_products_response
        mock_reach_plan_service.generate_reach_forecast.return_value = mock_reach_forecast_response

        # Mock enums (this might be more complex depending on actual usage)
        mock_enums = MagicMock()
        mock_enums.ReachPlanAgeRangeEnum.AGE_RANGE_18_65_UP = "AGE_RANGE_18_65_UP"
        mock_enums.GenderTypeEnum.FEMALE = "FEMALE"
        mock_enums.GenderTypeEnum.MALE = "MALE"
        mock_enums.DeviceEnum.DESKTOP = "DESKTOP"
        mock_enums.DeviceEnum.MOBILE = "MOBILE"
        mock_enums.DeviceEnum.TABLET = "TABLET"
        mock_google_ads_client.enums = mock_enums

        # Call the main function of forecast_reach.py
        # We need a customer_id for this test
        test_customer_id = "1234567890"

        # Capture stdout to check output
        with patch('sys.stdout', new_callable=MagicMock) as mock_stdout:
            forecast_reach.main(mock_google_ads_client, test_customer_id)

        # Assert that the main logic was called (e.g., services were used)
        # mock_load_from_storage.assert_called_once_with(version="v19") # This is removed as client is injected
        mock_google_ads_client.get_service.assert_any_call("ReachPlanService")

        # Assert that the service methods were called
        mock_reach_plan_service.list_plannable_locations.assert_called_once()
        mock_reach_plan_service.list_plannable_products.assert_called_once()
        # generate_reach_forecast is called by request_reach_curve, which is called by forecast_manual_mix
        mock_reach_plan_service.generate_reach_forecast.assert_called_once()

        # Example assertion on output (very basic, might need more specific checks)
        # This checks if "Plannable Locations" was printed by show_plannable_locations
        self.assertTrue(any("Plannable Locations" in call_args[0][0] for call_args in mock_stdout.write.call_args_list if call_args[0]))
        # This checks if "Plannable Products for Location ID" was printed by show_plannable_products
        self.assertTrue(any("Plannable Products for Location ID" in call_args[0][0] for call_args in mock_stdout.write.call_args_list if call_args[0]))
        # This checks if "Currency, Cost, On-Target Reach" header was printed by request_reach_curve
        self.assertTrue(any("Currency, Cost, On-Target Reach" in call_args[0][0] for call_args in mock_stdout.write.call_args_list if call_args[0]))


if __name__ == "__main__":
    unittest.main()
