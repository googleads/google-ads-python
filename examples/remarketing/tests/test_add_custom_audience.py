import unittest
from unittest.mock import patch, Mock, call, ANY
import io
import sys
from types import SimpleNamespace

from examples.remarketing import add_custom_audience # SUT (System Under Test)

class TestAddCustomAudience(unittest.TestCase):

    # --- Tests for create_custom_audience_member ---
    def test_create_keyword_member(self):
        mock_client = Mock(name="GoogleAdsClientMock_for_helper")
        # Initialize attributes to None so unset ones remain None
        mock_member_obj = Mock(
            name="CustomAudienceMemberInstanceMock_Keyword",
            keyword=None, url=None, app=None
        )
        mock_client.get_type.return_value = mock_member_obj

        mock_member_type_enum_obj = SimpleNamespace(
            KEYWORD="mock_keyword_enum_val", URL="mock_url_enum_val", APP="mock_app_enum_val"
        )
        mock_client.enums = SimpleNamespace(CustomAudienceMemberTypeEnum=mock_member_type_enum_obj)

        member_value = "test keyword"

        created_member = add_custom_audience.create_custom_audience_member(
            mock_client, mock_member_type_enum_obj.KEYWORD, member_value
        )

        mock_client.get_type.assert_called_once_with("CustomAudienceMember")
        self.assertEqual(created_member, mock_member_obj)
        self.assertEqual(created_member.member_type, mock_member_type_enum_obj.KEYWORD)
        self.assertEqual(created_member.keyword, member_value)
        self.assertIsNone(created_member.url, "URL should be None for KEYWORD type")
        self.assertIsNone(created_member.app, "App should be None for KEYWORD type")


    def test_create_url_member(self):
        mock_client = Mock(name="GoogleAdsClientMock_for_helper")
        mock_member_obj = Mock(
            name="CustomAudienceMemberInstanceMock_URL",
            keyword=None, url=None, app=None
        )
        mock_client.get_type.return_value = mock_member_obj

        mock_member_type_enum_obj = SimpleNamespace(
            KEYWORD="mock_keyword_enum_val", URL="mock_url_enum_val", APP="mock_app_enum_val"
        )
        mock_client.enums = SimpleNamespace(CustomAudienceMemberTypeEnum=mock_member_type_enum_obj)
        member_value = "http://example.com"

        created_member = add_custom_audience.create_custom_audience_member(
            mock_client, mock_member_type_enum_obj.URL, member_value
        )

        mock_client.get_type.assert_called_once_with("CustomAudienceMember")
        self.assertEqual(created_member, mock_member_obj)
        self.assertEqual(created_member.member_type, mock_member_type_enum_obj.URL)
        self.assertEqual(created_member.url, member_value)
        self.assertIsNone(created_member.keyword, "Keyword should be None for URL type")
        self.assertIsNone(created_member.app, "App should be None for URL type")

    def test_create_app_member(self):
        mock_client = Mock(name="GoogleAdsClientMock_for_helper")
        mock_member_obj = Mock(
            name="CustomAudienceMemberInstanceMock_App",
            keyword=None, url=None, app=None
        )
        mock_client.get_type.return_value = mock_member_obj

        mock_member_type_enum_obj = SimpleNamespace(
            KEYWORD="mock_keyword_enum_val", URL="mock_url_enum_val", APP="mock_app_enum_val"
        )
        mock_client.enums = SimpleNamespace(CustomAudienceMemberTypeEnum=mock_member_type_enum_obj)
        member_value = "com.example.app"

        created_member = add_custom_audience.create_custom_audience_member(
            mock_client, mock_member_type_enum_obj.APP, member_value
        )

        mock_client.get_type.assert_called_once_with("CustomAudienceMember")
        self.assertEqual(created_member, mock_member_obj)
        self.assertEqual(created_member.member_type, mock_member_type_enum_obj.APP)
        self.assertEqual(created_member.app, member_value)
        self.assertIsNone(created_member.keyword, "Keyword should be None for APP type")
        self.assertIsNone(created_member.url, "URL should be None for APP type")

    def test_create_invalid_member_type(self):
        mock_client = Mock(name="GoogleAdsClientMock_for_helper")
        # The SUT calls get_type before checking member_type, so mock its return value
        mock_client.get_type.return_value = Mock(keyword=None, url=None, app=None)


        mock_member_type_enum_obj = SimpleNamespace(
            KEYWORD="mock_keyword_enum_val", URL="mock_url_enum_val", APP="mock_app_enum_val"
        )
        mock_client.enums = SimpleNamespace(CustomAudienceMemberTypeEnum=mock_member_type_enum_obj)

        invalid_enum_value_to_pass = "MOCK_INVALID_ENUM_VALUE_PASSED"
        member_value = "some value"

        expected_error_msg = "The member type must be a MemberTypeEnum value of KEYWORD, URL, or APP"
        with self.assertRaisesRegex(ValueError, expected_error_msg):
            add_custom_audience.create_custom_audience_member(
                mock_client, invalid_enum_value_to_pass, member_value
            )
        mock_client.get_type.assert_called_once_with("CustomAudienceMember")


    # --- Test for main function ---
    @patch('examples.remarketing.add_custom_audience.create_custom_audience_member')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_success_path(self, mock_stdout, mock_create_member_func):
        mock_googleads_client = Mock(name="GoogleAdsClientMock_for_main")

        enums_holder = Mock(name="EnumsHolder")
        enums_holder.CustomAudienceTypeEnum = SimpleNamespace(SEARCH="mock_search_type_value")
        enums_holder.CustomAudienceStatusEnum = SimpleNamespace(ENABLED="mock_enabled_status_value")
        enums_holder.CustomAudienceMemberTypeEnum = SimpleNamespace(
            KEYWORD="mock_keyword_enum_for_main",
            URL="mock_url_enum_for_main",
            APP="mock_app_enum_for_main"
        )
        mock_googleads_client.enums = enums_holder

        mock_custom_audience_service = Mock(name="CustomAudienceServiceMock")
        mock_googleads_client.get_service.return_value = mock_custom_audience_service

        mock_ca_operation = Mock(name="CustomAudienceOperationMock")
        mock_custom_audience_obj = Mock(name="CustomAudienceObjMock")
        mock_custom_audience_obj.members = []
        mock_ca_operation.create = mock_custom_audience_obj

        mock_googleads_client.get_type.return_value = mock_ca_operation

        mock_members_returned_by_helper = [
            Mock(name=f"MemberFromHelper_{i}") for i in range(5)
        ]
        mock_create_member_func.side_effect = mock_members_returned_by_helper

        mock_mutate_response = Mock(name="MutateCustomAudiencesResponseMock")
        mock_result = Mock(name="CustomAudienceResultMock")
        mock_result.resource_name = "mock_custom_audience_resource_name"
        mock_mutate_response.results = [mock_result]
        mock_custom_audience_service.mutate_custom_audiences.return_value = mock_mutate_response

        test_customer_id = "1234567890"

        add_custom_audience.main(mock_googleads_client, test_customer_id)

        mock_googleads_client.get_service.assert_called_once_with("CustomAudienceService")
        mock_googleads_client.get_type.assert_called_once_with("CustomAudienceOperation")

        expected_helper_calls = [
            call(mock_googleads_client, enums_holder.CustomAudienceMemberTypeEnum.KEYWORD, "mars cruise"),
            call(mock_googleads_client, enums_holder.CustomAudienceMemberTypeEnum.KEYWORD, "jupiter cruise"),
            call(mock_googleads_client, enums_holder.CustomAudienceMemberTypeEnum.URL, "http://www.example.com/locations/mars"),
            call(mock_googleads_client, enums_holder.CustomAudienceMemberTypeEnum.URL, "http://www.example.com/locations/jupiter"),
            call(mock_googleads_client, enums_holder.CustomAudienceMemberTypeEnum.APP, "com.google.android.apps.adwords")
        ]
        mock_create_member_func.assert_has_calls(expected_helper_calls)
        self.assertEqual(mock_create_member_func.call_count, 5)

        mock_custom_audience_service.mutate_custom_audiences.assert_called_once()
        mutate_args = mock_custom_audience_service.mutate_custom_audiences.call_args
        self.assertEqual(mutate_args[1]['customer_id'], test_customer_id)

        op_passed_to_mutate = mutate_args[1]['operations'][0]
        self.assertEqual(op_passed_to_mutate, mock_ca_operation)

        self.assertTrue(mock_custom_audience_obj.name.startswith("Example CustomAudience #"))
        self.assertEqual(mock_custom_audience_obj.description, "Custom audiences who have searched specific terms on Google Search.")
        self.assertEqual(mock_custom_audience_obj.type_, enums_holder.CustomAudienceTypeEnum.SEARCH)
        self.assertEqual(mock_custom_audience_obj.status, enums_holder.CustomAudienceStatusEnum.ENABLED)

        self.assertEqual(len(mock_custom_audience_obj.members), 5)
        for i in range(5):
            self.assertEqual(mock_custom_audience_obj.members[i], mock_members_returned_by_helper[i])

        expected_sut_output = (
            "New custom audience added with resource name: "
            f"'{mock_result.resource_name}'\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_sut_output)


if __name__ == "__main__":
    unittest.main()
