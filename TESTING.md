# Testing

## Test strategy

Tests are located in [`tests/test_proto_topy.py`](tests/test_proto_topy.py) and cover:

- **Unit tests** for `ProtoModule`, `ProtoCollection`, and `DelimitedMessageFactory` — including compiler path resolution, proto compilation, message encoding/decoding, and stream handling.
- **Integration tests** that invoke the real `protoc` binary to compile `.proto` sources and exercise the generated Python modules.
- **Error path tests** — invalid proto source, missing dependencies, bad compiler path, type mismatches.

## Running tests

### Single Python version

```bash
tox -e py312
```

### All supported Python versions

```bash
tox -e clean,py310,py311,py312,py313,py314,report
```

The `clean` env erases accumulated coverage data before the run. The `report` env produces terminal, HTML (`htmlcov/`), and XML (`coverage.xml`) reports combining coverage from all versions.

### Linting

```bash
tox -e lint
```

Runs `ruff check .` and `ty check` (type checking).

### macOS — multiple protoc versions

[`tests/tox_mac.sh`](tests/tox_mac.sh) installs and cycles through the Homebrew protobuf bottles (`protobuf@29`, `protobuf@33`, `protobuf`) and runs the full tox suite against each:

```bash
bash tests/tox_mac.sh
```

## Google addressbook example test

`test_google_addressbook_example` is an end-to-end integration test based on the official Google Protocol Buffers tutorial example:

> https://github.com/protocolbuffers/protobuf/tree/main/examples

It fetches [`addressbook.proto`](https://raw.githubusercontent.com/protocolbuffers/protobuf/main/examples/addressbook.proto) — a real-world multi-message schema with nested types (`AddressBook`, `Person`, `PhoneNumber`) — compiles it at runtime via `protoc`, and verifies that a round-trip encode/decode of an address book produces the expected values.

The HTTP request is recorded and replayed via [vcrpy](https://github.com/kevin1024/vcrpy) / [pytest-recording](https://github.com/kiwicom/pytest-recording), so the test runs offline after the cassette is recorded. The cassette is stored at:

```
tests/cassettes/test_proto_topy/test_google_addressbook_example.yaml
```

To re-record the cassette (e.g. when the upstream proto changes):

```bash
pytest tests/test_proto_topy.py::test_google_addressbook_example --record-mode=once
```
