FROM golang:1.16-buster AS build

ARG IXO_FOLDER

WORKDIR /app

COPY ${IXO_FOLDER}/ /app

RUN make install

FROM alpine:3.13

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

ENV IXO_HOME=/home/ixo/

COPY --from=build /go/bin/ixod /usr/bin/ixod

COPY ${NETWORK}/genesis.json /ixo/genesis.json
COPY entrypoint.sh /ixo/entrypoint.sh

RUN apk add --no-cache ca-certificates libc6-compat

RUN adduser -H -u 1000 -g 1000 -D ixo && \
  mkdir -p ${IXO_HOME}/.ixod && \
  chown -R ixo:ixo /home/ixo

USER ixo

EXPOSE 26656

ENTRYPOINT [ "/ixo/entrypoint.sh"]