# Changelog

## [2.0.0] - 2026-03-15

### Added
- `ProtoModule` now accepts `file_path=None`: a unique filename (`definition_N.proto`) is auto-generated via a class-level counter.
- Python 3.13 and 3.14 support added to classifiers and CI matrix.
- `ty` type-checker added to the lint tox environment.
- `ruff` isort configuration added (`combine-as-imports = true`).

### Fixed
- `KeyError` in `test_compile_simple_dependency` caused by iterating duplicate `ProtoModule` values in `ProtoCollection.modules`. Fixed by deduplicating with `set()` before iterating.
- `compiler_version()` now correctly returns `None` instead of raising when no output is produced.

### Changed
- **Breaking**: dropped Python 3.8 and 3.9 support; minimum is now Python 3.10.
- `requires-python` updated from `>=3.8` to `>=3.10`.
- `ProtoCollection.modules` now indexes each module by both `Path` and `str` key for flexible lookup.
- Tox configuration migrated from `tox.ini` into `pyproject.toml`; `tox-uv` added as a requirement.
- `urllib3` version constraint relaxed (removed `<2` pin).
- CI: removed `py_39_proto_203` job; `py_31x_proto_252` matrix extended to include Python 3.12, 3.13, 3.14.
- CI: migrated `test.yml` from `actions/setup-python` + pip to `astral-sh/setup-uv`; replaced `pip install` steps with `uv run --extra`; removed Black from lint job.
- CI: updated GitHub Actions plugins to latest versions: `actions/checkout@v6`, `astral-sh/setup-uv@v7`, `actions/setup-python@v6`.

---

## [1.0.5] - 2024-08-29

### Added
- `workflow_dispatch` trigger added to CI workflow.
- `CONTRIBUTING.md` enhanced with releasing details.

### Changed
- Update versions of pre-commit hooks; use `macos-13` where `macos-14` is not supported.
- Exclude `setup.py` from `check-python-versions`; relax the check in the generated `.py`.

---

## [1.0.4] - 2024-02-07

### Fixed
- Repair wheel build.

### Changed
- Reintroduce `tox.ini`.
- Remove tagging from `bumpver` config.
- Adapt `CONTRIBUTING.md` to the releasing process.

---

## [1.0.3] - 2024-02-06

### Added
- Add a release workflow.

---

## [1.0.2] - 2024-02-06

### Added
- Add `README.md` to `pyproject.toml`.
- Add more details to `CONTRIBUTING.md`.
- Add Black dependency.

### Changed
- Move CI packages dependency to `pyproject.toml`.

---

## [1.0.1] - 2024-02-05

### Changed
- Remove direct dependency on Black in GitHub Actions.
- Isolate `compiler_path` to `compiled()` methods.

---

## [1.0.0] - 2024-02-04

### Added
- `ruff`-powered linting.
- Docstrings and examples for `ProtoCollection` and `DelimitedMessageFactory`.

### Changed
- **Breaking**: rename `ProtoCollection.compile()` to `compiled()`.
- **Breaking**: `compiler_path` is now a parameter of `compiled()` instead of the `ProtoCollection` constructor.
- Replace the use of protobuf `GetMessages` with `descriptor_pool` and `GetMessageClassesForFiles`.
- Remove `tox.ini` and `setup.cfg`; enhance `pyproject.toml`.

---

## [0.2.0] - 2024-02-04

### Added
- Add Google address book example to README.
- Add Python 3.12 support.
- Add `protoc` version matrix to CI actions.

### Fixed
- Pin `protoc` to version `3.20.3`; add a "latest" build.

### Changed
- Remove `ci` directory; centralize requirements.
- Migrate to `tox` 4 and `tox-gh`.

---

## [0.1.0] - 2023-06-08

### Added
- `ProtoCollection.compiler_version()` method added.
- Python 3.11 support added.
- `protoc` pinned to version `23.2` in CI; `arduino/setup-protoc` upgraded from `v1` to `v2`.
- `protoc --version` step added to CI workflows.
- `long_description_content_type` added to `setup.py`.

### Changed
- Improve robustness of `test_compiler_version()` and `test_compile_invalid_source()`.
- Increase overall test robustness; add dependency tests.

---

## [0.0.18] - 2022-11-17

### Changed
- Remove the use of `api_implementation` warning check.
- Replace `bytearray` with `bytes` in `bytes_read()` and `message_read()` return values.
- README converted from RST to Markdown.

---

## [0.0.17] - 2022-04-28

### Changed
- `DelimitedMessageFactory` stream type changed from `io.BytesIO` to `typing.BinaryIO`.

---

## [0.0.16] - 2022-04-24

### Changed
- **Breaking**: `bytes_read()` and `message_read()` generators now yield `(offset, data)` tuples instead of bare data, prefixing each message with its offset in the input stream.

---

## [0.0.15] - 2022-04-14

### Added
- `bytes_read()` generator added to `DelimitedMessageFactory` to yield raw byte chunks.
- `message_read()` generator added to `DelimitedMessageFactory` to yield decoded protobuf messages.

### Changed
- **Breaking**: rename `DelimitedMessage` to `DelimitedMessageFactory`.
- `DelimitedMessageFactory` now dispatches `read()` to either `bytes_read()` or `message_read()` depending on whether `message_type` is set.

---

## [0.0.14] - 2022-04-14

### Added
- `DelimitedMessage` class added (later renamed to `DelimitedMessageFactory`) for reading and writing length-delimited protobuf messages.
- `ProtoCollection` now parses the `FileDescriptorSet` and populates `.descriptor_set` and `.messages` using `GetMessages`.

---

## [0.0.13] - 2022-04-14

### Added
- `ProtoModule.compiled()` convenience method added, wrapping single-module compilation via `ProtoCollection`.
- Duplicate proto detection: `add_proto()` now raises `KeyError` if the same `file_path` is added twice.
- Encode and decode tests added.
- `protoc` installation added to CI.

### Changed
- Rename CI workflow file `github-actions.yml` to `test.yml`.

---

## [0.0.12] - 2022-04-13

### Changed
- **Breaking**: `ProtoModule().proto_source` renamed to `.source`.
- **Breaking**: `ProtoCollection().file_descriptor_set` renamed to `.descriptor_data`.
- `importlib.util` used instead of bare `importlib` for module loading.

---

## [0.0.11] - 2022-04-13

### Changed
- **Breaking**: rename `ProtoDict` to `ProtoCollection`; `.protos` dict renamed to `.modules`.
- **Breaking**: `ProtoModule` fields renamed: `module_core_name` → `name`, `content` → `proto_source`, `module_source` → `py_source`, `module` → `py`.
- `ProtoModule` now uses `importlib.util.spec_from_loader` and `module_from_spec` for module creation.
- `ProtoCollection` gains `.file_descriptor_set` attribute (serialized `FileDescriptorSet` bytes).

---

## [0.0.10] - 2022-04-12

### Fixed
- `raise_for_errs()`: early return when `errs` is empty (no exception raised on empty stderr).

### Changed
- Linting fixes in `entities.py`.

---

## [0.0.9] - 2022-04-12

### Added
- `__init__.py` files added to package directories to allow package importing.
- `raise_for_errs()` and `add_init_files()` extracted as separate methods on `ProtoCollection`.

### Changed
- `ProtoModule.__init__` now accepts `file_path` as `Path` instead of `str`.
- Allow injection of a `global_scope` dict into module execution.
- Tolerate `protoc` warnings for unused `.proto` files (only raise on real errors).

---

## [0.0.8] - 2022-04-12

### Changed
- License changed from LGPL-3.0 to MIT before making the source public.

---

## [0.0.7] - 2022-04-12

### Changed
- Version bump only (no functional changes).

---

## [0.0.6] - 2022-04-12

### Fixed
- Fix `protoc_command` extension: pass list of string paths instead of dict keys directly.

---

## [0.0.5] - 2022-04-12

### Added
- Type annotations added throughout (`Dict`, class-level field declarations).
- Index protos by full `file_path` instead of `module_core_name` to avoid conflicts.
- Use a single `TemporaryDirectory` for both source and output instead of two nested ones.
- `marshal()` static method added to write proto sources to the temp directory.

---

## [0.0.4] - 2022-04-11

### Changed
- `ProtoModule.__init__` signature changed: `file_name: str` replaced by `file_path: str`; `package_path` derived from `Path(file_path).parent` instead of being a constructor argument.
- `protoc` invocation refactored to use per-proto paths derived from `file_path`.

---

## [0.0.3] - 2022-04-11

### Added
- Core `ProtoModule` and `ProtoDict` classes introduced in `src/proto_topy/entities.py`.
- `ProtoDict.compile()` method: writes proto sources to a temp dir, invokes `protoc`, loads generated Python modules.
- `NoCompiler` and `CompilationFailed` exceptions added.
- Initial test suite added.

### Changed
- Removed docs/, future/, readthedocs scaffolding inherited from cookiecutter template.
- Simplified CI workflow; removed Sphinx documentation build.
- `setup.py` rewritten to read version and requirements dynamically.

---

## [0.0.2] - 2022-04-10

### Added
- Initial project skeleton.
