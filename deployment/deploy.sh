#!/bin/bash

cd /var/www/fyp-backend && git pull && pkill -f "uvicorn main:app" && nohup /var/www/fyp-backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &
