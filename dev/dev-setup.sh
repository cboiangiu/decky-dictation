#!/bin/bash
set -eu

# NOTE: This script must be run from within the 'dev' directory
# Example: cd dev && ./dev-setup.sh

# Function to log messages
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Help message
show_help() {
    cat << EOF
Development Setup Script for Decky Dictation Plugin

Usage: 
    ./dev-setup.sh [OPTIONS]

Options:
    -h, --help     Show this help message
    -c, --clean    Clean existing installation before setup

The script will set up the plugin directory structure and install dependencies.
EOF
}

# Parse arguments
CLEAN=0

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -c|--clean)
            CLEAN=1
            shift
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Get absolute paths
SCRIPT_DIR="$(pwd)"
PLUGIN_DIR="$SCRIPT_DIR/plugin_dir"
DATA_DIR="$PLUGIN_DIR/data"
LOGS_DIR="$PLUGIN_DIR/logs"
BIN_DIR="$PLUGIN_DIR/bin"

# Clean if requested
if [ "$CLEAN" -eq 1 ]; then
    log "Cleaning existing installation"
    rm -rf "$PLUGIN_DIR"
fi

# Create directory structure
mkdir -p "$DATA_DIR"
mkdir -p "$LOGS_DIR"
mkdir -p "$BIN_DIR"

# Install dependencies
log "Installing dependencies..."
temp_dir=$(mktemp -d)
cd "$temp_dir"

# Install nerd-dictation
log "Installing nerd-dictation..."
git clone https://github.com/ideasman42/nerd-dictation.git
mkdir -p "$BIN_DIR/nerd-dictation"
cp -r nerd-dictation/nerd-dictation "$BIN_DIR/nerd-dictation/nerd-dictation.py"

# Install dotool
log "Installing dotool..."
git clone https://git.sr.ht/~geb/dotool
cd dotool
./build.sh
cd ..
mkdir -p "$BIN_DIR/dotool"
cp -R dotool "$BIN_DIR/dotool"

# Install vosk and model
log "Installing vosk..."
pip install vosk --target="$BIN_DIR/vosk_libraries"

log "Downloading vosk model..."
wget https://alphacephei.com/kaldi/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip -d "$BIN_DIR/"

# Clean up
cd "$SCRIPT_DIR"
rm -rf "$temp_dir"

log "
Setup complete! Your plugin directory is ready at: $PLUGIN_DIR

Directory structure:
$PLUGIN_DIR/
├── data/
├── logs/
└── bin/
    ├── nerd-dictation/
    │   └── nerd-dictation.py
    ├── dotool/
    │   └── dotool
    ├── vosk_libraries/
    └── vosk-model-small-en-us-0.15/
" 
