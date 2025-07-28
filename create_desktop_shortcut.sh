#!/bin/bash

# ShamaOllama Desktop Shortcut Creator for Linux
# Creates a desktop entry for easy access

echo "🎸 Creating ShamaOllama Desktop Shortcut..."
echo ""

# Get the current directory (where the script is located)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create desktop entry
DESKTOP_FILE="$HOME/Desktop/ShamaOllama.desktop"

cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=ShamaOllama
Comment=Modern Ollama GUI - Paying homage to Animal House (1978)
Exec=bash "$SCRIPT_DIR/run_gui.sh"
Icon=utilities-terminal
Path=$SCRIPT_DIR
Terminal=false
StartupNotify=true
Categories=Development;Utility;
Keywords=AI;Ollama;Chat;Local;Machine Learning;
EOF

# Make the desktop file executable
chmod +x "$DESKTOP_FILE"

# Also create in applications directory for system-wide access
APPS_DIR="$HOME/.local/share/applications"
mkdir -p "$APPS_DIR"
cp "$DESKTOP_FILE" "$APPS_DIR/"

if [ -f "$DESKTOP_FILE" ]; then
    echo "✅ Desktop shortcut created successfully!"
    echo "📍 Desktop: $DESKTOP_FILE"
    echo "📍 Applications: $APPS_DIR/ShamaOllama.desktop"
    echo ""
    echo "You can now:"
    echo "• Double-click the ShamaOllama icon on your desktop"
    echo "• Find ShamaOllama in your applications menu"
    echo "• Pin it to your taskbar/dock"
else
    echo "❌ Failed to create desktop shortcut."
    echo "Please check permissions and try again."
fi

echo ""
