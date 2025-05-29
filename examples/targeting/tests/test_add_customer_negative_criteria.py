import unittest
from unittest.mock import MagicMock, patch, call
import sys

# Add the examples directory to the system path to import the script
sys.path.append(".")

from examples.targeting.add_customer_negative_criteria import main

class TestAddCustomerNegativeCriteria(unittest.TestCase):
    @patch("examples.targeting.add_customer_negative_criteria.GoogleAdsClient.load_from_storage")
    def test_main_function_calls(self, mock_load_client):
        # Mock customer ID
        MOCK_CUSTOMER_ID = "1234567890"

        # Create a mock GoogleAdsClient
        mock_google_ads_client = MagicMock()
        mock_load_client.return_value = mock_google_ads_client

        # Mock the CustomerNegativeCriterionService
        mock_customer_negative_criterion_service = MagicMock()
        mock_google_ads_client.get_service.return_value = mock_customer_negative_criterion_service

        # Mock the get_type method for CustomerNegativeCriterionOperation
        # In the script, client.get_type is called for "CustomerNegativeCriterionOperation"
        # and then attributes like "create.content_label.type_" or "create.placement.url" are set.
        # We need to ensure that when get_type("CustomerNegativeCriterionOperation") is called,
        # the returned mock can handle further attribute assignments for "create".

        def get_type_side_effect(type_name):
            if type_name == "CustomerNegativeCriterionOperation":
                # Return a new MagicMock each time to ensure operations are distinct
                # and allow "create" attribute to be set on it.
                mock_operation = MagicMock()
                # mock_operation.create = MagicMock() # This might be too early or too specific
                return mock_operation
            return MagicMock() # Default for other types if any

        mock_google_ads_client.get_type.side_effect = get_type_side_effect
        
        # Mock enums that are accessed from the client instance
        ContentLabelTypeEnum = mock_google_ads_client.enums.ContentLabelTypeEnum
        
        # Call the main function
        main(mock_google_ads_client, MOCK_CUSTOMER_ID)

        # Assert that mutate_customer_negative_criteria was called
        mock_customer_negative_criterion_service.mutate_customer_negative_criteria.assert_called_once()

        # Get the arguments passed to mutate_customer_negative_criteria
        args, kwargs = mock_customer_negative_criterion_service.mutate_customer_negative_criteria.call_args
        
        self.assertEqual(kwargs["customer_id"], MOCK_CUSTOMER_ID)
        operations = kwargs["operations"]
        self.assertEqual(len(operations), 2)  # Content Label and Placement

        # --- Verify Content Label Operation ---
        content_label_operation = operations[0]
        # The criterion is directly on the operation's "create" attribute
        created_content_label_criterion = content_label_operation.create
        self.assertEqual(
            created_content_label_criterion.content_label.type_,
            ContentLabelTypeEnum.TRAGEDY,
        )

        # --- Verify Placement Operation ---
        placement_operation = operations[1]
        created_placement_criterion = placement_operation.create
        self.assertEqual(
            created_placement_criterion.placement.url, "http://www.example.com"
        )

if __name__ == "__main__":
    unittest.main()
