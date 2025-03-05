#!/bin/sh
set -e

cd /backend

# Copy Vosk libraries
cp -r /vosk_libraries /backend/out/

# Setup nerd-dictation
cp -r /nerd-dictation /backend/out/

# Copy Vosk model
cp -r /vosk-model-small-en-us-0.15 /backend/out/

# Copy dotool
cp -r /dotool /backend/out/