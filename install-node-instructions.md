# IXO Blockchain Node Installation Guide

## Table of Contents

- [Hardware Requirements](#hardware-requirements)
- [Security Setup](#security-setup)
- [Basic Installation](#basic-installation)
- [Node Configuration](#node-configuration)
- [Monitoring Setup](#monitoring-setup)
- [Backup Procedures](#backup-procedures)
- [Validator Setup](#validator-setup)
- [Maintenance](#maintenance)
- [Troubleshooting](#troubleshooting)

## Hardware Requirements

**Minimum Requirements:**

- CPU: 2 cores
- RAM: 4GB
- Storage: 50GB SSD (NVMe preferred)
- Network: 100Mbps dedicated connection

_These specifications ensure optimal performance and reliability for running a full node._

## Security Setup

```bash
# With the `root` user, create a new dedicated user, set the new user's password, switch to the new user, and confirm that it has `sudo` privileges
useradd -m -s /bin/bash ixo
usermod -aG sudo ixo
# Store the password securely; preferrably to a password manager.
passwd ixo
su - ixo
sudo whoami
# `root` should be displayed

# Secure SSH - The following measures assume that you have generated an SSH key pair on your local machine
# Ensure that your public key is stored on the server.
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo systemctl restart sshd

# Firewall setup
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 26656/tcp  # P2P port
sudo ufw allow 26657/tcp  # RPC port (restrict to trusted IPs)
sudo ufw enable

# System security settings
sudo tee /etc/sysctl.d/99-ixo-node.conf > /dev/null <<EOF
# Network security
net.ipv4.tcp_syncookies=1
net.ipv4.tcp_max_syn_backlog=8192
net.ipv4.tcp_synack_retries=3

# System limits
fs.file-max=65535
vm.swappiness=1
EOF

sudo sysctl --system
```

## Basic Installation

### 1. System Updates and Dependencies

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install curl tar wget clang pkg-config libssl-dev jq build-essential bsdmainutils git make ncdu gcc chrony -y
```

### 2. Install Go

```bash
ver="1.22.4"  # Check latest compatible version
wget "https://golang.org/dl/go$ver.linux-amd64.tar.gz"
# Verify checksum (check official Go website for correct hash)
sha256sum "go$ver.linux-amd64.tar.gz"
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf "go$ver.linux-amd64.tar.gz"
rm "go$ver.linux-amd64.tar.gz"

# Set up Go environment
echo "export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin" >> $HOME/.bash_profile
echo "export GOPATH=$HOME/go" >> $HOME/.bash_profile
source $HOME/.bash_profile

# Verify installation
go version
```

### 3. Install Cosmovisor

```bash
go install github.com/cosmos/cosmos-sdk/cosmovisor/cmd/cosmovisor@latest

# Set up Cosmovisor directories
mkdir -p ~/.ixod/cosmovisor/genesis/bin
mkdir -p ~/.ixod/cosmovisor/upgrades
```

### 4. Build IXO Node

```bash
git clone https://github.com/ixofoundation/ixo-blockchain.git
cd ixo-blockchain
git checkout latest  # Replace with specific version tag
#git checkout v4.0.0
make install
# Place the binary in the Cosmovisor directory structure
mv $(which ixod) ~/.ixod/cosmovisor/genesis/bin/
ls -l ~/.ixod/cosmovisor/genesis/bin/ixod # Verify the binary placement
chmod +x ~/.ixod/cosmovisor/genesis/bin/ixod # Ensure the correct binary permissions
# Verify installation
ixod version
```

## Node Configuration

### 1. Initialize Node

```bash
ixod init "YourNodeName" --chain-id ixo-5  # Use current chain ID

# Download genesis file
curl -s https://raw.githubusercontent.com/ixofoundation/genesis/main/ixo-5/genesis.json > ~/.ixod/config/genesis.json

# Verify genesis checksum
jq -S -c -M '.' ~/.ixod/config/genesis.json | shasum -a 256
# cbd2eb53eaaad2a5783fbab1c1f428c11f4f26156185a4627119026ffd0dc01c
```

### 2. Configure Node

```bash
# Set minimum gas price
sed -i.bak 's/minimum-gas-prices = ""/minimum-gas-prices = "0.025uixo"/g' ~/.ixod/config/app.toml

# Add seeds and persistent peers
SEEDS="f79da5c87e40587c4cfef5d7b7902b6e69ac62bf@188.166.183.216:26656"  # Replace with actual seeds
PEERS="f79da5c87e40587c4cfef5d7b7902b6e69ac62bf@188.166.183.216:26656"  # Replace with actual peers
sed -i.bak -e "s/^seeds *=.*/seeds = \"$SEEDS\"/" ~/.ixod/config/config.toml
sed -i -e "s/^persistent_peers *=.*/persistent_peers = \"$PEERS\"/" ~/.ixod/config/config.toml

# Optimize configuration
sed -i 's/timeout_commit = "5s"/timeout_commit = "3s"/g' ~/.ixod/config/config.toml
sed -i 's/index_all_keys = false/index_all_keys = true/g' ~/.ixod/config/config.toml

# Configure pruning
pruning="custom"
pruning_keep_recent="1000"
pruning_keep_every="0"
pruning_interval="10"

sed -i -e "s/^pruning *=.*/pruning = \"$pruning\"/" $HOME/.ixod/config/app.toml
sed -i -e "s/^pruning-keep-recent *=.*/pruning-keep-recent = \"$pruning_keep_recent\"/" $HOME/.ixod/config/app.toml
sed -i -e "s/^pruning-keep-every *=.*/pruning-keep-every = \"$pruning_keep_every\"/" $HOME/.ixod/config/app.toml
sed -i -e "s/^pruning-interval *=.*/pruning-interval = \"$pruning_interval\"/" $HOME/.ixod/config/app.toml

# Add indexer capabilities
indexer="kv"  # Change to "psql" if using PostgreSQL, or "null" to disable
sed -i -e "s/^indexer *=.*/indexer = \"$indexer\"/" $HOME/.ixod/config/config.toml
```

### Pruning Explanation

- **Pruning Configuration:** The pruning settings are added to manage the node's data storage efficiently. By setting `pruning` to `"custom"`, you can specify how much historical data to keep and how often to prune.
- **Placement:** Adding these commands after the existing configuration settings ensures that all node parameters are set up in one place, making the setup process more organized and easier to follow.

### Indexer Considerations

- **PostgreSQL Setup:** If you choose `"psql"` for the indexer, ensure that you have a PostgreSQL database set up and configured to work with your node.
- **Performance:** Enabling indexing can increase disk usage and may impact performance, so choose the indexing method that best fits your needs.

### 3. Setup Systemd Service

```bash
sudo tee /etc/systemd/system/ixod.service > /dev/null <<EOF
[Unit]
Description=IXO Node
After=network-online.target

[Service]
User=$USER
ExecStart=$(which cosmovisor) run start
Restart=always
RestartSec=3
LimitNOFILE=65535
Environment="DAEMON_HOME=$HOME/.ixod"
Environment="DAEMON_NAME=ixod"
Environment="DAEMON_ALLOW_DOWNLOAD_BINARIES=false"
Environment="DAEMON_RESTART_AFTER_UPGRADE=true"

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable ixod
```

### 4. Start Node

Once you have configured everything and enabled the service, you can start the IXO blockchain node using the following steps:

1. **Start the Node Service:**

   - Use the following command to start the IXO node service:
     ```bash
     sudo systemctl start ixod
     ```

2. **Check the Status:**

   - To ensure that the node has started correctly, check the status of the service:
     ```bash
     sudo systemctl status ixod
     ```
   - Look for the "active (running)" status to confirm that the node is operational.

3. **View Logs:**
   - To monitor the node's activity and check for any errors, view the logs:
     ```bash
     journalctl -fu ixod -f
     ```
   - This will show real-time logs from the node, helping you verify that it is syncing with the network and operating as expected.

### Additional Considerations

- **Automatic Start on Boot:**

  - Since you have enabled the service with `sudo systemctl enable ixod`, the node will automatically start whenever the server is rebooted.

- **Troubleshooting:**
  - If the node does not start or you encounter issues, check the logs for error messages and ensure that all configuration files are correctly set up.

## Monitoring Setup

### 1. Basic Monitoring Script

```bash
cat > monitor-ixo.sh << 'EOF'
#!/bin/bash
# Basic monitoring checks
NODE_STATUS=$(curl -s localhost:26657/status)
CATCHING_UP=$(echo $NODE_STATUS | jq -r '.result.sync_info.catching_up')
LATEST_BLOCK=$(echo $NODE_STATUS | jq -r '.result.sync_info.latest_block_height')
VOTING_POWER=$(echo $NODE_STATUS | jq -r '.result.validator_info.voting_power')

echo "Node Status:"
echo "Catching up: $CATCHING_UP"
echo "Latest block: $LATEST_BLOCK"
echo "Voting power: $VOTING_POWER"
EOF

chmod +x monitor-ixo.sh
```

### 2. Additional Monitoring

#### 1. Install Prometheus and Node Exporter

```bash
# Install Prometheus
sudo apt-get install -y prometheus

# Configure Cosmos SDK metrics
sed -i 's/prometheus = false/prometheus = true/g' ~/.ixod/config/config.toml
sed -i 's/prometheus_listen_addr = ":26660"/prometheus_listen_addr = "127.0.0.1:26660"/g' ~/.ixod/config/config.toml
```

#### 2. Configure Prometheus

1. **Edit Prometheus Configuration:**

   - Open the Prometheus configuration file, usually located at `/etc/prometheus/prometheus.yml`, and add a job to scrape metrics from your IXO node:
     ```yaml
     scrape_configs:
       - job_name: "ixo_node"
         static_configs:
           - targets: ["localhost:26660"]
     ```

2. **Restart Prometheus:**

   - After editing the configuration, restart the Prometheus service to apply the changes:
     ```bash
     sudo systemctl restart prometheus
     ```

#### 3. Install and Configure Node Exporter

1. **Install Node Exporter:**

   - Download and install Node Exporter to collect system metrics:
     ```bash
     wget https://github.com/prometheus/node_exporter/releases/download/v1.3.1/node_exporter-1.3.1.linux-amd64.tar.gz
     tar xvfz node_exporter-1.3.1.linux-amd64.tar.gz
     sudo cp node_exporter-1.3.1.linux-amd64/node_exporter /usr/local/bin/
     ```

2. **Create a Systemd Service for Node Exporter:**

   - Create a service file for Node Exporter:

     ```bash
     sudo tee /etc/systemd/system/node_exporter.service > /dev/null <<EOF
     [Unit]
     Description=Node Exporter
     After=network.target

     [Service]
     User=$USER
     ExecStart=/usr/local/bin/node_exporter

     [Install]
     WantedBy=default.target
     EOF
     ```

3. **Start and Enable Node Exporter:**

   - Start the Node Exporter service and enable it to start on boot:
     ```bash
     sudo systemctl daemon-reload
     sudo systemctl start node_exporter
     sudo systemctl enable node_exporter
     ```

4. **Add Node Exporter to Prometheus:**

   - Add a new job to the Prometheus configuration to scrape metrics from Node Exporter:
     ```yaml
     scrape_configs:
       - job_name: "node_exporter"
         static_configs:
           - targets: ["localhost:9100"]
     ```

5. **Restart Prometheus:**

   - Restart Prometheus again to apply the new configuration:
     ```bash
     sudo systemctl restart prometheus
     ```

#### 4. Access Prometheus Dashboard

- **Open Prometheus Dashboard:**

  - Access the Prometheus web interface by navigating to `http://<your-server-ip>:9090` in your web browser. Here, you can query and visualize metrics collected from your IXO node and system.

By following these steps, you will have a basic monitoring setup using Prometheus and Node Exporter to track the performance and health of your IXO blockchain node.

## Backup Procedures

### 1. Create Backup Script

```bash
cat > backup-ixo-config.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="$HOME/ixo_backup"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

# Stop the service temporarily
sudo systemctl stop ixod

# Backup validator keys
cp ~/.ixod/config/priv_validator_key.json "$BACKUP_DIR/priv_validator_key.json_$DATE"
cp ~/.ixod/config/node_key.json "$BACKUP_DIR/node_key.json_$DATE"

# Backup validator state
cp ~/.ixod/data/priv_validator_state.json "$BACKUP_DIR/priv_validator_state.json_$DATE"

# Compress config directory
tar czf "$BACKUP_DIR/ixo_config_$DATE.tar.gz" ~/.ixod/config/

# Restart the service
sudo systemctl start ixod

# Cleanup old backups (keep last 7 days)
find "$BACKUP_DIR" -type f -mtime +7 -delete
EOF

chmod +x backup-ixo-config.sh
```

### 2. Backup `data` Directory

Backup your data directory in case of need to restore and export.

NB: Backups may take a long time to complete due to the large amount of data.
Make sure you have adequate space before attempting the backup (current size estimate is 100GB).

You can check the current size like this:

```bash
du -h /home/ixo/.ixod/data/
```

You can backup to the current directory like this:

```bash
tar -c -z -v -f ixo-4.tar.gz /home/ixo/.ixod/data/
```

## Validator Setup

### 1. Create Validator

```bash
# Create wallet
ixod keys add validator --keyring-backend file
ixod keys list --keyring-backend file # Shows your recently added account

# After receiving tokens, create validator
ixod tx staking create-validator \
  --amount=1000000uixo \
  --pubkey=$(ixod tendermint show-validator) \
  --moniker="YOUR_VALIDATOR_NAME" \
  --chain-id=ixo-5 \
  --commission-rate=0.10 \
  --commission-max-rate=0.20 \
  --commission-max-change-rate=0.01 \
  --min-self-delegation=1 \
  --gas=auto \
  --gas-adjustment=1.5 \
  --gas-prices=0.025uixo \
  --from=validator \
  --keyring-backend=file
```

## Maintenance

### Common Commands

```bash
# Check logs
journalctl -u ixod -f

# Check node status
ixod status

# Check sync status
curl -s localhost:26657/status | jq .result.sync_info

# Restart node
sudo systemctl restart ixod

# Stop node
sudo systemctl stop ixod
```

## Troubleshooting

### Common Issues and Solutions

1. Node Not Syncing

```bash
# Check network connectivity
curl -s localhost:26657/net_info | jq .result.n_peers

# Clear data if corrupted
sudo systemctl stop ixod
ixod tendermint unsafe-reset-all
sudo systemctl start ixod
```

2. Out of Memory

```bash
# Check memory usage
free -h

# Adjust system memory parameters
echo "vm.swappiness=1" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

3. Disk Space Issues

```bash
# Check disk usage
df -h

# Clean old data if necessary
sudo systemctl stop ixod
ixod tendermint unsafe-reset-all --keep-addr-book
sudo systemctl start ixod
```

### Emergency Procedures

1. Quick Node Recovery

```bash
# Backup keys
cp ~/.ixod/config/priv_validator_key.json ~/backup/
cp ~/.ixod/config/node_key.json ~/backup/

# Reset node
ixod tendermint unsafe-reset-all
```

2. Version Rollback

```bash
# Stop node
sudo systemctl stop ixod

# Switch to previous version
cd ixo-blockchain
git checkout <previous-version>
make install

# Start node
sudo systemctl start ixod
```

Remember to join the [IXO Discord](https://discord.gg/ixo) for community support and updates.
