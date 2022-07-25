FROM golang:1.18.4-alpine3.16

ARG IXO_FOLDER
ARG NETWORK
ARG IXO_RELEASE
ARG BUILD_DATE

LABEL MAINTAINER="Alexey Ulyanov <alex@gateway.fm>"
LABEL DESCRIPTION="Image for ixo validator"
LABEL NETWORK=${NETWORK}
LABEL RELEASE=${IXO_RELEASE}
LABEL BUILD_DATE=${BUILD_DATE}
LABEL NAME="gatewayfm/ixo"
LABEL URL="https://hub.docker.com/repository/docker/gatewayfm/ixo"
LABEL VCS_URL="https://github.com/ixofoundation/genesis"
LABEL DOCKER.CMD="docker run -v $(pwd)/ixo:/home/ixo/.ixod -p 26656:26656 -p 26657:26657 ixo:${NETWORK}-${IXO_RELEASE} start"

WORKDIR /app

COPY ${IXO_FOLDER}/ /app
COPY ${NETWORK}/genesis.json /ixo/genesis.json
COPY entrypoint.sh /ixo/entrypoint.sh

RUN apk update && \
  apk upgrade && \
  apk add --update alpine-sdk && \
  apk add --no-cache bash git openssh make cmake && \
  make install && \
  apk del bash git openssh make cmake --quiet && \
  mv /go/bin/ixod /usr/bin/ixod && \
  adduser -H -u 1000 -g 1000 -D ixo

USER ixo

EXPOSE 26656

ENTRYPOINT [ "/ixo/entrypoint.sh"]