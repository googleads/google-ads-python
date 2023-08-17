# Copyright 2022 Google LLC
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

import nox

PYTHON_VERSIONS = ["3.7"]


@nox.session(python=PYTHON_VERSIONS)
def tests(session):
    session.install(".")
    # modules for testing
    session.install(
        "mock>=4.0.3",
        "pyfakefs>=3.5,<3.7",
        "coverage==6.5.0",
    )
    session.run(
        "coverage",
        "run",
        "--append",
        "-m",
        "unittest",
        "discover",
        "-s=tests",
        "-p",
        "*_test.py",
    )
    session.run(
        "coverage", "report", "-m", "--omit=.nox/*,examples/*,*/__init__.py"
    )

# This session runs all the unit tests but with the lowest-possible versions
# of supported dependencies that are published by Google.
@nox.session(python=PYTHON_VERSIONS)
def tests_minimum_dependency_versions(session):
    session.install(".")
    # modules for testing
    session.install(
        "mock>=4.0.3",
        "pyfakefs>=3.5,<3.7",
        "coverage==6.5.0",
        # Google-published dependencies pinned to the
        # lowest possible version supported.
        "google-api-core==2.8.0",
        "proto-plus==1.19.6",
        "protobuf==3.12.0",
        "google-auth-oauthlib==0.3.0",
        "googleapis-common-protos==1.56.0",
        "grpcio==1.38.1",
        "grpcio-status==1.38.1",
    )
    session.run(
        "coverage",
        "run",
        "--append",
        "-m",
        "unittest",
        "discover",
        "-s=tests",
        "-p",
        "*_test.py",
    )
    session.run(
        "coverage", "report", "-m", "--omit=.nox/*,examples/*,*/__init__.py"
    )
