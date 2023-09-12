#!/bin/bash
set -e;

SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)";

###########################################
## THIS CODE IS EXECUTED WITHIN THE HOST ##
###########################################
if [ ! -f /.dockerenv ]; then
  docker build -t openfst-python-builder .
  docker run --rm --log-driver none \
	 -v ${SOURCE_DIR}:/host/src \
	 openfst-python-builder \
	 /host/src/create-manylinux-wheels.sh;
  exit 0;
fi;

#######################################################
## THIS CODE IS EXECUTED WITHIN THE DOCKER CONTAINER ##
#######################################################
set -ex;

# Copy host source directory, to avoid changes in the host.
cp -r /host/src /tmp/src;
rm -rf /tmp/src/build /tmp/src/dist;

declare -a PYTHON_VERSIONS=(cp36-cp36m cp37-cp37m cp38-cp38 cp39-cp39)

for py in "${PYTHON_VERSIONS[@]}"; do
  (
    cd /tmp/src;
    export PYTHON=/opt/python/$py/bin/python;
    export PATH="$PATH:/opt/python/$py/bin/"
    export MANYLINUX_BUILD=True
    echo "=== Installing dependencies for $py ===";
    $PYTHON -m pip install -U pip;
    $PYTHON -m pip install -U requests~=2.27 wheel~=0.37 setuptools~=59.6 Cython~=0.29;
    echo "=== Building for $py ==="
    $PYTHON setup.py clean;
    $PYTHON setup.py bdist_wheel;
  )
done;

echo "=== Reparing Wheels ===";
(
  export PYTHON=/opt/python/cp37-cp37m/bin/python;
  export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/tmp/src/openfst_python/lib"

  $PYTHON -m pip install -U auditwheel==5.4

  cd /tmp/src/
  for whl in dist/*.whl; do
    $PYTHON -m auditwheel repair "$whl" -w /host/src/dist/wheelhouse
  done
)

echo "=== Testing Wheels ==="
for py in "${PYTHON_VERSIONS[@]}"; do
  (
    cd /tmp;
    export PYTHON=/opt/python/$py/bin/python;
    $PYTHON -m pip uninstall -y openfst_python;
    $PYTHON -m pip install openfst_python --no-index -f /host/src/dist/wheelhouse --no-dependencies -v;
    $PYTHON -m unittest openfst_python.test;
  )
done;