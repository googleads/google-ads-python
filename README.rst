Google Ads API Client Library for Python
========================================

This project hosts the Python client library for the Google Ads API.

Build Status
------------
|build-status|

Features
--------
* Distributed via PyPI.
* Easy management of credentials.
* Easy creation of Google Ads API service clients.

Requirements
------------
* Python 3.7+
        - **NOTE:** Python 2 support has ceased as of v4.0. See this `blog post`_ for more detail.
* `pip`_


Documentation
-------------
This README has general information to get you started with the library, but more
extensive documentation can be found on our `Developer Site`_.

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
**client secret**, **refresh token**, **developer token**, or, if you
are authenticating via a service account you will instead need to specify
a **path_to_private_key_file** and **delegate_account**. If you
are authenticating with a manager account you will need to provide a
**login customer id** configuration value.

If you have not yet created a client ID, see the `Authorization guide`_
and the `authentication samples`_ to get started. Likewise, see
`Obtain your developer token`_ if you do not yet have one.

When initializing a `GoogleAdsClient` instance via the `load_from_storage`
class method, the default behavior is to load a configuration file named
**google-ads.yaml** located in your home directory. Included in this repository
is a `template`_ you can use.

For a complete walk-through of how to configure this library, please refer
to our `configuration documentation`_.

OAuth2 Options
##############

This client library can authenticate using one of three different OAuth2 flows, either the
`Installed Application Flow`_, the `Web Application Flow`_ or the `Service Account Flow`_.
The Installed Application Flow and Web Application Flow use the same credentials and are
functionally identical in terms of configuring this library. When retrieving the
configuration for these authentication flows, if configuration is present
for _both_ types of flows the library will default to using the Installed/Web Application
Flow. If you wish to use the Service Account Flow you must make sure that the Installed/Web
Application Flow `configuration values`_ are not present in your configuration.

Create a GoogleAdsClient
########################

Using YAML file
***************

You can run the following to retrieve a `GoogleAdsClient` instance using a
configuration file named **google-ads.yaml** stored in your home directory:

.. code-block:: python

  from google.ads.google_ads.client import GoogleAdsClient
  client = GoogleAdsClient.load_from_storage()

Using environment variables
***************************

You can also retrieve it by exporting environment variables.

* Required:

.. code-block:: bash

  export GOOGLE_ADS_DEVELOPER_TOKEN=INSERT_DEVELOPER_TOKEN_HERE

* Required for OAuth2 Installed Application Flow

.. code-block:: bash

  export GOOGLE_ADS_CLIENT_ID=INSERT_OAUTH2_CLIENT_ID_HERE
  export GOOGLE_ADS_CLIENT_SECRET=INSERT_OAUTH2_CLIENT_SECRET_HERE
  export GOOGLE_ADS_REFRESH_TOKEN=INSERT_REFRESH_TOKEN_HERE

* Required for OAuth2 Service Account Flow:

.. code-block:: bash

  export GOOGLE_ADS_PATH_TO_PRIVATE_KEY_FILE=INSERT_PRIVATE_KEY_PATH_HERE
  export GOOGLE_ADS_DELEGATED_ACCOUNT=INSERT_DELEGATED_ACCOUNT_HERE

* Optional:

.. code-block:: bash

  export GOOGLE_ADS_LOGIN_CUSTOMER_ID=INSERT_LOGIN_CUSTOMER_ID_HERE
  export GOOGLE_ADS_LOGGING=INSERT_GOOGLE_ADS_LOGGING

.. _GOOGLE_ADS_LOGGING:

GOOGLE_ADS_LOGGING should be a JSON with logging configuration. Example:

.. code-block:: json

  {"version": 1, "disable_existing_loggers": false, "formatters": {"default_fmt": {"format": "[%(asctime)s - %(levelname)s] %(message).5000s", "datefmt": "%Y-%m-%d %H:%M:%S"}}, "handlers": {"default_handler": {"class": "logging.StreamHandler", "formatter": "default_fmt"}}, "loggers": {"": {"handlers": ["default_handler"], "level": "INFO"}}}


Then run the following to retrieve a GoogleAdsClient instance:

.. code-block:: python

  from google.ads.google_ads.client import GoogleAdsClient
  client = GoogleAdsClient.load_from_env()

The `configuration documentation`_ has more information on how these different
sets of variables are set and retrieved.

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

More details can be found in our `proto getters documentation`_.

API versioning
################################
With the release of Google Ads API v1_0 it's now possible to specify an API
version when getting services and types. The ``get_service`` and ``get_type``
client methods accept a second named parameter, ``version`` that refers to a
valid API version. For example, to request an instance of the
``GoogleAdsService`` that uses Google Ads API version ``v2`` use the
following:

.. code-block:: python

  google_ads_service = client.get_service('GoogleAdsService', version='v2')

The currently available list of versions is:

* ``'v1'``
* ``'v2'``

Enabling and Configuring logging
################################
The library uses Python's built in logging framework. You can specify your
configuration via the configuration file (see `google-ads.yaml`_
for an example) or GOOGLE_ADS_LOGGING_ environment variable.
The library logs to ``stderr`` by default. You can easily pipe
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

.. |build-status| image:: https://storage.googleapis.com/gaa-clientlibs/badges/google-ads-python/buildstatus_ubuntu.png
.. _Developer Site: https://developers.google.com/google-ads/api/docs/client-libs/python/
.. _Installed Application Flow: https://developers.google.com/google-ads/api/docs/client-libs/python/oauth-installed
.. _Web Application Flow: https://developers.google.com/google-ads/api/docs/client-libs/python/oauth-web
.. _Service Account Flow: https://developers.google.com/google-ads/api/docs/client-libs/python/oauth-service
.. _configuration values: https://github.com/googleads/google-ads-python/blob/master/google-ads.yaml#L1
.. _pip: https://pip.pypa.io/en/stable/installing
.. _blog post: https://ads-developers.googleblog.com/2019/04/python-2-deprecation-in-ads-api-client.html
.. _template: https://github.com/googleads/google-ads-python/blob/master/google-ads.yaml
.. _configuration documentation: https://developers.google.com/google-ads/api/docs/client-libs/python/configuration
.. _Authorization guide: https://developers.google.com/google-ads/api/docs/oauth/overview
.. _proto getters documentation: https://developers.google.com/google-ads/api/docs/client-libs/python/proto-getters
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
