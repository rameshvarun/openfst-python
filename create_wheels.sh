#!/bin/bash
set -e;

SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)";

###########################################
## THIS CODE IS EXECUTED WITHIN THE HOST ##
###########################################
if [ ! -f /.dockerenv ]; then
  docker build -t openfst-python-builder .
  docker run --rm --log-driver none \
	 -v /tmp:/host/tmp \
	 -v ${SOURCE_DIR}:/host/src \
	 openfst-python-builder \
	 /host/src/create_wheels.sh;
  exit 0;
fi;

#######################################################
## THIS CODE IS EXECUTED WITHIN THE DOCKER CONTAINER ##
#######################################################
set -ex;

source /opt/rh/devtoolset-7/enable;

# Copy host source directory, to avoid changes in the host.
cp -r /host/src /tmp/src;
rm -rf /tmp/src/build /tmp/src/dist;

for py in cp36-cp36m; do
  (
    cd /tmp/src;
    export PYTHON=/opt/python/$py/bin/python;
    export PATH="$PATH:/opt/python/$py/bin/"
    echo "=== Installing dependencies for $py ===";
    $PYTHON -m pip install -U pip;
    $PYTHON -m pip install -U requests==2.27 wheel==0.37 setuptools==59.6 Cython==0.29 auditwheel==1.0;
    echo "=== Building for $py ==="
    $PYTHON setup.py clean;
    $PYTHON setup.py bdist_wheel;
    echo "=== Installing for $py ===";
    cd /tmp; 
    $PYTHON -m pip uninstall -y openfst_python;
    $PYTHON -m pip install openfst_python --no-index -f /tmp/src/dist --no-dependencies -v;
    echo "=== Testing for $py ===";
    $PYTHON -m unittest openfst_python.test;
  )
done;