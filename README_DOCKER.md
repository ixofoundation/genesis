# Build ixod binary

```bash
make build-ixod
```

# Build docker image

```bash
make build-image network=<network> # for example impacthub-3
```

# Run ixod in docker

1. Create a target folder where a volume will be mounted to

```bash
mkdir $(pwd)/.ixod
```

1. Start a container

   ```bash
    docker run -v $(pwd)/.ixod:/home/ixo/.ixod -p 26656:26656 -p 26657:26657 ixo:<network>-<release> start # ixo:pandora-4-v1.6.0
   ```

1. The `ixo` folder will have the correct genesis and config files

1. Update configuration according to the network related documentation

   ```
   nano .ixod/config/config.toml
   ```

1. Run container one more time
   ```bash
    docker run -v $(pwd)/.ixod:/home/ixo/.ixod -p 26656:26656 -p 26657:26657 -d ixo:<network>-<release> start # ixo:pandora-4-v1.6.0
   ```
