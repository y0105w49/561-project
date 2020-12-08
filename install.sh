#!/usr/bin/env bash
set -euo pipefail

echo "deb [trusted=yes] https://repo.iovisor.org/apt/bionic bionic-nightly main" | sudo tee /etc/apt/sources.list.d/iovisor.list
sudo apt-get update
sudo apt-get install -y bcc-tools python3-bcc "linux-headers-$(uname -r)"
sudo ip route add 0.0.0.0/0 dev lo
