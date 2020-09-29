

## Impacthub-1 launch setup

In this guide, we'll be going through the necessary steps and prep required to participate in impacthub-1's launch.

Firstly, clear the current node data and genesis file.

```
su ixo
ixod unsafe-reset-all
cd $HOME/.ixod/config
rm genesis.json
```

Ensure the correct ixo version:

```
ixod version
1.3.0
```


Then, download the network's genesis file to your node's configuration folder.

```
cd $HOME/.ixod/config
wget https://raw.githubusercontent.com/ixofoundation/genesis/master/impacthub-1/final-genesis.json
mv final-genesis.json genesis.json
```

Make sure the following command outputs this hash: 7b722ddd50ecd8b9111fa0b3bb810d099d74a6b25e6d615ac91542ed7b1501ac
```
shasum -a 256 genesis.json
```

Access the node's config. 

```text
nano $HOME/.ixod/config/config.toml
```

Add peers that are to be participating in the network at launch, by editing the persistent_peers setting to be the following array of peers. The default value of this entry should be "".

```
persistent_peers="dde3d8aacfef1490ef4ae43698e3e2648bb8363c@80.64.208.42:26656,f0d4546fa5e0c2d84a4244def186b9da3c12ba1a@46.166.138.214:26656,c95af93f0386f8e19e65997262c9f874d1901dc5@18.163.242.188:26656,cbe8c6a5a77f861db8edb1426b734f2cf1fa4020@18.166.133.210:26656,36e4738c7efcf353d3048e5e6073406d045bae9d@80.64.208.43:26656"
```

In the same config, replace the laddr parameter in the [rpc] section to 0.0.0.0 from 127.0.0.1. Make sure it is the correct laddr parameter, as there are multiple under various sections. Make sure it's the rpc section.
```
[rpc]
laddr = "tcp://127.0.0.1:26657"
```
to 
```
[rpc]
laddr = "tcp://0.0.0.0:26657"
```



Enable the peer exchange reactor `pex`, which enables nodes to share each other's peers. This ensures your node discovers other peers on the network. The default value of this entry may be "false". This must be changed to look as follows:

```text
pex = true 
```

Switch to root and start the ixo blockchain daemon.

```text
systemctl start ixod.service
```

and tail the node's logs.

```text
journalctl -f -u ixod.service
```

Ensure the node has started successfully.

```text
starting ABCI with Tendermint                module=main
```

If all these steps were completed successfully, the node should start participating in consensus and syncing post genesis launch time at noon (12pm) UTC on 30th September. 


**Final steps**:

1. Backup the generated `priv_validator_key.json` stored in `$HOME/.ixod/config/`, which is the validator's block/consensus signing key.
2. Obtain the node's peer ID and IP for sharing with other node operators.

```text
# Obtain the node's peering ID
ixod tendermint show-node-id

# Obtain the node's public IP
curl https://ipinfo.io/ip
```
3. Add the 2 results from the above commands to create the node's peering identity: <ID>@<IP>:26656
