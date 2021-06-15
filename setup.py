# Copyright 2018 Google LLC
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
"""A setup module for the Google Ads API client library."""

from setuptools import setup, find_packages
import io

install_requires = [
    "dataclasses >= 0.6, < 1.0.0; python_version < '3.7'",
    "google-auth-oauthlib >= 0.3.0, < 1.0.0",
    "google-api-core >= 1.21.0, < 2.0.0",
    "googleapis-common-protos >= 1.5.8, < 2.0.0",
    "grpcio >= 1.33.2, < 2.0.0",
    "proto-plus >= 1.18.0, < 2.0.0",
    "PyYAML >= 5.1, < 6.0",
    "setuptools >= 40.3.0",
    "pep562 >= 1.0, < 2.0",
    "nox == 2020.12.31",
]

with io.open("README.rst", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()


setup(
    name="google-ads",
    version="12.0.0",
    author="Google LLC",
    author_email="googleapis-packages@google.com",
    classifiers=[
        "Intended Audience :: Developers",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    description="Client library for the Google Ads API",
    include_package_data=True,
    python_requires=">=3.6",
    long_description=long_description,
    install_requires=install_requires,
    license="Apache 2.0",
    packages=find_packages(
        exclude=["examples", "examples.*", "tests", "tests.*"]
    ),
    namespace_packages=["google", "google.ads"],
    url="https://github.com/googleads/google-ads-python",
    zip_safe=False,
)
