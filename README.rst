Google Ads API Client Library for Python
========================================

This project hosts the Python client library for the Google Ads API.

Features
--------
* Distributed via PyPI.
* Easy management of credentials.
* Easy creation of Google Ads API service clients.

Requirements
------------
* Python 2.7.13+ / 3.5.3+
* `pip`_


Getting started
---------------

Installation
############

This library is distributed via PyPI. If you have not already done so, install
`pip`_, the following command to install this client library:

.. code-block::

  pip install google-ads

Configuration file setup
########################

To authenticate your API calls, you must specify your **client ID**,
**client secret**, **refresh token**, and **developer token**. If you have not
yet created a client ID, see the `Authorization guide`_ and the
`authentication samples`_ to get started. Likewise, see
`Obtain your developer token`_ if you do not yet have one.

When initializing a `GoogleAdsClient` instance via the `load_from_storage`
class method, the default behavior is to load a configuration file named
**google-ads.yaml** located in your home directory. Included in this repository
is a `template`_ you can use.

Create a GoogleAdsClient
########################

You can run the following to retrieve a `GoogleAdsClient` instance using a
configuration file named **google-ads.yaml** stored in your home directory:

.. code-block:: python

  client = google.ads.google_ads.client.GoogleAdsClient.load_from_storage()

Get types and service clients
#############################
You can use a `GoogleAdsClient` instance to retrieve any type or service used
by the API. To retrieve a type such as a `CampaignOperation`, provide its name
to the `get_type` method:

.. code-block:: python

  campaign_operation = client.get_type('CampaignOperation')

Likewise, you can provide the name of a service to `get_service` in order to
retrieve the corresponding service client instance:

.. code-block:: python

  google_ads_service = client.get_service('GoogleAdsService')

Miscellaneous
-------------

* `Wiki`_
* `Issue tracker`_
* `API documentation`_
* `API Support`_

Authors
-------

* `Mark Saniscalchi`_
* `David Wihl`_

.. _pip: https://pip.pypa.io/en/stable/installing
.. _template: https://github.com/googleads/google-ads-python/blob/master/google-ads.yaml
.. _Authorization guide: https://developers.google.com/google-ads/api/docs/oauth/overview
.. _authentication samples: https://github.com/googleads/google-ads-python/blob/master/examples/authentication
.. _Obtain your developer token: https://developers.google.com/google-ads/api/docs/first-call/dev-token
.. _Wiki: https://github.com/googleads/google-ads-python/wiki
.. _Issue tracker: https://github.com/googleads/google-ads-python/issues
.. _API documentation: https://developers.google.com/google-ads/api/
.. _API Support: https://developers.google.com/adwords/api/community/
.. _Mark Saniscalchi: https://github.com/msaniscalchi
.. _David Wihl: https://github.com/wihl

