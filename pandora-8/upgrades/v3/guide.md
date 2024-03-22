# v3 Testnet Upgrade Guide

Ixo v3 Gov Prop: <https://blockscan.testnet.ixo.earth/ixo/proposals/76>

Height: 5171650

## First Time Cosmovisor Setup

If you have never setup Cosmovisor before, follow the instructions [here](../v2/guide.md#first-time-cosmovisor-setup).

If you have already setup Cosmovisor, skip to the next section.

We highly recommend validators use cosmovisor to run their nodes. This
will make low-downtime upgrades smoother, as validators don't have to
manually upgrade binaries during the upgrade, and instead can
pre-install new binaries, and cosmovisor will automatically update them
based on on-chain SoftwareUpgrade proposals.

## Cosmovisor Upgrade

Create the v3 folder, make the build, and copy the daemon over to that folder

```sh
mkdir -p ~/.ixod/cosmovisor/upgrades/v3/bin
cd $HOME/ixo
git pull
git checkout v3.0.0
make build
cp build/ixod ~/.ixod/cosmovisor/upgrades/v3/bin
```

Now, at the upgrade height, Cosmovisor will upgrade to the v3 binary

## Use Ixo Service for Cosmovisor

Follow the instructions [here](../v2/guide.md#use-ixo-service-for-cosmovisor).

## Manual Option

1. Wait for Ixo to reach the upgrade height 5171650

2. Look for a panic message, followed by endless peer logs. Stop the daemon

3. Run the following commands:

```sh
cd $HOME/ixo
git pull
git checkout v3.0.0
make install
```

4. Start the ixo daemon again, watch the upgrade happen, and then continue to hit blocks

## Further Help

If you need more help, please reach out at our discord at <https://discord.com/invite/ixo>.
