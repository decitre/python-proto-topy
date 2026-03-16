[![test][test_badge]][test_target]
[![codecov][codecov_badge]][codecov]
[![version][version_badge]][pypi]
[![wheel][wheel_badge]][pypi]
[![python version][python_versions_badge]][pypi]
[![python implementation][python_implementation_badge]][pypi]

Compile protobuf strings into Python module objects at runtime. — no files, no code generation step:

```python
from proto_topy import ProtoModule

module = ProtoModule(
    source="message Hello { optional string name = 1; }",
).compiled()

msg = module.py.Hello(name="world")
assert msg.name == "world"
```

It is useful for programs needing to en/decode protobuf messages for which the definition is provided as a string at runtime.

## Installation

    pip install proto-topy

Prerequisite: `proto-topy` needs [protoc][protoc] to be installed. On macOS, a simple `brew install protobuf` shall suffice.

## single proto example: address book

Adaptation of the `protocolbuffers` [example](https://github.com/protocolbuffers/protobuf/tree/main/examples) from Google tutorial:

```python
from io import BytesIO
import requests
from proto_topy import ProtoModule

example_source = requests.get(
    "https://raw.githubusercontent.com/protocolbuffers/protobuf/main/"
    "examples/addressbook.proto").text

module = ProtoModule(source=example_source).compiled()

# Serialize an address book
buffer = BytesIO()
address_book = module.py.AddressBook()
person = address_book.people.add()
person.id = 111
person.name = "A Name"
person.email = "a.name@mail.com"
phone_number = person.phones.add()
phone_number.number = "+1234567"
phone_number.type = module.py.Person.MOBILE
buffer.write(address_book.SerializeToString())

# Deserialize it back
buffer.seek(0)
address_book = module.py.AddressBook()
address_book.ParseFromString(buffer.read())
for person in address_book.people:
    assert person.id == 111
    assert person.name == "A Name"
    assert person.email == "a.name@mail.com"

```

## multiple protos example

When several definition strings need to be considered, use a `ProtoCollection`:

```python
from proto_topy import ProtoModule, ProtoCollection
from google.protobuf.timestamp_pb2 import Timestamp

module1 = ProtoModule(
    file_path="p1/p2/other2.proto",
    source="""
    syntax = "proto3";
    import "google/protobuf/timestamp.proto";
    message OtherThing2 {
        google.protobuf.Timestamp created = 1;
    }"""
)

module2 = ProtoModule(
    file_path="p3/p4/test6.proto",
    source="""
    syntax = "proto3";
    import "p1/p2/other2.proto";
    message Test6 {
        OtherThing2 foo = 1;
    }"""
)

collection = ProtoCollection(module1, module2).compiled()

Test6 = collection.modules["p3/p4/test6.proto"].py.Test6
OtherThing2 = collection.modules["p1/p2/other2.proto"].py.OtherThing2

ts = Timestamp(seconds=1234567890)
thing = OtherThing2(created=ts)
msg = Test6(foo=thing)

assert msg.foo.created.seconds == 1234567890

```
## Stream of delimited messages

To decode a stream of contiguous protobuf messages of the same type, use `DelimitedMessageFactory`. Example:

```python
from io import BytesIO
from proto_topy import ProtoModule, DelimitedMessageFactory

module = ProtoModule(
    source="""
    syntax = "proto3";
    message TestInt { int32 val = 1; }
    """
).compiled()

integers = (module.py.TestInt(val=val) for val in range(10))
factory = DelimitedMessageFactory(BytesIO(), *integers)

factory.rewind()
for i, (offset, msg) in enumerate(factory.message_read(module.py.TestInt)):
    assert msg.val == i
```



[pypi]: https://pypi.org/project/proto-topy
[test_badge]: https://github.com/decitre/python-proto-topy/actions/workflows/test.yml/badge.svg
[test_target]: https://github.com/decitre/python-proto-topy/actions
[version_badge]: https://img.shields.io/pypi/v/proto-topy.svg
[wheel_badge]: https://img.shields.io/pypi/wheel/proto-topy.svg
[python_versions_badge]: https://img.shields.io/pypi/pyversions/proto-topy.svg
[python_implementation_badge]: https://img.shields.io/pypi/implementation/proto-topy.svg
[codecov_badge]: https://codecov.io/gh/decitre/python-proto-topy/branch/main/graph/badge.svg
[codecov]: https://codecov.io/gh/decitre/python-proto-topy
[tests]: tests/test_proto_topy.py
[protoc]: https://protobuf.dev/getting-started/pythontutorial/#compiling-protocol-buffers
