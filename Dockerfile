FROM docker.io/library/alpine:3.13

ARG network
ENV IXO_HOME=/home/ixo/

COPY bin/ixod /usr/bin/ixod

COPY ${network}/genesis.json /ixo/genesis.json
COPY entrypoint.sh /ixo/entrypoint.sh

RUN apk add --no-cache ca-certificates libc6-compat

RUN adduser -H -u 1000 -g 1000 -D ixo && \
  mkdir -p ${IXO_HOME}/.ixod && \
  chown -R ixo:ixo /home/ixo

USER ixo

EXPOSE 26656

ENTRYPOINT [ "/ixo/entrypoint.sh"]