import unittest
from unittest.mock import patch, MagicMock

from google.ads.googleads.client import GoogleAdsClient

# Assuming forecast_reach is importable, otherwise, we might need to adjust sys.path
# For now, let's assume it's in the python path or PYTHONPATH is set up correctly
# If not, we might need:
# import sys
# import os
# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR)) # Adjust based on actual structure
# sys.path.insert(0, PROJECT_ROOT)
from examples.planning import forecast_reach


class TestForecastReach(unittest.TestCase):

    MOCK_CUSTOMER_ID = "1234567890"
    MOCK_LOCATION_ID = "2840"  # US
    MOCK_CURRENCY_CODE = "USD"

    @patch("examples.planning.forecast_reach.GoogleAdsClient.load_from_storage")
    def test_main_flow(self, mock_load_client):
        # Mock the client and service
        mock_google_ads_client = MagicMock(spec=GoogleAdsClient)
        mock_reach_plan_service = MagicMock()
        mock_google_ads_client.get_service.return_value = mock_reach_plan_service
        mock_load_client.return_value = mock_google_ads_client

        # Call the main function with mocks
        # We need to simulate the behavior of the main function's internal calls.
        # The forecast_reach.py script's main calls other functions within it.
        # We will test these functions more directly.

        # --- Test show_plannable_locations ---
        forecast_reach.show_plannable_locations(mock_reach_plan_service)
        mock_reach_plan_service.list_plannable_locations.assert_called_once()

        # Reset mock for the next call if necessary (though for different functions, it's fine)
        mock_reach_plan_service.reset_mock()

        # --- Test show_plannable_products ---
        forecast_reach.show_plannable_products(
            mock_reach_plan_service, self.MOCK_LOCATION_ID
        )
        mock_reach_plan_service.list_plannable_products.assert_called_once_with(
            plannable_location_id=self.MOCK_LOCATION_ID
        )
        mock_reach_plan_service.reset_mock()

        # --- Test forecast_manual_mix (which calls request_reach_curve) ---
        # This is the most complex part due to the request construction.
        # We need to ensure generate_reach_forecast is called with the correct structure.

        # Mock the response for generate_reach_forecast to avoid issues if it expects a return
        mock_reach_plan_service.generate_reach_forecast.return_value = MagicMock()

        forecast_reach.forecast_manual_mix(
            mock_google_ads_client, # main function passes the client
            mock_reach_plan_service,
            self.MOCK_CUSTOMER_ID,
            self.MOCK_LOCATION_ID,
            self.MOCK_CURRENCY_CODE,
            5000000  # budget_micros
        )

        self.assertEqual(mock_load_client.call_args[1]["version"], "v19")
        mock_google_ads_client.get_service.assert_called_with("ReachPlanService", version="v19")

        # Assert generate_reach_forecast was called
        mock_reach_plan_service.generate_reach_forecast.assert_called_once()
        
        # Get the actual request passed to generate_reach_forecast
        call_args = mock_reach_plan_service.generate_reach_forecast.call_args
        request = call_args[1]['request'] # request is a keyword argument

        self.assertEqual(request.customer_id, self.MOCK_CUSTOMER_ID)
        self.assertEqual(request.campaign_duration.duration_micros, 28 * 24 * 60 * 60 * 1000000) # 28 days in micros
        self.assertEqual(request.currency_code, self.MOCK_CURRENCY_CODE)
        self.assertEqual(request.targeting.plannable_location_id, self.MOCK_LOCATION_ID)
        
        # Check planned_products (simplified check for brevity, real one would be more detailed)
        self.assertEqual(len(request.planned_products), 2)
        # Product 1: TrueView
        self.assertEqual(request.planned_products[0].plannable_product_code, "TRUEVIEW_IN_STREAM")
        self.assertEqual(request.planned_products[0].budget_micros, 3500000) # 70% of 5000000
        # Product 2: Bumper
        self.assertEqual(request.planned_products[1].plannable_product_code, "BUMPER")
        self.assertEqual(request.planned_products[1].budget_micros, 1500000) # 30% of 5000000

        # Check targeting details
        # Age ranges
        self.assertTrue(any(age.age_range == forecast_reach.AgeRangeEnum.AGE_RANGE_18_24 for age in request.targeting.age_ranges))
        self.assertTrue(any(age.age_range == forecast_reach.AgeRangeEnum.AGE_RANGE_25_34 for age in request.targeting.age_ranges))
        
        # Genders
        self.assertTrue(any(gender.type == forecast_reach.GenderTypeEnum.FEMALE for gender in request.targeting.genders))
        self.assertTrue(any(gender.type == forecast_reach.GenderTypeEnum.MALE for gender in request.targeting.genders))

        # Devices
        self.assertTrue(any(device.type == forecast_reach.DeviceEnum.DESKTOP for device in request.targeting.devices))
        self.assertTrue(any(device.type == forecast_reach.DeviceEnum.MOBILE for device in request.targeting.devices))
        self.assertTrue(any(device.type == forecast_reach.DeviceEnum.TABLET for device in request.targeting.devices))

    # The main function in forecast_reach.py is `main(client, customer_id)`.
    # We need to test this main entry point as well.
    @patch("examples.planning.forecast_reach.GoogleAdsClient.load_from_storage")
    @patch("examples.planning.forecast_reach.show_plannable_locations")
    @patch("examples.planning.forecast_reach.show_plannable_products")
    @patch("examples.planning.forecast_reach.forecast_manual_mix") # Actually calls forecast_reach_curve internally
    @patch("examples.planning.forecast_reach.forecast_suggested_mix")
    def test_main_function_calls(self, 
                                 mock_forecast_suggested_mix,
                                 mock_forecast_manual_mix,
                                 mock_show_plannable_products,
                                 mock_show_plannable_locations,
                                 mock_load_client):

        mock_google_ads_client = MagicMock(spec=GoogleAdsClient)
        mock_reach_plan_service = MagicMock()
        mock_google_ads_client.get_service.return_value = mock_reach_plan_service
        mock_load_client.return_value = mock_google_ads_client
        
        # Call the actual main function from the script
        forecast_reach.main(mock_google_ads_client, self.MOCK_CUSTOMER_ID)

        # Assertions
        mock_load_client.assert_called_once() # Check if load_from_storage was called by the script's main
        self.assertEqual(mock_load_client.call_args[1]["version"], "v19")

        mock_google_ads_client.get_service.assert_called_with("ReachPlanService", version="v19")

        # Check that the helper functions were called by main
        mock_show_plannable_locations.assert_called_once_with(mock_reach_plan_service)
        
        # The example script calls show_plannable_products with a hardcoded location_id if not provided
        # We need to ensure our test uses the same assumptions or mocks appropriately.
        # The script uses _DEFAULT_LOCATION as "2840" (US)
        _DEFAULT_LOCATION = "2840" # from forecast_reach.py
        _DEFAULT_CURRENCY_CODE = "USD" # from forecast_reach.py
        _DEFAULT_BUDGET_MICROS = 5_000_000 # from forecast_reach.py


        mock_show_plannable_products.assert_called_once_with(
            mock_reach_plan_service, _DEFAULT_LOCATION
        )
        
        mock_forecast_manual_mix.assert_called_once_with(
            mock_google_ads_client,
            mock_reach_plan_service,
            self.MOCK_CUSTOMER_ID,
            _DEFAULT_LOCATION,
            _DEFAULT_CURRENCY_CODE,
            _DEFAULT_BUDGET_MICROS,
        )

        # forecast_suggested_mix is also called in the original script's main
        mock_forecast_suggested_mix.assert_called_once_with(
            mock_google_ads_client,
            mock_reach_plan_service,
            self.MOCK_CUSTOMER_ID,
            _DEFAULT_LOCATION,
            _DEFAULT_CURRENCY_CODE,
            _DEFAULT_BUDGET_MICROS,
            # The following preferences are hardcoded in the example script's main
            # when calling forecast_suggested_mix
            is_trueview_ad_format_enabled=True,
            is_bumper_ad_format_enabled=True,
            is_in_stream_selectable_ad_format_enabled=False,
            is_out_stream_selectable_ad_format_enabled=False,
            is_non_skippable_ad_format_enabled=False
        )


if __name__ == "__main__":
    unittest.main()
