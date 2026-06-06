#!/bin/bash
set -e

echo "Installing build and runtime dependencies..."
pip install setuptools
pip install -r requirements.txt
echo "Installation complete."
