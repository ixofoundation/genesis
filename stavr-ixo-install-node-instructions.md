**IXO Blockchain Node Installation Guide**

This document provides a step-by-step guide for installing and setting up a full node for the IXO blockchain. Follow these instructions carefully to ensure a smooth setup.

---

## **1. Server Preparation**
Before installing the IXO node, update your system and install the necessary dependencies:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install curl tar wget clang pkg-config libssl-dev jq build-essential bsdmainutils git make ncdu gcc git jq chrony liblz4-tool -y
```

---

## **2. Install Go**
The IXO blockchain requires Go. Install the recommended version:

```bash
ver="1.21.6"
wget "https://golang.org/dl/go$ver.linux-amd64.tar.gz"
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf "go$ver.linux-amd64.tar.gz"
rm "go$ver.linux-amd64.tar.gz"
echo "export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin" >> $HOME/.bash_profile
source $HOME/.bash_profile
go version
```

Verify the installation:
```bash
go version
```

---

## **3. Build the IXO Node**
Clone the IXO repository and compile the node software:

```bash
git clone https://github.com/ixofoundation/ixo-blockchain.git
cd ixo-blockchain
git checkout latest
make install
```

Verify the installation:
```bash
ixod version
```

---

## **4. Initialize the Node**

Set up the node configuration:
```bash
ixod init "YourNodeName" --chain-id ixo-mainnet
```

Download the genesis file:
```bash
curl -s https://raw.githubusercontent.com/ixofoundation/ixo-blockchain/mainnet/genesis.json > ~/.ixod/config/genesis.json
```

Set peers and seeds:
```bash
sed -i 's/persistent_peers = ""/persistent_peers = "peer-addresses-here"/g' ~/.ixod/config/config.toml
```

---

## **5. Set Minimum Gas Price**

Modify the configuration file:
```bash
sed -i 's/minimum-gas-prices = ""/minimum-gas-prices = "0.025uixo"/g' ~/.ixod/config/app.toml
```

---

## **6. Create a Systemd Service**
To run the IXO node as a service, create a systemd file:

```bash
sudo tee /etc/systemd/system/ixod.service > /dev/null <<EOF
[Unit]
Description=IXO Node
After=network.target

[Service]
User=$USER
ExecStart=$(which ixod) start
Restart=always
RestartSec=3
LimitNOFILE=4096

[Install]
WantedBy=multi-user.target
EOF
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ixod
sudo systemctl start ixod
```

Check the node status:
```bash
ixod status
```

---

## **7. Fast Sync Using Snapshot**
To speed up the synchronization process, use a snapshot:

```bash
cd ~/.ixod
rm -rf data
wget -O snapshot.tar.gz "https://snapshots.url/ixo-latest.tar.gz"
tar -xzvf snapshot.tar.gz
rm snapshot.tar.gz
```

Restart the node:
```bash
sudo systemctl restart ixod
```

---

## **8. Validator Setup (Optional)**
If you want to run a validator, create a wallet and register as a validator:

Create a new wallet:
```bash
ixod keys add mywallet
```

Create a validator:
```bash
ixod tx staking create-validator \
--amount=1000000uixo \
--pubkey=$(ixod tendermint show-validator) \
--moniker="YourValidatorName" \
--chain-id=ixo-mainnet \
--commission-rate=0.10 \
--commission-max-rate=0.20 \
--commission-max-change-rate=0.01 \
--min-self-delegation=1 \
--from=mywallet
```

---

## **9. Node Maintenance**
- Check logs: `journalctl -u ixod -f`
- Restart node: `sudo systemctl restart ixod`
- Stop node: `sudo systemctl stop ixod`
- Upgrade node: `cd ixo-blockchain && git pull && make install`

---

## **Conclusion**
This guide outlines the steps to install, configure, and run an IXO blockchain node. For further support, visit the [official IXO documentation](https://github.com/ixofoundation/ixo-blockchain).

