# v7 (Opus) Mainnet Upgrade Guide

Ixo v7 (Opus) Gov Prop: <https://explorer.ixo.earth/ixo/gov/481>

Height: 17655000

> The on-chain software-upgrade name for this release is **`Opus`**. Cosmovisor
> therefore looks for the new binary under `~/.ixod/cosmovisor/upgrades/Opus/bin`
> (the upgrade name, not the `v7` tag).

## First Time Cosmovisor Setup

If you have never setup Cosmovisor before, follow the instructions [here](../v2/guide.md#first-time-cosmovisor-setup).

If you have already setup Cosmovisor, skip to the next section.

We highly recommend validators use cosmovisor to run their nodes. This
will make low-downtime upgrades smoother, as validators don't have to
manually upgrade binaries during the upgrade, and instead can
pre-install new binaries, and cosmovisor will automatically update them
based on on-chain SoftwareUpgrade proposals.

## Upgrade Prerequisites

Ixo v7 (Opus) requires golang **v1.22.11**. v6 was built with golang v1.22.4, so
please ensure you upgrade golang to v1.22.11 before building this release.

```sh
wget https://go.dev/dl/go1.22.11.linux-amd64.tar.gz
rm -rf /usr/local/go && tar -C /usr/local -xzf go1.22.11.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
go version   # should print go1.22.11
```

## Cosmovisor Upgrade

First ensure you have golang v1.22.11 installed.

Create the Opus folder, make the build, and copy the daemon over to that folder

```sh
mkdir -p ~/.ixod/cosmovisor/upgrades/Opus/bin
cd $HOME/ixo
git pull
git checkout v7.0.0
make build
cp build/ixod ~/.ixod/cosmovisor/upgrades/Opus/bin
```

Now, at the upgrade height, Cosmovisor will upgrade to the Opus (v7) binary.

## Use Ixo Service for Cosmovisor

Follow the instructions [here](../v2/guide.md#use-ixo-service-for-cosmovisor).

## Manual Option

1. Wait for Ixo to reach the upgrade height 17655000

2. Look for a panic message, followed by endless peer logs. Stop the daemon

3. Ensure system has golang v1.22.11

4. Run the following commands:

```sh
cd $HOME/ixo
git pull
git checkout v7.0.0
make install
```

5. Start the ixo daemon again, watch the upgrade happen, and then continue to hit blocks

## Further Help

If you need more help, please reach out at our discord at <https://discord.com/invite/ixo>.
