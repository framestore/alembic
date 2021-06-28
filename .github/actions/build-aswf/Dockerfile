FROM aswf/ci-usd:2021.6

# install dependencies
RUN yum install -y patchelf
RUN pip install auditwheel

# build imath dependecy
RUN git clone --depth 1 --branch v3.0.4 https://github.com/AcademySoftwareFoundation/Imath.git /Imath
RUN mkdir /imathbuild
RUN cd /imathbuild
RUN cmake /Imath -DPYTHON=ON
RUN make
RUN make install

# Setup dev environment
# WORKDIR /github/workspace
# ENV PLAT manylinux2010_x86_64
ENV PLAT manylinux_2_17_x86_64

# Copy build script and build
COPY build_alembic.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]
