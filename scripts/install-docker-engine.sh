#!/bin/bash
# Docker Desktop eltavolitasa es natív Docker Engine telepitese
# Futtasd: bash scripts/install-docker-engine.sh

set -e

echo "=== Docker Desktop eltavolitasa ==="
sudo apt-get remove -y docker-desktop 2>/dev/null || true
rm -f ~/.config/systemd/user/docker-desktop.service

echo "=== Natív Docker Engine telepitese ==="
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg lsb-release

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
    sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Felhasznalo hozzaadasa docker es plugdev csoporthoz
sudo usermod -aG docker,plugdev $USER

# librealsense udev szabalyok
sudo apt-get install -y librealsense2-utils
sudo udevadm control --reload-rules
sudo udevadm trigger

echo ""
echo "=== Kesz! ==="
echo "Jelentkezz ki es be ujra, majd: docker compose up --build"
