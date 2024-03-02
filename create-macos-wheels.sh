#!/bin/bash
set -e

SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

rm -rf /tmp/openfst_python
cp -r $SOURCE_DIR /tmp/openfst_python
cd /tmp/openfst_python

export MANYLINUX_BUILD=True

declare -a PYTHON_VERSIONS=(python3.8 python3.9 python3.10 python3.11 python3.12)

for py in "${PYTHON_VERSIONS[@]}"; do
    (
      echo "=== Building Wheel for $py ==="
      $py -m venv ./$py-venv
      source ./$py-venv/bin/activate

      pip install -U requests~=2.31 wheel~=0.42 setuptools~=68.0 Cython~=0.29

      python setup.py clean
      python setup.py bdist_wheel
    )
done;

echo "=== Reparing Wheels ===";
(
  cd /tmp/openfst_python
  mkdir -p $SOURCE_DIR/dist/wheelhouse/
  source ./python3.8-venv/bin/activate

  pip install delocate~=0.10.4

  for whl in dist/*.whl; do
    delocate-wheel -w $SOURCE_DIR/dist/wheelhouse/ -v "$whl" 
  done
)

echo "=== Testing Wheels ==="

# Remove the intermediate build files, so that we can test that
# the wheels are actually self contained.
rm -rf /tmp/openfst_python
mkdir -p /tmp/openfst_python

for py in "${PYTHON_VERSIONS[@]}"; do
    (
        cd /tmp/openfst_python
        $py -m venv ./$py-venv
        source ./$py-venv/bin/activate

        pip uninstall -y openfst_python;
        pip install openfst_python --no-index -f $SOURCE_DIR/dist/wheelhouse/ --no-dependencies -v;
        python -m unittest openfst_python.test;
    )
done;