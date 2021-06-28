# Pandora 2 Upgrade Instructions

The following document describes the necessary steps involved that full-node operators
must take in order to upgrade from `pandora-2` to `pandora-3`. The IXO team
will post an official updated genesis file, but it is recommended that validators
execute the following instructions in order to verify the resulting genesis file.

The upgrade procedure should be performed on `June 30, 2021 at or around <TODO> UTC` on block `<TODO>`, with `pandora-3` having a genesis time of `2021-06-30T<TODO>Z`.

  - [Updates](#updates)
  - [Risks](#risks)
  - [Recovery](#recovery)
  - [Upgrade Procedure](#upgrade-procedure)

## Updates

Many changes have occurred to the ixod software since the launch of pandora-2. These changes notably consist of many new features,
protocol changes, and application structural changes that favor developer ergonomics and application development.

<TODO>

__[ixo](https://github.com/ixofoundation/ixo-blockchain) application v1.5.0 is
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

Prior to exporting `pandora-2` state, validators are encouraged to take a full data snapshot at the
export height before proceeding. Snapshotting depends heavily on infrastructure, but generally this
can be done by backing up the `.ixocli` and `.ixod` directories.

It is critically important to back-up the `.ixod/data/priv_validator_state.json` file after stopping your ixod process. This file is updated every block as your validator participates in a consensus rounds. It is a critical file needed to prevent double-signing, in case the upgrade fails and the previous chain needs to be restarted.

In the event that the upgrade does not succeed, validators and operators must downgrade back to
v1.4.3 of the _ixo-blockchain_ repo and restore to their latest snapshot before restarting their nodes.

## Upgrade Procedure

__Note__: It is assumed you are currently operating a full-node running v1.4.3 of _ixo-blockchain_.

- The version/commit hash of ixo v1.5.0: `<TODO>`
- The upgrade height as agreed upon: **<TODO>**


1. Verify you are currently running the correct version (v1.4.3) of the _ixo-blockchain_:

   ```bash
   $ ixod version --long
   name: ixo
   server_name: ixod
   client_name: ixocli
   version: 1.4.3
   commit: <TODO>
   build_tags: ""
   go: go version go1.14.1 linux/amd64
   ```

2. Verify you have `jq` and `python` installed. If not, use the following command:

   ```bash
   sudo apt-get install jq python
   ```
   
4. Export existing state from `pandora-2`:

   **NOTE**: It is recommended for validators and operators to take a full data snapshot at the export
   height before proceeding in case the upgrade does not go as planned or if not enough voting power
   comes online in a sufficient and agreed upon amount of time. In such a case, the chain will fallback
   to continue operating `pandora-2`. See [Recovery](#recovery) for details on how to proceed.

   Before exporting state via the following command, the `ixod` binary must be stopped!

   ```bash
   $ ixod export --for-zero-height --height=<TODO> > exported.json
   ```

3. Verify the SHA256 of the (sorted) exported genesis file. This command outputs a hash of the file, to be compared  with the rest of the community.

   ```bash
   $ jq -S -c -M '' exported.json | shasum -a 256
   <hash output> -
   ```

4. At this point you now have a valid exported genesis state! All further steps now require
v1.5.0 of [ixo](https://github.com/ixofoundation/ixo-blockchain).

   **NOTE**: Go [1.16+](https://golang.org/dl/) is required!

   ```bash
   $ git clone https://github.com/ixofoundation/ixo-blockchain.git && cd ixo-blockchain && git checkout v1.5.0; make install
   ```

5. Verify you are currently running the correct version (v1.5.0) of _ixo_:

   ```bash
   $ ixod version --long
   name: ixo
   app_name: ixod
   version: 1.5.0
   commit: <TODO>
   build_tags: ""
   go: go version go1.16.1 linux/amd64

   ```

6. Migrate exported state from the current v1.4.3 version to the new v1.5.0 version. This will require running the migration Python script.

   Clone this repo to download the migration script.
   
   ```bash
   $ git clone https://github.com/ixofoundation/genesis
   $ cd genesis
   ```
   
   Move your previously generated _exported.json_ to the repo's /scripts folder, as the script requires for it to be in its folder.

   ```bash
   $ python migrate_export_to_v1.5.0
   ```

   **NOTE**: The `migrate_export_to_v1.5.0` script takes an input genesis state and migrates it to a genesis file _genesis.json_ readable by ixo v1.5.0, and updating the genesis time.

7. Verify the SHA256 of the final genesis JSON. This command outputs a hash of the file, to be compared with the rest of the community.

   ```bash
   $ jq -S -c -M '' genesis.json | shasum -a 256
   <hash output>  genesis.json
   ```

7. Backup and delete config files (TODO: add more info)

8. Re-configure your node (TODO: add more info)

9. Reset state:

   **NOTE**: Be sure you have a complete backed up state of your node before proceeding with this step.
   See [Recovery](#recovery) for details on how to proceed.

   ```bash
   $ ixod unsafe-reset-all
   ```

10. Move the new `genesis.json` to your `.ixod/config/` directory

11. Restart your node and wait for consensus to be reached with other validators.
