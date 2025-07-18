# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for add_flexible_rule_user_list."""

import unittest
from unittest.mock import patch, MagicMock

from examples.remarketing import add_flexible_rule_user_list


class AddFlexibleRuleUserListTest(unittest.TestCase):
    """Tests for the add_flexible_rule_user_list example."""

    @patch("uuid.uuid4", return_value="12345")
    @patch("google.ads.googleads.client.GoogleAdsClient")
    def test_main(self, mock_client_class, mock_uuid):
        """Tests that the main method runs without errors."""
        mock_client = mock_client_class.load_from_storage.return_value
        customer_id = "123456789"

        mock_user_list_service = MagicMock()
        mock_client.get_service.return_value = mock_user_list_service

        mock_user_list_operation = MagicMock()
        mock_client.get_type.return_value = mock_user_list_operation

        with patch(
            "examples.remarketing.add_flexible_rule_user_list.create_user_list_rule_info_from_url"
        ) as mock_create_rule_info:
            mock_create_rule_info.return_value = MagicMock()
            add_flexible_rule_user_list.main(mock_client, customer_id)

        mock_client.get_service.assert_called_once_with("UserListService")
        user_list_service = mock_client.get_service.return_value
        user_list_service.mutate_user_lists.assert_called_once()

        # Check that the user list was created with the correct properties
        create_request = user_list_service.mutate_user_lists.call_args[1][
            "operations"
        ][0]
        self.assertIn(
            "All visitors to http://example.com/example1 AND "
            "http://example.com/example2 but NOT "
            "http://example.com/example3",
            create_request.create.name,
        )
        self.assertEqual(
            create_request.create.description,
            "Visitors of both http://example.com/example1 AND "
            "http://example.com/example2 but NOT"
            "http://example.com/example3",
        )
        self.assertEqual(
            create_request.create.membership_status,
            mock_client.enums.UserListMembershipStatusEnum.OPEN,
        )

    @patch("google.ads.googleads.client.GoogleAdsClient")
    def test_create_user_list_rule_info_from_url(self, mock_client_class):
        """Tests that the create_user_list_rule_info_from_url method works."""
        mock_client = mock_client_class.load_from_storage.return_value
        url = "http://example.com"

        mock_rule_item = MagicMock()
        mock_rule_item_group = MagicMock()
        mock_rule_info = MagicMock()

        def get_type_side_effect(type_name):
            if type_name == "UserListRuleItemInfo":
                return mock_rule_item
            elif type_name == "UserListRuleItemGroupInfo":
                return mock_rule_item_group
            elif type_name == "UserListRuleInfo":
                return mock_rule_info
            return MagicMock()

        mock_client.get_type.side_effect = get_type_side_effect

        rule_info = add_flexible_rule_user_list.create_user_list_rule_info_from_url(
            mock_client, url
        )

        mock_rule_item_group.rule_items.append.assert_called_once_with(
            mock_rule_item
        )
        mock_rule_info.rule_item_groups.append.assert_called_once_with(
            mock_rule_item_group
        )

        self.assertEqual(rule_info, mock_rule_info)


if __name__ == "__main__":
    unittest.main()
