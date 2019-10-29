
## pandora-1 testnet



This guide will go through the steps required to get a node up and running on IXO's pandora-1 network.


An installation script `InstallIXO.sh` bash script has been included which is installs all that is required to start the IXO node.



These steps are to be run on an **Ubuntu 18.04** logged in as **root** user.
  


```

sudo -i

cd $HOME
git clone https://www.github.com/ixofoundation/genesis.git && git checkout master

cd genesis/pandora-1
bash InstallIXO.sh

```


Follow the configuration steps as the node is installed.
