
This guide will go through the steps required to get a node up and running on IXO's pandora networks.


For this guide, the following server will be required:
Ubuntu 18.04 OS
2 CPUs
2 GB RAM
30GB+ SSD
Networking: Allow incoming connections on port 26656
Static IP address

`

## pandora-1 testnet


An installation script `InstallIXO.sh` bash script has been included which prepares the environment, prerequisites, installs the IXO blockchain software and guides you through the node setup.

These steps are to be run once logged in as **root** user.  


##Ensure you are logged in as root
```
sudo -i
```
apt-get install git
cd $HOME
git clone https://www.github.com/ixofoundation/genesis.git && git checkout master

cd genesis/pandora-1
bash InstallIXO.sh

```

Follow the configuration steps as the node is installed.


