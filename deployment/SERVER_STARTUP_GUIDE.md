# FYP Backend - Server Startup Guide

## One-Time Setup Commands

These commands only need to be run once when setting up the server:

```bash
# Navigate to project directory
cd /var/www/fyp-backend/fyp-backend.git

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Creating the .env File

```bash
cat > .env << 'EOF'
SUPABASE_URL=https://vzylxrdujxgzlgogjvru.supabase.co
SUPABASE_KEY=your_supabase_api_key
MINIMAX_API_KEY=your_minimax_api_key
EOF
```

## Starting the Server

```bash
# Navigate to project directory
cd /var/www/fyp-backend/fyp-backend.git

# Activate virtual environment
source venv/bin/activate

# Start server in background
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > /root/server.log 2>&1 &

# Disown the process so it continues after logout
disown
```

## Testing the Server

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test AI endpoint
curl -X POST http://localhost:8000/ai/generate-instructions -H "Content-Type: application/json" -d "{\"currentPrompt\": \"test\", \"systemPrompt\": \"hi\"}"

# Test proposals endpoint
curl http://localhost:8000/proposals/
```

## Useful Commands

```bash
# Check server logs
cat /root/server.log

# Check if server is running
ps aux | grep uvicorn

# Stop the server
pkill -f uvicorn

# Restart the server (stop then start)
pkill -f uvicorn
cd /var/www/fyp-backend/fyp-backend.git
source venv/bin/activate
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > /root/server.log 2>&1 &
disown
```

## Alternative: systemd Service (Recommended for Production)

Create a systemd service file:

```bash
cat > /etc/systemd/system/fyp-backend.service << 'EOF'
[Unit]
Description=FYP Backend API
After=network.target

[Service]
User=root
WorkingDirectory=/var/www/fyp-backend/fyp-backend.git
ExecStart=/var/www/fyp-backend/fyp-backend.git/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF
```

Then run:
```bash
systemctl daemon-reload
systemctl enable fyp-backend
systemctl start fyp-backend
systemctl status fyp-backend
```

## Server Information

- **Server IP:** 159.65.225.228
- **Port:** 8000
- **Base URL:** http://159.65.225.228:8000
- **API Docs:** http://159.65.225.228:8000/docs
- **Health Check:** http://159.65.225.228:8000/health