#!/bin/bash
echo "Installing optional GPU detection dependencies..."
echo "This will enable enhanced hardware analysis for local AI recommendations."
echo

pip install -r requirements-gpu.txt

if [ $? -eq 0 ]; then
    echo
    echo "✅ GPU detection dependencies installed successfully!"
    echo "Enhanced hardware information is now available in ShamaOllama."
else
    echo
    echo "❌ Installation failed. Please check your Python and pip installation."
    echo "You can still use ShamaOllama with basic GPU detection."
fi

echo
echo "Press Enter to continue..."
read
