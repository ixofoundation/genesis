**Instructions to switch out the binary**

---

### 1. Stop the validator

```
sudo systemctl stop ixod
```

### 2. Backup validator info

For this prupose we would not be importing back in unless something goes wrong uring the upgrade process.

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

### 3. Backup data directory

Incase we need to restore to take the export route. Might take a while to backup.

```
tar -c -z -v -f pandora-7.tar.gz /home/ixo/.ixod/data/
```

### 4. Binary version

    ixod version

This should show

    0.19.3

if you have already switched out the binary please revert to 0.19.3 for this step

### 5. Exporting genesis (IXO user)

This will output a file called genesis.json

    # go to config directory and export hash
    cd ~/.ixod/config
    #make sure your user has docker permissions. Run this ONE command as root
    usermod -aG docker ixo
    #the docker file NEEDS to be run instead of doing the export through the binary since we ran into some issues regarding some of the modules.
    docker run -v /home/ixo/:/ixo/ ghcr.io/ixofoundation/ixo-blockchain:debug-0.19.4 export --for-zero-height --height=1044099 > exported.json

    #check hash for exported genesis
    jq -S -c -M '' exported.json | shasum -a 256
    result: 42faf5ec3cb924d831c1e4d14e019bc2c744a5a63722fd3c75ff369e7b892ea5  -

    #download migration script
    wget https://raw.githubusercontent.com/ixofoundation/genesis/main/pandora-8/scripts/migrate_export_from_v0.19.3_to_v0.20.0.py

    #run migrations
    python3 migrate_export_from_v0.19.3_to_v0.20.0.py

    #check hash for migrated genesis
    jq -S -c -M '' genesis.json | shasum -a 256
    result: bb4132cab90b8f942805215342e9c27d4db775c1f740edaee82bd7794ed91bec  -

If you initial hash is different please inform as via discord, however if the second hash is the same continue with the guide.

### 6. Reset validator

This will this will remove the addressbook and everything in the data directory, including the priv_validator_state.json

    ixod tendermint unsafe-reset-all

### 7. Remove previous peers

```
sed -i.bak -e "s/^persistent_peers *=.*/persistent_peers = \"\"/" ~/.ixod/config/config.toml
sed -i.bak -e "s/^seeds *=.*/seeds = \"\"/" ~/.ixod/config/config.toml
```

### 8. Add peers to config.toml

```
SEEDS=""
PEERS="650b6c33030c93c1c5aed92df52c08860c20f5b4@136.244.117.176:26656,2a7ef01058d42f9950b8e01415e60d6ee20e36f4@139.84.231.209:26656,245d3341fd17d302409f863e6e8863e276093150@57.128.144.250:26656"
sed -i.bak -e "s/^seeds *=.*/seeds = \"$SEEDS\"/" ~/.ixod/config/config.toml
sed -i.bak -e "s/^persistent_peers *=.*/persistent_peers = \"$PEERS\"/" ~/.ixod/config/config.toml
```

### 9. Verify golang version

Check the golang version

```
go version
```

If you aren't on 1.19.4 please update

```
go1.19.4 linux/amd64
```

Update only if you arent on go1.19.4 (HAS TO BE AS IXO USER)

```
wget https://go.dev/dl/go1.19.4.linux-amd64.tar.gz
rm -rf /usr/local/go && tar -C /usr/local -xzf go1.19.4.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
go version
```

### 10. Download and install the new binary

#### SKIP this step if you are already on 0.20.0

```
git clone https://github.com/ixofoundation/ixo-blockchain.git && cd ixo-blockchain && git checkout v0.20.0; make install
```

### 11. Verify Install

    ixod version

If the version matches 0.20.0 You can start the node

    systemctl restart ixod
