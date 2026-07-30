#!/bin/bash
# ==============================================================================
# Script Swap Memory 4GB untuk VPS Ubuntu 24.04 (Odoo + Hermes Agent)
# ==============================================================================

set -e

echo "=== Memulai Penyiapan Swap Memory 4GB ==="

# 1. Cek apakah swap sudah aktif
CURRENT_SWAP=$(sudo swapon --show | wc -l)

if [ "$CURRENT_SWAP" -gt 1 ]; then
    echo "Swap memory sudah aktif:"
    sudo swapon --show
    free -h
    exit 0
fi

# 2. Buat swap file 4GB
echo "[1/4] Mengalokasikan 4GB Swap File..."
sudo fallocate -l 4G /swapfile || sudo dd if=/dev/zero of=/swapfile bs=1M count=4096 status=progress

# 3. Setting hak akses aman
echo "[2/4] Mengatur izin akses 600 pada /swapfile..."
sudo chmod 600 /swapfile

# 4. Format swap
echo "[3/4] Mengaktifkan format swap..."
sudo mkswap /swapfile
sudo swapon /swapfile

# 5. Buat permanen di fstab
echo "[4/4] Menambahkan entry fstab..."
if ! grep -q '/swapfile' /etc/fstab; then
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
fi

# Set swappiness ke 10 agar RAM fisik lebih diutamakan
sudo sysctl vm.swappiness=10
if ! grep -q 'vm.swappiness' /etc/sysctl.conf; then
    echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
fi

echo "=== SELESAI! Status Memory Terbaru ==="
free -h
