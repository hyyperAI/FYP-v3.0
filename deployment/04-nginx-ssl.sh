#!/bin/bash

# =================================================================
# FYP Backend - Nginx & SSL Setup (Optional)
# =================================================================
# Install Nginx as reverse proxy with Let's Encrypt SSL
# =================================================================

set -e

echo "=========================================="
echo "FYP Backend - Nginx & SSL Setup"
echo "=========================================="
echo ""

DOMAIN=${1:-}
EMAIL=${2:-}

if [ -z "$DOMAIN" ]; then
    echo "Usage: ./04-nginx-ssl.sh <domain> <email>"
    echo "Example: ./04-nginx-ssl.sh api.example.com admin@example.com"
    exit 1
fi

echo "[1/6] Installing Nginx and Certbot..."
apt install -y nginx certbot python3-certbot-nginx

echo "[2/6] Creating Nginx configuration..."
cat > /etc/nginx/sites-available/fyp-backend <<EOF
server {
    listen 80;
    server_name ${DOMAIN};

    # Redirect to HTTPS
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name ${DOMAIN};

    # SSL Certificate
    ssl_certificate /etc/letsencrypt/live/${DOMAIN}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${DOMAIN}/privkey.pem;

    # SSL Configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Proxy to FastAPI
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
        proxy_read_timeout 86400;
    }

    # Logging
    access_log /var/log/nginx/fyp-backend-access.log;
    error_log /var/log/nginx/fyp-backend-error.log;
}
EOF

echo "[3/6] Enabling Nginx site..."
ln -sf /etc/nginx/sites-available/fyp-backend /etc/nginx/sites-enabled/
nginx -t

echo "[4/6] Obtaining SSL certificate..."
certbot --nginx -d "$DOMAIN" --email "$EMAIL" --non-interactive --agree-tos

echo "[5/6] Setting up SSL auto-renewal..."
systemctl enable certbot.timer
systemctl start certbot.timer

echo "[6/6] Starting Nginx..."
systemctl restart nginx

echo ""
echo "=========================================="
echo "Nginx & SSL setup complete!"
echo "=========================================="
echo ""
echo "Your API is now accessible at:"
echo "  HTTPS: https://${DOMAIN}/"
echo "  Docs:  https://${DOMAIN}/docs"
echo "  Health: https://${DOMAIN}/health"
echo ""
echo "Note: Direct IP access on port 8000 still works."
echo ""
