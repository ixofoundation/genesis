# ixo Network Validator: Pandora-2 Setup
This documentation details the requirements and steps required to operate a validator on ixo's Pandora-2 testnet.

## Infrastructure

The following server requirements are needed for Pandora-2:
- Ubuntu 18.04 OS 
- 2 CPUs 
- 2 GB RAM 
- 50GB SSD 
- Networking: Allow incoming connections on port 26656 
- Static IP address

## Installation

An installation script `InstallPandora.sh` has been included which prepares the environment, prerequisites, installs the IXO blockchain software and guides you through the node setup.

1. These steps are to be run once logged in as **root** user. Use the following command to access the root user.
    ```
    sudo -i
    ```

2. Install git to clone this repository on the VM
    ```
    apt-get install git
    ```

3. Access the root user's home directory and clone the repository
    ```
    cd $HOME
    git clone https://github.com/ixofoundation/genesis.git && git checkout master
    ```

    The pandora-2 directory includes:
    - The network's genesis file `genesis.json`, which includes pandora-2's network details, parameters and starting data.
    - `InstallPandora.sh`, which is to be run in the next step to install all the requirements and blockchain software to participate in the network.

4. Access the pandora-2 folder and run the installation script:
    ```
    cd pandora-2
    bash InstallPandora.sh
    ```

    This script goes through the following steps:
     - Installs Golang 1.13.8, make, gcc and curl. 
     - Updates and upgrades Ubuntu packages. 
     - Prompts user to create a new IXO non-sudo user to run the software with.
     -  Sets required environmental variables for Golang.
     - Clones the ixo-cosmos repo at the specific commit of pandora-2, 6abb0176a77b74bae04e1ba0b4cf753ab841ab2a. 
     - Creates the directories required for the ixo node configurations and blockchain data.
     - Installs the IXO blockchain daemon and CLI tool
     - Configures the node to use pandora-2's genesis file. 
     - Creates and an enables a systemd service with which the IXO node daemon will be run.
     
     Follow the configuration steps as the node is installed.

5. Switch to the new IXO user
	```
	su ixo
	```

6. Access the node's configuration file and add Simply VC's Pandora-2 peers.
	```
	nano $HOME/.ixod/config.toml
	```

    - **Required**: Find the `persistent_peers` parameter and add the following
    peers to its value. The default value of this entry should be `""`. This must be changed as follows:
    
    ```
    persistent_peers ="3e6c0845dadd4cd3702d11185ff242639cf77ab9@46.166.138.209:26656,c0b2d9f8380313f0e2756dc187a96b7c65cae49b@80.64.208.22:26656"
    ```
    - **Required**: Enable the peer exchange reactor `pex`, which enables nodes to share each other's peers. This ensures your node discovers other peers on the network. The default value of this entry should be "false". This must be changed as follows:
    ```
    pex = true 
    ```
    - **Optional**: The node's moniker can be changed from `Pandora node` to
    anything of your liking. The default value of the `moniker` entry is `"Pandora node".` This can be changed as desired.

7. Start the IXO blockchain daemon.
    ```
    systemctl start ixod.service
    ```

8. Check the node's logs as the root use

	Switch to the root user. This can be done by exiting the current user's shell instance.
	```
	exit
	```

	Tail the node's logs using the following:
	```
	journalctl -f -u ixod.service
	```

	Ensure the node is receiving and processing blocks, which would look like this:
	```
	Executed block    module=state height=20 validTxs=0 invalidTxs=0
	Committed state   module=state height=20 txs=0 appHash=3A6BB8049C10D0FB3C9C58A85B8FD840BBD28BDDCB8566621FEDFAB240C2FB5C
	```
9. If the above steps were done successfully, the node should be syncing through the whole Pandora-2 blockchain. Should you have any issues.

10. Next steps:
    1. Backing up the generated priv_validator_key.json, which is to be the validator's block/consensus signing key.
    2. Obtaining the node's peer ID and IP for sharing with other node operators
    3. Running the create-validator command
