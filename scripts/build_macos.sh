#!/usr/bin/env bash
set -e

echo "=== Building VoiceForge for macOS ==="

# Ensure icons exist
python assets/generate_icons.py

# Build app using PyInstaller spec
pyinstaller --clean voiceforge.spec

APP_PATH="dist/VoiceForge.app"
DMG_PATH="dist/VoiceForge-1.0.0-macOS.dmg"

if [ -d "$APP_PATH" ]; then
    echo "Creating macOS DMG installer..."
    if command -v create-dmg &> /dev/null; then
        create-dmg \
          --volname "VoiceForge Installer" \
          --window-pos 200 120 \
          --window-size 600 400 \
          --icon-size 100 \
          --icon "VoiceForge.app" 175 190 \
          --hide-extension "VoiceForge.app" \
          --app-drop-link 425 190 \
          "$DMG_PATH" \
          "$APP_PATH" || true
    else
        echo "Warning: create-dmg not installed. Fallback to basic zip asset."
        hdiutil create -volname "VoiceForge" -srcfolder "$APP_PATH" -ov -format UDZO "$DMG_PATH"
    fi
    echo "macOS build completed successfully."
else
    echo "Error: App bundle build failed!"
    exit 1
fi