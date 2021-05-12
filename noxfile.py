import glob
import nox
import os


@nox.session
def tests(session):
    print(os.getcwd())
    print(session)
    session.install(
        "google-auth-oauthlib>=0.3.0,< 1.0.0",
        "google-api-core>=1.21.0,< 2.0.0",
        "googleapis-common-protos>=1.5.8,< 2.0.0",
        "grpcio>=1.33.2,< 2.0.0",
        "proto-plus>=1.18.0,< 2.0.0",
        "PyYAML>=5.1,< 6.0",
        "setuptools>=40.3.0",
        "pep562>=1.0,< 2.0",
    )
    session.install(".")
    # modules for testing
    session.install(
        "mock>=3.0.0,<4.0.0",
        "pyfakefs>=3.5,<3.6",
        "coverage==5.5",
        # "libsqlite3-dev",
    )
    test_modules = [
        "tests.client_test.GoogleAdsClientTest",
        "tests.config_test.ConfigTest",
        "tests.oauth2_test.OAuth2Tests",
        "tests.util_test.ConvertStringTest",
        "tests.util_test.SetNestedMessageFieldTest",
        "tests.util_test.GetNestedMessageFieldTest",
    ]
    for module in test_modules:
        session.run(
            "coverage",
            "run",
            "--timid",
            "--source=.",
            "--append",
            "-m",
            "unittest",
            module,
        )
    # the copy of the test in the .nox folder in site-packages is the one with the accurate % coverage,
    # but locally, it works with these commands (is it looking at the wrong modules?)
    session.run(
        "coverage",
        "report",
        "-m",
        "--omit='*/site-packages/*'"
        # "--omit=google/ads/googleads/__init__.py",
        # *glob.glob("google/ads/googleads/*.py"),
        # "--include='*/google/ads/googleads/client.py'"
    )
    session.run(
        "coverage",
        "report",
        "-m",
        "--omit=google/ads/googleads/interceptors/__init__.py",
        *glob.glob("google/ads/googleads/interceptors/*.py"),
    )
    # below includes all files in dir and nested dirs but with same % coverage (0) for the files I care about
    # session.run("coverage", "report", "-m")
