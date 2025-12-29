#!/bin/bash

echo "🚀 Starting BERT Search Engine..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found"

# Check if dependencies are installed
if ! python3 -c "import fastapi" &> /dev/null; then
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt
fi

echo "✅ Dependencies installed"
echo ""
echo "🌐 Starting server on http://localhost:8000"
echo "📝 Press Ctrl+C to stop the server"
echo ""

python3 app.py
