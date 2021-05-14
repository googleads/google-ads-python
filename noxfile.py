import nox


@nox.session
def tests(session):
    session.install(".")
    # modules for testing
    session.install(
        "mock>=3.0.0,<4.0.0",
        "pyfakefs>=3.5,<3.6",
        "coverage==5.5",
    )
    test_modules = [
        "tests.client_test.GoogleAdsClientTest",
        "tests.config_test.ConfigTest",
        "tests.oauth2_test.OAuth2Tests",
        "tests.util_test.ConvertStringTest",
        "tests.util_test.SetNestedMessageFieldTest",
        "tests.util_test.GetNestedMessageFieldTest",
        "tests.interceptors.exception_interceptor_test.ExceptionInterceptorTest", 
        "tests.interceptors.interceptor_test.InterceptorTest",
        "tests.interceptors.logging_interceptor_test.LoggingInterceptorTest",
        "tests.interceptors.metadata_interceptor_test.MetadataInterceptorTest",
    ]
    session.run("coverage", "erase")
    for module in test_modules:
        session.run(
            "coverage",
            "run",
            "--append",
            "-m",
            "unittest",
            module,
        )
    session.run(
        "coverage",
        "report",
        "-m",
        "--omit=.nox/*"
    )

