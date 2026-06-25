# Cosmovisor Setup & Upgrade Guide (ixo)

The canonical guide for running an ixo node (`ixod`) with
[Cosmovisor](https://docs.cosmos.network/main/tooling/cosmovisor), and the
reference for the **upgrade-directory casing** behaviour that differs between
Cosmovisor versions. Every per-upgrade guide links back here.

Cosmovisor lets validators pre-install the next binary so the node switches
automatically at the on-chain upgrade height — minimal downtime, no manual swap.

---

## First-Time Cosmovisor Setup

If you already run Cosmovisor, skip to [Upgrade Directory Casing](#upgrade-directory-casing).

We highly recommend validators use Cosmovisor — at the upgrade height it swaps to
the pre-installed binary automatically. Docs: <https://docs.cosmos.network/main/tooling/cosmovisor>

### 1. Install

```sh
go install github.com/cosmos/cosmos-sdk/cosmovisor/cmd/cosmovisor@latest
```

> **Note your version** — run `cosmovisor version`. It determines the upgrade
> directory casing (see below).

### 2. Folder layout

```sh
mkdir -p ~/.ixod/cosmovisor/genesis/bin
mkdir -p ~/.ixod/cosmovisor/upgrades
cp $GOPATH/bin/ixod ~/.ixod/cosmovisor/genesis/bin   # your current binary
```

### 3. Environment variables

Set these in your `~/.profile` so they apply to every session:

```sh
echo "# Cosmovisor" >> ~/.profile
echo "export DAEMON_NAME=ixod" >> ~/.profile
echo "export DAEMON_HOME=$HOME/.ixod" >> ~/.profile
echo "export DAEMON_ALLOW_DOWNLOAD_BINARIES=false" >> ~/.profile   # off for security
echo "export DAEMON_LOG_BUFFER_SIZE=512" >> ~/.profile             # avoids a long-log crash
echo "export DAEMON_RESTART_AFTER_UPGRADE=true" >> ~/.profile      # unattended upgrades
echo "export UNSAFE_SKIP_BACKUP=true" >> ~/.profile                # optional — faster, no data backup
source ~/.profile
```

### 4. Run as a systemd service

```sh
echo "[Unit]
Description=Cosmovisor daemon
After=network-online.target
[Service]
Environment=\"DAEMON_NAME=ixod\"
Environment=\"DAEMON_HOME=${HOME}/.ixod\"
Environment=\"DAEMON_RESTART_AFTER_UPGRADE=true\"
Environment=\"DAEMON_ALLOW_DOWNLOAD_BINARIES=false\"
Environment=\"DAEMON_LOG_BUFFER_SIZE=512\"
Environment=\"UNSAFE_SKIP_BACKUP=true\"
User=$USER
ExecStart=${HOME}/go/bin/cosmovisor run start
Restart=always
RestartSec=3
LimitNOFILE=infinity
LimitNPROC=infinity
[Install]
WantedBy=multi-user.target
" > cosmovisor.service
sudo mv cosmovisor.service /etc/systemd/system/cosmovisor.service
sudo systemctl daemon-reload
sudo systemctl start cosmovisor
sudo systemctl status cosmovisor
journalctl -u cosmovisor -f
```

---

## Upgrade Directory Casing

**Read this before every upgrade — it's the most common reason Cosmovisor fails to switch binaries.**

On-chain upgrade names are **case-sensitive** and are often capitalised (e.g.
`Opus`, `Alpha`, `Dominia`). Cosmovisor reads that name from
`~/.ixod/data/upgrade-info.json` and looks for the new binary under
`~/.ixod/cosmovisor/upgrades/<name>/bin`.

**The catch:** Cosmovisor changed how it derives `<name>` from the on-chain name:

| Cosmovisor version | Behaviour | Folder for on-chain name `Alpha` |
|--------------------|-----------|----------------------------------|
| **≤ v1.3.x** (incl. **v1.0.0**) | uses the name **verbatim** | **`Alpha`** (exact case) |
| **≥ v1.4.0** (incl. v1.5.0, v1.7.x — current) | **lowercases** the name | **`alpha`** |

Why: v1.4.0 added `upgradePlan.Name = strings.ToLower(...)` in cosmovisor's
`scanner.go` — *"normalize name to prevent operator error in upgrade name case
sensitivity errors"* — and it's on by default. So newer Cosmovisor wants the
lowercase folder even though the on-chain name is capitalised.

Check your version with `cosmovisor version`.

### ✅ Recommended: a setup that works on any version

Create the binary under the **lowercase** name and add an **exact-case symlink**.
Cosmovisor then finds it whichever rule your version applies:

```sh
# example for an upgrade named "Alpha"
mkdir -p ~/.ixod/cosmovisor/upgrades/alpha/bin
cp build/ixod ~/.ixod/cosmovisor/upgrades/alpha/bin
cd ~/.ixod/cosmovisor/upgrades && ln -s alpha Alpha
```

(For an upgrade named `Opus`, use `opus` + `ln -s opus Opus`, and so on.)

### Alternative: force exact-case on newer Cosmovisor

Set `COSMOVISOR_DISABLE_RECASE=true` (as an env var, or in the service file) to
turn off the lowercasing on v1.4.0+, so it uses the exact on-chain case like the
older versions.

### How the per-upgrade guides phrase it

Each upgrade guide uses the **lowercase** folder name, which is correct for
**current Cosmovisor (≥ v1.4)**. If you run **Cosmovisor ≤ v1.3 (incl. v1.0.0)**,
use the **exact on-chain case** instead (e.g. `Alpha`, not `alpha`) — or just add
the symlink above and you don't have to think about it.

> Note: upgrades whose on-chain name is already lowercase (e.g. `v2`, `v3`, `v6`)
> have no casing difference — the folder is the same on every Cosmovisor version.

---

## Auto-download (alternative to building manually)

If `DAEMON_ALLOW_DOWNLOAD_BINARIES=true`, Cosmovisor can fetch the binary
automatically from the `binaries.json` published in each upgrade folder. Many
validators keep this **off** for security and pre-install the binary manually.

## Further Help

ixo Discord: <https://discord.com/invite/ixo>
