@echo off

echo Starting War Thunder Tactics Development Environment

echo Starting Backend Server...
start cmd /k "cd backend && npm start"

echo Starting Frontend Server...
start cmd /k "cd frontend && npm start"

echo Development servers started successfully!
echo Backend running at http://localhost:5000
echo Frontend running at http://localhost:3000 