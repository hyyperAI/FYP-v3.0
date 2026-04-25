#!/bin/bash

cd /var/www/fyp-backend && git pull
pkill -f "uvicorn main:app" || true
nohup /var/www/fyp-backend/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000 > app.log 2>&1 &

pkill -f "ngrok" || true
nohup ngrok http 8000 --host-header=rewrite > ngrok.log 2>&1 &
