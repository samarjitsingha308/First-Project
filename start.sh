#!/bin/bash

# Student Risk Prediction System - Start Script
# This script starts both backend and frontend

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "Starting Student Risk Prediction System"
echo "=========================================="
echo ""
echo "Working directory: $SCRIPT_DIR"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if setup was run
if [ ! -d "$SCRIPT_DIR/backend/venv" ]; then
    echo -e "${RED}Error: Virtual environment not found!${NC}"
    echo ""
    echo "It looks like you haven't run the setup script yet."
    echo ""
    echo "Please run the setup first:"
    echo -e "  ${GREEN}./setup.sh${NC}"
    echo ""
    echo "This will:"
    echo "  - Install all dependencies"
    echo "  - Create virtual environment"
    echo "  - Train the ML model"
    echo ""
    exit 1
fi

if [ ! -d "$SCRIPT_DIR/frontend/node_modules" ]; then
    echo -e "${YELLOW}Warning: Frontend dependencies not installed!${NC}"
    echo "Installing frontend dependencies..."
    cd "$SCRIPT_DIR/frontend"
    npm install
    cd "$SCRIPT_DIR"
fi

# Check if model exists
if [ ! -f "$SCRIPT_DIR/models/model.pkl" ]; then
    echo -e "${YELLOW}Warning: Model not found. Training model first...${NC}"
    cd "$SCRIPT_DIR/backend"
    source venv/bin/activate
    python train_model.py
    deactivate
    cd "$SCRIPT_DIR"
fi

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Shutting down..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start Backend
echo "Starting Backend API..."
cd "$SCRIPT_DIR/backend"
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
deactivate
cd "$SCRIPT_DIR"

echo -e "${GREEN}✓ Backend started on http://localhost:8000${NC}"

# Wait a bit for backend to start
sleep 3

# Start Frontend
echo "Starting Frontend..."
cd "$SCRIPT_DIR/frontend"
npm run dev &
FRONTEND_PID=$!
cd "$SCRIPT_DIR"

echo -e "${GREEN}✓ Frontend started on http://localhost:3000${NC}"
echo ""
echo "=========================================="
echo "Application is running!"
echo "=========================================="
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both services"
echo ""

# Wait for both processes
wait
