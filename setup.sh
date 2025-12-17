#!/bin/bash

# Student Risk Prediction System - Setup Script
# This script sets up the entire application

set -e

echo "=========================================="
echo "Student Risk Prediction System - Setup"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}Error: Node.js is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python and Node.js found${NC}"
echo ""

# Create necessary directories
echo "Creating directories..."
mkdir -p models data

# Setup Backend
echo ""
echo "=========================================="
echo "Setting up Backend..."
echo "=========================================="
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${GREEN}✓ Backend setup complete${NC}"

# Train model
echo ""
echo "=========================================="
echo "Training ML Model..."
echo "=========================================="
echo "This will generate synthetic data and train the model..."
python train_model.py

echo -e "${GREEN}✓ Model training complete${NC}"

# Deactivate virtual environment
deactivate

cd ..

# Setup Frontend
echo ""
echo "=========================================="
echo "Setting up Frontend..."
echo "=========================================="
cd frontend

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

echo -e "${GREEN}✓ Frontend setup complete${NC}"

cd ..

# Summary
echo ""
echo "=========================================="
echo "Setup Complete! 🎉"
echo "=========================================="
echo ""
echo "To run the application:"
echo ""
echo "Option 1: Using separate terminals"
echo "  Terminal 1 (Backend):"
echo "    cd backend"
echo "    source venv/bin/activate"
echo "    uvicorn main:app --reload"
echo ""
echo "  Terminal 2 (Frontend):"
echo "    cd frontend"
echo "    npm run dev"
echo ""
echo "Option 2: Using Docker"
echo "  docker-compose up"
echo ""
echo "Then open: http://localhost:3000"
echo "API docs at: http://localhost:8000/docs"
echo ""
echo -e "${GREEN}Happy predicting! 🎓${NC}"
