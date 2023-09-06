# OpenFst-Python

This project contains updated wheels for [jpuigcerver/openfst-python](https://github.com/jpuigcerver/openfst-python). Package version numbers track OpenFst versions, with an extra number to represent updates to this library. For example, `1.7.3.x` versions are all based off of OpenFst `1.7.3`.

## Installing

You can install the package directly from [GitHub releases](https://github.com/rameshvarun/openfst-python/releases).

```bash
pip install https://github.com/rameshvarun/openfst-python/releases/download/v1.7.3.0/openfst_python-1.7.3.0-cp37-cp37m-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
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
