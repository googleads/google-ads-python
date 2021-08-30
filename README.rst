Google Ads API Client Library for Python
========================================

This project hosts the Python client library for the Google Ads API.

Build Status
------------
|build-status|

Requirements
------------
* Python 3.7+

Installation
------------
.. code-block::

  pip install google-ads

Features
--------
* Distributed via PyPI.
* Easy management of credentials.
* Easy creation of Google Ads API service clients.

Documentation
-------------
Please refer to our `Developer Site`_ for documentation on how to install,
configure, and use this client library.

For Python 3.6 Users
--------------------
Version `12.0.0`_ of this library is the last version that is compatible with
Python 3.6. It contains support for `v6`_, `v7`_, and `v8`_ of the Google Ads
API. The newest API version, `v8`_, will be supported until the Spring of 2022.
Given that the `EOL`_ for Python 3.6 is December 23, 2021, we encourage our
users to upgrade to Python 3.7 or above as soon as possible to avoid issues.
Users who cannot upgrade can continue to safely use version `12.0.0`_ until
`v8`_ of the Google Ads API is deprecated. Please follow the
`Google Ads Developer Blog`_ for announcements of the specific deprecation
dates for the above API versions.

Protobuf Messages
-----------------
Version `14.0.0_` of this library introduced the **required** `use_proto_plus`
configuration option that specifies which type of protobuf message to use. For
information on why this flag is important and what the differences are between
the two message types, see the `Protobuf Messages`_ guide.

Miscellaneous
-------------

* `Issue tracker`_
* `API documentation`_
* `API Support`_

Authors
-------

* `Mark Saniscalchi`_
* `David Wihl`_
* `Ben Karl`_
* `Andrew Burke`_
* `Laura Chevalier`_

.. |build-status| image:: https://storage.googleapis.com/gaa-clientlibs/badges/google-ads-python/buildstatus_ubuntu.svg
.. _Developer Site: https://developers.google.com/google-ads/api/docs/client-libs/python/
.. _Issue tracker: https://github.com/googleads/google-ads-python/issues
.. _API documentation: https://developers.google.com/google-ads/api/
.. _API Support: https://developers.google.com/google-ads/api/support
.. _Mark Saniscalchi: https://github.com/msaniscalchi
.. _David Wihl: https://github.com/wihl
.. _Ben Karl: https://github.com/BenRKarl
.. _Andrew Burke: https://github.com/AndrewMBurke
.. _Laura Chevalier: https://github.com/laurachevalier4
.. _12.0.0: https://pypi.org/project/google-ads/12.0.0/
.. _14.0.0: https://pypi.org/project/google-ads/14.0.0/
.. _v6: https://developers.google.com/google-ads/api/reference/rpc/v6/overview
.. _v7: https://developers.google.com/google-ads/api/reference/rpc/v7/overview
.. _v8: https://developers.google.com/google-ads/api/reference/rpc/v8/overview
.. _EOL: https://endoflife.date/python
.. _Google Ads Developer Blog: https://ads-developers.googleblog.com/
.. _Protobuf Messages: https://developers.google.com/google-ads/api/docs/client-libs/python/protobuf-messages
