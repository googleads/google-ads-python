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
import os
import pathlib


PYTHON_VERSIONS = ["3.9", "3.10", "3.11", "3.12", "3.13"]
PROTOBUF_IMPLEMENTATIONS = ["python", "upb"]

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
TEST_DEPENDENCIES = [
    "pyfakefs>=5.0.0,<6.0",
    "coverage==6.5.0",
]
CURRENT_DIR = pathlib.Path(__file__).parent.absolute()
CONSTRAINTS_DIR = os.path.join(CURRENT_DIR, "tests", "constraints")


@nox.session(python=PYTHON_VERSIONS)
@nox.parametrize("protobuf_implementation", PROTOBUF_IMPLEMENTATIONS)
def tests(session, protobuf_implementation):
    session.install("-e", ".")
    # modules for testing
    session.install(*TEST_DEPENDENCIES)
    session.run(*FREEZE_COMMAND)
    session.run(
        *TEST_COMMAND,
        env={
            "PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION": protobuf_implementation,
        },
    )
    session.run(*COVERAGE_COMMAND)


# This session runs all the unit tests but with the lowest-possible versions
# of supported dependencies that are published by Google.
@nox.session(python=PYTHON_VERSIONS)
@nox.parametrize("protobuf_implementation", PROTOBUF_IMPLEMENTATIONS)
def tests_minimum_dependency_versions(session, protobuf_implementation):
    if session.python == "3.13":
        # If running Python 3.13 use the constraints file intended for it.
        filename = "constraints-3.13.txt"
    else:
        # If runnning a Python version other than 3.13 then use the constraints
        # file intended for all versions previous to 3.13.
        # TODO: Update this when new major versions of Python are adopted.
        filename = "constraints-less-than-3.13.txt"

    constraints_file = os.path.join(CONSTRAINTS_DIR, "minimums", filename)

    session.install("-e", ".")
    session.install(*TEST_DEPENDENCIES, "-c", constraints_file)
    session.run(*FREEZE_COMMAND)
    session.run(
        *TEST_COMMAND,
        env={
            "PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION": protobuf_implementation,
        },
    )
    session.run(*COVERAGE_COMMAND)
