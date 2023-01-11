# Build ixod binary

```bash
make build-ixod
```

# Build docker image

```bash
make build-image network=<network> # for example ixo-4
```
# Pull the docker image
   You don't need to do this step if you have already built.
   If you would like to pull the image you can go to 
   
   ```
   docker pull gatewayfm/ixo:ixo-4-v0.19.2
   ```
   This image is hosted here https://hub.docker.com/r/gatewayfm/ixo/tags
   

# Run ixod in docker

1. Create a target folder where a volume will be mounted to

   ```bash
   mkdir $(pwd)/.ixod
   ```

1. Start a container

   ```bash
    docker run -v $(pwd)/.ixod:/home/ixo/.ixod -p 26656:26656 -p 26657:26657 ixo:<network>-<release> start
   ```

1. The `ixo` folder will have the correct genesis and config files  

1. Update configuration according to the network related documentation

   ```
   nano .ixod/config/config.toml
   ```

1. Run container one more time
   ```bash
    docker run -v $(pwd)/.ixod:/home/ixo/.ixod -p 26656:26656 -p 26657:26657 -d ixo:<network>-<release> start 
   ```
