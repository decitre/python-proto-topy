## Linting & Testing

See [TESTING.md](TESTING.md) for the full test strategy and coverage details.

    uv pip install -e '.[dev]'
    pre-commit install
    tox -e lint   # ruff check + ty check
    tox           # all Python versions

`tox` uses the `protoc` compiler found in `PATH`. The CI workflow tests against protoc `25.x` and `34.x`.
On macOS, install protoc with `brew install protobuf`.

## Releasing

### 1. Create a release branch

Check the current version in `pyproject.toml`:

    grep current_version pyproject.toml   # e.g. -> 1.0.5

Create a branch for the next version (without the `rc` suffix):

    git checkout -b release/2.0.0

### 2. Make your changes

Implement bug fixes, new features, dependency updates, README and CHANGELOG notes, etc. Commit and push.

### 3. Bump to release candidate

Push the branch to remote first, then bump:

    git push -u origin release/2.0.0
    bumpver update --major --tag=rc   # 1.0.5 -> 2.0.0rc0

bumpver commits, tags `v2.0.0rc0`, and pushes automatically.

### 4. Open a pull request

Open a PR from `release/2.0.0` against `main`. Ensure:
- the `test` workflow jobs are all green
- Codecov still reports coverage at https://app.codecov.io/gh/decitre/python-proto-topy

If further changes are needed, iterate:

    bumpver update --tag-num   # 2.0.0rc0 -> 2.0.0rc1

### 5. Bump to final version

Once the RC is green:

    bumpver update --tag=final   # 2.0.0rc1 -> 2.0.0

Confirm the workflow is still green.

### 6. Merge into `main`

### 7. Publish on PyPI

Create a release in the [GitHub UI](https://github.com/decitre/python-proto-topy/releases):

- "Draft a new release"
- Choose the tag `v2.0.0` created by `bumpver` in step 5 (not the `rc` tags)
- Use the version as the release name
- Add the changes to the description
- "Publish release"
- Check the `release` [action](https://github.com/decitre/python-proto-topy/actions/workflows/release.yml)

### 8. Verify the published package

In a dedicated virtualenv:

    uv pip install proto-topy==2.0.0
    python -c "import proto_topy as pt; print(pt.__version__, pt.ProtoCollection().compiler_version())"