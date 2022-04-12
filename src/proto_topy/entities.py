from collections import namedtuple
from distutils.spawn import find_executable
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from subprocess import PIPE, STDOUT, check_output, Popen
import importlib
import sys
import types
from typing import Dict
from logging import getLogger, basicConfig, DEBUG
logger = getLogger(__file__)


class ProtoModule:
    file_path: str
    package_path: str
    module_core_name: str
    content: str
    module_source: str
    module: str

    def __init__(self, file_path: str, content: str):
        self.file_path = file_path
        self.module_core_name, _, _ = Path(file_path).name.partition(".proto")
        self.content = content
        self.package_path = Path(file_path).parent
        self.module = None
        self.module_source = None

    def set_module(self, content: str):
        self.module_source = content
        self.module = types.ModuleType(self.module_core_name)
        exec(content, globals(), self.module.__dict__)


class NoCompiler(Exception):
    pass


class CompilationFailed(Exception):
    pass


class ProtoDict:
    compiler_path: str
    protos: Dict[str, ProtoModule]

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
        self.protos[proto.file_path] = proto

    def compile(self):
        # proto_file_paths = []
        with TemporaryDirectory() as dir:
            protoc_command = [str(self.compiler_path.resolve()), f"--proto_path={dir}", f"--python_out={dir}"]

            protos_target_paths = {Path(dir, proto.file_path):proto for proto in self.protos.values()}
            ProtoDict.marshal(protos_target_paths)
            protoc_command.extend(protos_target_paths)

            compilation = Popen(protoc_command, stdout=PIPE, stderr=PIPE)
            compilation.wait()
            outs, errs = compilation.communicate()
            if errs:
                logger.warning(errs.decode())
                raise CompilationFailed(errs)

            for proto in self.protos.values():
                with open(Path(dir, proto.package_path, f"{proto.module_core_name}_pb2.py")) as module_path:
                    proto.set_module(module_path.read())

    @staticmethod
    def marshal(protos: Dict[Path, ProtoModule]) -> None:  # , proto_file_paths):
        for target_file_path, proto in protos.items():
            Path(target_file_path.stem).mkdir(parents=True, exist_ok=True)
            #proto_file_paths.append(str(proto_file_path))
            with open(str(target_file_path), "wt") as o:
                o.write(proto.content)
