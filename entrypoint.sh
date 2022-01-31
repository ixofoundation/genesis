#!/usr/bin/env sh

if [ ! -f "/home/ixo/.ixod/config/config.toml" ]; then
  echo "File config.toml not found. Initializing ixo client"
  ixod init "ImpactHub node"

  echo "Copy genesis.json to the config folder"
  cp /ixo/genesis.json /home/ixo/.ixod/config/genesis.json
  chown -R ixo:ixo /home/ixo/.ixod/config/genesis.json

  echo "\n---------------------------"
  echo "Please update the generated config.toml file"
  exit 0
fi

echo "\n---"
echo "Your peer ID:"
ixod tendermint show-node-id
echo "---\n"

echo "---"
echo "Node's tendermint validator info"
ixod tendermint show-validator
echo "---\n"

exec ixod "$@"
