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
[GitHub Docs](https://docs.github.com/en/pull-requests/reference/pull-requests) for more
information on using pull requests.

## Community Guidelines

This project follows [Google's Open Source Community
Guidelines](https://opensource.google/conduct/).

## Code Style

This library conforms to [PEP 8](https://www.python.org/dev/peps/pep-0008/)
style guidelines and enforces an 80 character line width. Run the auto-formatter [`black`](https://github.com/psf/black) on the
non-generated codebase whenever making changes. First, install `black`:

```bash
python -m pip install black
```

You can manually run the formatter on all non-generated code with the following
command:

```bash
python -m black -l 80 --exclude "/(v[0-9]+|\.eggs|\.git|_cache|\.nox|\.tox|\.venv|\.svn|_build|buck-out|build|dist)/" .
```

Alternatively, if you intend to contribute regularly, you can append the
following script to `.git/hooks/pre-commit`:

```bash
FILES=$(git diff --cached --name-only --diff-filter=ACMR "*.py" | grep -v "google/ads/googleads/v.*")
echo "${FILES}" | xargs python -m black -l 80
echo "${FILES}" | xargs git add
```
