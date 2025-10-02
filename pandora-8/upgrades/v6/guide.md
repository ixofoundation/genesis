# v6 Testnet Upgrade Guide

Ixo v6 Gov Prop: <https://explorer.ixo.earth/testnet-ixo/gov/106>

Height: 13962900

## First Time Cosmovisor Setup

If you have never setup Cosmovisor before, follow the instructions [here](../v2/guide.md#first-time-cosmovisor-setup).

If you have already setup Cosmovisor, skip to the next section.

We highly recommend validators use cosmovisor to run their nodes. This
will make low-downtime upgrades smoother, as validators don't have to
manually upgrade binaries during the upgrade, and instead can
pre-install new binaries, and cosmovisor will automatically update them
based on on-chain SoftwareUpgrade proposals.

## Upgrade Prerequisites

Ixo v6 requires golang v1.22.4. If you are not coming from v5-Dominia-Plus which
requires golang v1.22.4 please ensure to install golang v1.22.4.

## Cosmovisor Upgrade

First ensure you have golang v1.22.4 installed.

Create the v6 folder, make the build, and copy the daemon over to that folder

```sh
mkdir -p ~/.ixod/cosmovisor/upgrades/v6/bin
cd $HOME/ixo
git pull
git checkout v6.0.0
make build
cp build/ixod ~/.ixod/cosmovisor/upgrades/v6/bin
```

Now, at the upgrade height, Cosmovisor will upgrade to the v6 binary

## Use Ixo Service for Cosmovisor

Follow the instructions [here](../v2/guide.md#use-ixo-service-for-cosmovisor).

## Manual Option

1. Wait for Ixo to reach the upgrade height 13962900

2. Look for a panic message, followed by endless peer logs. Stop the daemon

3. Ensure system has golang v1.22.4

4. Run the following commands:

```sh
cd $HOME/ixo
git pull
git checkout v6.0.0
make install
```

4. Start the ixo daemon again, watch the upgrade happen, and then continue to hit blocks

## Further Help

If you need more help, please reach out at our discord at <https://discord.com/invite/ixo>.
