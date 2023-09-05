# OpenFst-Python

This project contains updated wheels for [jpuigcerver/openfst-python](https://github.com/jpuigcerver/openfst-python). Version number tracks OpenFst version, with an extra number to represent updates to this library. For example, `1.7.3.x` versions are all based off of OpenFst `1.7.3`.

## Building Wheels

The wheels are built in a [manylinux](https://github.com/pypa/manylinux) Docker container. You must have Docker installed to build them.

```
git clone https://github.com/rameshvarun/openfst-python.git
cd openfst-python
./create_wheels.sh

# Wheels are built under dist/wheelhouse
ls dist/wheelhouse
```