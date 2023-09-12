docker run -it \
	 -v ${PWD}:/host/src \
	 python:3.8-bookworm \
	 bash -c "cp -r /host/src /src; cd src; pip install -U requests~=2.27 Cython~=0.29; python setup.py install; cd /tmp; python -m unittest openfst_python.test"