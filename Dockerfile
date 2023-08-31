FROM quay.io/pypa/manylinux2014_x86_64

RUN yum install -y centos-release-scl
RUN yum install -y devtoolset-7
RUN yum install -y zlib-devel