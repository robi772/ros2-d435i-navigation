#!/bin/bash
# Docker Desktop eltavolitasa es udev szabalyok beallitasa
# Ha a Docker Engine mar telepitve van, csak az udev reszt futtatja
# Futtasd: bash scripts/install-docker-engine.sh

set -e

echo "=== Docker Desktop eltavolitasa ==="
sudo apt-get remove -y docker-desktop 2>/dev/null || true
rm -f ~/.config/systemd/user/docker-desktop.service
rm -f ~/.docker/desktop/docker.sock 2>/dev/null || true

# Ellenorizzuk hogy fut-e mar a Docker Engine
if ! command -v docker &>/dev/null; then
    echo "=== Docker Engine telepitese ==="
    sudo apt-get update
    sudo apt-get install -y ca-certificates curl gnupg

    sudo install -m 0755 -d /etc/apt/keyrings

    # Csak akkor adjuk hozza a repo-t ha meg nem letezik
    if [ ! -f /etc/apt/keyrings/docker.asc ] && [ ! -f /etc/apt/keyrings/docker.gpg ]; then
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
            sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
        sudo chmod a+r /etc/apt/keyrings/docker.gpg
        echo \
          "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
          https://download.docker.com/linux/ubuntu \
          $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
          sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    fi

    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
else
    echo "Docker Engine mar telepitve van: $(docker --version)"
fi

echo "=== Csoportjogok beallitasa ==="
sudo usermod -aG docker $USER
sudo usermod -aG plugdev $USER 2>/dev/null || true

echo "=== librealsense udev szabalyok ==="
# Udev szabalyok letoltese kozvetlenul
if [ ! -f /etc/udev/rules.d/99-realsense-libusb.rules ]; then
    echo "Udev szabalyok letoltese..."
    sudo curl -fsSL \
        https://raw.githubusercontent.com/IntelRealSense/librealsense/master/config/99-realsense-libusb.rules \
        -o /etc/udev/rules.d/99-realsense-libusb.rules
    echo "Udev szabalyok letoltve."
else
    echo "Udev szabalyok mar megvannak."
fi

sudo udevadm control --reload-rules
sudo udevadm trigger

echo ""
echo "=== Kesz! ==="
echo "FONTOS: Jelentkezz ki es be ujra a csoportjogok miatt!"
echo "Majd: cd ~/ros2-d435i-navigation && docker compose up --build"
