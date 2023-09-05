from __future__ import print_function

import hashlib
import os
import re
import requests
import shutil
import subprocess
import sys
import multiprocessing

from distutils.command.build import build
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext
from distutils.command.clean import clean
from Cython.Build import cythonize

OPENFST_VERSION = "1.7.3"
OPENFST_DIR = f"./openfst-{OPENFST_VERSION}"
OPENFST_ARCHIVE = f"openfst-{OPENFST_VERSION}.tar.gz"
OPENFST_URL = f"http://www.openfst.org/twiki/pub/FST/FstDownload/{OPENFST_ARCHIVE}"

PACKAGE_DIR = os.path.realpath(os.path.dirname(__file__))

class OpenFstClean(clean):
    def run(self):
        if os.path.exists(OPENFST_DIR):
            shutil.rmtree(OPENFST_DIR)
        if os.path.exists(OPENFST_ARCHIVE):
            os.remove(OPENFST_ARCHIVE)
        super().run()

class OpenFstBuildExt(build_ext):
    def openfst_download_and_extract(self):
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

    def openfst_configure_and_make(self):
        old_dir = os.getcwd()
        os.chdir(OPENFST_DIR)
        subprocess.check_call([
            "./configure",
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

    def openfst_copy_libraries(self):
        libraries = [
            "src/extensions/far/.libs/libfstfar.so",
            "src/extensions/far/.libs/libfstfar.so.17",
            "src/extensions/far/.libs/libfstfarscript.so",
            "src/extensions/far/.libs/libfstfarscript.so.17",
            "src/script/.libs/libfstscript.so",
            "src/script/.libs/libfstscript.so.17",
            "src/lib/.libs/libfst.so",
            "src/lib/.libs/libfst.so.17",
        ]
        destination = "./openfst_python/lib"
        if not os.path.isdir(destination):
            os.mkdir(destination)

        for library in libraries:
            shutil.copy(os.path.join(OPENFST_DIR, library), destination)

    def run(self):
        self.openfst_download_and_extract()
        self.openfst_configure_and_make()
        self.openfst_copy_libraries()
        super().run()

with open(os.path.join(os.path.dirname(__file__), "README.md"), "r") as fh:
    long_description = fh.read()

setup(
    name="openfst_python",
    version=OPENFST_VERSION,
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
        library_dirs=[os.path.join(PACKAGE_DIR, "./openfst_python/lib")],
        libraries=["fst", "fstscript", "fstfar", "fstfarscript"],
        extra_link_args = ["-Wl,-rpath=$ORIGIN/lib/."],
    )],
    package_data={
        'openfst_python': ['lib/*']
    },
    cmdclass=dict(build_ext=OpenFstBuildExt, clean=OpenFstClean),
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
