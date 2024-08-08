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

from setuptools import setup, find_namespace_packages

install_requires = [
    "google-auth-oauthlib >= 0.3.0, < 2.0.0",
    "google-api-core >= 2.13.0, <= 3.0.0",
    "googleapis-common-protos >= 1.56.3, < 2.0.0",
    # NOTE: Source code for grpcio and grpcio-status exist in the same
    # grpc/grpc monorepo and thus these two dependencies should always
    # have the same version range.
    "grpcio >= 1.59.0, < 2.0.0",
    "grpcio-status >= 1.59.0, < 2.0.0",
    "proto-plus >= 1.22.3, < 2.0.0",
    "PyYAML >= 5.1, < 7.0",
    "protobuf >= 4.25.0, < 6.0.0",
]

with open("README.rst", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name="google-ads",
    version="25.0.0",
    author="Google LLC",
    author_email="googleapis-packages@google.com",
    classifiers=[
        "Intended Audience :: Developers",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    description="Client library for the Google Ads API",
    include_package_data=True,
    python_requires=">=3.8, <3.13",
    long_description=long_description,
    install_requires=install_requires,
    extras_require={
        "tests": [
            "nox >= 2020.12.31, < 2022.6",
        ]
    },
    license="Apache 2.0",
    packages=find_namespace_packages(
        include=["google.ads.*"],
        exclude=["examples", "examples.*", "tests", "tests.*"],
    ),
    url="https://github.com/googleads/google-ads-python",
    zip_safe=False,
)
