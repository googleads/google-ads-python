import unittest
from unittest.mock import MagicMock, patch, call
import sys
import uuid # Import uuid

# Add the examples directory to the system path
sys.path.insert(0, '../../..')

from examples.error_handling.handle_partial_failure import (
    main,
    create_ad_groups,
    is_partial_failure_error_present,
    print_results,
)
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


class TestHandlePartialFailure(unittest.TestCase):
    @patch("examples.error_handling.handle_partial_failure.create_ad_groups")
    @patch("examples.error_handling.handle_partial_failure.print_results")
    def test_main_success(self, mock_print_results, mock_create_ad_groups):
        mock_client = MagicMock(spec=GoogleAdsClient)
        mock_customer_id = "test_customer_id"
        mock_campaign_id = "test_campaign_id"
        mock_ad_group_response = MagicMock()
        mock_create_ad_groups.return_value = mock_ad_group_response

        main(mock_client, mock_customer_id, mock_campaign_id)

        mock_create_ad_groups.assert_called_once_with(
            mock_client, mock_customer_id, mock_campaign_id
        )
        mock_print_results.assert_called_once_with(mock_client, mock_ad_group_response)

    @patch("examples.error_handling.handle_partial_failure.create_ad_groups")
    @patch("examples.error_handling.handle_partial_failure.print_results")
    @patch("sys.exit") # Mock sys.exit to prevent test termination
    def test_main_google_ads_exception(
        self, mock_sys_exit, mock_print_results, mock_create_ad_groups
    ):
        mock_client = MagicMock(spec=GoogleAdsClient)
        mock_customer_id = "test_customer_id"
        mock_campaign_id = "test_campaign_id"
        mock_google_ads_exception = GoogleAdsException(
            error=MagicMock(),
            failure=MagicMock(errors=[MagicMock(message=MagicMock())]),
            request_id="test_request_id"
        )
        mock_create_ad_groups.side_effect = mock_google_ads_exception

        main(mock_client, mock_customer_id, mock_campaign_id)

        mock_create_ad_groups.assert_called_once_with(
            mock_client, mock_customer_id, mock_campaign_id
        )
        self.assertFalse(mock_print_results.called)
        mock_sys_exit.assert_called_once_with(1)

    @patch("uuid.uuid4") # Patch uuid.uuid4
    def test_create_ad_groups(self, mock_uuid4):
        mock_client = MagicMock(spec=GoogleAdsClient)
        mock_customer_id = "test_customer_id"
        mock_campaign_id = "test_campaign_id"

        mock_ad_group_service = MagicMock()
        mock_campaign_service = MagicMock()
        mock_client.get_service.side_effect = [
            mock_ad_group_service,
            mock_campaign_service,
        ]

        mock_campaign_service.campaign_path.side_effect = [
            "valid_campaign_path",
            "invalid_campaign_path",
        ]

        # Mock AdGroupOperation objects
        mock_ad_group_op1 = MagicMock()
        mock_ad_group_op2 = MagicMock()
        mock_ad_group_op3 = MagicMock()
        mock_client.get_type.side_effect = lambda type_name: {
            "AdGroupOperation": MagicMock(),
            "MutateAdGroupsRequest": MagicMock()
        }[type_name]


        # Configure the create attribute of the mock operations
        mock_op1_create = MagicMock()
        mock_ad_group_op1.create = mock_op1_create
        mock_op2_create = MagicMock()
        mock_ad_group_op2.create = mock_op2_create
        mock_op3_create = MagicMock()
        mock_ad_group_op3.create = mock_op3_create

        # Temporarily mock get_type to return specific operation mocks
        def get_type_side_effect(type_name):
            if type_name == "AdGroupOperation":
                # Return a new mock each time for the operations list
                return MagicMock()
            elif type_name == "MutateAdGroupsRequest":
                return MagicMock()
            raise ValueError(f"Unexpected type: {type_name}")

        mock_client.get_type = MagicMock(side_effect=get_type_side_effect)
        # Need to ensure that the mock_client.get_type("AdGroupOperation").create attributes are set correctly
        # This is a bit tricky because get_type is called multiple times for AdGroupOperation
        # We'll create the operations manually and assign them to the side_effect of client.get_type

        op_mocks = [mock_ad_group_op1, mock_ad_group_op2, mock_ad_group_op3, MagicMock()] # Last one for MutateAdGroupsRequest
        get_type_call_count = 0
        def side_effect_get_type(name):
            nonlocal get_type_call_count
            current_mock = None
            if name == "AdGroupOperation":
                current_mock = op_mocks[get_type_call_count]
            elif name == "MutateAdGroupsRequest":
                current_mock = op_mocks[3] # The MutateAdGroupsRequest mock
            get_type_call_count += 1
            return current_mock

        mock_client.get_type = MagicMock(side_effect=side_effect_get_type)


        mock_uuid_value = "test-uuid"
        mock_uuid4.return_value = mock_uuid_value

        expected_response = MagicMock()
        mock_ad_group_service.mutate_ad_groups.return_value = expected_response

        response = create_ad_groups(mock_client, mock_customer_id, mock_campaign_id)

        self.assertEqual(response, expected_response)
        self.assertEqual(mock_client.get_service.call_count, 2)
        mock_client.get_service.assert_any_call("AdGroupService")
        mock_client.get_service.assert_any_call("CampaignService")
        self.assertEqual(mock_campaign_service.campaign_path.call_count, 2)
        mock_campaign_service.campaign_path.assert_any_call(
            mock_customer_id, mock_campaign_id
        )
        mock_campaign_service.campaign_path.assert_any_call(
            mock_customer_id, 0
        )

        # Check AdGroupOperation creations
        # Check calls to client.get_type("AdGroupOperation")
        # There should be 3 calls for AdGroupOperation, and 1 for MutateAdGroupsRequest
        self.assertEqual(mock_client.get_type.call_count, 4)
        calls_to_get_type = [call("AdGroupOperation"), call("AdGroupOperation"), call("AdGroupOperation"), call("MutateAdGroupsRequest")]
        mock_client.get_type.assert_has_calls(calls_to_get_type, any_order=False)


        # Check that the create attribute was accessed for each AdGroupOperation mock
        self.assertTrue(op_mocks[0].create.called)
        self.assertTrue(op_mocks[1].create.called)
        self.assertTrue(op_mocks[2].create.called)


        # Check names and campaigns (using the .create mocks)
        self.assertEqual(op_mocks[0].create.name, f"Valid AdGroup: {mock_uuid_value}")
        self.assertEqual(op_mocks[0].create.campaign, "valid_campaign_path")

        self.assertEqual(op_mocks[1].create.name, f"Broken AdGroup: {mock_uuid_value}")
        self.assertEqual(op_mocks[1].create.campaign, "invalid_campaign_path")

        self.assertEqual(op_mocks[2].create.name, op_mocks[0].create.name)
        self.assertEqual(op_mocks[2].create.campaign, "valid_campaign_path")


        # Check mutate_ad_groups call
        mutate_request_mock = op_mocks[3] # This is the MutateAdGroupsRequest mock
        self.assertEqual(mutate_request_mock.customer_id, mock_customer_id)
        self.assertEqual(len(mutate_request_mock.operations), 3)
        self.assertTrue(mutate_request_mock.partial_failure)
        mock_ad_group_service.mutate_ad_groups.assert_called_once_with(
            request=mutate_request_mock
        )


    def test_is_partial_failure_error_present_true(self):
        mock_response = MagicMock()
        mock_response.partial_failure_error.code = 1 # Non-zero code

        self.assertTrue(is_partial_failure_error_present(mock_response))

    def test_is_partial_failure_error_present_false(self):
        mock_response = MagicMock()
        mock_response.partial_failure_error.code = 0 # Zero code

        self.assertFalse(is_partial_failure_error_present(mock_response))

    def test_is_partial_failure_error_present_no_error_attribute(self):
        mock_response_no_error_attr = MagicMock()
        # Simulate the partial_failure_error attribute not being present or being None
        del mock_response_no_error_attr.partial_failure_error

        # We expect getattr to return None, and then getattr on None for 'code' to return None
        # which should result in False
        self.assertFalse(is_partial_failure_error_present(mock_response_no_error_attr))

    def test_is_partial_failure_error_present_no_code_attribute(self):
        mock_response_no_code_attr = MagicMock()
        # Simulate partial_failure_error being present but not having a 'code' attribute
        mock_response_no_code_attr.partial_failure_error = MagicMock()
        del mock_response_no_code_attr.partial_failure_error.code

        self.assertFalse(is_partial_failure_error_present(mock_response_no_code_attr))


    @patch("examples.error_handling.handle_partial_failure.is_partial_failure_error_present")
    @patch("builtins.print") # To capture print statements
    def test_print_results_with_partial_failure(
        self, mock_print, mock_is_partial_failure
    ):
        mock_client = MagicMock(spec=GoogleAdsClient)
        mock_response = MagicMock()
        mock_is_partial_failure.return_value = True

        mock_partial_failure_error = MagicMock()
        mock_response.partial_failure_error = mock_partial_failure_error

        # Mock error details
        mock_error_detail1 = MagicMock()
        mock_error_detail1.value = b"serialized_failure1"
        mock_error_detail2 = MagicMock()
        mock_error_detail2.value = b"serialized_failure2"
        mock_partial_failure_error.details = [mock_error_detail1, mock_error_detail2]

        # Mock GoogleAdsFailure deserialization
        mock_failure_message_type = MagicMock()
        mock_client.get_type.return_value = mock_failure_message_type

        mock_failure_object1 = MagicMock()
        mock_error1 = MagicMock()
        mock_error1.location.field_path_elements = [MagicMock(index=0)]
        mock_error1.message = "Error Message 1"
        mock_error1.error_code = "ErrorCode1"
        mock_failure_object1.errors = [mock_error1]

        mock_failure_object2 = MagicMock()
        mock_error2 = MagicMock()
        mock_error2.location.field_path_elements = [MagicMock(index=1)]
        mock_error2.message = "Error Message 2"
        mock_error2.error_code = "ErrorCode2"
        mock_failure_object2.errors = [mock_error2]

        # Ensure deserialize is a static method or part of the type
        mock_google_ads_failure_class = MagicMock()
        mock_google_ads_failure_class.deserialize.side_effect = [
            mock_failure_object1,
            mock_failure_object2,
        ]
        # Patching type() is tricky, so we'll mock the behavior of type(failure_message)
        with patch("builtins.type", return_value=mock_google_ads_failure_class):
            # Mock successful results
            mock_result1 = MagicMock(resource_name="resource1")
            mock_result2 = None # Failed operation
            mock_result3 = MagicMock(resource_name="resource3")
            mock_response.results = [mock_result1, mock_result2, mock_result3]

            print_results(mock_client, mock_response)

        mock_is_partial_failure.assert_called_once_with(mock_response)
        mock_client.get_type.assert_has_calls([call("GoogleAdsFailure"), call("GoogleAdsFailure")])
        mock_google_ads_failure_class.deserialize.assert_has_calls([
            call(b"serialized_failure1"),
            call(b"serialized_failure2"),
        ])

        # Check print calls for errors
        mock_print.assert_any_call("Partial failures occurred. Details will be shown below.\n")
        mock_print.assert_any_call(
            "A partial failure at index 0 occurred \n"
            "Error message: Error Message 1\n"
            "Error code: ErrorCode1"
        )
        mock_print.assert_any_call(
            "A partial failure at index 1 occurred \n"
            "Error message: Error Message 2\n"
            "Error code: ErrorCode2"
        )

        # Check print calls for successful results
        mock_print.assert_any_call("Created ad group with resource_name: resource1.")
        mock_print.assert_any_call("Created ad group with resource_name: resource3.")
        # Ensure the "All operations completed successfully" message was NOT printed
        self.assertNotEqual(mock_print.call_args_list[0][0][0], "All operations completed successfully. No partial failure to show.")


    @patch("examples.error_handling.handle_partial_failure.is_partial_failure_error_present")
    @patch("builtins.print")
    def test_print_results_no_partial_failure(
        self, mock_print, mock_is_partial_failure
    ):
        mock_client = MagicMock(spec=GoogleAdsClient)
        mock_response = MagicMock()
        mock_is_partial_failure.return_value = False

        # Mock successful results
        mock_result1 = MagicMock(resource_name="resource1")
        mock_result2 = MagicMock(resource_name="resource2")
        mock_response.results = [mock_result1, mock_result2]

        print_results(mock_client, mock_response)

        mock_is_partial_failure.assert_called_once_with(mock_response)
        mock_print.assert_any_call(
            "All operations completed successfully. No partial failure to show."
        )
        mock_print.assert_any_call("Created ad group with resource_name: resource1.")
        mock_print.assert_any_call("Created ad group with resource_name: resource2.")
        # Ensure client.get_type was not called for GoogleAdsFailure
        mock_client.get_type.assert_not_called()


if __name__ == "__main__":
    unittest.main()
