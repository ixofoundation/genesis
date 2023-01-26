**Patch instructions**
___
### 1. Stop the validator
```
sudo systemctl stop ixod
```
### 2. Backup validator info
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
Incase we need to restore to take the export route. Might take a while to backup. Ensure 40GB of free space (Not necessary with this patch)
```
tar -c -z -v -f pandora-7.tar.gz /home/ixo/.ixod/data/
cp ~/priv_validator_state.json ~/.ixod/data/priv_validator_state.json 
```
### 9. Verify golang version
Check the golang version
```
go version
```
If you aren't on 1.19.4 please update
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
### 10.  Download and install the new binary
#### SKIP this step if you are already on 0.19.3
```
git clone https://github.com/ixofoundation/ixo-blockchain.git && cd ixo-blockchain && git checkout v0.19.3; make install
```
### 11. Verify Install
```
ixod version --long
```

``````

### 12. Start chain
Start the node and wait for other validators to come online.
```
systemctl restart ixod
```
