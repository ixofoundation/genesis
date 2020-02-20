#!/bin/bash

GOFILENAME="go1.13.8.linux-amd64.tar.gz"
GODOWNLOADLINK="https://dl.google.com/go/$GOFILENAME"

echo "Ixo Chain Installer"
echo -e "-------------------------\n\n"
sleep 2

if [ "$USER" != "root" ]; then
        echo "You must be logged in as root to use this installer!"
        exit 0;
fi

echo "Starting IXO based install"
sleep 1
echo "Installing dependencies"
apt-get update -y
apt-get upgrade -y
apt-get install -y make gcc curl
rm -r /usr/local/go
rm -r ~/go 
cd ~

cd $HOME && curl -O $GODOWNLOADLINK
sleep 1
tar -xvf $HOME/$GOFILENAME

rm $HOME/$GOFILENAME
mv $HOME/go /usr/local

USERNAME=ixo
echo "Creating new IXO system user"
sleep 1

if getent passwd $USERNAME > /dev/null 2>&1; then
	echo "the user exists"
else
	adduser $USERNAME
fi
sleep 1

HOME="/home/$USERNAME"
GOROOT="/usr/local/go"
GOPATH="$HOME/go"
GOBIN="$GOPATH/bin"
GITNAME="ixofoundation"
GITREPO="ixo-cosmos"
GITRELEASE="master"
GITCOMMIT="7ee1d6f268ce0bee281c165eb5c4c9951dcd3229"

su $USERNAME <<EOSU

sleep 1
cd /home/$USERNAME
mkdir /home/$USERNAME/go

sleep 1

export GOROOT="$GOROOT"
export GOPATH="$GOPATH"
export PATH="$PATH:$GOROOT/bin:$GOPATH/bin"
export GO11MODULE=ON

echo "export GOROOT=\"$GOROOT\"" >> $HOME/.bashrc
echo "export GOPATH=\"$GOPATH\"" >> $HOME/.bashrc
echo "export PATH=\"\$PATH:\$GOROOT/bin:\$GOPATH/bin\"" >> $HOME/.bashrc
echo "export GO11MODULE=on" >> $HOME/.bashrc

sleep 1

cd $HOME
sleep 1
mkdir -p $GOPATH/src/github.com/$GITNAME
cd $GOPATH/src/github.com/$GITNAME
git clone https://github.com/$GITNAME/$GITREPO
sleep 1
cd $GITREPO && git fetch --all && git checkout $GITCOMMIT
sleep 1
make clean
make distclean
make go-mod-cache
make install

sleep 1

EOSU

DAEMONNAME="ixod"
CLINAME="ixocli"

DAEMON=$GOBIN/$DAEMONNAME
CLI=$GOBIN/$CLINAME

sleep 1

read -p "Initialising configuration of the node - Input the node's moniker: " MONIKERNAME

mkdir /home/ixo/.ixod
mkdir /home/ixo/.ixod/config

chown -R ixo:ixo /home/ixo/.$DAEMONNAME
chown -R ixo:ixo /home/ixo/.$DAEMONNAME/config/

su $USERNAME <<EOSU

$DAEMON init "$MONIKERNAME"

EOSU

sleep 5

cp /root/genesis/guides/genesis.json /home/ixo/.ixod/config/genesis.json

chown -R ixo:ixo /home/ixo/.$DAEMONNAME/config/genesis.json

CONFIG_FILE="/home/ixo/.$DAEMONNAME/config/config.toml"

sed -i 's/pex =.*/pex = true/' $CONFIG_FILE
sed -i 's/persistent_peers.*/persistent_peers = "ffb550c044dcf63726c24d18f54ddbb2d7b15609@46.166.138.209:26656,a9fb4f7437e47b15c8b9f22f4cc960535e21fa99@80.64.208.22:26656"/' $CONFIG_FILE

echo "---"
echo "Your peer ID:"
$DAEMON tendermint show-node-id
echo "---"

  cat << EOF > /etc/systemd/system/$DAEMONNAME.service
# /etc/systemd/system/$DAEMONNAME.service

[Unit]
Description=$DAEMONNAME Node
After=network.target
 
[Service]
Type=simple
User=$USERNAME
WorkingDirectory=$HOME
ExecStart=$DAEMON start
Restart=on-failure
RestartSec=3
LimitNOFILE=4096
 
[Install]
WantedBy=multi-user.target

EOF

systemctl daemon-reload

sleep 3

systemctl enable $DAEMONNAME.service
systemctl start $DAEMONNAME.service

echo "Service created at /etc/systemd/system/$DAEMONNAME.service."
echo "Run 'systemctl start $DAEMONNAME.service' to start the node"
