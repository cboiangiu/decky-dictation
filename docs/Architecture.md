# Steam Deck Dictation Plugin Architecture

## Overview
The Steam Deck Dictation Plugin is built on a hybrid architecture combining Python backend for audio processing and TypeScript/React frontend for UI integration.

## Core Components

### nerd-dictation
The core dictation functionality is powered by nerd-dictation, a lightweight Python-based dictation tool that:
- Operates as a standalone Python script (no installation required)
- Integrates with PulseAudio for audio capture
- Uses Vosk for speech-to-text processing
- Supports multiple input simulation backends

#### nerd-dictation Architecture
```
[Audio Capture] -> [Speech Processing] -> [Text Processing] -> [Input Simulation]
    (parec)           (Vosk)          (nerd-dictation)      (dotool)
```

#### Input Simulation Options
nerd-dictation supports multiple input simulation backends:
- **xdotool**: X11 automation tool (pre-installed on Steam Deck)
  - Works reliably in Desktop Mode (X11/KWin)
  - Limited functionality in Gaming Mode due to XWayland dependencies
- **ydotool**: Wayland-compatible input tool
  - Requires daemon and /dev/uinput access
  - Works in both Desktop and Gaming modes
- **dotool**: Direct /dev/uinput access (Currently Used)
  - Simplest implementation
  - Works reliably in both Desktop and Gaming modes
  - No daemon requirement
  - Supports both direct (dotool) and client/server (dotoolc/dotoold) modes

#### Why dotool?
We chose dotool for the Steam Deck implementation because:
1. Direct /dev/uinput access is already permitted for the deck user
2. Works consistently across both Desktop (KWin/X11) and Gaming (Gamescope/Wayland) modes
3. Simpler architecture compared to ydotool (no daemon required)
4. More reliable than xdotool in Gaming Mode

### Audio Processing Pipeline
Detailed flow of audio processing:
1. **Audio Capture**
   - Uses parec (PulseAudio) for audio stream capture
   - Configurable sampling rate and audio parameters

2. **Speech Recognition**
   - Vosk small model (~70MB) processes audio stream
   - Offline processing (no internet required)
   - Optimized for real-time transcription

3. **Text Processing**
   - nerd-dictation processes Vosk output
   - Handles text formatting and command interpretation

4. **Input Simulation**
   - dotool sends processed text directly to /dev/uinput
   - Simulates keyboard input at system level

### Backend Components
- **Dictator Module**: Core Python class managing dictation state and processing
- **Audio Capture**: Uses PulseAudio (parec) for audio stream capture
- **Speech Recognition**: Vosk library for offline speech-to-text
- **Input Simulation**: dotool for direct /dev/uinput access

### Frontend Components
- **React UI**: Decky-integrated user interface
- **State Management**: Real-time dictation status
- **Settings Interface**: User configuration management

## Technical Details

### Audio Processing
- Uses PulseAudio for reliable audio capture
- Vosk small model (~70MB) for efficient speech recognition
- Direct /dev/uinput access for reliable input simulation

### Environment-Specific Behavior

#### Desktop Mode (KWin/X11)
- Full functionality through native X11 support
- Direct input simulation via dotool
- PulseAudio integration for audio capture

#### Gaming Mode (Gamescope/Wayland)
- Full functionality through Wayland compatibility
- Direct input simulation via dotool
- Consistent behavior with Desktop Mode

### Security Considerations
- Requires /dev/uinput access (pre-configured on Steam Deck)
- Runs with user privileges
- No network access required for core functionality
- Audio capture limited to active sessions

## Data Flow
1. User initiates dictation through Decky UI
2. Frontend signals backend to start nerd-dictation
3. nerd-dictation initiates audio capture through parec
4. Audio stream is processed by Vosk in real-time
5. nerd-dictation processes recognized text
6. Text is sent to dotool for input simulation
7. Input appears in active application/game

## Dependencies
- Frontend: Decky Frontend Library
- Backend: 
  - Python
  - nerd-dictation (single script, no installation)
  - Vosk (small model, ~70MB)
  - PulseAudio
  - dotool
- System: 
  - /dev/uinput access
  - XDG_RUNTIME_DIR environment variable

## Configuration
nerd-dictation can be configured for:
- Push-to-talk or continuous dictation modes
- Custom input simulation backend selection
- Audio device selection
- Language model selection
- Text formatting preferences

## Future Considerations
- Potential migration to dotoolc/dotoold for improved performance
- Additional language model support
- Custom command integration
- Enhanced text formatting options
