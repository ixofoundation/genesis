# ixo Network Validator: Pandora-3 Setup
This documentation details the requirements and steps required to operate a validator on ixo's Pandora-3 testnet.

## Infrastructure

The following server requirements are needed for Pandora-3:
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

    The pandora-3 directory includes:
    - The network's genesis file `genesis.json`, which includes pandora-3's network details, parameters and starting data.
    - `InstallPandora.sh`, which is to be run in the next step to install all the requirements and blockchain software to participate in the network.

4. Access the pandora-3 folder and run the installation script:
    ```
    cd pandora-3
    bash InstallPandora.sh
    ```

    This script goes through the following steps:
     - Installs Golang 1.16.4, make, gcc and curl. 
     - Updates and upgrades Ubuntu packages. 
     - Prompts user to create a new IXO non-sudo user to run the software with.
     -  Sets required environmental variables for Golang.
     - Clones the ixo-cosmos repo at the specific commit of pandora-3, <TODO>. 
     - Creates the directories required for the ixo node configurations and blockchain data.
     - Installs the IXO blockchain daemon
     - Configures the node to use pandora-3's genesis file. 
     - Creates and an enables a systemd service with which the IXO node daemon will be run.
     
     Follow the configuration steps as the node is installed.

5. Switch to the new IXO user
	```
	su ixo
	```

6. Access the node's configuration file and add Simply VC's Pandora-3 peers.
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
	2:37PM INF Block{
	  Header{
	    Version:        {11 0}
	    ChainID:        pandora-3
	    Height:         1
	    Time:           2021-06-28 12:26:24.49165307 +0000 UTC
	    LastBlockID:    :0:000000000000
	    LastCommit:     E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855
	    Data:           E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855
	    Validators:     348A4D5CFF4D9757FC0D2086E8B2FB372228CE84B1E71E1516689CF7341BCB8E
	    NextValidators: 348A4D5CFF4D9757FC0D2086E8B2FB372228CE84B1E71E1516689CF7341BCB8E
	    App:            E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855
	    Consensus:      048091BC7DDC283F77BFBF91D73C44DA58C3DF8A9CBC867405D8B7F3DAADA22F
	    Results:        E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855
	    Evidence:       E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855
	    Proposer:       19C8815FCF3D8AD751EF8A296FAECC60C0E7E691
	  }#A00892D42F17EFE60305B4F1F293F901EEB262B8F22C109A840C2B927F415456
	  Data{

	  }#E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855
	  EvidenceData{

	  }#E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855
	  Commit{
	    Height:     0
	    Round:      0
	    BlockID:    :0:000000000000
	    Signatures:

	  }#E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855
}#A00892D42F17EFE60305B4F1F293F901EEB262B8F22C109A840C2B927F415456 module=consensus
2:37PM INF minted coins from module account amount=123587uixo from=mint module=x/bank
2:37PM INF Executed block height=1 invalidTxs=0 module=state validTxs=0
2:37PM INF commit synced commit=436F6D6D697449447B5B323535203639203135352031333020323239203432203130362032352032353220323135203233302032352032343720313538203339203139322036362031343220313432203136352032303220322039322031343120313838203832203133392035203139382031392039203134395D3A317D
2:37PM INF Committed state appHash=FF459B82E52A6A19FCD7E619F79E27C0428E8EA5CA025C8DBC528B05C6130995 height=1 module=state txs=0
2:37PM INF Updating evidence pool last_block_height=1 last_block_time=2021-06-28T12:26:24Z module=evidence
2:37PM INF Indexed block height=1 module=txindex
	```
9. If the above steps were done successfully, the node should be syncing through the whole Pandora-3 blockchain.

10. Next steps:
    1. Backing up the generated priv_validator_key.json, which is to be the validator's block/consensus signing key.
    2. Obtaining the node's peer ID and IP for sharing with other node operators
    3. Running the create-validator command
