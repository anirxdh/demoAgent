#!/bin/bash

echo "🤖 Setting up OpenAI AI Agent Demo..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the agent:"
echo "  1. Make sure you have your OPENAI_API_KEY in the .env file"
echo "  2. Activate the virtual environment: source venv/bin/activate"
echo "  3. Run the agent: python main.py"
echo ""
echo "Or simply run:"
echo "  source venv/bin/activate && python main.py"


