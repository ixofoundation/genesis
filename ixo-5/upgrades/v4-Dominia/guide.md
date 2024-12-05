# v4-Dominia Upgrade Guide

Ixo Dominia Gov Prop: <https://explorer.ixo.earth/ixo/gov/455>

Countdown: <https://explorer.ixo.earth/ixo/block/9256500>

Height: 9181350

## First Time Cosmovisor Setup

If you have never setup Cosmovisor before, follow the instructions [here](../v2/guide.md#first-time-cosmovisor-setup).

If you have already setup Cosmovisor, skip to the next section.

We highly recommend validators use cosmovisor to run their nodes. This
will make low-downtime upgrades smoother, as validators don't have to
manually upgrade binaries during the upgrade, and instead can
pre-install new binaries, and cosmovisor will automatically update them
based on on-chain SoftwareUpgrade proposals.

## Upgrade Prerequisites

Ixo Dominia requires golang v1.22.4. Before attempting to build/install v4-Dominia
please upgrade the golang version to v1.22.4. There is a script to quickly upgrade golang
to the correct version [here](upgrade_go_v1.22.4.sh).

Note after the script you may need to log out and log back in for changes to take effect.

## Cosmovisor Upgrade

First ensure you have golang v1.22.4 installed.

Create the Dominia folder, make the build, and copy the daemon over to that folder

```sh
mkdir -p ~/.ixod/cosmovisor/upgrades/Dominia/bin
cd $HOME/ixo
git pull
git checkout v4.0.0
make build
cp build/ixod ~/.ixod/cosmovisor/upgrades/Dominia/bin
```

Now, at the upgrade height, Cosmovisor will upgrade to the Dominia binary

## Use Ixo Service for Cosmovisor

Follow the instructions [here](../v2/guide.md#use-ixo-service-for-cosmovisor).

## Manual Option

1. Wait for Ixo to reach the upgrade height 9256500

2. Look for a panic message, followed by endless peer logs. Stop the daemon

3. Upgrade golang to v1.22.4

4. Run the following commands:

```sh
cd $HOME/ixo
git pull
git checkout v4.0.0
make install
```

4. Start the ixo daemon again, watch the upgrade happen, and then continue to hit blocks

## Further Help

If you need more help, please reach out at our discord at <https://discord.com/invite/ixo>.
