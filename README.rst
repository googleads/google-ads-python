Google Ads API Client Library for Python
========================================

This project hosts the Python client library for the Google Ads API.

Build Status
------------
|build-status|

Requirements
------------
* Python 3.7+

Note that Python 3.7 is deprecated in this package, and it will become fully
incompatible in a future version. Please upgrade to Python 3.8 or higher to
ensure you can continue using this package to access the Google Ads API.

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

Minimum Dependency Versions
---------------------------
Version `21.2.0`_ of this library *lowered* the minimum version for some
dependencies in order to improve compatibility with other applications and
packages that rely on `protobuf`_ version 3.

Note that using protobuf 3 will cause performance degredations in this library,
so you may experience slower response times. For optimal performance we
recommend using protobuf versions 4.21.5 or higher.

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
.. _14.0.0: https://pypi.org/project/google-ads/14.0.0/
.. _21.2.0: https://pypi.org/project/google-ads/21.2.0/
.. _Protobuf Messages: https://developers.google.com/google-ads/api/docs/client-libs/python/protobuf-messages
.. _protobuf: https://pypi.org/project/protobuf/
