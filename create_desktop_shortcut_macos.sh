#!/bin/bash

# ShamaOllama Desktop Shortcut Creator for macOS
# Creates a desktop alias and Applications entry

echo "🎸 Creating ShamaOllama Desktop Shortcut..."
echo ""

# Get the current directory (where the script is located)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create a simple app bundle structure
APP_NAME="ShamaOllama.app"
APP_PATH="$HOME/Desktop/$APP_NAME"
CONTENTS_DIR="$APP_PATH/Contents"
MACOS_DIR="$CONTENTS_DIR/MacOS"
RESOURCES_DIR="$CONTENTS_DIR/Resources"

# Create directories
mkdir -p "$MACOS_DIR"
mkdir -p "$RESOURCES_DIR"

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
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.12</string>
    <key>LSUIElement</key>
    <false/>
</dict>
</plist>
EOF

# Create executable launcher
cat > "$MACOS_DIR/ShamaOllama" << EOF
#!/bin/bash
cd "$SCRIPT_DIR"
./run_gui.sh
EOF

# Make executable
chmod +x "$MACOS_DIR/ShamaOllama"

# Copy to Applications folder too
cp -r "$APP_PATH" "/Applications/" 2>/dev/null || echo "Note: Couldn't copy to /Applications (permission needed)"

if [ -d "$APP_PATH" ]; then
    echo "✅ Desktop shortcut created successfully!"
    echo "📍 Desktop: $APP_PATH"
    echo "📍 Applications: /Applications/$APP_NAME (if permissions allowed)"
    echo ""
    echo "You can now:"
    echo "• Double-click the ShamaOllama app on your desktop"
    echo "• Find ShamaOllama in your Applications folder"
    echo "• Add it to your Dock"
else
    echo "❌ Failed to create desktop shortcut."
    echo "Please check permissions and try again."
fi

echo ""
