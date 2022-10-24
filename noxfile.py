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


@nox.session(python=["3.7"])
def tests(session):
    session.install(".")
    # modules for testing
    session.install(
        "mock>=3.0.0,<4.0.0",
        "pyfakefs>=3.5,<3.6",
        "coverage==5.5",
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
