# ixo node configuration

The following document describes various processes that validator operators will require to go through whilst getting their systems up and running.

  - [Creating an ixo wallet](#creating-an-ixo-wallet)
  - [Receiving ixo tokens](#receiving-ixo-tokens)
  - [Checking account balance](#checking-account-balance)
  - [Check node sync status](#check-node-sync-status)
  - [Registering validator](#registering-validator)
  - [Staking ixo](#staking-ixo)
  - [Backing up your keys](#backing-up-your-keys)
  - [Monitoring](#monitoring)
  - [Troubleshooting](#troubleshooting)

A great resource for learning about Cosmos-based validator operations is the following guide: https://github.com/cosmos/cosmos/blob/master/VALIDATORS_FAQ.md

## Creating an ixo wallet

There are currently 2 ways to generate an ixo wallet. These are the following:
1. Keplr browser extension

   1. This is installed through the Chrome extension store, and can be used to create a new account. Currently, token transfers are the only compatible transactions that can be done with Keplr.

   2. Select between `ixo` on Keplr, which will display your ixo address.

2. `ixod` cli tool

   1. `ixod`, the software used to validate on the network, can be used to generate a wallet and participate in the network with transactions.

   2. Generating an account can be done with the following command. It will ask for a passphrase which will be used to lock your wallet, away from unauthorised use.

        ```
        ixod keys add mykeyname
        ```

   3. This will output a new address and 24 word backup seed phrase, which you must make sure to back up.

## Receiving ixo tokens

To receive tokens to your wallet, you must distribute your wallet address to a 3rd party. On Keplr, this can be found on the UI.

For testnet tokens, you may use this Telegram faucet bot to instantly receive tokens: https://t.me/joinchat/fz9ZZBScHbhiY2E0 

However, whilst using `ixod`, you must use the following command to display the address of you generated wallet. This will ask for your passphrase prior to outputting the account details.

```
ixod keys show mykeyname
```

## Checking account balance

Access https://blockscan-pandora.ixo.world/ and paste the address in the top menu bar, which will direct you to your address' page.

`ixod` can also be used to query your token balances as follows. Balances are in uixo which means that 1 ixo balance will be displayed as 1000000 uixo.
```
ixod query bank balances <address>
```

## Check node sync status

To check on the status of syncing:
```
ixod status 2>&1 | jq .SyncInfo
```
If this command fails with parse error: ..., then try just:
```
ixod status
```

If `ixod` status fails with:

```
Error: failed to parse log level (main:info,state:info,statesync:info,*:error): Unknown Level String: 'main:info,state:info,statesync:info,*:error', defaulting to NoLevel
```

then run:

```
sed -i.bak 's/^log_level/# log_level/' $HOME/.ixod/config/config.toml
```

If `ixod` status fails with:
```
ERROR: Status: Post http://localhost:26657: dial tcp [::1]:26657: connect: connection refused
```
then you should run `sudo journalctl -u ixod.service` and diagnose the failure.

### Status output
If the status command succeeds, this will give output like:
```
{
  "latest_block_hash": "6B87878277C9164006F2E7C544A27C2A4010D0107F436645BFE35BAEBE50CDF2",
  "latest_app_hash": "010EF4A62021F88D097591D6A31906CF9E5FA4359DC523B535E3C411DC6010B1",
  "latest_block_height": "233053",
  "latest_block_time": "2020-01-31T22:12:45.006715122Z",
  "catching_up": true
}
```
The main thing to watch is that the block height is increasing. Once you are caught up with the chain, `catching_up` will become false. At that point, you can start using your node to create a validator.

## Registering validator

If you are upgrading, view [README_UPGRADE.md](./README_UPGRADE.md).

Firstly, generate your validator node's ixo public key. This is derived from the `priv_validator_key.json` file stored in `/home/ixo/.ixod/config/`.

NOTE: The following command will give incorrect values if you don't run it under the same machine and user that is currently running your validator:

```
ixod tendermint show-validator
```

This will then be used for creating a validator. Run the following command to see the required and optional paramater to be used when creating your validator:
```
ixod tx staking create-validator -h
```
An example of creating a validator with 1 ixo self-delegation and 10% commission. You need the correct --pubkey= flag with the key in single quotes as described in the above section, or you will lose your staking tokens:

```
ixod tx staking create-validator \
--amount=1000000uixo \
--pubkey="add your validator's public key here (ixovalconspub...)" \
--moniker="add your validator's nickname here" \
--commission-rate="0.10" \
--commission-max-rate="0.20" \
--commission-max-change-rate="0.01" \
--min-self-delegation="1" \
--from=<key name here> \
--chain-id=pandora-5 \
--gas=auto \
--fees=3000uixo 
```

To check on the status of your validator:

```
ixod status 2>&1 | jq .ValidatorInfo
```

After you have completed this guide, your validator should be up and ready to receive delegations. To view the current validator list, check out the ixo explorer. https://blockscan-pandora.ixo.world/validators


## Staking ixo

Staking your tokens can be done using `ixod` and delegating your desired amount to uixo to the validator of choice.

```
ixod tx staking delegate <validator address (ixovaloper...)> 1000000uixo --chain-id=pandora-4 --gas=auto --fees=3000uixo --from=<your key name here>
```

## Backing up your keys

2 types of private keys must be backed up when operating a validator on the ixo network.

1. The validator operator account, which is the address that owns the validator, which is the one used to run the create-validator transaction. This is backed up in the following ways:

    1. Safekeeping the 24 words retrieved when originally generating the account.
    2. Using `ixod keys export <my key name>` to export a private key, which can then be re imported using `ixod keys import <my key name>`

2. The validator consensus key, which is a json file located at `/home/ixo/.ixod/config/priv_validator_key.json`. To restore this, import the file back into its location. Be careful whilst doing this, as the same key running on multiple nodes will result in your validator being permanently jailed and slashed due to double signing.


## Monitoring

Follow the following guide to set up a PANIC cosmos monitoring tool for your ixo validator. https://medium.com/simply-vc/panic-installing-an-emergency-notification-system-for-your-cosmos-validator-part-1-b5a53f32601e

Learn how to monitor using Grafana / Prometheus using this guide: https://medium.com/cypher-core/cosmos-how-to-set-up-your-own-network-monitoring-dashboard-fe49c63a8271



## Troubleshooting

1. `Command 'ixod' not found` 

   1. Switch to `ixo` user
   3. Access the user's home, `cd $HOME`
   4. Run the following to allow your Ubuntu to find `ixod` in the go directories:

      ```
      echo "export GOROOT=\"$GOROOT\"" >> $HOME/.bashrc
      echo "export GOPATH=\"$GOPATH\"" >> $HOME/.bashrc
      echo "export PATH=\"\$PATH:\$GOROOT/bin:\$GOPATH/bin\"" >> $HOME/.bashrc
      echo "export GO11MODULE=on" >> $HOME/.bashrc
      ```

   5. Run `source .bashrc`
   6. Try `ixod version` again
   7. If issues persist, run `InstallPandora.sh` again to confirm correct installation of Golang and ixo software.

