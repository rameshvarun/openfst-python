#!/bin/bash
set -e;

git ls-files -z | xargs -0 tar -czvf /tmp/openfst-python.tar.gz

docker run -it \
	 -v /tmp:/host/tmp \
	 python:3.8-bookworm \
	 bash -c "pip install -U requests~=2.27 Cython~=0.29; pip install --verbose /host/tmp/openfst-python.tar.gz; cd /tmp; python -m unittest openfst_python.test"