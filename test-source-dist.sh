#!/bin/bash
set -e;

git archive --format=tar -o /tmp/openfst-python.tar HEAD

docker run -it \
	 -v /tmp:/host/tmp \
	 python:3.8-bookworm \
	 bash -c "pip install -U requests~=2.27 Cython~=0.29; pip install --verbose /host/tmp/openfst-python.tar; cd /tmp; python -m unittest openfst_python.test"