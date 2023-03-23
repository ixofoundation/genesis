# Upgrade instructions from ixo-4 to ixo-5

### 1. Stop the validator

```
sudo systemctl stop ixod
```

### 2. Backup validator info

NB: Important to backup your validator information.

**priv validator key**
- priv_validator_key.json
  - Recovers your validator if this upgrade does not go as planned.

```
cp ~/.ixod/config/priv_validator_key.json ~/
```

**priv validator state**

- priv_validator_state.json
  - Prevents double signing when restarting the node.
```
cp ~/.ixod/data/priv_validator_state.json ~/
```

We will not import these unless something goes wrong during the upgrade process.

### 3. Backup data directory

Backup your data directory in case we need to restore and take the export route.

NB: It might take a while for this backup to complete.

Make sure you have adequate space before attempting the backup (current size estimate is 92GB).

You can check the current size like this:

    du -h /home/ixo/.ixod/data/

You can backup to the current directory like this:

    tar -c -z -v -f ixo-4.tar.gz /home/ixo/.ixod/data/

### 4. Confirm binary version

    ixod version

This should show

    0.19.3

If you have already switched out the binary and are not on 0.19.3, please revert to 0.19.3.

### 5. Exporting genesis (with IXO user)

This will output a file called genesis.json

    # go to config directory and export
    cd ~/.ixod/config
    ixod export --for-zero-height --height=1344999 > exported.json

    #check hash for exported genesis
    jq -S -c -M '' exported.json | shasum -a 256
    result: {result}

    #download migration script
    wget https://raw.githubusercontent.com/ixofoundation/genesis/main/ixo-5/scripts/migrate_export_from_v0.19.3_to_v0.20.0.py

    #run migrations
    python3 migrate_export_from_v0.19.3_to_v0.20.0.py

    #check hash for migrated genesis
    jq -S -c -M '' genesis.json | shasum -a 256
    result: {result} 

1. If your exported.json hash is different to the above, notify the `validator-chat` channel on Discord.
1. If your genesis.json hash is the same as above you can continue with the guide.

### 6. Reset validator

NB: This will remove the `addressbook` and everything in the data directory, including the priv_validator_state.json

    ixod tendermint unsafe-reset-all

### 7. Remove previous peers

```
sed -i.bak -e "s/^persistent_peers *=.*/persistent_peers = \"\"/" ~/.ixod/config/config.toml
sed -i.bak -e "s/^seeds *=.*/seeds = \"\"/" ~/.ixod/config/config.toml
```

### 8. Add peers to config.toml

```
SEEDS=""
PEERS="ef2035826146c718a2196edfeca47630e14e36f7@135.181.223.115:2130,a8d9811a2f08b8a6c77e4319097d6fd84520645e@139.84.226.60:26656,f79da5c87e40587c4cfef5d7b7902b6e69ac62bf@188.166.183.216:26656,386277f9c6a0c402889032ff76585d0a2dae7bc5@104.248.1.56:26656,26593e0854848ede80d5cd963dc8a775634e2acc@23.88.69.167:26656"
sed -i.bak -e "s/^seeds *=.*/seeds = \"$SEEDS\"/" ~/.ixod/config/config.toml
sed -i.bak -e "s/^persistent_peers *=.*/persistent_peers = \"$PEERS\"/" ~/.ixod/config/config.toml
```

### 9. Verify golang version

Check the golang version

```
go version
```

```
go1.19.4 linux/amd64
```

NB: Update if you are not on go1.19.4 (ensure this is with the IXO user!)

```
#as the IXO user
wget https://go.dev/dl/go1.19.4.linux-amd64.tar.gz
rm -rf /usr/local/go && tar -C /usr/local -xzf go1.19.4.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
go version
```

### 10. Download and install the new ixo binary

#### Skip this step if you are already on 0.20.0

```
git clone https://github.com/ixofoundation/ixo-blockchain.git && cd ixo-blockchain && git checkout v0.20.0; make install
```

### 11. Verify Install
Ensure that your node is on version 0.20.0.

    ixod version

If this shows 0.20.0, then start your node.

    systemctl restart ixod

### Note. External signers
In case of external signers like TMKMS (Tendermint KMS) remember to change `id / chain_ids` and adapt `state_file`
