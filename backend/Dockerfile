# Use the Steam Deck Holo toolchain as base image
FROM ghcr.io/steamdeckhomebrew/holo-toolchain-go:latest

# Install required system packages:
# - git: for cloning repositories
# - libxkbcommon: dependency for dotool
# - pkg-config: build dependency
# - python-pip: for installing vosk
# - scdoc: dependency for dotool
# - unzip: for extracting vosk model
# - wget: for downloading vosk model
RUN pacman -Sydd --noconfirm \
    git \
    libxkbcommon \
    pkg-config \
    python-pip \
    scdoc \
    unzip \
    wget \
    && pacman -Scc --noconfirm

# Install all components in a single layer to reduce image size:
# 1. Install vosk speech recognition library
# 2. Clone nerd-dictation for speech-to-text
# 3. Download and extract the small English vosk model
# 4. Clone and build dotool (input automation tool)
RUN pip3 install vosk --target=/vosk_libraries \
    && git clone --depth 1 https://github.com/ideasman42/nerd-dictation.git \
    && wget https://alphacephei.com/kaldi/models/vosk-model-small-en-us-0.15.zip \
    && unzip vosk-model-small-en-us-0.15.zip \
    && rm vosk-model-small-en-us-0.15.zip \
    && git clone --depth 1 https://git.sr.ht/~geb/dotool \
    && cd dotool && ./build.sh

# Set the entrypoint script that will copy all components to their final locations
ENTRYPOINT [ "/backend/entrypoint.sh" ]
