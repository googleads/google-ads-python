import nox


@nox.session(python=["3.6", "3.7"])
def tests(session):
    session.install(".")
    # modules for testing
    session.install(
        "mock>=3.0.0,<4.0.0", "pyfakefs>=3.5,<3.6", "coverage==5.5",
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
