IXO_ROOT		   ?= https://github.com/ixofoundation/ixo-blockchain
IXO_RELEASE	   ?= v0.16.0
IXO_DST_FOLDER ?= ixo-blockchain-${IXO_RELEASE}
GOOS 					 ?= linux
GOARCH				 ?= amd64

all: clone build-ixod

clone:
	@echo "Cloning repo ${IXO_ROOT}"
	test -d ${IXO_DST_FOLDER} || \
	git clone ${IXO_ROOT} ${IXO_DST_FOLDER}
	cd ${IXO_DST_FOLDER} && \
	git fetch --all && \
	git checkout ${IXO_RELEASE}

build-ixod: clone
	docker run \
	-v "$(CURDIR)/${IXO_DST_FOLDER}:/app" \
	-v "$(CURDIR)/bin:/go/bin/" \
	-e GOARCH=${GOARCH} \
	-e GOOS=${GOOS} \
	--workdir "/app" golang:1.16 make install

build-image: clone
ifndef network
	$(error network is undefined)
endif
	docker build --build-arg IXO_FOLDER=${IXO_DST_FOLDER} \
							 --build-arg NETWORK=$(network) \
							 --build-arg IXO_RELEASE=$(IXO_RELEASE) \
							 --build-arg BUILD_DATE=$(`date +'%y.%m.%d'`) \
							 -t ixo:$(network)-${IXO_RELEASE} .

clean:
	rm -rf ${IXO_DST_FOLDER} bin
