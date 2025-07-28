#!/bin/bash

# ShamaOllama Universal Desktop Shortcut Creator
# Automatically detects platform and creates appropriate shortcut

echo "🎸 ShamaOllama Desktop Shortcut Creator"
echo "Paying homage to 'Shama Lama Ding Dong' from Animal House (1978)"
echo ""

# Detect operating system
OS="$(uname -s)"
case "${OS}" in
    Linux*)     PLATFORM=Linux;;
    Darwin*)    PLATFORM=Mac;;
    CYGWIN*)    PLATFORM=Cygwin;;
    MINGW*)     PLATFORM=MinGw;;
    *)          PLATFORM="Unknown:${OS}"
esac

echo "Detected platform: $PLATFORM"
echo ""

# Get the current directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

case $PLATFORM in
    Linux)
        echo "Creating Linux desktop entry..."
        
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
        
        chmod +x "$DESKTOP_FILE"
        
        # Also create in applications directory
        APPS_DIR="$HOME/.local/share/applications"
        mkdir -p "$APPS_DIR"
        cp "$DESKTOP_FILE" "$APPS_DIR/"
        
        echo "✅ Linux desktop shortcut created!"
        echo "📍 Desktop: $DESKTOP_FILE"
        echo "📍 Applications menu: Available in applications"
        ;;
        
    Mac)
        echo "Creating macOS app bundle..."
        
        # Create app bundle
        APP_NAME="ShamaOllama.app"
        APP_PATH="$HOME/Desktop/$APP_NAME"
        CONTENTS_DIR="$APP_PATH/Contents"
        MACOS_DIR="$CONTENTS_DIR/MacOS"
        
        mkdir -p "$MACOS_DIR"
        
        # Create Info.plist
        cat > "$CONTENTS_DIR/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>ShamaOllama</string>
    <key>CFBundleIdentifier</key>
    <string>com.blancuzzi.shamollama</string>
    <key>CFBundleName</key>
    <string>ShamaOllama</string>
    <key>CFBundleDisplayName</key>
    <string>ShamaOllama</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
</dict>
</plist>
EOF
        
        # Create executable
        cat > "$MACOS_DIR/ShamaOllama" << EOF
#!/bin/bash
cd "$SCRIPT_DIR"
./run_gui.sh
EOF
        
        chmod +x "$MACOS_DIR/ShamaOllama"
        
        echo "✅ macOS app bundle created!"
        echo "📍 Desktop: $APP_PATH"
        ;;
        
    *)
        echo "❌ Unsupported platform: $PLATFORM"
        echo ""
        echo "For Windows, please run: create_desktop_shortcut.bat"
        echo "For manual setup, use the run_gui scripts directly."
        exit 1
        ;;
esac

echo ""
echo "🎉 Desktop shortcut created successfully!"
echo ""
echo "You can now launch ShamaOllama by:"
echo "• Double-clicking the desktop shortcut"
echo "• Finding it in your applications menu/Launchpad"
echo "• Pinning it to your taskbar/dock"
echo ""
echo "Enjoy your AI conversations! 🎸✨"
