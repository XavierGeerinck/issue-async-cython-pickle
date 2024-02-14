# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

import multiprocessing
import os
from distutils.core import setup
from pathlib import Path
from typing import List

from Cython.Build import cythonize
from setuptools import Extension

DIR_SOURCE = Path("my_module")
DIR_BUILD = Path("dist/build_cython")

EXCLUDE_FILES = []

# Set this to True to build Cython extensions
# https://cibuildwheel.readthedocs.io/en/stable/faq/#optional-extensions
IS_CI_BUILD = os.environ.get("CIBUILDWHEEL", "0") == "1"

print("========================================================")
print("CONFIGURING BUILD")
print("Is CI Build:", IS_CI_BUILD)
print("========================================================")


def get_py_modules() -> List[Extension]:
    """
    Collect all .py files and turn them into module bames
    """
    modules: List[Path] = []

    # Loop over python files except the ones ending on _pb2.py
    for py_file in DIR_SOURCE.glob("**/*.py"):
        # Don't compile excluded files
        if str(py_file) in EXCLUDE_FILES:
            print("[Cythonize - Skip]", str(py_file))
            continue

        modules.append(py_file)

    return modules


def convert_paths_to_module_names(paths: List[Path]) -> List[str]:
    """
    Convert a list of paths to a list of module names by removing the extension and replacing / with .
    """
    return [convert_path_to_module_name(path) for path in paths]


def convert_path_to_module_name(path: Path) -> str:
    """
    Convert a path to a module name by removing the extension and replacing / with .
    """
    return str(path).replace("/", ".").replace(".py", "")


def cythonize_helper(extension_modules: List[Extension]) -> List[Extension]:
    """Cythonize all Python extensions"""

    return cythonize(
        module_list=extension_modules,
        # Don't build in source tree (this leaves behind .c files)
        build_dir=DIR_BUILD,
        # Don't generate an .html output file. This will contain source.
        annotate=False,
        # Parallelize our build
        nthreads=multiprocessing.cpu_count() * 2,
        # Tell Cython we're using Python 3
        compiler_directives={"language_level": "3"},
        # (Optional) Always rebuild, even if files untouched
        force=True,
    )


def get_extension_modules() -> List[Extension]:
    """
    Collect all .py files and turn them into Distutils/Setuptools Extensions
    """
    modules: List[Extension] = []

    # Loop over python files except the ones ending on _pb2.py
    for py_file in DIR_SOURCE.glob("**/*.py"):
        # Don't compile excluded files
        if str(py_file) in EXCLUDE_FILES:
            print("[Cythonize - Skip]", str(py_file))
            continue

        module = Extension(
            name=convert_path_to_module_name(py_file),
            sources=[str(py_file)],
        )

        modules.append(module)

    return modules


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    long_description=long_description,
    long_description_content_type="text/markdown",
    # Explicitly build the tree of files we want to include
    # this is provided as a module path (so .'s and no extension)
    # if it is not a CI_BUILD, we include everything under the main source folder
    py_modules=convert_paths_to_module_names(
        EXCLUDE_FILES if IS_CI_BUILD else get_py_modules()
    ),
    # Build C/C++ extensions
    ext_modules=cythonize_helper(get_extension_modules()) if IS_CI_BUILD else [],
)
