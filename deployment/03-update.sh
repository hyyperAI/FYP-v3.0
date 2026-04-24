#!/bin/bash

# =================================================================
# FYP Backend - Update Script
# =================================================================
# Pull latest changes from GitHub and restart service
# =================================================================

set -e

echo "=========================================="
echo "FYP Backend - Update"
echo "=========================================="
echo ""

SERVICE_NAME="fyp-backend"
APP_DIR="/var/www/fyp-backend/fyp-backend"

echo "[1/5] Stopping service..."
systemctl stop "$SERVICE_NAME"

echo "[2/5] Pulling latest code..."
cd "$APP_DIR"
sudo -u fypapp git pull origin main

echo "[3/5] Updating dependencies..."
sudo -u fypapp "$APP_DIR/venv/bin/pip" install -r requirements.txt

echo "[4/5] Restarting service..."
systemctl restart "$SERVICE_NAME"

echo "[5/5] Checking service status..."
sleep 2
if systemctl is-active --quiet "$SERVICE_NAME"; then
    echo ""
    echo "✅ Update completed successfully!"
    echo ""
    systemctl status "$SERVICE_NAME" --no-pager
else
    echo ""
    echo "❌ Service failed to start. Check logs:"
    echo "   journalctl -u $SERVICE_NAME -n 50"
    exit 1
fi

echo ""
echo "Update complete! 🌐"
