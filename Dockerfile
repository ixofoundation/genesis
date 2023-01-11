FROM golang:1.19.4-buster

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

# Add user to run the application
# and create application directories for uploaded data and static data
RUN adduser --disabled-password --gecos '' ixo

RUN make install && mv /go/bin/ixod /usr/bin/ixod

USER ixo

EXPOSE 26656

ENTRYPOINT [ "/ixo/entrypoint.sh"]