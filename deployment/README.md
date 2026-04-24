# FYP Backend - DigitalOcean Deployment Guide

## Overview

This guide will help you deploy the FYP Job Matching Backend to a DigitalOcean droplet with Ubuntu 22.04 LTS.

## Prerequisites

1. A DigitalOcean account
2. A droplet with Ubuntu 22.04 LTS (minimum $5/month)
3. SSH access to the droplet
4. Supabase credentials (URL and API Key)

## Quick Deployment

### Step 1: Create DigitalOcean Droplet

1. Log in to [DigitalOcean](https://www.digitalocean.com)
2. Click "Create" → "Droplets"
3. Configure:
   - **Choose an Image**: Ubuntu 22.04 LTS
   - **Choose a Size**: Basic plan, $5/month (sFO1 - 1GB RAM)
   - **Choose a Region**: Select nearest to your users (NYC, SFO, etc.)
   - **Authentication**: SSH keys recommended
4. Click "Create Droplet"
5. Note the IPv4 IP address once created

### Step 2: Connect to Droplet

```bash
ssh root@YOUR_DROPLET_IP
```

### Step 3: Run Deployment Scripts

Once connected to your droplet, run these commands:

```bash
# Navigate to deployment directory
cd /root

# Download deployment scripts (or clone from GitHub)
git clone https://github.com/hyyperAI/FYP-v3.0.git
cd FYP-v3.0/fyp-backend/deployment

# Run the complete deployment
chmod +x *.sh
./QUICKSTART.sh
```

Or run scripts individually:

```bash
# 1. Setup server
./01-setup.sh

# 2. Deploy application
./02-deploy.sh

# 3. Configure environment
nano /var/www/fyp-backend/.env
```

### Step 4: Configure Supabase Credentials

Edit the `.env` file:

```bash
nano /var/www/fyp-backend/.env
```

Update with your actual Supabase credentials:

```
SUPABASE_URL=https://vzylxrdujxgzlgogjvru.supabase.co
SUPABASE_KEY=your_actual_supabase_anon_or_service_role_key_here
```

### Step 5: Restart Service

```bash
systemctl restart fyp-backend
```

### Step 6: Test Deployment

```bash
# Test health endpoint
curl http://YOUR_DROPLET_IP:8000/health

# Check service status
systemctl status fyp-backend

# View logs
journalctl -u fyp-backend -n 50 --no-pager
```

## Deployment Scripts

### `01-setup.sh` - Server Setup
- Updates system packages
- Installs Python 3, pip, virtualenv
- Creates application user
- Configures UFW firewall
- Installs Fail2Ban for security

### `02-deploy.sh` - Application Deployment
- Clones repository from GitHub
- Creates Python virtual environment
- Installs dependencies
- Configures systemd service
- Starts the application

### `03-update.sh` - Update Script
- Pulls latest changes from GitHub
- Updates dependencies
- Restarts service

### `04-nginx-ssl.sh` - Nginx & SSL Setup (Optional)
- Installs Nginx as reverse proxy
- Configures Let's Encrypt SSL
- Sets up automatic certificate renewal

## API Endpoints

After deployment, your API will be available at:

- **Base URL**: `http://YOUR_DROPLET_IP:8000`
- **Health Check**: `http://YOUR_DROPLET_IP:8000/health`
- **API Documentation**: `http://YOUR_DROPLET_IP:8000/docs`
- **ReDoc Documentation**: `http://YOUR_DROPLET_IP:8000/redoc`

## Service Management

```bash
# Start service
systemctl start fyp-backend

# Stop service
systemctl stop fyp-backend

# Restart service
systemctl restart fyp-backend

# View status
systemctl status fyp-backend

# View logs
journalctl -u fyp-backend -f
```

## Updating the Application

```bash
# SSH into your droplet
ssh root@YOUR_DROPLET_IP

# Navigate to deployment directory
cd /var/www/fyp-backend/fyp-backend/deployment

# Run update script
./03-update.sh
```

## Firewall Configuration

The deployment script automatically configures UFW with these rules:

- **22 (SSH)**: Access for SSH connections
- **80 (HTTP)**: Web traffic (for Nginx)
- **443 (HTTPS)**: Secure web traffic (for SSL)
- **8000 (API)**: FYP Backend API

## Troubleshooting

### Service won't start

```bash
# Check logs
journalctl -u fyp-backend -n 100 --no-pager

# Common issues:
# - Missing .env file
# - Incorrect Supabase credentials
# - Port 8000 already in use
```

### Application errors

```bash
# Activate virtual environment
source /var/www/fyp-backend/fyp-backend/venv/bin/activate

# Test run manually
cd /var/www/fyp-backend/fyp-backend
uvicorn main:app --host 0.0.0.0 --port 8000

# Check for import errors
python -c "import main"
```

### Database connection issues

Verify your Supabase credentials:
```bash
cat /var/www/fyp-backend/.env
```

Test Supabase connection:
```bash
source /var/www/fyp-backend/fyp-backend/venv/bin/activate
python
>>> from config import SUPABASE_URL, SUPABASE_KEY
>>> print(SUPABASE_URL, SUPABASE_KEY)
```

## Production Considerations

For production deployment, consider:

1. **SSL/HTTPS**: Run `04-nginx-ssl.sh` to add SSL with Let's Encrypt
2. **Domain**: Point a domain to your droplet IP
3. **Monitoring**: Set up monitoring tools (e.g., UptimeRobot)
4. **Backups**: Configure automated backups for your Supabase database
5. **Logging**: Set up log aggregation (e.g., ELK stack)
6. **Security**: 
   - Use SSH keys instead of passwords
   - Keep system updated: `apt update && apt upgrade`
   - Review Fail2Ban logs regularly

## Supabase Setup

Make sure your Supabase project has:

1. **Tables Created**: jobs, filters, proposals, users
2. **API Enabled**: Anonymous and service role keys generated
3. **RLS Policies**: Appropriate row-level security policies configured

## Support

For issues:
1. Check service logs: `journalctl -u fyp-backend -n 50`
2. Test API endpoints
3. Verify Supabase credentials
4. Check Supabase project status

## Cost Summary

- **DigitalOcean Droplet**: $5/month (1GB RAM, 25GB SSD)
- **Supabase**: Free tier available (includes 500MB database, 1GB transfer)
- **SSL Certificate**: Free (Let's Encrypt)
- **Total**: $5/month minimum

## Backup Commands

```bash
# Backup application
tar -czf fyp-backend-backup.tar.gz /var/www/fyp-backend

# Backup service file
cp /etc/systemd/system/fyp-backend.service ~/fyp-backend-backup.service

# Backup logs
journalctl -u fyp-backend > fyp-backend-logs.txt
```

## Uninstallation

```bash
# Stop service
systemctl stop fyp-backend

# Disable service
systemctl disable fyp-backend

# Remove files
rm /etc/systemd/system/fyp-backend.service
rm -rf /var/www/fyp-backend

# Remove firewall rules
ufw delete allow 8000/tcp
```
