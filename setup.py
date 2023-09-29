#!/usr/bin/env python3
from __future__ import print_function

import hashlib
import os
import re
import requests
import shutil
import subprocess
import sys
import multiprocessing
import platform

from distutils.command.build import build
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext
from distutils.command.clean import clean
from Cython.Build import cythonize

OPENFST_VERSION = "1.7.3"
LIBRARY_VERSION = "2"

OPENFST_DIR = f"./openfst-{OPENFST_VERSION}"
OPENFST_ARCHIVE = f"openfst-{OPENFST_VERSION}.tar.gz"
OPENFST_URL = f"http://www.openfst.org/twiki/pub/FST/FstDownload/{OPENFST_ARCHIVE}"

PACKAGE_DIR = os.path.realpath(os.path.dirname(__file__))
LIB_DIR = os.path.join(PACKAGE_DIR, "openfst_python", "lib")

def openfst_download_and_extract():
    # Skip if OpenFST dir already exists.
    if os.path.exists(OPENFST_DIR):
        return

    # Download OpenFST archive.
    if not os.path.exists(OPENFST_ARCHIVE):
        print("Downloading from %s" % OPENFST_URL)
        r = requests.get(OPENFST_URL, verify=False, stream=True)
        r.raw.decode_content = True
        with open(OPENFST_ARCHIVE, "wb") as f:
            shutil.copyfileobj(r.raw, f)

    subprocess.check_call(["tar", "xzf", OPENFST_ARCHIVE])

def openfst_configure_and_make():
    old_dir = os.getcwd()
    os.chdir(OPENFST_DIR)
    subprocess.check_call([
        "./configure",
        f"--libdir={LIB_DIR}",
        "--enable-compact-fsts",
        "--enable-compress",
        "--enable-const-fsts",
        "--enable-far",
        "--enable-linear-fsts",
        "--enable-lookahead-fsts",
        "--enable-special",
    ])
    subprocess.check_call(["make", f"-j{multiprocessing.cpu_count()}"])
    os.chdir(old_dir)

def openfst_copy_libraries():
    linux_libraries = [
        "src/extensions/far/.libs/libfstfar.so",
        "src/extensions/far/.libs/libfstfar.so.17",
        "src/extensions/far/.libs/libfstfarscript.so",
        "src/extensions/far/.libs/libfstfarscript.so.17",
        "src/script/.libs/libfstscript.so",
        "src/script/.libs/libfstscript.so.17",
        "src/lib/.libs/libfst.so",
        "src/lib/.libs/libfst.so.17",
    ]

    macos_libraries = [
        "src/extensions/far/.libs/libfstfar.dylib",
        "src/extensions/far/.libs/libfstfar.17.dylib",
        "src/extensions/far/.libs/libfstfarscript.dylib",
        "src/extensions/far/.libs/libfstfarscript.17.dylib",
        "src/script/.libs/libfstscript.dylib",
        "src/script/.libs/libfstscript.17.dylib",
        "src/lib/.libs/libfst.dylib",
        "src/lib/.libs/libfst.17.dylib",
    ]

    if platform.system() == "Linux":
        libraries = linux_libraries
    elif platform.system() == "Darwin":
        libraries = macos_libraries
    else:
        raise Exception(f"Unknown platform {platform.system()}")

    if not os.path.isdir(LIB_DIR):
        os.mkdir(LIB_DIR)

    for library in libraries:
        shutil.copy(os.path.join(OPENFST_DIR, library), LIB_DIR)

openfst_download_and_extract()
openfst_configure_and_make()
openfst_copy_libraries()

with open(os.path.join(PACKAGE_DIR, "README.md"), "r") as fh:
    long_description = fh.read()

MANYLINUX_BUILD = os.environ.get("MANYLINUX_BUILD", "false").strip().lower() == "true"
package_data = {} if MANYLINUX_BUILD else { 'openfst_python': ['lib/*'] }
extra_link_args = [] if MANYLINUX_BUILD else ["-Wl,-rpath=$ORIGIN/lib/."]

setup(
    name="openfst_python",
    version=f"{OPENFST_VERSION}.{LIBRARY_VERSION}",
    description="Stand-alone OpenFST bindings for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jpuigcerver/openfst-python",
    author="Joan Puigcerver",
    author_email="joapuipe@gmail.com",
    license="MIT",
    packages=find_packages(),
    ext_modules=[Extension(
        name="openfst_python.pywrapfst",
        sources=[os.path.join(OPENFST_DIR, "src/extensions/python/pywrapfst.cc")],
        include_dirs=[os.path.join(OPENFST_DIR, "src/include/")],
        library_dirs=[LIB_DIR],
        libraries=["fst", "fstscript", "fstfar", "fstfarscript"],
        extra_link_args=extra_link_args,
        extra_compile_args=["-std=c++11"]
    )],
    package_data=package_data,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    setup_requires=["Cython", "requests"],
    zip_safe=False,
)
