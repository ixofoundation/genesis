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
GITREPO="ixo-blockchain"
GITRELEASE="v1.4.3"


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
cd $GITREPO && git fetch --all && git checkout $GITRELEASE
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

mkdir /home/ixo/.ixod
mkdir /home/ixo/.ixod/config

cp /root/genesis/pandora-2/genesis.json /home/ixo/.ixod/config/genesis.json

chown -R ixo:ixo /home/ixo/.$DAEMONNAME
chown -R ixo:ixo /home/ixo/.$DAEMONNAME/config/
chown -R ixo:ixo /home/ixo/.$DAEMONNAME/config/genesis.json


su $USERNAME <<EOSU

$DAEMON init "Pandora node"

EOSU

sleep 5

cp /root/genesis/pandora-2/genesis.json /home/ixo/.ixod/config/genesis.json

chown -R ixo:ixo /home/ixo/.$DAEMONNAME/config/genesis.json


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

echo "Service created at /etc/systemd/system/$DAEMONNAME.service."
echo "Run 'systemctl start $DAEMONNAME.service' to start the node"
