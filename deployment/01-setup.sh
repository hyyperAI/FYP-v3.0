#!/bin/bash

# =================================================================
# FYP Backend - Initial Server Setup Script
# =================================================================
# Run this script as root on a fresh Ubuntu 22.04 droplet
# =================================================================

set -e  # Exit on any error

echo "=========================================="
echo "FYP Backend - Server Setup"
echo "=========================================="
echo ""

# Update system
echo "[1/6] Updating system packages..."
apt update && apt upgrade -y

# Install Python and dependencies
echo "[2/6] Installing Python 3 and dependencies..."
apt install -y python3 python3-pip python3-venv git curl ufw

# Create application user
echo "[3/6] Creating application user..."
if id "fypapp" &>/dev/null; then
    echo "User 'fypapp' already exists"
else
    useradd -m -s /bin/bash fypapp
    echo "User 'fypapp' created"
fi

# Create application directory
echo "[4/6] Setting up application directory..."
mkdir -p /var/www/fyp-backend
chown -R fypapp:fypapp /var/www/fyp-backend

# Install Fail2Ban for security
echo "[5/6] Installing Fail2Ban for security..."
apt install -y fail2ban
systemctl enable fail2ban
systemctl start fail2ban

# Configure UFW firewall
echo "[6/6] Configuring firewall..."
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow http
ufw allow https
ufw allow 8000/tcp comment 'FYP API'
ufw --force enable

echo ""
echo "=========================================="
echo "Server setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Run: ./02-deploy.sh"
echo "2. Configure environment variables in /var/www/fyp-backend/.env"
echo "3. Start service: systemctl start fyp-backend"
echo ""
