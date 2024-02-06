[![test][test_badge]][test_target]
[![version][version_badge]][pypi]
[![wheel][wheel_badge]][pypi]
[![python version][python_versions_badge]][pypi]
[![python implementation][python_implementation_badge]][pypi]

A Python package that
- takes a `str` containing protobuf messages definitions
- returns a `types.ModuleType` instance

It is useful for programs needing to en/decode protobuf messages for which the definition is provided as a string at runtime.

## Installation

    pip install proto-topy

Prerequisite: `proto-topy` needs [protoc][protoc] to be installed. On macOS, a simple `brew install protobuf` shall suffice.

## single proto example: address book

Adaptation of the `protocolbuffers` [example](https://github.com/protocolbuffers/protobuf/tree/main/examples):

```python
import requests
from pathlib import Path
from proto_topy import ProtoModule

# Retrieve protobuf messages definitions as a string
example_source = requests.get(
    "https://raw.githubusercontent.com/protocolbuffers/protobuf/main/"
    "examples/addressbook.proto").text

example_path = Path(
    "protocolbuffers/protobuf/blob/main/examples/addressbook.proto")

# Compile and import
module = ProtoModule(file_path=example_path, source=example_source).compiled()

# Produce a serialized address book
address_book = module.py.AddressBook()
person = address_book.people.add()
person.id = 111
person.name = "A Name"
person.email = "a.name@mail.com"
phone_number = person.phones.add()
phone_number.number = "+1234567"
phone_number.type = module.py.Person.MOBILE
with open("address_book.data", "wb") as o:
    o.write(address_book.SerializeToString())

# Use a serialized address book
address_book = module.py.AddressBook()
with open("address_book.data", "rb") as i:
    address_book.ParseFromString(i.read())
    for person in address_book.people:
        print(person.id, person.name, person.email, phone_number.number)
```

## multiple protos example

When several `.proto` need to be considered, use a `ProtoCollection`:

```python
import sys
from pathlib import Path
from proto_topy import ProtoModule, ProtoCollection

module1 = ProtoModule(
    file_path=Path("p1/p2/other2.proto"),
    source="""
    syntax = "proto3";
    import "google/protobuf/timestamp.proto";
    message OtherThing2 {
        google.protobuf.Timestamp created = 1;
    };"""
)

module2 = ProtoModule(
    file_path=Path("p3/p4/test6.proto"),
    source="""
    syntax = "proto3";
    import "p1/p2/other2.proto";
    message Test6 {
        OtherThing2 foo = 1;
    };"""
)

collection = ProtoCollection(module1, module2).compiled()
sys.modules.update({proto.name: proto.py
                    for proto in collection.modules.values()})
print(sys.modules['test6'].Test6,
      sys.modules['other2'].OtherThing2)
```
## Stream of delimited messages

To decode a stream of contiguous protobuf messages of the same type, use `DelimitedMessageFactory`. Example:

```python
from io import BytesIO
from pathlib import Path
from proto_topy import ProtoModule, DelimitedMessageFactory

# Generate Python module
module = ProtoModule(
    file_path=Path("int32_streams.proto"),
    source="""
    syntax = "proto3";
    message TestInt { int32 val = 1; };"""
).compiled()

# Feed a DelimitedMessageFactory with a sequence of TestInt instances for a range of 10 ints
integers = (module.py.TestInt(val=val) for val in range(10))
factory = DelimitedMessageFactory(BytesIO(), *integers)

# Rewind and read the stream of 10 protobuf messages
factory.rewind()
for offset_val in factory.message_read(module.py.TestInt):
    print(f"TestInt message of val set to {offset_val[1]}")
```



[pypi]: https://pypi.org/project/proto-topy
[test_badge]: https://github.com/decitre/python-proto-topy/actions/workflows/test.yml/badge.svg
[test_target]: https://github.com/decitre/python-proto-topy/actions
[version_badge]: https://img.shields.io/pypi/v/proto-topy.svg
[wheel_badge]: https://img.shields.io/pypi/wheel/proto-topy.svg
[python_versions_badge]: https://img.shields.io/pypi/pyversions/proto-topy.svg
[python_implementation_badge]: https://img.shields.io/pypi/implementation/proto-topy.svg
[tests]: tests/test_proto_topy.py
[protoc]: https://protobuf.dev/getting-started/pythontutorial/#compiling-protocol-buffers
