# syntax=docker/dockerfile:1
FROM alpine:latest
WORKDIR /root
RUN apk update

# Fetch Super Tilt Bro.'s source code
RUN apk add git
RUN git clone https://github.com/sgadrat/super-tilt-bro.git
WORKDIR /root/super-tilt-bro
RUN git checkout 2.5

# Build Super Tilt Bro.
RUN apk add bash curl build-base
RUN deps/build-deps.sh
ENV XA_BIN=/root/super-tilt-bro/deps/xa65-stb/xa/xa
ENV CC_BIN=/root/super-tilt-bro/deps/gcc-6502-bits/prefix/bin/6502-gcc
ENV HUFFMUNCH_BIN=/root/super-tilt-bro/deps/huffmunch/huffmunch
ENV SKIP_RESCUE_IMG=2
RUN ls /root/super-tilt-bro/deps/gcc-6502-bits
RUN ls /root/super-tilt-bro/deps/gcc-6502-bits/prefix
RUN ls /root/super-tilt-bro/deps/gcc-6502-bits/prefix/bin
RUN ls /root/super-tilt-bro/deps/gcc-6502-bits/prefix/bin/6502-gcc
RUN ldd /root/super-tilt-bro/deps/gcc-6502-bits/prefix/bin/6502-gcc
RUN ./build.sh

# Install Webservice
RUN apk add python3 py3-pip py3-flask
COPY hello.py /root/

WORKDIR /root
ENV FLASK_APP=hello
EXPOSE 8000
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8000"]
