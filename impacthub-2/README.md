# Impact Hub 1 Upgrade Instructions

The following document describes the necessary steps involved that full-node operators
must take in order to upgrade from `impacthub-1` to `impacthub-2`. The IXO team
will post an official updated genesis file, but it is recommended that validators
execute the following instructions in order to verify the resulting genesis file.

The upgrade procedure should be performed on `March 18, 2021 at or around 11:05 UTC` on block `2567800`.

  - [Updates](#updates)
  - [Risks](#risks)
  - [Recovery](#recovery)
  - [Upgrade Procedure](#upgrade-procedure)
  - [Notes for Service Providers](#notes-for-service-providers)

## Updates

Many changes have occurred to the ixod software since the launch of mainnet. These changes notably consist of many new features,
protocol changes, and application structural changes that favor developer ergonomics and application development.

- Upgraded blockchain to be on par with Cosmos v0.39 practices
- Errors and error reporting were updated
- A number of decorators were defined in line with Cosmos v0.39 practices
- (app) Added an `UpgradeKeeper` and `EvidenceKeeper`
- (app) Added functionality to be able to create a test ixo app
- (cmd) Added an add-genesis-account cobra command that adds a genesis account to the genesis file
- (x/did, x/ixo, x/project) Made changes to public key getters
- (x/project) Fixed project minimum funding check
- (x/project) Added blacklisted addresses to `CreateTestInput`
- (x/project) Added an event type for updating an agent
- (x/project) Added claim template ID when creating claims
- (x/bonds) Added bond controller DID, which runs `MsgUpdateBondState`
- (x/bonds) Added 'alpha bond' flag and 'allow sells' flag to augmented bonding curves
- (x/bonds) Introduced public alpha
- (x/bonds) Added new detailed bonds list query
- Fixed `demo_project_x_bonds.sh`
- Added scripts `run_with_all_data_dev.sh`, `run_with_genesis_file.sh`, `run_with_all_data_and_genesis_file.sh`

__[ixo](https://github.com/ixofoundation/ixo-blockchain) application v1.4.3 is
what full node operators will upgrade to and run in this next major upgrade__.

## Risks

As a validator performing the upgrade procedure on your consensus nodes carries a heightened risk of
double-signing and being slashed. The most important piece of this procedure is verifying your
software version and genesis file hash before starting your validator and signing.

The riskiest thing a validator can do is discover that they made a mistake and repeat the upgrade
procedure again during the network startup. If you discover a mistake in the process, the best thing
to do is wait for the network to start before correcting it. If the network is halted and you have
started with a different genesis file than the expected one, seek advice from a Tendermint developer
before resetting your validator.

## Recovery

Prior to exporting `impacthub-1` state, validators are encouraged to take a full data snapshot at the
export height before proceeding. Snapshotting depends heavily on infrastructure, but generally this
can be done by backing up the `.ixocli` and `.ixod` directories.

It is critically important to back-up the `.ixod/data/priv_validator_state.json` file after stopping your ixod process. This file is updated every block as your validator participates in a consensus rounds. It is a critical file needed to prevent double-signing, in case the upgrade fails and the previous chain needs to be restarted.

In the event that the upgrade does not succeed, validators and operators must downgrade back to
v1.3.0 of the _ixo-blockchain_ repo and restore to their latest snapshot before restarting their nodes.

## Upgrade Procedure

__Note__: It is assumed you are currently operating a full-node running v1.3.0 of _ixo-blockchain_.

- The version/commit hash of ixo v1.4.3: `6abb0176a77b74bae04e1ba0b4cf753ab841ab2a`
- The upgrade height as agreed upon: **2,567,800**


1. Verify you are currently running the correct version (v0.34.6+) of the _Cosmos SDK_:

   ```bash
   $ ixod version --long
   name: ixo
   server_name: ixod
   client_name: ixocli
   version: 1.3.0
   commit: 006dbc7f4009c2208b79160d5a030c1bd574c4c4
   build_tags: ""
   go: go version go1.14.1 linux/amd64
   ```

2. Export existing state from `impacthub-1`:

   **NOTE**: It is recommended for validators and operators to take a full data snapshot at the export
   height before proceeding in case the upgrade does not go as planned or if not enough voting power
   comes online in a sufficient and agreed upon amount of time. In such a case, the chain will fallback
   to continue operating `impacthub-1`. See [Recovery](#recovery) for details on how to proceed.

   Before exporting state via the following command, the `ixod` binary must be stopped!

   ```bash
   $ ixod export --for-zero-height --height=2567800 > impacthub_1_genesis_export.json
   ```

3. Verify the SHA256 of the (sorted) exported genesis file with the rest of the community:

   ```bash
   $ jq -S -c -M '' impacthub_1_genesis_export.json | shasum -a 256
   [PLACEHOLDER]  impacthub_1_genesis_export.json
   ```

4. At this point you now have a valid exported genesis state! All further steps now require
v1.4.3 of [ixo](https://github.com/ixofoundation/ixo-blockchain).

   **NOTE**: Go [1.14+](https://golang.org/dl/) is required!

   ```bash
   $ git clone https://github.com/ixofoundation/ixo-blockchain.git && cd ixo && git checkout v1.4.3; make install
   ```

5. Verify you are currently running the correct version (v1.4.3) of _ixo_:

   ```bash
   $ ixod version --long
   name: ixo
   server_name: ixod
   client_name: ixocli
   version: 1.4.3
   commit: 6abb0176a77b74bae04e1ba0b4cf753ab841ab2a
   build_tags: ""
   go: go version go1.14.1 linux/amd64

   ```

6. Migrate exported state from the current v1.3.0 version to the new v1.4.3 version. This will require running the migration Python script.

   Clone this repo to download the migration script.
   
   ```bash
   $ git clone https://github.com/ixofoundation/genesis
   $ cd genesis
   ```
   
   Move your previously generated _exported.json_ to the repo's /scripts folder, as the script requires for it to be in its folder.

   ```bash
   $ python migrate_export_to_v1.4.3
   ```

   **NOTE**: The `migrate_export_to_v1` script takes an input genesis state and migrates it to a genesis file _genesis.json_ readable by ixo v1.4.3.

7. Verify the SHA256 of the final genesis JSON:

   ```bash
   $ jq -S -c -M '' genesis.json | shasum -a 256
   [PLACEHOLDER]  genesis.json
   ```

8. Reset state:

   **NOTE**: Be sure you have a complete backed up state of your node before proceeding with this step.
   See [Recovery](#recovery) for details on how to proceed.

   ```bash
   $ ixod unsafe-reset-all
   ```

9. Move the new `genesis.json` to your `.ixod/config/` directory

10. Restart your node and wait for consensus to be reached with other validators.
