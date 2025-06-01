import unittest
from unittest.mock import patch, Mock, ANY
import io
import sys
from types import SimpleNamespace

from examples.remarketing import add_conversion_action

class TestAddConversionAction(unittest.TestCase):

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_success_path(self, mock_stdout):
        mock_googleads_client = Mock()

        enums_holder = Mock()
        mock_conversion_action_type_enum = SimpleNamespace(UPLOAD_CLICKS="mock_upload_clicks_value")
        mock_conversion_action_category_enum = SimpleNamespace(DEFAULT="mock_default_category_value")
        mock_conversion_action_status_enum = SimpleNamespace(ENABLED="mock_enabled_status_value")

        enums_holder.ConversionActionTypeEnum = mock_conversion_action_type_enum
        enums_holder.ConversionActionCategoryEnum = mock_conversion_action_category_enum
        enums_holder.ConversionActionStatusEnum = mock_conversion_action_status_enum
        mock_googleads_client.enums = enums_holder

        mock_conversion_action_service = Mock()
        mock_googleads_client.get_service.return_value = mock_conversion_action_service

        get_type_mock_method = mock_googleads_client.get_type

        def get_type_side_effect_debug(type_name):
            mock_stdout.write(f"DEBUG_SIDE_EFFECT: get_type called with '{type_name}'\n")
            if type_name == "ConversionActionOperation":
                operation_mock = Mock(name="ConversionActionOperationMock")
                operation_mock.create = Mock(name="ConversionActionMock")
                operation_mock.create.value_settings = Mock(name="ValueSettingsMock")
                return operation_mock

            mock_stdout.write(f"DEBUG_SIDE_EFFECT: Unexpected type_name '{type_name}', returning generic Mock\n")
            return Mock()

        get_type_mock_method.side_effect = get_type_side_effect_debug

        mock_mutate_response = Mock()
        mock_result = Mock()
        mock_result.resource_name = "customers/1234567890/conversionActions/9876543210"
        mock_mutate_response.results = [mock_result]
        mock_conversion_action_service.mutate_conversion_actions.return_value = mock_mutate_response

        test_customer_id = "1234567890" # This is passed to main, but not used in the SUT's print statement

        add_conversion_action.main(mock_googleads_client, test_customer_id)

        # Assertions
        mock_googleads_client.get_service.assert_called_once_with("ConversionActionService")

        mock_stdout.write(f"DEBUG_INTERNAL: mock_googleads_client.get_type.mock_calls: {get_type_mock_method.mock_calls}\n")

        get_type_mock_method.assert_called_once_with("ConversionActionOperation")

        mock_conversion_action_service.mutate_conversion_actions.assert_called_once()
        call_args = mock_conversion_action_service.mutate_conversion_actions.call_args
        self.assertEqual(call_args[1]['customer_id'], test_customer_id)

        operations = call_args[1]['operations']
        self.assertEqual(len(operations), 1)
        created_conversion_action = operations[0].create

        self.assertTrue(created_conversion_action.name.startswith("Earth to Mars Cruises Conversion "))
        self.assertEqual(created_conversion_action.type_, "mock_upload_clicks_value")
        self.assertEqual(created_conversion_action.category, "mock_default_category_value")
        self.assertEqual(created_conversion_action.status, "mock_enabled_status_value")
        self.assertEqual(created_conversion_action.view_through_lookback_window_days, 15)
        self.assertEqual(created_conversion_action.value_settings.default_value, 15.0)
        self.assertEqual(created_conversion_action.value_settings.always_use_default_value, True)

        # Corrected expected_sut_output to match the SUT's actual print statement
        expected_sut_output = (
            f"Created conversion action "
            f'"{mock_result.resource_name}".\n'
        )

        captured_value = mock_stdout.getvalue()
        self.assertIn("DEBUG_SIDE_EFFECT: get_type called with 'ConversionActionOperation'", captured_value)
        self.assertIn("DEBUG_INTERNAL: mock_googleads_client.get_type.mock_calls", captured_value)
        self.assertIn(expected_sut_output, captured_value)

if __name__ == "__main__":
    unittest.main()
