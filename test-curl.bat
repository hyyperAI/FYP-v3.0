@echo off
curl -X POST http://localhost:8000/ai/generate-instructions -H "Content-Type: application/json" -d "{\"currentPrompt\": \"Write a proposal intro for a web development job\", \"systemPrompt\": \"You are an expert Upwork proposal writer AI.\"}"
