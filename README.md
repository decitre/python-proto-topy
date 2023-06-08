[![test][test_badge]][test_target]
[![version][version_badge]][pypi]
[![wheel][wheel_badge]][pypi]
[![python version][python_versions_badge]][pypi]
[![python implementation][python_implementation_badge]][pypi]

A tool that 
- takes a `str` containing protobuf messages definitions 
- returns a `types.ModuleType` instance

It is useful for Python programs needing to parse protobuf messages without having to host `.proto` files in their code base.


## Installation

    pip install proto-topy

## Usage example

```python
import sys, os
from pathlib import Path
from distutils.spawn import find_executable
from proto_topy.entities import ProtoModule
from google.protobuf.timestamp_pb2 import Timestamp

protoc_path = Path(find_executable("protoc") or os.environ.get('PROTOC'))

source = """

    syntax = "proto3";
    import "google/protobuf/timestamp.proto";
    
    message Test5 {
        google.protobuf.Timestamp created = 1;
    }

"""

proto = ProtoModule(file_path=Path("test5.proto"), source=source).compiled(protoc_path)
sys.modules["test5"] = proto.py

assert isinstance(proto.py.Test5().created, Timestamp)
```

More examples in [test_proto_topy.py][tests].

[pypi]: https://pypi.org/project/proto-topy
[test_badge]: https://github.com/decitre/python-proto-topy/actions/workflows/test.yml/badge.svg
[test_target]: https://github.com/decitre/python-proto-topy/actions
[version_badge]: https://img.shields.io/pypi/v/proto-topy.svg
[wheel_badge]: https://img.shields.io/pypi/wheel/proto-topy.svg
[python_versions_badge]: https://img.shields.io/pypi/pyversions/proto-topy.svg
[python_implementation_badge]: https://img.shields.io/pypi/implementation/proto-topy.svg
[tests]: tests/test_proto_topy.py