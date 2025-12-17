#!/bin/bash

# Student Risk Prediction System - Start Script
# This script starts both backend and frontend

set -e

echo "=========================================="
echo "Starting Student Risk Prediction System"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if model exists
if [ ! -f "models/model.pkl" ]; then
    echo -e "${YELLOW}Warning: Model not found. Training model first...${NC}"
    cd backend
    source venv/bin/activate
    python train_model.py
    deactivate
    cd ..
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
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
deactivate
cd ..

echo -e "${GREEN}✓ Backend started on http://localhost:8000${NC}"

# Wait a bit for backend to start
sleep 3

# Start Frontend
echo "Starting Frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

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
