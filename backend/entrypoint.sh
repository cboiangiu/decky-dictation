#!/bin/sh
set -e

cd /backend

cp -r /vosk /backend/out/

cp -r /nerd-dictation /backend/out/

cp -r /vosk-model-small-en-us-0.15 /backend/out/
