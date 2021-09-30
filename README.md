# genesis

Genesis files and configurations for ixo protocol networks:

- [pandora-4 (testnet)](./pandora-4/README.md)
- [impacthub-3 (mainnet)](./impacthub-3/README.md)

# Build ixod binary

```bash
make build-ixod
```

# Build docker image

```bash
make build-image network=<network> # for example impacthub-3
```

# Run ixod in docker

1. Start a container

   ```
    docker run -v $(pwd)/ixo:/home/ixo/.ixod -p 26656:26656 -p 26657:26657 ixo:<network>-<release> start # ixo:pandora-4-v1.6.0
   ```

1. The `ixo` folder will be create in the current directory

1. Update configuration according to the network related documentation

   ```
   nano ixo/config/config.toml
   ```

1. Run container one more time
