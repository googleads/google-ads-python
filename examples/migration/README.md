Google Ads Client Library for Python - Migration examples

This folder contains code examples that illustrate how to migrate from the AdWords API to the Google Ads API in a step-by-step manner. The following code examples are provided.


CampaignManagement
This folder contains a code example that shows how to create a Google Ads Search campaign. The code example does the following operations:

Create a budget
Create a campaign
Create an ad group
Create text ads
Create keywords


The code example starts with CreateCompleteCampaignAdWordsApiOnly.py that shows the whole functionality developed in AdWords API. CreateCompleteCampaignBothApisPhase1.py through CreateCompleteCampaignBothApisPhase4.py shows how to migrate functionality incrementally from the AdWords API to the Google Ads API. CreateCompleteCampaignGoogleAdsApiOnly.py shows the code example fully transformed into using the Google Ads API.

Running the examples: 
1. cd into /migration directory 
2. Run pip install -r requirements.txt to install dependencies. 

Fill in the required authentication credentials and parameters to run the examples from the command line. 
