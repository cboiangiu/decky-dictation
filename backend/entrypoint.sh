#!/bin/sh
set -e

OUTDIR="/backend/out"

cd /backend

cp -r /vosk /backend/out/

cp -r /nerd-dictation /backend/out/
