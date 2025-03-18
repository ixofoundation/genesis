# IXO Blockchain Node Synchronisation

In order to become a part of the validator set, your node data has to be synced to the rest of the validator set.  
This guide describes the available options, their pros & cons, and how they relate in terms of speed and security.

When setting up a new node on the IXO Impact Hub chain (or any Cosmos-based blockchain), there are three primary methods to catch up with the validators and synchronize your node with the network

## Full Sync (Default Method)

This is the most secure but slowest way to synchronize your node with the blockchain.  

**Note**
- Ensure that you install v0.20.0 of ixo-blockchain.
- Allow the Cosmosvisor binary updates to update when required.

### How It Works

• Your node downloads all historical blocks from genesis and verifies each transaction.
• This ensures full validation and security but takes considerable time, depending on network traffic and hardware.

### Steps

1. Install and configure the node software named `ixod` for Impact Hub.
2. Start the node with:

```bash
ixod start
```

3. The node will fetch all historical blocks and validate them.

### Pros

✅ Most secure—ensures the integrity of all historical transactions.  
✅ No reliance on third-party sources.

### Cons

❌ Very slow—could take several days to fully sync.  
❌ High resource usage—requires ample disk space and bandwidth.

## State Sync (Fastest Method)

This is the fastest way to catch up with the validators. Instead of replaying all historical blocks, it fetches the latest state snapshot and starts from there.  

**Note**
- Ensure that you install the latest version of ixo-blockchain; currently v4.0.0.
- Make sure that you absolutely trust the source.

### Instructions
Using the STAVR StateSync facilities.  

```bash
systemctl stop ixod
SNAP_RPC=https://ixo.rpc.m.stavr.tech:443
LATEST_HEIGHT=$(curl -s $SNAP_RPC/block | jq -r .result.block.header.height); \
BLOCK_HEIGHT=$((LATEST_HEIGHT - 1000)); \
TRUST_HASH=$(curl -s "$SNAP_RPC/block?height=$BLOCK_HEIGHT" | jq -r .result.block_id.hash)

echo $LATEST_HEIGHT $BLOCK_HEIGHT $TRUST_HASH

sed -i.bak -E "s|^(enable[[:space:]]+=[[:space:]]+).*$|\1true| ; \
s|^(rpc_servers[[:space:]]+=[[:space:]]+).*$|\1\"$SNAP_RPC,$SNAP_RPC\"| ; \
s|^(trust_height[[:space:]]+=[[:space:]]+).*$|\1$BLOCK_HEIGHT| ; \
s|^(trust_hash[[:space:]]+=[[:space:]]+).*$|\1\"$TRUST_HASH\"| ; \
s|^(seeds[[:space:]]+=[[:space:]]+).*$|\1\"\"|" $HOME/.ixod/config/config.toml
ixod tendermint unsafe-reset-all --home /home/ixo/.ixod
wget -O $HOME/.ixod/config/addrbook.json "https://server-1.stavr.tech/Mainnet/Ixo/addrbook.json"
curl -o - -L https://ixo.wasm.stavr.tech/wasm-ixod.tar.lz4 | lz4 -c -d - | tar -x -C $HOME/.ixod
sudo systemctl restart ixod && journalctl -fu ixod -o cat
```

### How It Works

• Instead of processing all blocks from genesis, the node fetches a recent application state snapshot.
• After downloading the state, the node starts verifying new transactions from that point.

### Steps

1. Enable state sync by finding an available state sync provider (like an RPC node that offers snapshots).
2. Modify the node’s config.toml with the provider’s details:

```plaintext
[statesync]
enable = true
rpc_servers = "https://rpc-provider1.com,https://rpc-provider2.com"
trust_height = <latest height>
trust_hash = "<block hash at trusted height>"
```

3. Restart the node:

```bash
ixod start
```

4. The node fetches the latest snapshot and syncs instantly.

### Pros

✅ Fastest method—minutes to a few hours instead of days.  
✅ Low resource usage—does not require storing full historical data.

### Cons

❌ Relies on trusted RPC providers—if compromised, security may be affected.  
❌ Not suitable for archive nodes (which need full historical data).

## Snapshot Sync (Midway Between Full Sync & State Sync)

This method downloads a pre-synchronized blockchain snapshot, allowing the node to resume from a recent height.  

**Note**
- Ensure that you install the latest version of ixo-blockchain; currently v4.0.0.


### How It Works

• The node downloads a snapshot file containing the blockchain state up to a certain block height.
• After extracting it, the node resumes normal syncing from that height onwards.

### Steps

1. Find a snapshot provider from the IXO community or snapshot services.
2. Download and extract the snapshot:

```bash
wget -O snapshot.tar.gz <snapshot-url>
tar -xzvf snapshot.tar.gz -C ~/.ixod
```

3. Start the node:

```bash
ixod start
```

### Pros

✅ Much faster than full sync but more secure than state sync.  
✅ Can be restarted from a recent height without relying on third-party RPCs.

### Cons

❌ Requires downloading large snapshot files (~GBs).  
❌ Still takes some time to sync beyond the snapshot height.

## Which Method Should You Choose?

| Method | Speed 🚀 | Security 🔒 | Best Use Case |  
| Full Sync | 🐌 Slow | ✅ Most Secure| If you want full transaction history. |  
| State Sync | ⚡ Fast | ⚠️ Requires Trust | If you want the fastest startup and are okay with using trusted providers. |  
| Snapshot Sync | 🏃 Medium | ✅ Secure | If you want a balance of speed and security. |

### Final Recommendation

- If you need speed - Use State Sync.
- If you need security - Use Full Sync.
- If you need a balance - Use Snapshot Sync.
