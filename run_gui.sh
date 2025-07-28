#!/bin/bash

# ShamaOllama Launcher Script for Linux/macOS
# Copyright (c) 2025 John Blancuzzi
# Licensed under the MIT License
# Paying homage to "Shama Lama Ding Dong" from Animal House (1978)

echo "🎸 Starting ShamaOllama..."
echo "Paying homage to 'Shama Lama Ding Dong' from Animal House (1978)"
echo ""

# Change to the script directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ -d ".venv" ]; then
    echo "📦 Activating virtual environment..."
    source .venv/bin/activate
else
    echo "⚠️  Virtual environment not found. Using system Python."
fi

# Check if requirements are installed
echo "🔍 Checking dependencies..."
if [ -f "requirements.txt" ]; then
    if ! python -c "import customtkinter, requests" 2>/dev/null; then
        echo "📥 Installing dependencies..."
        pip install -r requirements.txt
    fi
fi

# Check if Ollama is accessible
echo "� Checking Ollama status..."
if curl -s http://localhost:11434/api/version >/dev/null 2>&1; then
    echo "✅ Ollama is running!"
else
    echo ""
    echo "⚠️  WARNING: Ollama is not running or not installed!"
    echo ""
    echo "📋 To fix this:"
    echo "  1. Download from: https://ollama.ai"
    echo "  2. Install Ollama for your platform"
    echo "  3. Run: ollama pull llama3.2:1b  (small model)"
    echo "  4. Or: ollama pull llama3.2:3b   (better quality)"
    echo ""
    echo "🎯 ShamaOllama will start, but you'll need Ollama running to chat."
    echo ""
    read -p "Press Enter to continue..."
fi

echo ""
echo "🎨 Launching Ollama GUI..."
echo ""

# Run the application
python main.py

echo ""
echo "👋 Ollama GUI closed. Thanks for using it!"
