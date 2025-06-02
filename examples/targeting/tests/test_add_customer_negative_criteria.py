import unittest
from unittest.mock import Mock, patch, call
import argparse
import sys

# Assuming the script is in examples.targeting relative to the project root
# Adjust the import path if your structure is different or if running tests from a different CWD
try:
    from examples.targeting import add_customer_negative_criteria
except ImportError:
    # Fallback if the above fails, possibly due to how tests are run
    import add_customer_negative_criteria

# Define a known customer ID for testing
_TEST_CUSTOMER_ID = "1234567890"
# Based on documentation and common Protobuf enum patterns:
# UNSPECIFIED (0), UNKNOWN (1), SEXUALLY_SUGGESTIVE (2), BELOW_THE_FOLD (3),
# PARKED_DOMAIN (4), JUVENILE (5), PROFANITY (6), TRAGEDY (7)
_CONTENT_LABEL_TYPE_TRAGEDY_INT_VALUE = 7


class TestAddCustomerNegativeCriteria(unittest.TestCase):
    @patch("examples.targeting.add_customer_negative_criteria.GoogleAdsClient.load_from_storage")
    def setUp(self, mock_load_from_storage):
        self.mock_google_ads_client = Mock()
        mock_load_from_storage.return_value = self.mock_google_ads_client

        # Mock the CustomerNegativeCriterionService
        self.mock_criterion_service = Mock()
        self.mock_google_ads_client.get_service.return_value = self.mock_criterion_service

        # Mock the enums
        # Directly assign integer value for TRAGEDY
        mock_content_label_type_enum = Mock()
        mock_content_label_type_enum.TRAGEDY = _CONTENT_LABEL_TYPE_TRAGEDY_INT_VALUE
        self.mock_google_ads_client.enums.ContentLabelTypeEnum = mock_content_label_type_enum

        # The script calls client.get_type("CustomerNegativeCriterionOperation") twice.
        # We need to provide two distinct mock operation objects.
        self.mock_tragedy_op = Mock(spec=["create"]) # spec to help catch typos
        self.mock_placement_op = Mock(spec=["create"])

        # Configure client.get_type to return these mocks in sequence.
        # This list will be consumed by successive calls to get_type.
        get_type_side_effects = [
            self.mock_tragedy_op,
            self.mock_placement_op,
        ]
        self.mock_google_ads_client.get_type.side_effect = lambda type_name: (
            get_type_side_effects.pop(0) if type_name == "CustomerNegativeCriterionOperation"
            and get_type_side_effects else Mock() # Default mock for other types
        )

        # Configure the mock service's mutate method to return a mock response
        # This is needed by the print statement in the script's main()
        mock_response = Mock()
        mock_response.results = [Mock()] # Simulate one result for len()
        self.mock_criterion_service.mutate_customer_negative_criteria.return_value = mock_response


    def test_main_logic(self):
        """Tests the core logic of the main function."""
        # Call the main function from the script
        add_customer_negative_criteria.main(
            self.mock_google_ads_client, _TEST_CUSTOMER_ID
        )

        # Assert that get_service was called for CustomerNegativeCriterionService
        self.mock_google_ads_client.get_service.assert_called_once_with(
            "CustomerNegativeCriterionService"
        )

        # Assert that get_type was called twice for "CustomerNegativeCriterionOperation"
        self.assertEqual(self.mock_google_ads_client.get_type.call_count, 2)
        self.mock_google_ads_client.get_type.assert_any_call("CustomerNegativeCriterionOperation")

        # Assert tragedy criterion configuration
        self.assertEqual(
            self.mock_tragedy_op.create.content_label.type_,
            _CONTENT_LABEL_TYPE_TRAGEDY_INT_VALUE,
        )
        # Assert placement criterion configuration
        self.assertEqual(
            self.mock_placement_op.create.placement.url,
            "http://www.example.com",
        )

        # Assert that mutate_customer_negative_criteria was called with both operations
        self.mock_criterion_service.mutate_customer_negative_criteria.assert_called_once_with(
            customer_id=_TEST_CUSTOMER_ID,
            operations=[self.mock_tragedy_op, self.mock_placement_op],
        )

    @patch("examples.targeting.add_customer_negative_criteria.argparse.ArgumentParser")
    @patch("examples.targeting.add_customer_negative_criteria.GoogleAdsClient.load_from_storage")
    @patch("examples.targeting.add_customer_negative_criteria.main")
    def test_main_execution_path(
        self, mock_main_function, mock_load_from_storage, mock_argument_parser
    ):
        """Tests the script's entry point (__name__ == '__main__')."""
        # Mock the ArgumentParser to control command-line arguments
        mock_parser_instance = Mock()
        mock_parser_instance.parse_args.return_value = argparse.Namespace(
            customer_id=_TEST_CUSTOMER_ID,
            # Add other args if your script has more, e.g. config_path
            # For add_customer_negative_criteria.py, it seems only customer_id is mandatory
            google_ads_config_path=None # Assuming default path if not provided
        )
        mock_argument_parser.return_value = mock_parser_instance

        # Mock the GoogleAdsClient.load_from_storage that would be called by the __main__ block
        mock_client_instance_main = Mock()
        mock_load_from_storage.return_value = mock_client_instance_main

        # Configure this client instance like the one in setUp
        mock_main_criterion_service = Mock()
        mock_client_instance_main.get_service.return_value = mock_main_criterion_service

        mock_main_response = Mock()
        mock_main_response.results = [Mock()] # Simulate one result for len()
        mock_main_criterion_service.mutate_customer_negative_criteria.return_value = mock_main_response

        mock_main_tragedy_op = Mock(spec=["create"])
        mock_main_placement_op = Mock(spec=["create"])
        main_get_type_side_effects = [mock_main_tragedy_op, mock_main_placement_op]
        mock_client_instance_main.get_type.side_effect = lambda type_name: (
            main_get_type_side_effects.pop(0) if type_name == "CustomerNegativeCriterionOperation"
            and main_get_type_side_effects else Mock()
        )

        mock_main_content_label_enum = Mock()
        mock_main_content_label_enum.TRAGEDY = _CONTENT_LABEL_TYPE_TRAGEDY_INT_VALUE
        mock_client_instance_main.enums.ContentLabelTypeEnum = mock_main_content_label_enum

        # To test the __main__ block, we can execute the script's contents
        # in a controlled environment. runpy is good for this.
        # We need to ensure that 'if __name__ == "__main__":' block is triggered.

        # Option 1: Using runpy.run_module
        # This is often cleaner if the module can be found by runpy
        import runpy
        # Store original sys.argv
        original_argv = list(sys.argv)
        try:
            # Set up sys.argv as if called from command line
            sys.argv = [
                "add_customer_negative_criteria.py", # Script name
                "--customer_id", _TEST_CUSTOMER_ID,
            ]
            runpy.run_module("examples.targeting.add_customer_negative_criteria", run_name="__main__")
        finally:
            # Restore original sys.argv
            sys.argv = original_argv

        # Assert that main was called by the __main__ block
        mock_main_function.assert_called_once_with(
            mock_client_instance_main, _TEST_CUSTOMER_ID
        )
        # Assert that ArgumentParser was used as expected
        mock_argument_parser.assert_called_once()
        mock_parser_instance.add_argument.assert_any_call(
            "-c", "--customer_id", type=str, required=True, help="The Google Ads customer ID."
        )
        mock_parser_instance.parse_args.assert_called_once()


if __name__ == "__main__":
    unittest.main()
