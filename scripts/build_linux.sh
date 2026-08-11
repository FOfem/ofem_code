#!/usr/bin/env bash
set -e

echo "=== Building VoiceForge for Linux ==="
python assets/generate_icons.py
pyinstaller --clean voiceforge.spec
echo "Linux binary generated in dist/VoiceForge"