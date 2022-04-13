from collections import namedtuple
from distutils.spawn import find_executable
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from subprocess import PIPE, STDOUT, check_output, Popen
import importlib.util
import sys
import types
from typing import Dict
from logging import getLogger, basicConfig, DEBUG
logger = getLogger(Path(__file__).name)


class ProtoModule:
    name: str
    package_path: Path
    file_path: Path
    source: str
    py_source: str
    py: types.ModuleType

    def __init__(self, file_path: Path, source: str):
        self.file_path = file_path
        self.name, _, _ = self.file_path.name.partition(".proto")
        self.source = source
        self.package_path = self.file_path.parent
        self.py = None
        self.py_source = None

    def set_module(self, content: str, global_scope: dict = None):
        self.py_source = content
        spec = importlib.util.spec_from_loader(self.name, loader=None)
        compiled_content = compile(content, self.name, "exec")
        self.py = importlib.util.module_from_spec(spec)
        exec(compiled_content, self.py.__dict__)


class NoCompiler(Exception):
    pass


class CompilationFailed(Exception):
    pass


class ProtoCollection:
    compiler_path: Path
    modules: Dict[Path, ProtoModule]
    descriptor_data: bytes

    def __init__(self, compiler_path: Path, *protos: ProtoModule):
        self.modules = {}
        self.compiler_path = compiler_path
        self.descriptor_data = None

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
        self.modules[proto.file_path] = proto

    def compile(self, global_scope: dict = None) -> None:
        with TemporaryDirectory() as dir:
            protos_target_paths = {Path(dir, proto.file_path): proto for proto in self.modules.values()}
            proto_source_files = [str(file_path) for file_path in protos_target_paths.keys()]
            ProtoCollection.marshal(protos_target_paths)

            compile_to_py_options = [f"--proto_path={dir}", f"--python_out={dir}"]
            ProtoCollection._do_compile(self.compiler_path, compile_to_py_options, proto_source_files)

            artifact_fds_path = Path(dir, "artifacts.fds")
            compile_to_py_options = ["--include_imports", f"--proto_path={dir}", f"--descriptor_set_out={artifact_fds_path}"]
            ProtoCollection._do_compile(self.compiler_path, compile_to_py_options, proto_source_files)
            with open(str(artifact_fds_path), mode="rb") as f:
                self.descriptor_data = f.read()

            self._add_init_files(dir)

            sys.path.append(dir)
            for proto in self.modules.values():
                with open(Path(dir, proto.package_path, f"{proto.name}_pb2.py")) as module_path:
                    proto.set_module(module_path.read(), global_scope=global_scope)
            sys.path.pop()

    @staticmethod
    def _do_compile(compiler_path: Path, compile_to_py_options: list, proto_source_files: list) -> None:
        compile_command = [str(compiler_path.resolve())]
        compile_command.extend(compile_to_py_options)
        compile_command.extend(proto_source_files)
        compilation = Popen(compile_command, stdout=PIPE, stderr=PIPE)
        compilation.wait()
        outs, errs = compilation.communicate()
        ProtoCollection._raise_for_errs(errs)

    @staticmethod
    def _raise_for_errs(errs: bytes) -> None:
        warnings = []
        errors = []
        if not errs:
            return
        for err_line in errs.decode().strip().split("\n"):
            if "warning:" in err_line and err_line.endswith(".proto is unused."):
                warnings.append(err_line)
                continue
            errors.append(err_line)

        if warnings:
            logger.warning("\n".join(warnings))
        if errors:
            raise CompilationFailed("\n".join(errors))

    def _add_init_files(self, base_dir: Path) -> None:
        for proto in self.modules.values():
            Path(base_dir, proto.package_path, "__init__.py").touch()
            for parent_path in proto.package_path.parents:
                Path(base_dir, parent_path, "__init__.py").touch()

    @staticmethod
    def marshal(protos: Dict[Path, ProtoModule]) -> None:
        for target_file_path, proto in protos.items():
            Path(target_file_path.parent).mkdir(parents=True, exist_ok=True)
            with open(str(target_file_path), "wt") as o:
                o.write(proto.source)
