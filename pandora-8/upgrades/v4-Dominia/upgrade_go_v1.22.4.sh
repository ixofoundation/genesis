#!/bin/bash

GO_VERSION="1.22.4"
GO_FILENAME="go$GO_VERSION.linux-amd64.tar.gz"
GO_DOWNLOAD_LINK="https://dl.google.com/go/$GO_FILENAME"

echo "Upgrading Go to version $GO_VERSION"
echo -e "-------------------------\n\n"
sleep 2

if [ "$EUID" -ne 0 ]; then
  echo "You must be logged in as root to perform this upgrade!"
  exit 1
fi

echo "Removing existing Go installation..."
rm -rf /usr/local/go

echo "Downloading Go $GO_VERSION..."
curl -OL $GO_DOWNLOAD_LINK

echo "Installing Go $GO_VERSION..."
tar -C /usr/local -xzf $GO_FILENAME

echo "Cleaning up..."
rm $GO_FILENAME

# Update PATH in /etc/profile if not already present
if ! grep -q "/usr/local/go/bin" /etc/profile; then
  echo "Updating PATH in /etc/profile..."
  echo "export PATH=\$PATH:/usr/local/go/bin" >>/etc/profile
  source /etc/profile
fi

echo "Go has been upgraded to version $GO_VERSION"
echo "You may need to log out and log back in for changes to take effect."
