import unittest
from unittest.mock import patch, MagicMock, call

from examples.basic_operations import search_for_google_ads_fields

class TestSearchForGoogleAdsFields(unittest.TestCase):

    @patch("examples.basic_operations.search_for_google_ads_fields.argparse.ArgumentParser")
    @patch("examples.basic_operations.search_for_google_ads_fields.GoogleAdsClient.load_from_storage")
    def test_main(self, mock_load_from_storage, mock_argument_parser):
        # Mock the GoogleAdsClient
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client

        # Mock the GoogleAdsFieldService
        mock_field_service = MagicMock()
        mock_google_ads_client.get_service.return_value = mock_field_service

        # Mock command line arguments
        mock_args = MagicMock()
        mock_args.query = "SELECT campaign.name FROM campaign" # Example query
        mock_argument_parser.return_value.parse_args.return_value = mock_args

        # Mock the response from GoogleAdsFieldService.search_google_ads_fields
        mock_field1 = MagicMock()
        mock_field1.resource_name = "googleAdsFields/campaign.name"
        mock_field1.name = "campaign.name"
        mock_field1.category = mock_google_ads_client.enums.GoogleAdsFieldCategoryEnum.RESOURCE
        mock_field1.selectable = True
        mock_field1.filterable = True
        mock_field1.sortable = True
        mock_field1.selectable_with = ["ad_group.name", "customer.id"]
        mock_field1.attribute_resources = ["campaign_budget"]
        mock_field1.metrics = ["metrics.clicks", "metrics.impressions"]

        mock_field_service.search_google_ads_fields.return_value = iter([mock_field1]) # search returns an iterator

        # Call the main function of the example script
        with patch("builtins.print") as mock_print:
            search_for_google_ads_fields.main(mock_google_ads_client, mock_args.query)

        # Assertions
        mock_load_from_storage.assert_called_once_with(version="v19")
        mock_google_ads_client.get_service.assert_called_once_with("GoogleAdsFieldService")

        mock_field_service.search_google_ads_fields.assert_called_once_with(query=mock_args.query)

        # Verify print output (simplified, can be more detailed)
        # Note: The script has complex print formatting, so we'll check for key parts.
        mock_print.assert_any_call("Printing results for the following query:")
        mock_print.assert_any_call(mock_args.query)
        mock_print.assert_any_call("----") # Separator
        mock_print.assert_any_call("Results:")
        mock_print.assert_any_call(
            f"Resource Name: {mock_field1.resource_name}
"
            f"Name: {mock_field1.name}
"
            f"Category: {mock_google_ads_client.enums.GoogleAdsFieldCategoryEnum.GoogleAdsFieldCategory.Name(mock_field1.category)}
"
            f"Selectable: {mock_field1.selectable}
"
            f"Filterable: {mock_field1.filterable}
"
            f"Sortable: {mock_field1.sortable}
"
            f"Selectable With: {mock_field1.selectable_with}
"
            f"Attribute Resources: {mock_field1.attribute_resources}
"
            f"Metrics: {mock_field1.metrics}
"
        )


if __name__ == "__main__":
    unittest.main()
