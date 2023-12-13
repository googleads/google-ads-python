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

PYTHON_VERSIONS = ["3.8", "3.9", "3.10", "3.11", "3.12"]

TEST_COMMAND = [
    "coverage",
    "run",
    "--append",
    "-m",
    "unittest",
    "discover",
    "--buffer",
    "-s=tests",
    "-p",
    "*_test.py",
]
COVERAGE_COMMAND = [
    "coverage",
    "report",
    "-m",
    "--omit=.nox/*,examples/*,*/__init__.py",
]
FREEZE_COMMAND = ["python", "-m", "pip", "freeze"]


@nox.session(python=PYTHON_VERSIONS)
def tests(session):
    session.install(".")
    # modules for testing
    session.install(
        "pyfakefs>=5.0.0,<6.0",
        "coverage==6.5.0",
    )
    session.run(*FREEZE_COMMAND)
    session.run(*TEST_COMMAND)
    session.run(*COVERAGE_COMMAND)


# This session runs all the unit tests but with the lowest-possible versions
# of supported dependencies that are published by Google.
@nox.session(python=PYTHON_VERSIONS)
def tests_minimum_dependency_versions(session):
    session.install(".")
    # modules for testing
    session.install(
        "pyfakefs>=5.0.0,<6.0",
        "coverage==6.5.0",
        # Google-published dependencies pinned to the
        # lowest possible version supported.
        "google-api-core==2.13.0",
        "proto-plus==1.22.3",
        "protobuf==4.25.0",
        "google-auth-oauthlib==0.3.0",
        "googleapis-common-protos==1.56.3",
        "grpcio==1.59.0",
        "grpcio-status==1.59.0",
    )
    session.run(*FREEZE_COMMAND)
    session.run(*TEST_COMMAND)
    session.run(*COVERAGE_COMMAND)
