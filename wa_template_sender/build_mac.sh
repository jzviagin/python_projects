#!/bin/bash
# Build "WA Sender.app" and copy it into /Applications.
# Needs a Python with Tk: the python.org installer has it; with Homebrew run
# `brew install python-tk` first.
set -euo pipefail
cd "$(dirname "$0")"

python3 -m venv .venv
.venv/bin/pip install -q pyinstaller
.venv/bin/pyinstaller --noconfirm --windowed --name "WA Sender" \
    --icon assets/icon.icns wa_sender_gui.py

rm -rf "/Applications/WA Sender.app"
cp -R "dist/WA Sender.app" /Applications/
echo "Installed: /Applications/WA Sender.app"
