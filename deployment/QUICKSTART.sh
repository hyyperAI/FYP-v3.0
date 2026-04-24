#!/bin/bash

# =================================================================
# FYP Backend - Complete Deployment Quickstart
# =================================================================
# Run this script as root to deploy the entire stack
# =================================================================

set -e

echo "=========================================="
echo "FYP Backend - Complete Deployment"
echo "=========================================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root: sudo ./QUICKSTART.sh"
    exit 1
fi

# Get server IP
SERVER_IP=$(curl -s ifconfig.me)

echo "Server IP: $SERVER_IP"
echo "This script will:"
echo "  1. Setup server (update, firewall, user)"
echo "  2. Deploy FYP Backend application"
echo "  3. Configure and start service"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

# Run setup
echo ""
echo "Running server setup..."
bash ./01-setup.sh

# Run deployment
echo ""
echo "Deploying application..."
bash ./02-deploy.sh

echo ""
echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo ""
echo "API Endpoints:"
echo "  Health: http://$SERVER_IP:8000/health"
echo "  Docs:  http://$SERVER_IP:8000/docs"
echo "  Root:  http://$SERVER_IP:8000/"
echo ""
echo "Next Steps:"
echo "  1. Edit /var/www/fyp-backend/.env with your SUPABASE_KEY"
echo "  2. Restart service: systemctl restart fyp-backend"
echo "  3. Test: curl http://$SERVER_IP:8000/health"
echo ""
