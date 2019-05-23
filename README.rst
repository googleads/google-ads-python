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
        - **NOTE:** Python 2 support will cease by the end of 2019. See this `blog post`_ for more detail.
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
**client secret**, **refresh token**, **developer token**, and, if
you are authenticating with a manager account, a **login customer id**.
If you have not yet created a client ID, see the `Authorization guide`_
and the `authentication samples`_ to get started. Likewise, see
`Obtain your developer token`_ if you do not yet have one.

When initializing a `GoogleAdsClient` instance via the `load_from_storage`
class method, the default behavior is to load a configuration file named
**google-ads.yaml** located in your home directory. Included in this repository
is a `template`_ you can use.

For a complete walk-through of the OAuth Installed Application flow in Python, 
please refer to `this page of the wiki`_.

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

API versioning
################################
With the release of Google Ads API v1_0 it's now possible to specify an API
version when getting services and types. The ``get_service`` and ``get_type``
client methods accept a second named parameter, ``version`` that refers to a
valid API version. For example, to request an instance of the
``GoogleAdsService`` that uses Google Ads API version ``v1`` use the
following:

.. code-block:: python

  google_ads_service = client.get_service('GoogleAdsService', version='v1')

The currently available list of versions is:

* ``'v1'``

Enabling and Configuring logging
################################
The library uses Python's built in logging framework. You can specify your
configuration via the configuration file; see `google-ads.yaml`_
for an example. The library logs to ``stderr`` by default. You can easily pipe
log messages to a file; when running an example:

.. code-block:: bash

  python example.py args 2> example.log

It's also possible to configure logging programmatically using `Python's
built-in logging library`_ by setting a logging configuration *before*
initializing the client. You can retrieve the client logger instance and
configure it with the following example:

.. code-block:: python

  logging.basicConfig(level=logging.INFO, format='[%(asctime)s - %(levelname)s] %(message).5000s')
  logging.getLogger('google.ads.google_ads.client').setLevel(logging.INFO)

**NOTE:** The client logger is configured when the client is initialized, so if
you have logger configurations in your google-ads.yaml file and you want to
override them programmatically, you will need to call the above lines _before_
initializing the client, otherwise the configuration from yaml will take
precedent as it's provided first.

The client generates logs at a few different levels and you can set your
configuration to see some or all of the below:

+-------------+--------------------------------------------------------------------+---------------------------------------------------------------------------------------+
| Level       | Successful Request                                                 | Failed Request                                                                        |
+=============+====================================================================+=======================================================================================+
| ``DEBUG``   | A detailed log with complete request and response objects as JSON. | None                                                                                  |
+-------------+--------------------------------------------------------------------+---------------------------------------------------------------------------------------+
| ``INFO``    | A concise summary with specific request and response fields.       | A detailed log with complete request and exception objects as JSON.                   |
+-------------+--------------------------------------------------------------------+---------------------------------------------------------------------------------------+
| ``WARNING`` | None                                                               | A concise summary with specific request information, the exception state and message. |
+-------------+--------------------------------------------------------------------+---------------------------------------------------------------------------------------+

Since the Python logging framework ignores log messages that are less severe
than the configured level, setting to ``WARNING`` means you will only see
concise messages related to failed requests, but setting to ``DEBUG`` means
you will see all possible types of logs in the above table.

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
* `Ben Karl`_

.. _pip: https://pip.pypa.io/en/stable/installing
.. _blog post: https://ads-developers.googleblog.com/2019/04/python-2-deprecation-in-ads-api-client.html
.. _template: https://github.com/googleads/google-ads-python/blob/master/google-ads.yaml
.. _this page of the wiki: https://github.com/googleads/google-ads-python/wiki/OAuth-Installed-Application-Flow
.. _Authorization guide: https://developers.google.com/google-ads/api/docs/oauth/overview
.. _authentication samples: https://github.com/googleads/google-ads-python/blob/master/examples/authentication
.. _Obtain your developer token: https://developers.google.com/google-ads/api/docs/first-call/dev-token
.. _google-ads.yaml: https://github.com/googleads/google-ads-python/blob/master/google-ads.yaml
.. _Python's built-in logging library: https://docs.python.org/2/library/logging.html
.. _Wiki: https://github.com/googleads/google-ads-python/wiki
.. _Issue tracker: https://github.com/googleads/google-ads-python/issues
.. _API documentation: https://developers.google.com/google-ads/api/
.. _API Support: https://developers.google.com/google-ads/api/support
.. _Mark Saniscalchi: https://github.com/msaniscalchi
.. _David Wihl: https://github.com/wihl
.. _Ben Karl: https://github.com/BenRKarl
