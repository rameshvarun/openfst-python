# OpenFst-Python

This project contains updated wheels for [jpuigcerver/openfst-python](https://github.com/jpuigcerver/openfst-python).
Package version numbers track OpenFst versions, with an extra number to represent updates to this library.
For example, `1.7.3.x` versions are all based off of OpenFst `1.7.3`.

## Installing

You can install the package by using `--find-links` or pointing directly at a wheel.

```bash
# Automatically select the correct wheel.
pip install --find-links https://rameshvarun.github.io/openfst-python/ openfst-python==1.7.3.1

# Directly install the provided wheel.
pip install https://github.com/rameshvarun/openfst-python/releases/download/v1.7.3.1/openfst_python-1.7.3.1-cp37-cp37m-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

# Run package unit tests
python -m unittest openfst_python.test
```

## Building Wheels

The wheels are built in a [manylinux](https://github.com/pypa/manylinux) Docker container. You must have Docker installed to build them.

```bash
git clone https://github.com/rameshvarun/openfst-python.git
cd openfst-python
./create_wheels.sh

# Wheels are built under dist/wheelhouse
ls dist/wheelhouse
```
