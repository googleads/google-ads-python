import unittest
from unittest.mock import patch, MagicMock, call

from examples.basic_operations import update_ad_group

class TestUpdateAdGroup(unittest.TestCase):

    @patch("examples.basic_operations.update_ad_group.argparse.ArgumentParser")
    @patch("examples.basic_operations.update_ad_group.GoogleAdsClient.load_from_storage")
    def test_main(self, mock_load_from_storage, mock_argument_parser):
        # Mock the GoogleAdsClient
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client

        # Mock the AdGroupService
        mock_ad_group_service = MagicMock()
        mock_google_ads_client.get_service.return_value = mock_ad_group_service

        # Mock client.get_type for AdGroupOperation and FieldMask
        mock_ad_group_operation_type = MagicMock()
        # mock_field_mask_utils = MagicMock() # FieldMaskUtil is a utility, not a type from client.get_type

        def get_type_side_effect(type_name, version=None):
            if type_name == "AdGroupOperation":
                return mock_ad_group_operation_type
            # FieldMask is usually part of google.protobuf.field_mask_pb2 directly or through helpers
            # For this test, direct construction or a simple mock might be enough if client.get_type("FieldMask") isn't used.
            # If it is, it needs to be added here.
            raise ValueError(f"Unexpected type: {type_name}")
        mock_google_ads_client.get_type.side_effect = get_type_side_effect

        # Patch FieldMaskUtil if it's imported and used directly by the example
        # This assumes FieldMaskUtil is being used as `client.field_mask_util.with_ただ`
        # If it's `from google.protobuf import field_mask_pb2` and then `field_mask_pb2.FieldMask(paths=...)`
        # then that path needs to be patched or the object constructed.
        # For simplicity, we'll assume the example script might construct FieldMask directly or uses a helper
        # that doesn't need complex mocking for this unit test's focus.
        # The core is to check the operation passed to mutate_ad_groups.

        # Mock command line arguments
        mock_args = MagicMock()
        mock_args.customer_id = "1234567890"
        mock_args.ad_group_id = "ADGROUPID1"
        mock_args.cpc_bid_micro_amount = 1000000 # 1 an ad_group_id
        mock_argument_parser.return_value.parse_args.return_value = mock_args

        ad_group_resource_name = f"customers/{mock_args.customer_id}/adGroups/{mock_args.ad_group_id}"

        # Mock the response for AdGroupService.mutate_ad_groups
        mock_mutate_response = MagicMock()
        mock_mutate_result = MagicMock()
        mock_mutate_result.resource_name = ad_group_resource_name
        mock_mutate_response.results = [mock_mutate_result]
        mock_ad_group_service.mutate_ad_groups.return_value = mock_mutate_response

        # Call the main function of the example script
        with patch("builtins.print") as mock_print,              patch("google.ads.googleads.client.GoogleAdsClient.get_type") as mock_get_type_on_instance:
            # Mocking get_type on the instance of the client used in main
            mock_ad_group_type_instance = MagicMock()
            mock_ad_group_type_instance.resource_name = ad_group_resource_name

            def get_type_instance_side_effect(type_name):
                if type_name == "AdGroup":
                    return mock_ad_group_type_instance
                elif type_name == "AdGroupOperation":
                    return MagicMock() # Return a fresh mock for the operation itself
                raise ValueError(f"Unexpected type for instance: {type_name}")
            mock_get_type_on_instance.side_effect = get_type_instance_side_effect

            # Patching FieldMaskUtil if it's from google.protobuf.field_mask_pb2
            # This depends on how FieldMaskUtil is used in the actual example script
            # For now, we assume the operation is constructed and FieldMask is part of it
            with patch("google.protobuf.field_mask_pb2.FieldMask") as mock_field_mask:
                update_ad_group.main(mock_google_ads_client, mock_args.customer_id,
                                     mock_args.ad_group_id, mock_args.cpc_bid_micro_amount)

        # Assertions
        mock_load_from_storage.assert_called_once_with(version="v19")
        mock_google_ads_client.get_service.assert_called_once_with("AdGroupService")

        # Check that get_type was called for AdGroupOperation and AdGroup on the client instance
        mock_get_type_on_instance.assert_any_call("AdGroupOperation")
        mock_get_type_on_instance.assert_any_call("AdGroup")


        self.assertEqual(mock_ad_group_service.mutate_ad_groups.call_count, 1)
        args_mutate, kwargs_mutate = mock_ad_group_service.mutate_ad_groups.call_args

        self.assertEqual(kwargs_mutate['customer_id'], mock_args.customer_id)

        operation = kwargs_mutate['operations'][0]
        # Check the update field of the operation
        self.assertEqual(operation.update.resource_name, ad_group_resource_name)
        self.assertEqual(operation.update.cpc_bid_micros, mock_args.cpc_bid_micro_amount)

        # Check that FieldMask was called correctly (paths might vary based on actual update)
        # This assumes FieldMask is created with paths=['cpc_bid_micros']
        mock_field_mask.assert_called_once_with(paths=['cpc_bid_micros'])
        self.assertEqual(operation.update_mask, mock_field_mask.return_value)

        # Verify print output
        expected_print_call = call(
            f"Ad group with resource name '{ad_group_resource_name}' was updated."
        )
        mock_print.assert_has_calls([expected_print_call])

if __name__ == "__main__":
    unittest.main()
