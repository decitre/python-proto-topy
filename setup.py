#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import io
import re
from glob import glob
from os.path import basename, dirname, join, splitext
from typing import Set, Any, List, Dict

from setuptools import find_packages
from setuptools import setup
from pathlib import Path


def get_property(prop, packages_path: str, packages: List[str]) -> Set[Any]:
    """
    Searches and returns a property from all packages __init__.py files
    :param prop: property searched
    :param packages_path: root path of packages to search into
    :param packages: array of packages paths
    :return: an set of values
    """
    results = set()
    namespace: Dict[str, Any] = {}
    for package in packages:
        init_file = open(Path(packages_path, package, "__init__.py")).read()
        exec(init_file, namespace)
        if prop in namespace:
            results.add(namespace[prop])
    return results


def get_requirements(file_path: str, no_precise_version: bool = False) -> List[str]:
    requirements = []
    try:
        with open(file_path, "rt") as r:
            for line in r.readlines():
                package = line.strip()
                if not package or package.startswith("#"):
                    continue
                if no_precise_version:
                    package = package.split("==")[0]
                requirements.append(package)
    except FileExistsError:
        pass
    return requirements


def read(*names, **kwargs):
    with io.open(join(dirname(__file__), *names),
                 encoding=kwargs.get('encoding', 'utf8')) as fh:
        return fh.read()


project_name = "proto-topy"
main_package_name = "proto_topy"
github_home = "https://github.com/decitre"


if __name__ == '__main__':

    _packages_path = "src"
    _packages = find_packages(where=_packages_path)
    version = get_property("__version__", _packages_path, _packages).pop()
    requirements = ["click"]
    requirements.extend(get_requirements("requirements.txt", no_precise_version=True))
    requirements_test = get_requirements("requirements_test.txt")

    setup(
        name=project_name,
        version=version,
        license='LGPL-3.0-or-later',
        description='Yet another tool to compile .proto to in memory modules',
        long_description=re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', read('README.rst')),
        author='Emmanuel Decitre',
        url=f'{github_home}/python-{project_name}',
        packages=_packages,
        package_dir={'': _packages_path},
        py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
        include_package_data=True,
        zip_safe=False,
        classifiers=[
            # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: OS Independent",
        ],
        project_urls={
            'Issue Tracker': f'{github_home}/python-{project_name}/issues',
        },
        keywords=[
            # eg: 'keyword1', 'keyword2', 'keyword3',
        ],
        python_requires='>=3.6',
        install_requires=requirements,
        extras_require={
            "dev": requirements_test
            # eg:
            #   'rst': ['docutils>=0.11'],
            #   ':python_version=="2.6"': ['argparse'],
        },
    )
