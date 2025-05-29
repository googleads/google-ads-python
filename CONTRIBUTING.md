# How to Contribute

We'd love to accept your patches and contributions to this project. There are
just a few small guidelines you need to follow.

## Contributor License Agreement

Contributions to this project must be accompanied by a Contributor License
Agreement. You (or your employer) retain the copyright to your contribution;
this simply gives us permission to use and redistribute your contributions as
part of the project. Head over to <https://cla.developers.google.com/> to see
your current agreements on file or to sign a new one.

You generally only need to submit a CLA once, so if you've already submitted one
(even if it was for a different project), you probably don't need to do it
again.

## Code reviews

All submissions, including submissions by project members, require review. We
use GitHub pull requests for this purpose. Consult
[GitHub Help](https://help.github.com/articles/about-pull-requests/) for more
information on using pull requests.

## Community Guidelines

This project follows [Google's Open Source Community
Guidelines](https://opensource.google.com/conduct/).

## Code Style

This library conforms to [PEP 8](https://www.python.org/dev/peps/pep-0008/)
style guidelines and enforces an 80 character line width. It's recommended
that any contributor run the auto-formatter [`black`](https://github.com/psf/black),
version 19.10b0 on the non-generated codebase whenever making changes. To get
started, first install the appropriate version of `black`:

```
python -m pip install black==19.10b0
```

You can manually run the formatter on all non-generated code with the following
command:

```
python -m black -l 80 --exclude "/(v[0-9]+|\.eggs|\.git|_cache|\.nox|\.tox|\.venv|\.svn|_build|buck-out|build|dist)/" .
```

Alternatively, if you intend to contribute regularly, it might be easier to
append this script to the `.git/hooks/pre-commit` file:

```
FILES=$(git diff --cached --name-only --diff-filter=ACMR "*.py" | grep -v "google/ads/google_ads/v.*")
echo "${FILES}" | xargs python -m black -l 80
echo "${FILES}" | xargs git add
```

## Running Tests

This project uses [nox](https://nox.thea.codes/) for automated testing and linting across different Python environments. Nox is configured in the `noxfile.py` at the root of the repository.

To run the test suite:

1.  Ensure you have `nox` installed. If not, you can install it via pip:
    ```bash
    python -m pip install nox
    ```

2.  To list all available nox sessions (which might include different Python versions, linting, etc.), run:
    ```bash
    nox -l
    ```

3.  To run all default test sessions, execute the following command from the root of the repository:
    ```bash
    nox
    ```

4.  If you want to run a specific test session (e.g., tests for a particular Python version or a linting session), you can specify it using the `-s` flag. For example:
    ```bash
    nox -s tests-3.8
    ```
    (The exact session names can be found using `nox -l`.)

The newly added tests for the `examples/assets` directory are part of the standard test sessions and will be executed automatically when you run `nox`.
