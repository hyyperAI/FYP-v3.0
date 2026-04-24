#!/bin/bash

# =================================================================
# FYP Backend - Deployment Script
# =================================================================
# Clones repository, installs dependencies, and configures service
# =================================================================

set -e

echo "=========================================="
echo "FYP Backend - Deployment"
echo "=========================================="
echo ""

# Variables
APP_DIR="/var/www/fyp-backend"
REPO_URL="https://github.com/hyyperAI/FYP-v3.0.git"
SERVICE_NAME="fyp-backend"

# Switch to fypapp user for deployment
echo "[1/7] Preparing deployment directory..."
cd "$APP_DIR"

# Clone or update repository
echo "[2/7] Cloning repository..."
if [ -d ".git" ]; then
    echo "Repository already exists, pulling latest..."
    sudo -u fypapp git pull origin main
else
    sudo -u fypapp git clone "$REPO_URL" "$APP_DIR"
fi

# Create virtual environment
echo "[3/7] Creating Python virtual environment..."
cd "$APP_DIR/fyp-backend"
if [ -d "venv" ]; then
    echo "Virtual environment exists, skipping..."
else
    sudo -u fypapp python3 -m venv venv
fi

# Install dependencies
echo "[4/7] Installing Python dependencies..."
sudo -u fypapp "$APP_DIR/fyp-backend/venv/bin/pip" install --upgrade pip
sudo -u fypapp "$APP_DIR/fyp-backend/venv/bin/pip" install -r "$APP_DIR/fyp-backend/requirements.txt"

# Create .env file if it doesn't exist
echo "[5/7] Configuring environment variables..."
if [ ! -f "$APP_DIR/fyp-backend/.env" ]; then
    echo "SUPABASE_URL=https://vzylxrdujxgzlgogjvru.supabase.co" | sudo -u fypapp tee "$APP_DIR/fyp-backend/.env" > /dev/null
    echo "SUPABASE_KEY=your_supabase_key_here" | sudo -u fypapp tee -a "$APP_DIR/fyp-backend/.env" > /dev/null
    echo "⚠️  Please edit /var/www/fyp-backend/.env and add your actual SUPABASE_KEY"
else
    echo ".env file already exists"
fi

# Copy systemd service file
echo "[6/7] Installing systemd service..."
cp "$APP_DIR/fyp-backend/deployment/fyp-backend.service" /etc/systemd/system/
chmod 644 /etc/systemd/system/fyp-backend.service

# Reload systemd and start service
echo "[7/7] Starting FYP Backend service..."
systemctl daemon-reload
systemctl enable "$SERVICE_NAME"
systemctl restart "$SERVICE_NAME"

# Check service status
sleep 2
if systemctl is-active --quiet "$SERVICE_NAME"; then
    echo ""
    echo "✅ FYP Backend deployed successfully!"
    echo ""
    echo "Service status:"
    systemctl status "$SERVICE_NAME" --no-pager
else
    echo ""
    echo "❌ Failed to start service. Check logs with:"
    echo "   journalctl -u $SERVICE_NAME -n 50"
    exit 1
fi

echo ""
echo "=========================================="
echo "Deployment complete!"
echo "=========================================="
echo ""
echo "Important: Edit /var/www/fyp-backend/.env and add your actual SUPABASE_KEY"
echo ""
echo "API endpoints:"
echo "  Health: http://YOUR_IP:8000/health"
echo "  Docs:   http://YOUR_IP:8000/docs"
echo "  Root:   http://YOUR_IP:8000/"
echo ""
