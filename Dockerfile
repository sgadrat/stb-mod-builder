# syntax=docker/dockerfile:1
FROM alpine:latest
WORKDIR /root
RUN apk update

# Fetch Super Tilt Bro.'s source code
RUN apk add git
RUN git clone https://github.com/sgadrat/super-tilt-bro.git
WORKDIR /root/super-tilt-bro

# Build Super Tilt Bro.
RUN apk add bash curl build-base
RUN deps/build-deps.sh
ENV XA_BIN=/root/super-tilt-bro/deps/xa65-stb/xa/xa
ENV CC_BIN=/root/super-tilt-bro/deps/gcc-6502-bits/prefix/bin/6502-gcc
ENV HUFFMUNCH_BIN=/root/super-tilt-bro/deps/huffmunch/huffmunch
ENV SKIP_RESCUE_IMG=2
ENV LD_PRELOAD=/lib/libgcompat.so.0
RUN ./build.sh

# Extract original mod as a single json file
COPY stb-tools/ /root/stb-tools/
RUN PYTHONPATH=$PYTHONPATH:/root/super-tilt-bro/tools /root/stb-tools/json_to_dict.py /root/super-tilt-bro/game-mod/mod.json > /root/original-mod.json
RUN rm -rf /root/stb-tools/

# Install Webservice
RUN apk add python3 py3-pip py3-flask py3-gunicorn
COPY stb-mod-builder-service.py /root/

WORKDIR /root
EXPOSE 8000

# Note "--workers=1 --threads=2",
#  this is important as the docker does not support parallel builds and service's code is not multiprocess-safe
#  the service is thread-safe though so a second thread is good to reject rapidly concurent builds
CMD ["gunicorn", "--workers=1", "--threads=2", "--bind=0.0.0.0:8000", "stb-mod-builder-service:app"]
