from collections import namedtuple
from distutils.spawn import find_executable
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from subprocess import PIPE, STDOUT, check_output, Popen
import importlib
import sys
import types
from logging import getLogger, basicConfig, DEBUG
logger = getLogger(__file__)


class ProtoModule:
    def __init__(self, file_name: str, content: str, package_path: str = None):
        self.file_name = file_name
        self.module_core_name, _, _ = file_name.partition(".proto")
        self.content = content
        self.package_path = package_path or ""
        self.module = None
        self.module_source = None

    def set_module(self, content: str):
        self.module_source = content
        self.module = types.ModuleType(self.module_core_name)
        #print(content)
        #exec("import google", self.module.__dict__)
        #import google.protobuf
        exec(content, globals(), self.module.__dict__)
        #print(self.module.__dict__)



class NoCompiler(Exception):
    pass


class CompilationFailed(Exception):
    pass


class ProtoDict:
    protos: dict

    def __init__(self, compiler_path: Path, *protos: ProtoModule):
        self.protos = {}
        self.compiler_path = compiler_path
        if not self.compiler_path:
            if 'PROTOC' in os.environ and os.path.exists(os.environ['PROTOC']):
                self.compiler_path = Path(os.environ['PROTOC'])
            else:
                self.compiler_path or Path(find_executable('protoc'))
        if not self.compiler_path.is_file():
            raise FileNotFoundError()

        for proto in protos or []:
            self.add_proto(proto)

    def add_proto(self, proto: ProtoModule):
        self.protos[proto.module_core_name] = proto

    def compile(self):
        proto_file_paths = []
        with TemporaryDirectory() as src:
            for module_core_name, proto in self.protos.items():
                Path(src, proto.package_path).mkdir(parents=True, exist_ok=True)
                proto_file_path = Path(src, proto.package_path, proto.file_name)
                proto_file_paths.append(proto_file_path)
                with open(proto_file_path, "wt") as o:
                    o.write(proto.content)
            with TemporaryDirectory() as out:
                protoc_command = [self.compiler_path.resolve(), f"--proto_path={src}", f"--python_out={out}"]
                protoc_command.extend(proto_file_paths)
                compilation = Popen(protoc_command, stdout=PIPE, stderr=PIPE)
                compilation.wait()
                outs, errs = compilation.communicate()
                if errs:
                    logger.warning(errs.decode())
                    raise CompilationFailed(errs)
                for module_core_name, proto in self.protos.items():
                    with open(Path(out, f"{proto.module_core_name}_pb2.py")) as module_path:
                        proto.set_module(module_path.read())
