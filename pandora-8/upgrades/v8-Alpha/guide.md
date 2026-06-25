# v8 (Alpha) Testnet Upgrade Guide

Ixo v8 (Alpha) Gov Prop: <https://explorer.ixo.earth/testnet-ixo/gov/109>

Height: 17955740

> **This is an emergency security release. Please upgrade promptly.**

> **Cosmovisor folder casing.** The on-chain upgrade name is **`Alpha`**. On
> current Cosmovisor (≥ v1.4) the upgrade folder is **lowercase `alpha`**; on older
> Cosmovisor (≤ v1.3, incl. v1.0.0) use the exact case **`Alpha`** instead. The
> steps below use lowercase `alpha` — for older Cosmovisor, or one setup that works
> on any version, see the
> [Cosmovisor Guide](../../../COSMOVISOR.md#upgrade-directory-casing).

## First Time Cosmovisor Setup

If you have never setup Cosmovisor before, follow the instructions [here](../../../COSMOVISOR.md#first-time-cosmovisor-setup).

If you have already setup Cosmovisor, skip to the next section.

We highly recommend validators use cosmovisor to run their nodes. This
will make low-downtime upgrades smoother, as validators don't have to
manually upgrade binaries during the upgrade, and instead can
pre-install new binaries, and cosmovisor will automatically update them
based on on-chain SoftwareUpgrade proposals.

## Upgrade Prerequisites

Ixo v8 (Alpha) is built with golang **v1.22.11** — the same version as v7 (Opus),
so if you already built and ran v7 you do **not** need to change your Go version.
If you are coming from an older release, install golang v1.22.11 first:

```sh
wget https://go.dev/dl/go1.22.11.linux-amd64.tar.gz
rm -rf /usr/local/go && tar -C /usr/local -xzf go1.22.11.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
go version   # should print go1.22.11
```

## Cosmovisor Upgrade

First ensure you have golang v1.22.11 installed.

Build the binary and place it under the **lowercase `alpha`** upgrade folder
(if you run an older Cosmovisor, see the casing note above):

```sh
mkdir -p ~/.ixod/cosmovisor/upgrades/alpha/bin
cd $HOME/ixo
git fetch --all --tags
git checkout v8.0.0
make build
cp build/ixod ~/.ixod/cosmovisor/upgrades/alpha/bin
```

Now, at the upgrade height, Cosmovisor will automatically switch to the Alpha (v8) binary.

### Auto-download (alternative)

If your cosmovisor is configured with `DAEMON_ALLOW_DOWNLOAD_BINARIES=true`, the
binaries in [`binaries.json`](./binaries.json) will be fetched automatically from
the v8.0.0 GitHub release — no manual build required.

> **Database backend:** the released binary uses the default `goleveldb`. If you
> run `pebbledb`, build from source with `COSMOS_BUILD_OPTIONS=pebbledb make build`
> instead (the auto-download binary is goleveldb only).

## Use Ixo Service for Cosmovisor

Follow the instructions [here](../v2/guide.md#use-ixo-service-for-cosmovisor).

## Manual Option

1. Wait for Ixo to reach the upgrade height 17955740

2. Look for a panic message (`UPGRADE "Alpha" NEEDED at height: 17955740`),
   followed by endless peer logs. Stop the daemon.

3. Ensure system has golang v1.22.11

4. Run the following commands:

```sh
cd $HOME/ixo
git fetch --all --tags
git checkout v8.0.0
make install
```

5. Start the ixo daemon again, watch the upgrade happen, and then continue to hit blocks

## Further Help

If you need more help, please reach out at our discord at <https://discord.com/invite/ixo>.
