Upgrade.md
**Upgrade instructions**
___
### 1. Stop the validator
```
sudo systemctl stop ixod
```
### 1. Backup validator info
This consists of:
This key is essential in recovering your validator if this upgrade does not go as planned. The state is to make sure your validator does not double sign when restarting the node.
- priv_validator_key.json
- priv_validator_state.json
**priv validator key**
```
cp ~/.ixod/config/priv_validator_key.json ~/
```
**priv validator state**
```
cp ~/.ixod/data/priv_validator_state.json ~/
```
### 1. Backup data directory
Incase we need to restore to take the export route. Might take a while to backup. Ensure 40GB of free space
```
tar -c -z -v -f ixo-4.tar.gz /home/ixo/.ixod/data/
```

### 1. Remove chain data
We are clearing the current state and restart from a snapshot starting out at block height 308,205
```
ixod tendermint unsafe-reset-all
```
### 1. Downloading snapshot 

Snapshot guide provided by [k0kk0k](https://github.com/k0kk0k/cosmos-snapshots-doc/blob/main/ixo.md) . This will download a snapshot of the chain at block 308,205 and unzip it into the data directory.
```
cd ~/.ixod/data
SNAP_NAME=$(curl -s https://snapshots.stake2.me/ixo/ | egrep -o ">ixo.*tar" | tr -d ">" | tail -n1); \
wget -O - https://snapshots.stake2.me/ixo/${SNAP_NAME} | tar xf -
```
### 1. Restore validator info
To prevent double signing
```
cp ~/priv_validator_state.json ~/.ixod/data/priv_validator_state.json 
```
### 1. Remove previous peers
This step is to remove the probability of an attempt to sync to a node that has not been through the upgrade process and is running an older node. Missing this step could lead to attempting to sync to a node that has not taken part in the patch yet.
```
sed -i.bak -e "s/^persistent_peers *=.*/persistent_peers = \"\"/" ~/.ixod/config/config.toml
sed -i.bak -e "s/^seeds *=.*/seeds = \"\"/" ~/.ixod/config/config.toml
```
### 1. Add peers to config.toml
These peers are all verified to have started from the snapshot **TO BE ADDED**
```
SEEDS=""
PEERS="a8d9811a2f08b8a6c77e4319097d6fd84520645e@139.84.226.60:26656,f79da5c87e40587c4cfef5d7b7902b6e69ac62bf@188.166.183.216:26656,386277f9c6a0c402889032ff76585d0a2dae7bc5@104.248.1.56:26656,26593e0854848ede80d5cd963dc8a775634e2acc@23.88.69.167:26656"
sed -i.bak -e "s/^seeds *=.*/seeds = \"$SEEDS\"/" ~/.ixod/config/config.toml
sed -i.bak -e "s/^persistent_peers *=.*/persistent_peers = \"$PEERS\"/" ~/.ixod/config/config.toml
```
### 1. Verify golang version
Check the golang version
```
go version
```
If you are not on 1.19.4 please update
```
go version go1.19.4 linux/amd64
```
Update to (HAS TO BE AS IXO USER)
```
wget https://go.dev/dl/go1.19.4.linux-amd64.tar.gz
rm -rf /usr/local/go && tar -C /usr/local -xzf go1.19.4.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
go version
```
### 1.  Download and install the new binary
```
git clone https://github.com/ixofoundation/ixo-blockchain.git && cd ixo-blockchain && git checkout v0.19.2; make install
```
### 1. Verify Install
```
ixod version --long
```

```
./ixod version --long
name: ixo
server_name: ixod
version: 0.19.2
commit: b5607af9980b32b5f6a053f2e6980c71b47d9489
build_tags: ""
go: go version go1.19.4 linux/amd64
build_deps:
- filippo.io/edwards25519@v1.0.0-beta.2
- github.com/99designs/keyring@v1.2.1 => github.com/cosmos/keyring@v1.1.7-0.20210622111912-ef00f8ac3d76
- github.com/ChainSafe/go-schnorrkel@v0.0.0-20200405005733-88cbf1b4c40d
- github.com/CosmWasm/wasmd@v0.29.2
- github.com/CosmWasm/wasmvm@v1.1.1
- github.com/Workiva/go-datastructures@v1.0.53
- github.com/armon/go-metrics@v0.4.0
- github.com/beorn7/perks@v1.0.1
- github.com/bgentry/speakeasy@v0.1.0
- github.com/btcsuite/btcd@v0.22.1
- github.com/btcsuite/btcutil@v1.0.3-0.20201208143702-a53e38424cce
- github.com/cespare/xxhash/v2@v2.1.2
- github.com/coinbase/rosetta-sdk-go@v0.7.0
- github.com/confio/ics23/go@v0.7.0 => github.com/cosmos/cosmos-sdk/ics23/go@v0.8.0
- github.com/cosmos/btcutil@v1.0.4
- github.com/cosmos/cosmos-proto@v1.0.0-alpha7
- github.com/cosmos/cosmos-sdk@v0.45.9
- github.com/cosmos/go-bip39@v1.0.0
- github.com/cosmos/gogoproto@v1.4.2
- github.com/cosmos/iavl@v0.19.4
- github.com/cosmos/ibc-go/v3@v3.3.0
- github.com/creachadair/taskgroup@v0.3.2
- github.com/davecgh/go-spew@v1.1.1
- github.com/desertbit/timer@v0.0.0-20180107155436-c41aec40b27f
- github.com/dvsekhvalnov/jose2go@v1.5.0
- github.com/felixge/httpsnoop@v1.0.1
- github.com/fsnotify/fsnotify@v1.5.4
- github.com/go-kit/kit@v0.12.0
- github.com/go-kit/log@v0.2.1
- github.com/go-logfmt/logfmt@v0.5.1
- github.com/godbus/dbus@v0.0.0-20190726142602-4481cbc300e2
- github.com/gogo/gateway@v1.1.0
- github.com/gogo/protobuf@v1.3.3 => github.com/regen-network/protobuf@v1.3.3-alpha.regen.1
- github.com/golang/protobuf@v1.5.2
- github.com/golang/snappy@v0.0.4
- github.com/google/btree@v1.1.2
- github.com/google/gofuzz@v1.2.0
- github.com/google/orderedcode@v0.0.1
- github.com/gorilla/handlers@v1.5.1
- github.com/gorilla/mux@v1.8.0
- github.com/gorilla/websocket@v1.5.0
- github.com/grpc-ecosystem/go-grpc-middleware@v1.3.0
- github.com/grpc-ecosystem/grpc-gateway@v1.16.0
- github.com/gsterjov/go-libsecret@v0.0.0-20161001094733-a6f4afe4910c
- github.com/gtank/merlin@v0.1.1
- github.com/gtank/ristretto255@v0.1.2
- github.com/hashicorp/go-immutable-radix@v1.3.1
- github.com/hashicorp/golang-lru@v0.5.4
- github.com/hashicorp/hcl@v1.0.0
- github.com/hdevalence/ed25519consensus@v0.0.0-20210204194344-59a8610d2b87
- github.com/improbable-eng/grpc-web@v0.14.1
- github.com/klauspost/compress@v1.15.11
- github.com/lib/pq@v1.10.6
- github.com/libp2p/go-buffer-pool@v0.1.0
- github.com/magiconair/properties@v1.8.6
- github.com/mattn/go-colorable@v0.1.13
- github.com/mattn/go-isatty@v0.0.16
- github.com/matttproud/golang_protobuf_extensions@v1.0.2-0.20181231171920-c182affec369
- github.com/mimoo/StrobeGo@v0.0.0-20210601165009-122bf33a46e0
- github.com/minio/highwayhash@v1.0.2
- github.com/mitchellh/mapstructure@v1.5.0
- github.com/mtibben/percent@v0.2.1
- github.com/pelletier/go-toml/v2@v2.0.5
- github.com/pkg/errors@v0.9.1
- github.com/pmezard/go-difflib@v1.0.0
- github.com/prometheus/client_golang@v1.13.0
- github.com/prometheus/client_model@v0.2.0
- github.com/prometheus/common@v0.37.0
- github.com/prometheus/procfs@v0.8.0
- github.com/rakyll/statik@v0.1.7
- github.com/rcrowley/go-metrics@v0.0.0-20201227073835-cf1acfcdf475
- github.com/regen-network/cosmos-proto@v0.3.1
- github.com/rs/cors@v1.8.2
- github.com/rs/zerolog@v1.27.0
- github.com/spf13/afero@v1.8.2
- github.com/spf13/cast@v1.5.0
- github.com/spf13/cobra@v1.6.0
- github.com/spf13/jwalterweatherman@v1.1.0
- github.com/spf13/pflag@v1.0.5
- github.com/spf13/viper@v1.13.0
- github.com/stretchr/testify@v1.8.0
- github.com/subosito/gotenv@v1.4.1
- github.com/syndtr/goleveldb@v1.0.1-0.20210819022825-2ae1ddf74ef7
- github.com/tendermint/btcd@v0.1.1
- github.com/tendermint/crypto@v0.0.0-20191022145703-50d29ede1e15
- github.com/tendermint/go-amino@v0.16.0
- github.com/tendermint/tendermint@v0.34.23
- github.com/tendermint/tm-db@v0.6.7
- golang.org/x/crypto@v0.1.0
- golang.org/x/exp@v0.0.0-20220722155223-a9213eeb770e
- golang.org/x/net@v0.1.0
- golang.org/x/sys@v0.1.0
- golang.org/x/term@v0.1.0
- golang.org/x/text@v0.4.0
- google.golang.org/genproto@v0.0.0-20221014213838-99cd37c6964a
- google.golang.org/grpc@v1.50.1 => google.golang.org/grpc@v1.33.2
- google.golang.org/protobuf@v1.28.2-0.20220831092852-f930b1dc76e8
- gopkg.in/ini.v1@v1.67.0
- gopkg.in/yaml.v2@v2.4.0
- gopkg.in/yaml.v3@v3.0.1
- nhooyr.io/websocket@v1.8.6
cosmos_sdk_version: v0.45.9
```

### 1. Start chain at ```January, 12 2023, 3 PM UTC```
Start the node
```
systemctl restart ixod
```
