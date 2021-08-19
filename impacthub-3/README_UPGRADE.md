# Upgrade Instructions: ImpactHub-2 -> ImpactHub-3

The following document describes the necessary steps involved that full-node operators
must take in order to upgrade from `impacthub-2` to `impacthub-3`. The IXO team
will post an official updated genesis file, but it is recommended that validators
execute the following instructions in order to verify the resulting genesis file.

The upgrade procedure should be started on `August 19, 2021 at or around 11:35 UTC` by halting on block `2289900`, with the new and exported genesis file of `impacthub-3` having a genesis time of `2021-08-19T12:00:00Z`.


  - [Updates](#updates)
  - [Risks](#risks)
  - [Recovery](#recovery)
  - [Halting impacthub-2](#recovery)
  - [Upgrade Procedure](#upgrade-procedure)

## Updates

Many changes have occurred to the ixod software since the launch of impacthub-2. These changes notably consist of an upgrade to
v0.42.6 of Cosmos SDK "Stargate", removal of some modules, new messages, bug fixes, and general application structural changes
that favor developer ergonomics and application development. There were also upgrades to the `bonds` module to enable reserve 
withdrawals, typically for funding purposes. Any existing bond in impacthub-2 will have reserve withdrawals disabled.

- Upgraded to Cosmos SDK v0.42.6 "Stargate" 
  - Introduced protobuf and grpc-gateway
  - Deprecated use of `ixocli` which is now part of `ixod`
- Deprecated `oracles` and `treasury` modules
- Added new demo scripts: `demo_gov_param_change.sh`, `ibc/demo.sh`
- Updated and fixed all demo scripts
- Updated general documentation
- (project) Introduced `MsgUpdateProjectDoc`
- (project) Fixed bug which does not allow us to go to PAIDOUT status if there are zero funds

__[ixo](https://github.com/ixofoundation/ixo-blockchain) application v1.6.0 is
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

Prior to exporting `impacthub-2` state, validators are encouraged to take a full data snapshot at the
export height before proceeding. Snapshotting depends heavily on infrastructure, but generally this
can be done by backing up the `.ixod` directory.

It is critically important to back-up the `.ixod/data/priv_validator_state.json` file after stopping your ixod process. This file is updated every block as your validator participates in a consensus rounds. It is a critical file needed to prevent double-signing, in case the upgrade fails and the previous chain needs to be restarted.

In the event that the upgrade does not succeed, validators and operators must downgrade back to
v1.4.3 of the _ixo-blockchain_ repo and restore to their latest snapshot before restarting their nodes.

## Halting impacthub-2

The current chain, impacthub-2, is proposed to be stopped at block `2289900`. It is important that validators set their nodes to stop processing transactions and participating in consensus at this height, by doing the following:

1. Access the `app.toml` configuration file in the `$HOME/.ixod` directory
2. Set `halt-height = 2289900`
3. Save your changes.
4. Restart the `ixod.service` using `systemctl restart ixod.service`.
5. Monitor your node at around the time of the halt, 11:35am UTC on Aug 19th, and ensure that it halts at the above block. This can be checked from the node's logs, RPC or Prometheus endpoint. 
6. Blocks will stop being produced once 33%+ of voting power stops participating in consensus.

## Upgrade Procedure

__Note__: It is assumed you are currently operating a full-node running v1.4.3 of _ixo-blockchain_.

- The version/commit hash of ixo v1.6.0: `21e2c962e18220888d529bf156406260a321cf80`
- The upgrade height as agreed upon: **`2289900`**


1. Verify you are currently running the correct version (v1.4.3) of the _ixo-blockchain_:

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

1. Verify you have `jq` and `python` installed. If not, use the following command:

   ```bash
   sudo apt-get install jq python
   ```
   
1. Export existing state from `impacthub-2`:

   **NOTE**: It is recommended for validators and operators to take a full data snapshot at the export
   height before proceeding in case the upgrade does not go as planned or if not enough voting power
   comes online in a sufficient and agreed upon amount of time. In such a case, the chain will fallback
   to continue operating `impacthub-2`. See [Recovery](#recovery) for details on how to proceed.

   Before exporting state via the following command, the `ixod` binary must be stopped!

   ```bash
   $ ixod export --for-zero-height --height=2289900 > exported.json
   ```

1. Verify the SHA256 of the (sorted) exported genesis file. This command outputs a hash of the file, to be compared  with the rest of the community.

   ```bash
   $ jq -S -c -M '' exported.json | shasum -a 256
   <hash output> -
   ```

1. At this point you now have a valid exported genesis state! All further steps now require
v1.6.0 of [ixo](https://github.com/ixofoundation/ixo-blockchain).

   **NOTE**: Go [1.15+](https://golang.org/dl/) is required!

   ```bash
   $ git clone https://github.com/ixofoundation/ixo-blockchain.git && cd ixo-blockchain && git checkout v1.6.0; make install
   ```

1. Backup/rename config files

   ```bash
   $ # Navigate to .ixod/config/ folder, by default ~/.ixod/config/
   $ mv app.toml app.toml.backup
   $ mv config.toml config.toml.backup
   ```

1. Verify you are currently running the correct version (v1.6.0) of _ixo_:

   ```bash
   $ ixod version --long
   name: ixo
   server_name: ixod
   version: 1.6.0
   commit: 21e2c962e18220888d529bf156406260a321cf80
   build_tags: ""
   go: go version go1.16.4 linux/amd64
   build_deps:
   - github.com/99designs/keyring@v1.1.6
   ...
   - gopkg.in/yaml.v3@v3.0.0-20200313102051-9f266ea9e77c
   cosmos_sdk_version: v0.42.6
   ```

1. Migrate exported state from the current v1.4.3 version to the new v1.6.0 version. This will require running an `ixod` command and the migration Python script.

   Run the following command on the previously generated _exported.json_:
   
      ```bash
   $ ixod migrate v0.40 exported.json
   ```
   
   Copy the json output into a new _exported_step_1.json_ file, excluding any command warnings that may show up in the process.
   
   ```bash
   $ nano exported_step_1.json
   ```

   Clone this repo to download the Python migration script.
   
   ```bash
   $ git clone https://github.com/ixofoundation/genesis
   $ cd genesis
   $ git checkout impacthub-3
   $ cd impacthub-3
   ```

   Move the _exported_step_1.json_ file to the repo's /scripts folder, as the script requires for it to be in its folder.

   ```bash
   $ python migrate_export_from_v1.4.3_to_v1.6.0
   ```

   **NOTE**: The `migrate_export_from_v1.4.3_to_v1.6.0` script takes an input genesis state and migrates it to a genesis file _genesis.json_ readable by ixo v1.6.0, and updating the genesis time and initial height.
   
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

1. Re-configure your node, since we deleted the configs in the above steps.


   ```bash
   $ # Navigate to .ixod/config/ folder, by default ~/.ixod/config/
   $ nano config.toml
   $ nano app.toml
   ```
 
   In app.toml:
   - ```minimum-gas-prices``` should be set to "0.025uixo"
   - (optional) enable API and set address to ```0.0.0.0```
   
   In config.toml:
   - ```moniker``` should be re-set
   - (optional) Set RPC laddr to ```0.0.0.0```
   - ```persistent_peers``` should be set to ```"cbe8c6a5a77f861db8edb1426b734f2cf1fa4020@18.166.133.210:26656,36e4738c7efcf353d3048e5e6073406d045bae9d@80.64.208.42:26656,f0d4546fa5e0c2d84a4244def186b9da3c12ba1a@46.166.138.214:26656,c95af93f0386f8e19e65997262c9f874d1901dc5@18.163.242.188:26656"```
   - ```pex``` should be set to ```true```

1. Move the new `genesis.json` to your `.ixod/config/` directory

1. Restart your node and wait for consensus to be reached with other validators.

## Python Migration Script Steps

This section lists all steps that the [Python migration script](./scripts/migrate_export_from_v1.4.3_to_v1.6.0.py) performs.

### Changes due to v1.4.3 to v1.5.0

- [**auth**] Removes `"treasury"` module account and replaces it with a `'transfer'` module account (**treasury** module was removed; **transfer** module was added)
- [**bank**] Adds `denom_metadata` for IXO and ATOM tokens, the latter copied from `cosmoshub-4` genesis
- [**capability**] Initialises the **capability** module state with IBC related capabilities, copied from `cosmoshub-4` genesis
- [**did**] Migrates DID docs because of a new structure of data
- [**ibc**] Initialises the **ibc** module state with empty lists and a list of `'allowed_clients'` having just the `'07-tendermint'` client allowed
- [**oracles**] Remove **oracles** state, since module no longer exists
- [**projects**] Migrates project account maps, claims, project docs, withdrawal infos, due to new structure of data
- [**staking**] Set `exported` to `true`
- [**treasury**] Remove **treasury** state, since module no longer exists
- [**transfer**] Initialise the **transfer** module state with IBC enabled and using port `'transfer'`
- [**vesting**] Add blank **vesting** module state
- [**general**] Replaces any `null`s (`None` in Python) with an empty list `[]`

### Changes due to v1.5.0 to v1.6.0

- [**bonds**] For each bond, sets reserve withdrawal address to fee address
- [**bonds**] For each bond, disables reserve withdrawals by default
- [**bonds**] For each bond, sets the available reserve to the current reserve

### General changes

- [**general**] Update chain ID to `impacthub-3`
- [**general**] Update genesis time
- [**general**] Update initial height to `1`
