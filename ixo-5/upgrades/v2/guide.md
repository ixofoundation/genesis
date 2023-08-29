# v2 Testnet Upgrade Guide

Ixo v2 Gov Prop: <https://www.mintscan.io/ixo/proposals/439>

Countdown: <https://www.mintscan.io/ixo/blocks/2383000>

Height: 2383000

## First Time Cosmovisor Setup

If you have never setup Cosmovisor before, follow the following instructions.

If you have already setup Cosmovisor, skip to the next section.

We highly recommend validators use cosmovisor to run their nodes. This
will make low-downtime upgrades smoother, as validators don't have to
manually upgrade binaries during the upgrade, and instead can
pre-install new binaries, and cosmovisor will automatically update them
based on on-chain SoftwareUpgrade proposals.

You should review the docs for cosmovisor located here:
<https://docs.cosmos.network/main/tooling/cosmovisor>

If you choose to use cosmovisor, please continue with these
instructions:

To install Cosmovisor:

```sh
go install github.com/cosmos/cosmos-sdk/cosmovisor/cmd/cosmovisor@latest
```

After this, you must make the necessary folders for cosmosvisor in your
daemon home directory (\~/.ixod).

```sh
mkdir -p ~/.ixod
mkdir -p ~/.ixod/cosmovisor
mkdir -p ~/.ixod/cosmovisor/genesis
mkdir -p ~/.ixod/cosmovisor/genesis/bin
mkdir -p ~/.ixod/cosmovisor/upgrades
```

Copy the current v0.20 ixod binary into the
cosmovisor/genesis folder.

```sh
cp $GOPATH/bin/ixod ~/.ixod/cosmovisor/genesis/bin
```

Cosmovisor is now ready to be set up for v2.

Cosmovisor requires some ENVIRONMENT VARIABLES be set in order to
function properly. We recommend setting these in your `.profile` so it
is automatically set in every session.

For validators we recommmend setting

- `DAEMON_ALLOW_DOWNLOAD_BINARIES=false` for security reasons
- `DAEMON_LOG_BUFFER_SIZE=512` to avoid a bug with extra long log
  lines crashing the server.
- `DAEMON_RESTART_AFTER_UPGRADE=true` for unattended upgrades

Set these environment variables:

```sh
echo "# Setup Cosmovisor" >> ~/.profile
echo "export DAEMON_NAME=ixod" >> ~/.profile
echo "export DAEMON_HOME=$HOME/.ixod" >> ~/.profile
echo "export DAEMON_ALLOW_DOWNLOAD_BINARIES=false" >> ~/.profile
echo "export DAEMON_LOG_BUFFER_SIZE=512" >> ~/.profile
echo "export DAEMON_RESTART_AFTER_UPGRADE=true" >> ~/.profile
echo "export UNSAFE_SKIP_BACKUP=true" >> ~/.profile
source ~/.profile
```

You may leave out `UNSAFE_SKIP_BACKUP=true`, however the backup takes a decent amount of time. If you do skip it please ensure there are other sources incase something goes wrong.

## Cosmovisor Upgrade

Create the v2 folder, make the build, and copy the daemon over to that folder

```sh
mkdir -p ~/.ixod/cosmovisor/upgrades/v2/bin
cd $HOME/ixo
git pull
git checkout v2.0.0
make build
cp build/ixod ~/.ixod/cosmovisor/upgrades/v2/bin
```

Now, at the upgrade height, Cosmovisor will upgrade to the v2 binary

## Use Ixo Service for Cosmovisor

### Setup Ixo Service

Set up a service to allow cosmovisor to run in the background as well as restart automatically if it runs into any problems:

```sh
echo "[Unit]
Description=Cosmovisor daemon
After=network-online.target
[Service]
Environment="DAEMON_NAME=ixod"
Environment="DAEMON_HOME=${HOME}/.ixod"
Environment="DAEMON_RESTART_AFTER_UPGRADE=true"
Environment="DAEMON_ALLOW_DOWNLOAD_BINARIES=false"
Environment="DAEMON_LOG_BUFFER_SIZE=512"
Environment="UNSAFE_SKIP_BACKUP=true"
User=$USER
ExecStart=${HOME}/go/bin/cosmovisor run start
Restart=always
RestartSec=3
LimitNOFILE=infinity
LimitNPROC=infinity
[Install]
WantedBy=multi-user.target
" >cosmovisor.service
```

Move this new file to the systemd directory:

```sh
sudo mv cosmovisor.service /etc/systemd/system/cosmovisor.service
```

### Start Ixo Service

Reload and start the service:

```sh
sudo systemctl daemon-reload
sudo systemctl restart systemd-journald
sudo systemctl start cosmovisor
```

Check the status of the service:

```sh
sudo systemctl status cosmovisor
```

To see live logs of the service:

```sh
journalctl -u cosmovisor -f
```

## Manual Option

1. Wait for Ixo to reach the upgrade height 2383000

2. Look for a panic message, followed by endless peer logs. Stop the daemon

3. Run the following commands:

```sh
cd $HOME/ixo
git pull
git checkout v2.0.0
make install
```

4. Start the ixo daemon again, watch the upgrade happen, and then continue to hit blocks

## Further Help

If you need more help, please reach out at our discord at <https://discord.com/invite/ixo>.
