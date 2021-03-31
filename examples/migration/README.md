Google Ads Client Library for Python - Migration examples

This folder contains code examples that illustrate how to migrate from the
AdWords API to the Google Ads API in a step-by-step manner. The following code
examples are provided.


CampaignManagement
This folder contains a code example that shows how to create a Google Ads Search
campaign. The code example does the following operations:

* Create a budget
* Create a campaign
* Create an ad group
* Create text ads
* Create keywords


The code example starts with create_complete_campaign_adwords_api_only.py that
shows the whole functionality developed in AdWords API.
create_complete_campaign_both_apis_phase_1.py through
create_complete_campaign_both_apis_phase_4.py shows how to migrate functionality
incrementally from the AdWords API to the Google Ads API.
create_complete_campaign_googleads_api_only.py shows the code example fully
transformed into using the Google Ads API.

Running the examples:
1. cd into ./migration directory.
2. Run pip install -r requirements.txt to install dependencies.
3. Fill in the required authentication credentials, see
[here](https://github.com/googleads/google-ads-python#configuration-file-setup)
for the Google Ads API client library, and
[here](https://github.com/googleads/googleads-python-lib#getting-started) for
the AdWords client library.
4. Run each example from the command line, providing the required parameters.

