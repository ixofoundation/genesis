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

## Security Setup

```bash
# SSH to your newly created server instance with the `root` user
ssh root@your-IP-address

# You will see the following message when you connect for the first time.
# "The authenticity of host 'your-IP-address (your-IP-address)' can't be established.
# "ED25519 key fingerprint is SHA256:moHx1ry2XgUxrlelNaL2wukQQdGc8lg+7Hmr4fQqWH8."
# "This key is not known by any other names."
# You can confirm the cryptographic fingerprint by:
#   1. Running this command on the host console (usually a web browser terminal on your cloud provider).
#     ssh-keygen -l -f /etc/ssh/ssh_host_ed25519_key.pub
#   2. Comparing the hash with the "ED25519 key fingerprint is SHA256:moHx1ry2XgUxrlelNaL2wukQQdGc8lg+7Hms5fQqWH8."
# You can continue and select "yes" when hey are the same.
# "Are you sure you want to continue connecting (yes/no/[fingerprint])? yes"
# "Warning: Permanently added 'your-IP-address' (ED25519) to the list of known hosts."

# With the `root` user, create a new dedicated user, set the new user's password, switch to the new user, and confirm that it has `sudo` privileges
useradd -m -s /bin/bash ixo
usermod -aG sudo ixo
# Store the password securely; preferrably to a password manager.
passwd ixo
# Switch to the new user
su - ixo
# Confirm that the new user has sudo privileges
sudo whoami
# `root` should be displayed

# Disconnect from SSH
exit
# Ensure that your public key is stored on the server.
ssh-copy-id root@your-IP-address
# SSH connect as the `root` user
# Switch to the ixo user and create the .ssh directory with appropriate permissions
su - ixo
mkdir -p ~/.ssh
chmod 700 ~/.ssh/
# Switch to the `root` user and copy the public key to the ixo user with appropriate permissions
su - root
cp /root/.ssh/authorized_keys /home/ixo/.ssh/authorized_keys
chown ixo:ixo /home/ixo/.ssh/ -R
chmod 600 /home/ixo/.ssh//authorized_keys
# Test SSH Login as the ixo user from your local machine
ssh ixo@your-IP-address
# Secure SSH - The following measures assume that you have generated an SSH key pair on your local machine
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo systemctl restart sshd

# Firewall setup
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
# P2P port
sudo ufw allow 26656/tcp
sudo ufw enable

# Create the system security settings configuration
sudo tee /etc/sysctl.d/99-ixo-node.conf > /dev/null <<EOF
# Network security
net.ipv4.tcp_syncookies=1
net.ipv4.tcp_max_syn_backlog=8192
net.ipv4.tcp_synack_retries=3

# System limits
fs.file-max=65535
vm.swappiness=1
EOF
# Confirm that the configuration was written to file
cat /etc/sysctl.d/99-ixo-node.conf
# Apply all sysctl changes immediately
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
ver="1.22.4"  # Latest currently compatible version
wget "https://golang.org/dl/go$ver.linux-amd64.tar.gz"
# Verify checksum (check official Go website for correct hash)
sha256sum "go$ver.linux-amd64.tar.gz"
# Compare this with the official checksum from Go's download page
echo "Checksum at site https://go.dev/dl is: ba79d4526102575196273416239cca418a651e049c2b099f3159db85e7bade7d for $ver"
echo "Your downloaded file's checksum is: $(sha256sum go$ver.linux-amd64.tar.gz | awk '{print $1}')"
# Clean up
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

### 4. Build IXO

```bash
git clone https://github.com/ixofoundation/ixo-blockchain.git
cd ixo-blockchain
# Replace with specific version tag based on your synchronisation method strategy
# Full Sync requires > git checkout v0.20.0
# State Sync and Snapshot Sync require > git checkout v4.0.0
git checkout ...
make install
# Place the binary in the Cosmovisor directory structure
mv $(which ixod) ~/.ixod/cosmovisor/genesis/bin/
# Verify the binary placement
ls -l ~/.ixod/cosmovisor/genesis/bin/ixod
# Ensure the correct binary permissions
chmod +x ~/.ixod/cosmovisor/genesis/bin/ixod
# Set up a symbolic link to ensure simple command-line usage
ln -s ~/.ixod/cosmovisor/genesis/bin/ixod ~/go/bin/ixod
# Verify installation
ixod version --long | grep -e commit -e version
```

## Node Configuration

### 1. Initialize Node

```bash
# Initialise with the current chain ID and replace "YourNodeName" with your organisation name
ixod init "YourNodeName" --chain-id ixo-5
# Set the default chain ID
ixod config chain-id ixo-5
# The command has changed in Cosmos SDK v0.50
# ixod config set client chain-id ixo-5

# Download the suggested genesis file
curl -s https://raw.githubusercontent.com/ixofoundation/genesis/main/ixo-5/genesis.json > ~/.ixod/config/genesis.json

# Verify genesis checksum
jq -S -c -M '.' ~/.ixod/config/genesis.json | shasum -a 256
# cbd2eb53eaaad2a5783fbab1c1f428c11f4f26156185a4627119026ffd0dc01c
```

### 2. Configure Node

```bash
# Add seeds and persistent peers
# Replace with actual seeds adn peers provided by the community
# For example: SEEDS="f79da5c87e40587c4cfef5d7b7902b6e69ac62bf@188.166.183.216:26656"
# And: PEERS="f79da5c87e40587c4cfef5d7b7902b6e69ac62bf@188.166.183.216:26656"
SEEDS="node-id@node-ip-address:port"
PEERS="node-id@node-ip-address:port"
sed -i.bak -e "s/^seeds *=.*/seeds = \"$SEEDS\"/" ~/.ixod/config/config.toml
sed -i -e "s/^persistent_peers *=.*/persistent_peers = \"$PEERS\"/" ~/.ixod/config/config.toml

# Configure pruning
pruning="custom"
pruning_keep_recent="1000"
pruning_keep_every="0"
pruning_interval="10"

sed -i -e "s/^pruning *=.*/pruning = \"$pruning\"/" $HOME/.ixod/config/app.toml
sed -i -e "s/^pruning-keep-recent *=.*/pruning-keep-recent = \"$pruning_keep_recent\"/" $HOME/.ixod/config/app.toml
sed -i -e "s/^pruning-keep-every *=.*/pruning-keep-every = \"$pruning_keep_every\"/" $HOME/.ixod/config/app.toml
sed -i -e "s/^pruning-interval *=.*/pruning-interval = \"$pruning_interval\"/" $HOME/.ixod/config/app.toml
```

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

Use the following command to start the IXO node service:

```bash
sudo systemctl start ixod
```

2. **Check the Status:**

To ensure that the node has started correctly, check the status of the service:

```bash
systemctl status ixod
```

Look for the "active (running)" status to confirm that the node is operational.

3. **View Logs:**
   To monitor the node's activity and check for any errors, view the logs:

```bash
journalctl -fu ixod -f
```

This will show real-time logs from the node, helping you verify that it is syncing with the network and operating as expected.

## Validator Setup

### 1. Create or Recover Wallet

```bash
# Create your validator wallet or recover an existing one by replacing <walletname> with your wallet's name
# Ensure that you choose a strong keyring passphrase and enter it twice when prompted
ixod keys add <walletname>
# Show your recently added account
ixod keys list
# Recover an existing wallet with this command
# ixod keys add <walletname> --recover
```

### 2. Create Validator

```bash
# After receiving IXO tokens into your <walletname> account, create your validator for this node
# <your-node-pub-key> can be retrieved with this command:
ixod tendermint show-validator
# First, create a JSON file with the following details.
{
        "pubkey": {"@type":"/cosmos.crypto.ed25519.PubKey","key":"<your-node-pub-key>"},
        "amount": "1000000uixo",
        "moniker": "<your-validator-name>",
        "commission-rate": "0.1",
        "commission-max-rate": "0.2",
        "commission-max-change-rate": "0.01",
}
# Then, create your validator
ixod tx staking create-validator /path/to/validator.json --from ixo-test-node --gas-prices 0.025uixo --gas auto --gas-adjustment 1.5
# View details about your validator
ixod tendermint show-address
ixod tendermint show-node-id
```

### 3. Update Validator

```bash
ixod tx staking edit-validator \
--new-moniker "Your_Moniker" \
--identity "Keybase_ID" \
--details "Your_Description" \
--website "Your_Website" \
--security-contact "Your_Email" \
--chain-id ixo-5 \
--commission-rate 0.05 \
--from Wallet_Name \
--gas 350000 -y
```

## Additional Information

### Pruning Explanation

- **Pruning Configuration:** The pruning settings are added to manage the node's data storage efficiently. By setting `pruning` to `"custom"`, you can specify how much historical data to keep and how often to prune.
- **Placement:** Adding these commands after the existing configuration settings ensures that all node parameters are set up in one place, making the setup process more organized and easier to follow.

### Keep this in mind

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

# Using the `monitor-ixo.sh` Script

# Execute the script directly
./monitor-ixo.sh

# Run it with a timestamp for logging
date && ./monitor-ixo.sh

# Set up as a cron job for regular checks (every 5 minutes)
# First, edit your crontab:
crontab -e
# Then add this line:
*/5 * * * * cd /home/ixo && ./monitor-ixo.sh >> monitor_logs.txt
```

The output shows three critical metrics:

- **Catching up**: `true` means your node is still syncing, `false` means it's in sync
- **Latest block**: Compare this with explorer.ixo.earth to verify you're at the chain tip
- **Voting power**: Should match your staked amount; 0 might indicate you're jailed or not in active set

This script provides a quick health check - if you see "Catching up: true" for extended periods or your voting power drops unexpectedly, you should investigate immediately.

Enhance this with alerts (via Telegram/Discord bots) on missed blocks and expanding the script to check system resources (CPU/RAM/disk space).

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

Open the Prometheus configuration file, usually located at `/etc/prometheus/prometheus.yml`, and add a job to scrape metrics from your IXO node:

```yaml
scrape_configs:
  - job_name: "ixo_node"
    static_configs:
      - targets: ["localhost:26660"]
```

2. **Restart Prometheus:**

After editing the configuration, restart the Prometheus service to apply the changes:

```bash
sudo systemctl restart prometheus
```

#### 3. Install and Configure Node Exporter

1. **Install Node Exporter:**

Download and install Node Exporter to collect system metrics:

```bash
wget https://github.com/prometheus/node_exporter/releases/download/v1.3.1/node_exporter-1.3.1.linux-amd64.tar.gz
tar xvfz node_exporter-1.3.1.linux-amd64.tar.gz
sudo cp node_exporter-1.3.1.linux-amd64/node_exporter /usr/local/bin/
```

2. **Create a Systemd Service for Node Exporter:**

Create a service file for Node Exporter:

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

Start the Node Exporter service and enable it to start on boot:

```bash
sudo systemctl daemon-reload
sudo systemctl start node_exporter
sudo systemctl enable node_exporter
```

4. **Add Node Exporter to Prometheus:**

Add a new job to the Prometheus configuration to scrape metrics from Node Exporter:

```yaml
scrape_configs:
  - job_name: "node_exporter"
    static_configs:
      - targets: ["localhost:9100"]
```

5. **Restart Prometheus:**

Restart Prometheus again to apply the new configuration:

```bash
sudo systemctl restart prometheus
```

#### 4. Access Prometheus Dashboard

- **Open Prometheus Dashboard:**

  - Access the Prometheus web interface by navigating to `http://<your-server-ip>:9090` in your web browser. Here, you can query and visualize metrics collected from your IXO node and system.

By following these steps, you will have a basic monitoring setup using Prometheus and Node Exporter to track the performance and health of your IXO blockchain node.

#### 5. Install and Configure Grafana

Grafana provides powerful visualization capabilities for your monitoring data. Here's how to set it up:

##### 1. **Install Grafana:**

```bash
# Add Grafana APT repository
sudo apt-get install -y apt-transport-https software-properties-common
sudo wget -q -O /usr/share/keyrings/grafana.key https://apt.grafana.io/gpg.key
echo "deb [signed-by=/usr/share/keyrings/grafana.key] https://apt.grafana.io stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list

# Update and install
sudo apt-get update
sudo apt-get install -y grafana

# Start and enable Grafana
sudo systemctl daemon-reload
sudo systemctl start grafana-server
sudo systemctl enable grafana-server
```

##### 2. **Access Grafana UI:**

- Open your browser and navigate to `http://<your-server-ip>:3000`
- Log in with default credentials (admin/admin) and set a new password when prompted

##### 3. **Add Prometheus as a Data Source:**

- In Grafana, navigate to Configuration > Data Sources > Add data source
- Select "Prometheus"
- Set the URL to `http://localhost:9090`
- Click "Save & Test" to ensure the connection works

##### 4. **Import Validator Dashboard:**

Grafana uses JSON files to import pre-configured dashboards.

<details>
  <summary>Click to view a basic dashboard for IXO validators</summary>

```bash
# Create a dashboard JSON file
cat > ixo_validator_dashboard.json << 'EOF'
{
  "annotations": {
    "list": [
      {
        "builtIn": 1,
        "datasource": "-- Grafana --",
        "enable": true,
        "hide": true,
        "iconColor": "rgba(0, 211, 255, 1)",
        "name": "Annotations & Alerts",
        "type": "dashboard"
      }
    ]
  },
  "editable": true,
  "gnetId": null,
  "graphTooltip": 0,
  "id": 1,
  "links": [],
  "panels": [
    {
      "alert": {
        "alertRuleTags": {},
        "conditions": [
          {
            "evaluator": {
              "params": [
                0
              ],
              "type": "gt"
            },
            "operator": {
              "type": "and"
            },
            "query": {
              "params": [
                "A",
                "5m",
                "now"
              ]
            },
            "reducer": {
              "params": [],
              "type": "avg"
            },
            "type": "query"
          }
        ],
        "executionErrorState": "alerting",
        "for": "5m",
        "frequency": "1m",
        "handler": 1,
        "name": "Validator Status",
        "noDataState": "no_data",
        "notifications": []
      },
      "aliasColors": {},
      "bars": false,
      "dashLength": 10,
      "dashes": false,
      "datasource": "Prometheus",
      "fieldConfig": {
        "defaults": {
          "custom": {}
        },
        "overrides": []
      },
      "fill": 1,
      "fillGradient": 0,
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 0,
        "y": 0
      },
      "hiddenSeries": false,
      "id": 2,
      "legend": {
        "avg": false,
        "current": false,
        "max": false,
        "min": false,
        "show": true,
        "total": false,
        "values": false
      },
      "lines": true,
      "linewidth": 1,
      "nullPointMode": "null",
      "options": {
        "alertThreshold": true
      },
      "percentage": false,
      "pluginVersion": "7.3.7",
      "pointradius": 2,
      "points": false,
      "renderer": "flot",
      "seriesOverrides": [],
      "spaceLength": 10,
      "stack": false,
      "steppedLine": false,
      "targets": [
        {
          "expr": "tendermint_consensus_validator_power",
          "interval": "",
          "legendFormat": "Voting Power",
          "refId": "A"
        }
      ],
      "thresholds": [
        {
          "colorMode": "critical",
          "fill": true,
          "line": true,
          "op": "lt",
          "value": 1
        }
      ],
      "timeFrom": null,
      "timeRegions": [],
      "timeShift": null,
      "title": "Validator Status",
      "tooltip": {
        "shared": true,
        "sort": 0,
        "value_type": "individual"
      },
      "type": "graph",
      "xaxis": {
        "buckets": null,
        "mode": "time",
        "name": null,
        "show": true,
        "values": []
      },
      "yaxes": [
        {
          "format": "short",
          "label": null,
          "logBase": 1,
          "max": null,
          "min": null,
          "show": true
        },
        {
          "format": "short",
          "label": null,
          "logBase": 1,
          "max": null,
          "min": null,
          "show": true
        }
      ],
      "yaxis": {
        "align": false,
        "alignLevel": null
      }
    },
    {
      "aliasColors": {},
      "bars": false,
      "dashLength": 10,
      "dashes": false,
      "datasource": "Prometheus",
      "fieldConfig": {
        "defaults": {
          "custom": {}
        },
        "overrides": []
      },
      "fill": 1,
      "fillGradient": 0,
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 12,
        "y": 0
      },
      "hiddenSeries": false,
      "id": 6,
      "legend": {
        "avg": false,
        "current": false,
        "max": false,
        "min": false,
        "show": true,
        "total": false,
        "values": false
      },
      "lines": true,
      "linewidth": 1,
      "nullPointMode": "null",
      "options": {
        "alertThreshold": true
      },
      "percentage": false,
      "pluginVersion": "7.3.7",
      "pointradius": 2,
      "points": false,
      "renderer": "flot",
      "seriesOverrides": [],
      "spaceLength": 10,
      "stack": false,
      "steppedLine": false,
      "targets": [
        {
          "expr": "tendermint_consensus_latest_block_height",
          "interval": "",
          "legendFormat": "Block Height",
          "refId": "A"
        }
      ],
      "thresholds": [],
      "timeFrom": null,
      "timeRegions": [],
      "timeShift": null,
      "title": "Latest Block Height",
      "tooltip": {
        "shared": true,
        "sort": 0,
        "value_type": "individual"
      },
      "type": "graph",
      "xaxis": {
        "buckets": null,
        "mode": "time",
        "name": null,
        "show": true,
        "values": []
      },
      "yaxes": [
        {
          "format": "short",
          "label": null,
          "logBase": 1,
          "max": null,
          "min": null,
          "show": true
        },
        {
          "format": "short",
          "label": null,
          "logBase": 1,
          "max": null,
          "min": null,
          "show": true
        }
      ],
      "yaxis": {
        "align": false,
        "alignLevel": null
      }
    },
    {
      "alert": {
        "alertRuleTags": {},
        "conditions": [
          {
            "evaluator": {
              "params": [
                80
              ],
              "type": "gt"
            },
            "operator": {
              "type": "and"
            },
            "query": {
              "params": [
                "A",
                "5m",
                "now"
              ]
            },
            "reducer": {
              "params": [],
              "type": "avg"
            },
            "type": "query"
          }
        ],
        "executionErrorState": "alerting",
        "for": "5m",
        "frequency": "1m",
        "handler": 1,
        "name": "Disk Usage Alert",
        "noDataState": "no_data",
        "notifications": []
      },
      "aliasColors": {},
      "bars": false,
      "dashLength": 10,
      "dashes": false,
      "datasource": "Prometheus",
      "description": "",
      "fieldConfig": {
        "defaults": {
          "custom": {}
        },
        "overrides": []
      },
      "fill": 1,
      "fillGradient": 0,
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 0,
        "y": 8
      },
      "hiddenSeries": false,
      "id": 8,
      "legend": {
        "avg": false,
        "current": false,
        "max": false,
        "min": false,
        "show": true,
        "total": false,
        "values": false
      },
      "lines": true,
      "linewidth": 1,
      "nullPointMode": "null",
      "options": {
        "alertThreshold": true
      },
      "percentage": false,
      "pluginVersion": "7.3.7",
      "pointradius": 2,
      "points": false,
      "renderer": "flot",
      "seriesOverrides": [],
      "spaceLength": 10,
      "stack": false,
      "steppedLine": false,
      "targets": [
        {
          "expr": "100 - ((node_filesystem_avail_bytes{mountpoint="/"} * 100) / node_filesystem_size_bytes{mountpoint="/"})",
          "interval": "",
          "legendFormat": "Disk Usage %",
          "refId": "A"
        }
      ],
      "thresholds": [
        {
          "colorMode": "critical",
          "fill": true,
          "line": true,
          "op": "gt",
          "value": 80
        }
      ],
      "timeFrom": null,
      "timeRegions": [],
      "timeShift": null,
      "title": "Disk Usage",
      "tooltip": {
        "shared": true,
        "sort": 0,
        "value_type": "individual"
      },
      "type": "graph",
      "xaxis": {
        "buckets": null,
        "mode": "time",
        "name": null,
        "show": true,
        "values": []
      },
      "yaxes": [
        {
          "format": "percent",
          "label": null,
          "logBase": 1,
          "max": "100",
          "min": "0",
          "show": true
        },
        {
          "format": "short",
          "label": null,
          "logBase": 1,
          "max": null,
          "min": null,
          "show": true
        }
      ],
      "yaxis": {
        "align": false,
        "alignLevel": null
      }
    },
    {
      "alert": {
        "alertRuleTags": {},
        "conditions": [
          {
            "evaluator": {
              "params": [
                0
              ],
              "type": "lt"
            },
            "operator": {
              "type": "and"
            },
            "query": {
              "params": [
                "A",
                "5m",
                "now"
              ]
            },
            "reducer": {
              "params": [],
              "type": "avg"
            },
            "type": "query"
          }
        ],
        "executionErrorState": "alerting",
        "for": "5m",
        "frequency": "1m",
        "handler": 1,
        "name": "Peer Count Alert",
        "noDataState": "no_data",
        "notifications": []
      },
      "aliasColors": {},
      "bars": false,
      "dashLength": 10,
      "dashes": false,
      "datasource": "Prometheus",
      "fieldConfig": {
        "defaults": {
          "custom": {}
        },
        "overrides": []
      },
      "fill": 1,
      "fillGradient": 0,
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 12,
        "y": 8
      },
      "hiddenSeries": false,
      "id": 4,
      "legend": {
        "avg": false,
        "current": false,
        "max": false,
        "min": false,
        "show": true,
        "total": false,
        "values": false
      },
      "lines": true,
      "linewidth": 1,
      "nullPointMode": "null",
      "options": {
        "alertThreshold": true
      },
      "percentage": false,
      "pluginVersion": "7.3.7",
      "pointradius": 2,
      "points": false,
      "renderer": "flot",
      "seriesOverrides": [],
      "spaceLength": 10,
      "stack": false,
      "steppedLine": false,
      "targets": [
        {
          "expr": "tendermint_p2p_peers",
          "interval": "",
          "legendFormat": "Connected Peers",
          "refId": "A"
        }
      ],
      "thresholds": [
        {
          "colorMode": "critical",
          "fill": true,
          "line": true,
          "op": "lt",
          "value": 3
        }
      ],
      "timeFrom": null,
      "timeRegions": [],
      "timeShift": null,
      "title": "Peer Count",
      "tooltip": {
        "shared": true,
        "sort": 0,
        "value_type": "individual"
      },
      "type": "graph",
      "xaxis": {
        "buckets": null,
        "mode": "time",
        "name": null,
        "show": true,
        "values": []
      },
      "yaxes": [
        {
          "format": "short",
          "label": null,
          "logBase": 1,
          "max": null,
          "min": null,
          "show": true
        },
        {
          "format": "short",
          "label": null,
          "logBase": 1,
          "max": null,
          "min": null,
          "show": true
        }
      ],
      "yaxis": {
        "align": false,
        "alignLevel": null
      }
    },
    {
      "alert": {
        "alertRuleTags": {},
        "conditions": [
          {
            "evaluator": {
              "params": [
                90
              ],
              "type": "gt"
            },
            "operator": {
              "type": "and"
            },
            "query": {
              "params": [
                "A",
                "5m",
                "now"
              ]
            },
            "reducer": {
              "params": [],
              "type": "avg"
            },
            "type": "query"
          }
        ],
        "executionErrorState": "alerting",
        "for": "5m",
        "frequency": "1m",
        "handler": 1,
        "name": "Memory Usage Alert",
        "noDataState": "no_data",
        "notifications": []
      },
      "aliasColors": {},
      "bars": false,
      "dashLength": 10,
      "dashes": false,
      "datasource": "Prometheus",
      "fieldConfig": {
        "defaults": {
          "custom": {}
        },
        "overrides": []
      },
      "fill": 1,
      "fillGradient": 0,
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 0,
        "y": 16
      },
      "hiddenSeries": false,
      "id": 10,
      "legend": {
        "avg": false,
        "current": false,
        "max": false,
        "min": false,
        "show": true,
        "total": false,
        "values": false
      },
      "lines": true,
      "linewidth": 1,
      "nullPointMode": "null",
      "options": {
        "alertThreshold": true
      },
      "percentage": false,
      "pluginVersion": "7.3.7",
      "pointradius": 2,
      "points": false,
      "renderer": "flot",
      "seriesOverrides": [],
      "spaceLength": 10,
      "stack": false,
      "steppedLine": false,
      "targets": [
        {
          "expr": "100 * (1 - ((node_memory_MemAvailable_bytes or node_memory_MemFree_bytes + node_memory_Cached_bytes + node_memory_Buffers_bytes) / node_memory_MemTotal_bytes))",
          "interval": "",
          "legendFormat": "Memory Usage",
          "refId": "A"
        }
      ],
      "thresholds": [
        {
          "colorMode": "critical",
          "fill": true,
          "line": true,
          "op": "gt",
          "value": 90
        }
      ],
      "timeFrom": null,
      "timeRegions": [],
      "timeShift": null,
      "title": "Memory Usage",
      "tooltip": {
        "shared": true,
        "sort": 0,
        "value_type": "individual"
      },
      "type": "graph",
      "xaxis": {
        "buckets": null,
        "mode": "time",
        "name": null,
        "show": true,
        "values": []
      },
      "yaxes": [
        {
          "format": "percent",
          "label": null,
          "logBase": 1,
          "max": "100",
          "min": "0",
          "show": true
        },
        {
          "format": "short",
          "label": null,
          "logBase": 1,
          "max": null,
          "min": null,
          "show": true
        }
      ],
      "yaxis": {
        "align": false,
        "alignLevel": null
      }
    },
    {
      "alert": {
        "alertRuleTags": {},
        "conditions": [
          {
            "evaluator": {
              "params": [
                90
              ],
              "type": "gt"
            },
            "operator": {
              "type": "and"
            },
            "query": {
              "params": [
                "A",
                "5m",
                "now"
              ]
            },
            "reducer": {
              "params": [],
              "type": "avg"
            },
            "type": "query"
          }
        ],
        "executionErrorState": "alerting",
        "for": "5m",
        "frequency": "1m",
        "handler": 1,
        "name": "CPU Usage Alert",
        "noDataState": "no_data",
        "notifications": []
      },
      "aliasColors": {},
      "bars": false,
      "dashLength": 10,
      "dashes": false,
      "datasource": "Prometheus",
      "fieldConfig": {
        "defaults": {
          "custom": {}
        },
        "overrides": []
      },
      "fill": 1,
      "fillGradient": 0,
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 12,
        "y": 16
      },
      "hiddenSeries": false,
      "id": 12,
      "legend": {
        "avg": false,
        "current": false,
        "max": false,
        "min": false,
        "show": true,
        "total": false,
        "values": false
      },
      "lines": true,
      "linewidth": 1,
      "nullPointMode": "null",
      "options": {
        "alertThreshold": true
      },
      "percentage": false,
      "pluginVersion": "7.3.7",
      "pointradius": 2,
      "points": false,
      "renderer": "flot",
      "seriesOverrides": [],
      "spaceLength": 10,
      "stack": false,
      "steppedLine": false,
      "targets": [
        {
          "expr": "100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)",
          "interval": "",
          "legendFormat": "CPU Usage",
          "refId": "A"
        }
      ],
      "thresholds": [
        {
          "colorMode": "critical",
          "fill": true,
          "line": true,
          "op": "gt",
          "value": 90
        }
      ],
      "timeFrom": null,
      "timeRegions": [],
      "timeShift": null,
      "title": "CPU Usage",
      "tooltip": {
        "shared": true,
        "sort": 0,
        "value_type": "individual"
      },
      "type": "graph",
      "xaxis": {
        "buckets": null,
        "mode": "time",
        "name": null,
        "show": true,
        "values": []
      },
      "yaxes": [
        {
          "format": "percent",
          "label": null,
          "logBase": 1,
          "max": "100",
          "min": "0",
          "show": true
        },
        {
          "format": "short",
          "label": null,
          "logBase": 1,
          "max": null,
          "min": null,
          "show": true
        }
      ],
      "yaxis": {
        "align": false,
        "alignLevel": null
      }
    }
  ],
  "refresh": "10s",
  "schemaVersion": 26,
  "style": "dark",
  "tags": [],
  "templating": {
    "list": []
  },
  "time": {
    "from": "now-6h",
    "to": "now"
  },
  "timepicker": {},
  "timezone": "",
  "title": "IXO Validator Dashboard",
  "uid": "ixo_validator",
  "version": 1
}
EOF
```

</details>

##### 5. **Import the Dashboard:**

- In Grafana, navigate to Dashboards > Import
- Click "Upload JSON file" and select the `ixo_validator_dashboard.json` file you created
- Select "Prometheus" as the data source
- Click "Import"

#### 6. Configure Alerting

Grafana includes an alerting system that can send notifications when certain conditions are met:

##### 1. **Set Up Notification Channel:**

- Navigate to Alerting > Notification channels > New channel
- Choose your preferred notification method (e.g., Email, Telegram, Discord Webhook)
- Configure the channel with appropriate details
- Test the notification to ensure it works

##### 2. **Add Alert Rules for Critical Validator Metrics:**

The imported dashboard includes some predefined alerts. You can modify these or create new ones for:

- Missed blocks
- Validator jailing
- Disk space issues
- Peer connectivity problems
- Synchronization issues

##### 3. **Example Prometheus Alert Rules:**

For more advanced alerting, you can add custom rules to Prometheus:

<details>
  <summary>Click to expand an example Prometheus rules file</summary>

```bash
# Create Prometheus rules file
sudo tee /etc/prometheus/rules/ixo_validator.rules.yml > /dev/null << EOF
groups:
- name: ixo_validator
  rules:
  - alert: ValidatorDown
    expr: tendermint_consensus_validator_power < 1
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "Validator is down or not in active set"
      description: "Validator has no voting power for more than 5 minutes."

  - alert: MissedBlocks
    expr: (increase(tendermint_consensus_rounds_total[5m]) - increase(tendermint_consensus_num_txs[5m])) > 10
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Validator missing blocks"
      description: "Validator might be missing blocks or not proposing transactions."

  - alert: DiskSpaceCritical
    expr: 100 - ((node_filesystem_avail_bytes{mountpoint="/"} * 100) / node_filesystem_size_bytes{mountpoint="/"}) > 90
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "Disk space critical"
      description: "Validator running out of disk space (>90% used)."

  - alert: LowPeerCount
    expr: tendermint_p2p_peers < 3
    for: 10m
    labels:
      severity: warning
    annotations:
      summary: "Low peer count"
      description: "Validator has less than 3 peers for more than 10 minutes."
EOF
```

</details>

##### 4. **Update Prometheus Configuration:**

Add the rules file to your Prometheus configuration:

```bash
sudo tee -a /etc/prometheus/prometheus.yml > /dev/null << EOF
# Load rules once and periodically evaluate them
rule_files:
  - "rules/ixo_validator.rules.yml"
EOF

# Restart Prometheus to apply changes
sudo systemctl restart prometheus
```

#### 7. Key Metrics to Monitor

Focus on these critical metrics:

##### 1. **Validator Health:**

- **Voting Power**: Should match your stake - if it drops to 0, you're not in the active set
- **Block Height**: Should increase steadily - stagnation indicates sync issues
- **Peer Count**: Should be at least 3-5 peers - fewer peers may indicate network isolation

##### 2. **System Resources:**

- **Disk Usage**: Should stay below 80% - blockchain data grows over time
- **Memory Usage**: High usage may indicate memory leaks
- **CPU Usage**: Spikes during block proposal are normal, but sustained high usage is concerning

##### 3. **Network Performance:**

- **Block Production Rate**: For proposers, monitor successful block proposals
- **Missed Blocks**: Indicates connectivity or performance issues
- **Transaction Processing**: Monitor transaction throughput when your node is the proposer

#### 8. Interpreting Dashboard Data

- **Block Height Plateaus**: If your block height stops increasing while other validators continue, you're falling out of sync
- **Voting Power Drops**: Immediate investigation required - could indicate jailing events
- **Peer Count Fluctuations**: Normal to some degree, but persistent low counts require network troubleshooting
- **Resource Usage Patterns**: Learn your node's normal patterns to identify abnormal behavior

By combining these monitoring tools with proper alerting, you'll stay ahead of potential issues and maintain high validator performance on the IXO network.

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

## Decommissioning Node

If you need to shut down your validator node and destroy the server, follow these steps for a graceful exit:

### 1. Unjail Validator (if necessary)

```bash
ixod tx slashing unjail --from your-wallet-name --gas-prices 0.025uixo --gas auto --gas-adjustment 1.5
```

### 2. Remove Validator from Active Set

```bash
# Remove your validator from the active validator set
ixod tx staking unbond $(ixod keys show your-wallet-name --bech val -a) <amount_to_unbond>uixo --from your-wallet-name --gas-prices 0.025uixo --gas auto --gas-adjustment 1.5
```

### 3. Backup Important Files

Before shutting down, backup your validator keys:

```bash
# Create a backup directory on your local machine
mkdir -p ixo_validator_backup

# Copy important files (adjust paths if needed)
scp ixo@your-server-ip:~/.ixod/config/priv_validator_key.json ixo_validator_backup/
scp ixo@your-server-ip:~/.ixod/config/node_key.json ixo_validator_backup/
scp ixo@your-server-ip:~/.ixod/config/client.toml ixo_validator_backup/
scp -r ixo@your-server-ip:~/.ixod/keyring-* ixo_validator_backup/
```

### 4. Stop and Disable Services

```bash
sudo systemctl stop ixod
sudo systemctl disable ixod
```

### 5. Optional: Withdraw Funds

If your tokens have finished unbonding (typically 21 days) and you want to send them to another address:

```bash
ixod tx bank send $(ixod keys show your-wallet-name -a) <destination_address> <amount>uixo --from your-wallet-name --gas-prices 0.025uixo --gas auto --gas-adjustment 1.5
```

### Important Notes

- The unbonding period is typically 21 days, during which your tokens are locked
- Ensure you have backed up your mnemonic phrase/private keys before destroying the server
- Consider informing the IXO community in Discord or Telegram if you've been an active validator
- You can now safely terminate your server instance through your cloud provider's interface

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

## Support

Remember to join the [IXO Discord](https://discord.gg/ixo) for community support and updates.  
The [IXO Telegram group](https://t.me/ixonetwork) is also very responsive.
