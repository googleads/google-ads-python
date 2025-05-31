import unittest
from unittest.mock import patch, MagicMock
import io
import sys

from examples.account_management import update_user_access
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.v19.services.services.google_ads_service import GoogleAdsServiceClient
from google.ads.googleads.v19.services.services.customer_user_access_service import CustomerUserAccessServiceClient
from google.ads.googleads.v19.enums.types.access_role import AccessRoleEnum
from google.ads.googleads.v19.resources.types.customer_user_access import CustomerUserAccess
from google.ads.googleads.v19.services.types import GoogleAdsRow # For search response
from google.ads.googleads.v19.services.types import SearchGoogleAdsRequest # Corrected path

class TestUpdateUserAccess(unittest.TestCase):

    @patch('examples.account_management.update_user_access.protobuf_helpers.field_mask')
    @patch('examples.account_management.update_user_access.GoogleAdsClient')
    def test_main_updates_user_access(self, mock_google_ads_client_class, mock_field_mask_helper):
        # 1. Setup Mocks
        mock_client_instance = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client_class.load_from_storage.return_value = mock_client_instance

        mock_ga_service = MagicMock(spec=GoogleAdsServiceClient)
        mock_cua_service = MagicMock(spec=CustomerUserAccessServiceClient)

        def get_service_side_effect(service_name):
            if service_name == "GoogleAdsService":
                return mock_ga_service
            elif service_name == "CustomerUserAccessService":
                return mock_cua_service
            raise ValueError(f"Unexpected service requested: {service_name}")
        mock_client_instance.get_service.side_effect = get_service_side_effect

        # Mock client.get_type for operations and requests
        mock_search_request = MagicMock(spec=SearchGoogleAdsRequest)
        mock_cua_operation = MagicMock() # CustomerUserAccessOperation

        def get_type_side_effect(type_name):
            if type_name == "SearchGoogleAdsRequest":
                return mock_search_request
            elif type_name == "CustomerUserAccessOperation":
                return mock_cua_operation
            raise ValueError(f"Unexpected type requested by script: {type_name}")
        mock_client_instance.get_type.side_effect = get_type_side_effect

        # Mock client.enums.AccessRoleEnum
        # The script uses getattr(access_role_enum, access_role_str)
        mock_client_instance.enums = MagicMock()
        mock_client_instance.enums.AccessRoleEnum = AccessRoleEnum.AccessRole # The inner enum with members

        # Mock client.copy_from (used for update_mask)
        mock_client_instance.copy_from = MagicMock()
        mock_field_mask_helper.return_value = MagicMock(paths=["access_role"])


        # --- Mocking for get_user_access phase ---
        customer_id = "customer123"
        email_address_to_find = "user@example.com"
        user_id_to_return = 98765
        original_access_role_enum = AccessRoleEnum.AccessRole.STANDARD
        creation_date_time = "2023-01-01 12:00:00"

        mock_search_row = GoogleAdsRow()
        # Populate mock_search_row.customer_user_access
        mock_search_row.customer_user_access.user_id = user_id_to_return
        mock_search_row.customer_user_access.email_address = email_address_to_find
        mock_search_row.customer_user_access.access_role = original_access_role_enum
        mock_search_row.customer_user_access.access_creation_date_time = creation_date_time

        # google_ads_service.search returns an iterator of rows directly
        mock_ga_service.search.return_value = iter([mock_search_row])


        # --- Mocking for modify_user_access phase ---
        access_role_str_to_set = "ADMIN" # This is what's passed to main
        expected_new_access_role_enum = AccessRoleEnum.AccessRole.ADMIN

        # Mock customer_user_access_path
        expected_cua_resource_name = f"customers/{customer_id}/customerUserAccesses/{user_id_to_return}"
        mock_cua_service.customer_user_access_path.return_value = expected_cua_resource_name

        # Mock mutate_customer_user_access response
        mock_mutate_cua_response = MagicMock()
        mock_mutate_cua_response.result.resource_name = expected_cua_resource_name # Usually same after update
        mock_cua_service.mutate_customer_user_access.return_value = mock_mutate_cua_response

        # 2. Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # 3. Call the main function
        update_user_access.main(mock_client_instance, customer_id, email_address_to_find, access_role_str_to_set)

        # 4. Restore stdout
        sys.stdout = sys.__stdout__

        # 5. Assertions
        # Assert get_service calls
        mock_client_instance.get_service.assert_any_call("GoogleAdsService")
        mock_client_instance.get_service.assert_any_call("CustomerUserAccessService")

        # Assert get_type calls
        mock_client_instance.get_type.assert_any_call("SearchGoogleAdsRequest")
        mock_client_instance.get_type.assert_any_call("CustomerUserAccessOperation")

        # Assertions for get_user_access (search call)
        mock_ga_service.search.assert_called_once_with(request=mock_search_request)
        self.assertEqual(mock_search_request.customer_id, customer_id)
        expected_search_query = f"""
        SELECT
          customer_user_access.user_id,
          customer_user_access.email_address,
          customer_user_access.access_role,
          customer_user_access.access_creation_date_time
        FROM customer_user_access
        WHERE customer_user_access.email_address LIKE '{email_address_to_find}'"""
        # Compare stripped queries to avoid issues with leading/trailing whitespace
        self.assertEqual(mock_search_request.query.strip(), expected_search_query.strip())

        # Assertions for modify_user_access (mutate call)
        mock_cua_service.customer_user_access_path.assert_called_once_with(customer_id, user_id_to_return)

        mock_client_instance.copy_from.assert_called_once()
        copy_from_args = mock_client_instance.copy_from.call_args[0]
        self.assertEqual(copy_from_args[0], mock_cua_operation.update_mask)
        self.assertEqual(copy_from_args[1], mock_field_mask_helper.return_value)

        mock_cua_service.mutate_customer_user_access.assert_called_once()
        mutate_call_args = mock_cua_service.mutate_customer_user_access.call_args
        self.assertEqual(mutate_call_args.kwargs['customer_id'], customer_id)
        self.assertEqual(mutate_call_args.kwargs['operation'], mock_cua_operation)

        # Verify the updated object's attributes
        self.assertEqual(mock_cua_operation.update.resource_name, expected_cua_resource_name)
        self.assertEqual(mock_cua_operation.update.access_role, expected_new_access_role_enum)

        # Verify printed output
        output = captured_output.getvalue()

        expected_output_get_user = (
            "Customer user access with "
            f"User ID = '{user_id_to_return}', "
            f"Access Role = '{original_access_role_enum.value}', and " # Script prints enum int value
            f"Creation Time = {creation_date_time} "
            f"was found in Customer ID: {customer_id}.\n"
        )
        expected_output_modify_user = (
            "Successfully modified customer user access with resource name: "
            f"{mock_mutate_cua_response.result.resource_name}.\n"
        )
        self.assertIn(expected_output_get_user, output)
        self.assertIn(expected_output_modify_user, output)

if __name__ == "__main__":
    unittest.main()
