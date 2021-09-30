IXO_ROOT		   ?= https://github.com/ixofoundation/ixo-blockchain
IXO_RELEASE	   ?= v1.6.0
IXO_DST_FOLDER ?= ixo-blockchain-${IXO_RELEASE}


all: clone build-ixod

clone:
	@echo "Clonning repo ${IXO_ROOT}"
	test -d ${IXO_DST_FOLDER} || \
	git clone ${IXO_ROOT} ${IXO_DST_FOLDER}
	cd ${IXO_DST_FOLDER} && \
	git fetch --all && \
	git checkout ${IXO_RELEASE}

build-ixod: clone
	docker run \
	-v "$(CURDIR)/${IXO_DST_FOLDER}:/app" \
	-v "$(CURDIR)/bin:/go/bin/" \
	-e GOARCH="amd64" \
	-e GOOS="linux" \
	--workdir "/app" golang:1.16 make install

build-ixod-darwin: clone
	docker run --rm \
	-v "$(CURDIR)/${IXO_DST_FOLDER}:/app" \
	-v "$(CURDIR)/bin:/go/bin/" \
	-e GOARCH="amd64" \
	-e GOOS="darwin" \
	--workdir "/app" golang:1.16 make install

build-image: build-ixod
ifndef network
	$(error network is undefined)
endif
	docker build --build-arg network=$(network) -t ixo:$(network)-${IXO_RELEASE} .

clean:
	rm -rf ${IXO_DST_FOLDER} bin
