# Pandora-5 Upgrade Instructions

### Please Note

Earlier this year we decided to change the versioning scheme of of the blockchain due to better reflect the state of the project and alignment to the Cosmos-SDK. 
As a validator upgrading from Pandora-4 you your versions might indicate v1.6.0 while we are talking about v.0.16.0. Basically our Major version was moved to minor. The next new stable version would be v0.18.0.

---

The following document describes the necessary steps involved that full-node operators
must take in order to upgrade from `pandora-4` to `pandora-5`. The IXO team
will post an official updated genesis file, but it is recommended that validators
execute the following instructions in order to verify the resulting genesis file.

The upgrade procedure should be started on `July 14, 2022 at or around 10:00 UTC` by halting on block `5250000`, with the new and exported genesis file of `pandora-5` having a genesis time of `2022-07-14T10:00:00Z`.

  - [Updates](#updates)
  - [Risks](#risks)
  - [Recovery](#recovery)
  - [Upgrade Procedure](#upgrade-procedure)

## Updates

Little has changed with regards to our core IXO modules, we added the support for smart contracts via CosmWasm and upgrade the chain to Cosmos-SDK v0.45.

__[ixo](https://github.com/ixofoundation/ixo-blockchain) application v0.18.0 is
what full node operators will upgrade to and run in this next major upgrade__.

## Risks

As a validator performing the upgrade procedure on your consensus nodes carries a heightened risk of
double-signing and being slashed. The most important piece of this procedure is verifying your
software version and genesis file hash before starting your validator and signing.

The riskiest thing a validator can do is discover that they made a mistake and repeat the upgrade
procedure again during the network startup. If you discover a mistake in the process, the best thing
to do is wait for the network to start before correcting it. If the network is halted and you have
started with a different genesis file than the expected one, seek advice from an ixo developer
before resetting your validator.

## Recovery

Prior to exporting `pandora-4` state, validators are encouraged to take a full data snapshot at the
export height before proceeding. Snapshotting depends heavily on infrastructure, but generally this
can be done by backing up the `.ixod` directory.

It is critically important to back-up the `.ixod/data/priv_validator_state.json` file after stopping your ixod process. This file is updated every block as your validator participates in a consensus rounds. It is a critical file needed to prevent double-signing, in case the upgrade fails and the previous chain needs to be restarted.

In the event that the upgrade does not succeed, validators and operators must downgrade back to
v0.16.2 of the _ixo-blockchain_ repo and restore to their latest snapshot before restarting their nodes.

## Upgrade Procedure

__Note__: It is assumed you are currently operating a full-node running v0.16.x of _ixo-blockchain_.

- The version/commit hash of ixo v0.18.0: `21e2c962e18220888d529bf156406260a321cf80` NEED TO UPDATE
- The upgrade height as agreed upon: **`5250000`** NEED TO UPDATE


1. Verify you are currently running the correct version (v0.16.0) of the _ixo-blockchain_:
NEED TO UPDATE
   ```bash
   $ ixod version --long
   name: ixo
   server_name: ixod
   version: 1.5.0-39-gce96460
   commit: ce96460aec48758edba336fd7a66a908f0309972
   build_tags: ""
   go: go version go1.16.4 linux/amd64
   build_deps:
   - github.com/99designs/keyring@v1.1.6
   ...
   - gopkg.in/yaml.v3@v3.0.0-20200313102051-9f266ea9e77c
   cosmos_sdk_version: v0.42.6
   ```

1. Verify you have `jq` and `python` installed. If not, use the following command:

   ```bash
   sudo apt-get install jq python
   ```
   
1. Export existing state from `pandora-4`:

   **NOTE**: It is recommended for validators and operators to take a full data snapshot at the export
   height before proceeding in case the upgrade does not go as planned or if not enough voting power
   comes online in a sufficient and agreed upon amount of time. In such a case, the chain will fallback
   to continue operating `pandora-4`. See [Recovery](#recovery) for details on how to proceed.

   Before exporting state via the following command, the `ixod` binary must be stopped!

   ```bash
   $ ixod export --for-zero-height --height=5250000 > exported.json
   ```

1. Verify the SHA256 of the (sorted) exported genesis file. This command outputs a hash of the file, to be compared  with the rest of the community.

   ```bash
   $ jq -S -c -M '' exported.json | shasum -a 256
   <hash output> -
   ```

1. At this point you now have a valid exported genesis state! All further steps now require
v0.18.0 of [ixo](https://github.com/ixofoundation/ixo-blockchain).

   **NOTE**: Go [1.18+](https://golang.org/dl/) is required!

   ```bash
   $ git clone https://github.com/ixofoundation/ixo-blockchain.git && cd ixo-blockchain && git checkout v0.18.0; make install
   ```

1. Verify you are currently running the correct version (v0.18.0) of _ixo_:

   ```bash
   $ ixod version --long
   name: ixo
   server_name: ixod
   version: 0.18.0
   commit: 21e2c962e18220888d529bf156406260a321cf80
   build_tags: ""
   go: go version go1.16.4 linux/amd64
   build_deps:
   ...
   cosmos_sdk_version: v0.45.4
   ```

1. Migrate exported state from the current v0.16.0 version to the new v0.18.0 version. This will require running the migration Python script.
   
   Clone this repo to download the Python migration script.
   
   ```bash
   $ git clone https://github.com/ixofoundation/genesis
   $ cd genesis
   $ git checkout pandora-5
   $ cd pandora-5
   ```

   Move your previously generated _exported.json_ to the repo's /scripts folder, as the script requires for it to be in its folder.

   ```bash
   $ python migrate_export_from_v0.16.0_to_v0.18.0
   ```

   **NOTE**: The `migrate_export_from_v0.16.0_to_v0.18.0` script takes an input genesis state and migrates it to a genesis file _genesis.json_ readable by ixo v0.18.0, and updating the genesis time and initial height.
   
   **NOTE**: If you would like to understand what the Python migration script does, please refer to the [Python migration script steps](#python-migration-script-steps) section

1. Verify the SHA256 of the final genesis JSON. This command outputs a hash of the file, to be compared with the rest of the community.

   ```bash
   $ jq -S -c -M '' genesis.json | shasum -a 256
   <hash output>  genesis.json
   ```

1. Reset state:

   **NOTE**: Be sure you have a complete backed up state of your node before proceeding with this step.
   See [Recovery](#recovery) for details on how to proceed.

   ```bash
   $ ixod unsafe-reset-all
   ```

1. Move the new `genesis.json` to your `.ixod/config/` directory

1. Restart your node and wait for consensus to be reached with other validators.

## Python Migration Script Steps

This section lists all steps that the [Python migration script](./scripts/migrate_export_from_v0.16.0_to_v0.18.0.py) performs.

- [**bonds**] For each bond, sets reserve withdrawal address to fee address
- [**bonds**] For each bond, disables reserve withdrawals by default
- [**bonds**] For each bond, sets the available reserve to the current reserve
- [**general**] Update chain ID to `pandora-5`
- [**general**] Update genesis time
- [**general**] Update initial height to `1`
