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

Protobuf Messages
-----------------
Version `14.0.0`_ of this library introduced the **required** `use_proto_plus`
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
* `Bob Hancock`_

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
.. _Bob Hancock: https://github.com/bobhancock
.. _12.0.0: https://pypi.org/project/google-ads/12.0.0/
.. _14.0.0: https://pypi.org/project/google-ads/14.0.0/
.. _15.0.0: https://pypi.org/project/google-ads/15.0.0/
.. _v9: https://developers.google.com/google-ads/api/reference/rpc/v9/overview
.. _v10: https://developers.google.com/google-ads/api/reference/rpc/v10/overview
.. _EOL: https://endoflife.date/python
.. _Google Ads Developer Blog: https://ads-developers.googleblog.com/
.. _Protobuf Messages: https://developers.google.com/google-ads/api/docs/client-libs/python/protobuf-messages
