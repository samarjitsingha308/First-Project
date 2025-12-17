#!/bin/bash

# Alternative Start Script - Manual Method
# Use this if the automatic start.sh doesn't work

echo "=========================================="
echo "Manual Start - Student Risk Prediction"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "This script will show you the commands to run in separate terminals."
echo ""
echo "=========================================="
echo "TERMINAL 1 - Backend"
echo "=========================================="
echo ""
echo "Run these commands:"
echo -e "${GREEN}"
echo "cd /workspace/backend"
echo "source venv/bin/activate"
echo "uvicorn main:app --reload --host 0.0.0.0 --port 8000"
echo -e "${NC}"
echo ""
echo "=========================================="
echo "TERMINAL 2 - Frontend"
echo "=========================================="
echo ""
echo "Run these commands:"
echo -e "${GREEN}"
echo "cd /workspace/frontend"
echo "npm run dev"
echo -e "${NC}"
echo ""
echo "=========================================="
echo "Then open: http://localhost:3000"
echo "=========================================="
