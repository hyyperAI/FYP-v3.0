# FYP Job Matching Backend - Deployment Configuration

## Digital Ocean Droplet Setup

### 1. Server Requirements
- Ubuntu 22.04 LTS
- Python 3.10+
- 1GB RAM minimum (2GB recommended)
- NGINX as reverse proxy
- systemd for process management

### 2. Directory Structure
```
/var/www/fyp-backend/
├── app/                    # Application code
├── venv/                   # Python virtual environment
├── logs/                   # Application logs
└── gunicorn.sock           # Gunicorn socket file
```

### 3. Installation Steps

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3-pip python3-venv nginx ufw

# Create application directory
sudo mkdir -p /var/www/fyp-backend
sudo chown -R $USER:$USER /var/www/fyp-backend

# Clone repository
git clone <your-repo> /var/www/fyp-backend/app
cd /var/www/fyp-backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r app/requirements.txt

# Create systemd service
sudo nano /etc/systemd/system/fyp-backend.service
```

### 4. systemd Service Configuration
```ini
[Unit]
Description=FYP Job Matching Backend
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/fyp-backend
Environment="PATH=/var/www/fyp-backend/venv/bin"
ExecStart=/var/www/fyp-backend/venv/bin/gunicorn \
    --workers 4 \
    --bind unix:/var/www/fyp-backend/gunicorn.sock \
    main:app

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### 5. NGINX Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/fyp-backend/gunicorn.sock;
    }

    location /docs {
        proxy_pass http://unix:/var/www/fyp-backend/gunicorn.sock;
    }
}
```

### 6. Environment Variables
Create `/var/www/fyp-backend/.env`:
```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-or-service-key
HOST=0.0.0.0
PORT=8000
```

### 7. Firewall Setup
```bash
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

### 8. Start Services
```bash
# Start backend
sudo systemctl start fyp-backend
sudo systemctl enable fyp-backend

# Start NGINX
sudo systemctl start nginx
sudo systemctl enable nginx
```

## Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| `SUPABASE_URL` | Supabase project URL | Yes |
| `SUPABASE_KEY` | Supabase API key (anon or service) | Yes |
| `HOST` | Server host (default: 0.0.0.0) | No |
| `PORT` | Server port (default: 8000) | No |

## Security Notes

1. **Never commit `.env`** - Use `.env.example` template
2. **Use service role key** only for backend operations
3. **Enable RLS** in Supabase for production
4. **Use HTTPS** - Configure SSL certificate
5. **Rate limiting** - Configure in NGINX if needed

## Troubleshooting

```bash
# Check service status
sudo systemctl status fyp-backend

# View logs
sudo journalctl -u fyp-backend -f

# Restart service
sudo systemctl restart fyp-backend

# Check NGINX
sudo nginx -t
sudo systemctl status nginx
```