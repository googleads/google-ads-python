import unittest
from unittest.mock import MagicMock, patch

from google.ads.googleads.client import GoogleAdsClient
# Corrected version to v19
from google.ads.googleads.v19.enums import (
    ConversionActionCategoryEnum,
    ConversionActionStatusEnum,
    ConversionActionTypeEnum,
)
# ConversionOriginEnum was not used in the original script or the test logic for it.
# from google.ads.googleads.v19.enums import ConversionOriginEnum
from google.ads.googleads.v19.resources.types.conversion_action import (
    ConversionAction,
)
# Corrected import path for ConversionActionServiceClient based on grep results
from google.ads.googleads.v19.services.services.conversion_action_service.client import (
    ConversionActionServiceClient,
)
# ConversionActionOperation is a type and should be imported from the types module
from google.ads.googleads.v19.services.types.conversion_action_service import (
    ConversionActionOperation,
)


# Import the main function from the module to be tested
from examples.remarketing.add_conversion_action import main


class TestAddConversionAction(unittest.TestCase):
    @patch("examples.remarketing.add_conversion_action.uuid.uuid4")
    @patch("google.ads.googleads.client.GoogleAdsClient.load_from_storage")
    def test_main_function_calls(
        self, mock_load_from_storage, mock_uuid4
    ):
        # Configure the mock GoogleAdsClient
        mock_google_ads_client = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client.api_version = "v19"  # Corrected API version
        mock_load_from_storage.return_value = mock_google_ads_client

        # Mock the enums used by the script
        # We provide mocks that return the integer values expected by protobuf messages
        mock_conversion_action_type_enum = MagicMock()
        mock_conversion_action_type_enum.UPLOAD_CLICKS = 7  # As per .proto definition

        mock_conversion_action_category_enum = MagicMock()
        mock_conversion_action_category_enum.DEFAULT = 4 # DEFAULT = 4 for ConversionActionCategory

        mock_conversion_action_status_enum = MagicMock()
        mock_conversion_action_status_enum.ENABLED = 2    # ENABLED = 2 for ConversionActionStatus

        mock_enums_obj = MagicMock()
        mock_enums_obj.ConversionActionTypeEnum = mock_conversion_action_type_enum
        mock_enums_obj.ConversionActionCategoryEnum = mock_conversion_action_category_enum
        mock_enums_obj.ConversionActionStatusEnum = mock_conversion_action_status_enum
        mock_google_ads_client.enums = mock_enums_obj

        # Configure the mock ConversionActionService
        mock_conversion_action_service = MagicMock(
            spec=ConversionActionServiceClient  # Corrected spec
        )
        mock_google_ads_client.get_service.return_value = (
            mock_conversion_action_service
        )

        # Mock the get_type method for ConversionActionOperation and other types
        def mock_get_type(type_name, **kwargs): # Add **kwargs to handle potential version args
            if type_name == "ConversionActionOperation":
                mock_op = MagicMock()
                # The 'create' field in ConversionActionOperation is of type ConversionAction.
                # We need to ensure this mock can be assigned to operation.create
                mock_op.create = mock_google_ads_client.get_type("ConversionAction")
                return mock_op
            elif type_name == "ConversionAction":
                # This will be assigned to operation.create
                mock_action = MagicMock(spec=ConversionAction)
                # Explicitly create the value_settings attribute on the mock ConversionAction,
                # as it will be accessed and modified by the script.
                mock_action.value_settings = mock_google_ads_client.get_type("ValueSettings")
                return mock_action
            elif type_name == "ValueSettings":
                # This mock will be assigned to mock_action.value_settings
                return MagicMock()
            elif type_name == "AttributionModelSettings": # Not used by current script
                return MagicMock()
            # Add other types if needed by the script
            return MagicMock()

        mock_google_ads_client.get_type.side_effect = mock_get_type

        # Mock uuid.uuid4() to return a fixed UUID
        mock_uuid4.return_value = "test-uuid"

        # Define a dummy customer ID
        customer_id = "1234567890"

        # Call the main function
        main(mock_google_ads_client, customer_id)

        # Assert that get_service was called for "ConversionActionService"
        mock_google_ads_client.get_service.assert_any_call(
            "ConversionActionService"
        )

        # Assert that mutate_conversion_actions was called once
        self.assertEqual(
            mock_conversion_action_service.mutate_conversion_actions.call_count,
            1,
        )

        # Get the arguments passed to mutate_conversion_actions
        call_args = (
            mock_conversion_action_service.mutate_conversion_actions.call_args
        )
        
        # The method is called with keyword arguments in the script
        # call_args.args would be empty, call_args.kwargs would have the arguments
        self.assertFalse(call_args.args, "mutate_conversion_actions should be called with keyword arguments, not positional ones.")
        self.assertTrue(call_args.kwargs, "mutate_conversion_actions should be called with keyword arguments.")

        passed_customer_id = call_args.kwargs.get('customer_id')
        passed_operations = call_args.kwargs.get('operations')

        self.assertEqual(passed_customer_id, customer_id)
        self.assertIsNotNone(passed_operations, "Operations list was not passed as a keyword argument.")
        self.assertEqual(len(passed_operations), 1)

        # Get the operation and the created conversion action
        operation = passed_operations[0]
        # The 'create' attribute is set on the operation object itself by get_type mock
        created_action = operation.create

        # Assertions for the ConversionAction attributes
        self.assertEqual(
            created_action.name, "Earth to Mars Cruises Conversion test-uuid"
        )
        # Assertions for the ConversionAction attributes using integer values
        self.assertEqual(
            created_action.type_,
            7,  # Corresponds to UPLOAD_CLICKS
        )
        self.assertEqual(
            created_action.category,
            4,  # Corresponds to DEFAULT for ConversionActionCategory
        )
        self.assertEqual(
            created_action.status,
            2,  # Corresponds to ENABLED for ConversionActionStatus
        )
        # For ValueSettings, check if it was set (it's an object)
        self.assertIsNotNone(created_action.value_settings)
        # Check specific attributes of value_settings
        # The script being tested sets these:
        # value_settings.default_value = 15.0
        # value_settings.always_use_default_value = True
        self.assertEqual(created_action.value_settings.default_value, 15.0)
        self.assertTrue(created_action.value_settings.always_use_default_value)


        # The attribute primary_for_goal is not explicitly set in the add_conversion_action.py script for UPLOAD_CLICKS type.
        # It defaults to True for many types, but it's better to assert what's explicitly set or documented as default.
        # For UPLOAD_CLICKS, primary_for_goal is not set in the script.
        # Let's remove this assertion if it's not set, or verify default behavior if critical.
        # After checking the ConversionAction resource type, primary_for_goal is a boolean.
        # If the script doesn't set it, it will take on its default value (often True if not specified).
        # The example script does not set primary_for_goal.
        # self.assertTrue(created_action.primary_for_goal)
        # Let's verify if the mock handles this. If it's not set, it won't be on the mock unless spec is very strict or default values are part of mock.
        # For now, let's remove this line, as it's not explicitly set in the script.


if __name__ == "__main__":
    unittest.main()
