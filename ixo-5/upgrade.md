# Upgrade instructions from ixo-4 to ixo-5

### 1. Stop the validator

```
sudo systemctl stop ixod
```

### 2. Backup validator info

For this prupose we would not be importing back in unless something goes wrong during the upgrade process.

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

Incase we need to restore to take the export route. Might take a while to backup. Make sure you have adequate space before attempting a backup. The size estimate as of current is 91GB+.  
Check the current size:

    du -h /home/ixo/.ixod/data/

Backup to current directory

    tar -c -z -v -f ixo-4.tar.gz /home/ixo/.ixod/data/

### 4. Confirm binary version

    ixod version

This should show

    0.19.3

if you have already switched out the binary please revert to 0.19.3 for this step

### 5. Exporting genesis (IXO user)

This will output a file called genesis.json

    # go to config directory and export hash
    cd ~/.ixod/config
    ixod export --for-zero-height --height={height} > exported.json

    #check hash for exported genesis
    jq -S -c -M '' exported.json | shasum -a 256
    result: {result}

    #download migration script
    wget {raw-link}

    #run migrations
    python3 migrate_export_from_v0.19.3_to_v0.20.0.py

    #check hash for migrated genesis
    jq -S -c -M '' genesis.json | shasum -a 256
    result: {result} 


If your genesis.json hash is the same you can continue with the guide, If exported.json hash is different please do let as know via discord.
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
PEERS="a8d9811a2f08b8a6c77e4319097d6fd84520645e@139.84.226.60:26656,f79da5c87e40587c4cfef5d7b7902b6e69ac62bf@188.166.183.216:26656,386277f9c6a0c402889032ff76585d0a2dae7bc5@104.248.1.56:26656,26593e0854848ede80d5cd963dc8a775634e2acc@23.88.69.167:26656"
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
