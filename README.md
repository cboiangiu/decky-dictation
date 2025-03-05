# Steam Deck Dictation Plugin

A Decky plugin that enables voice dictation on your Steam Deck, allowing you to use voice input anywhere text input is supported.

## 🎯 Features

- Voice-to-text dictation anywhere on your Steam Deck
- Push-to-talk or continuous dictation modes
- Real-time transcription
- Seamless integration with Steam Deck's interface

## 📖 Quick Start Guide

1. Install the plugin through the Decky Plugin Store
2. Launch the plugin from your Quick Access menu
3. Choose your preferred dictation mode (push-to-talk or continuous)
4. Start dictating!

## 🛠️ Installation

### For Users
1. Install [Decky Loader](https://github.com/SteamDeckHomebrew/decky-loader)
2. Open the Decky Plugin Store
3. Search for "Dictation" and click Install
4. Restart your Steam Deck

### For Developers
Please see our detailed guides:
- [Setting Up Your Build Environment](docs/1_Configure_Build_Environment.md)
- [Configuring Your Steam Deck](docs/2_Configure_Steam_Deck.md)
- [Building the Plugin](docs/3_Build_Plugin.md)
- [Deploying the Plugin](docs/4_Deploy_Plugin.md)

## 🏗️ Architecture

The Steam Deck Dictation Plugin is built on a hybrid architecture combining Python and TypeScript:

### Backend (Python)
- Core dictation functionality using PulseAudio for audio capture
- Speech recognition processing
- System integration with Steam Deck's audio system

### Frontend (TypeScript/React)
- User interface integration with Steam Deck's Quick Access menu
- Real-time status display
- Configuration controls
- Seamless integration with Decky's UI framework

### Key Components
- `main.py`: Core plugin backend and dictation control
- `src/`: Frontend UI components and state management
- `backend/`: Speech recognition and audio processing
- `py_modules/`: Python module dependencies

## ⚙️ Configuration

The plugin can be configured through its settings menu in the Quick Access overlay:

- Dictation Mode: Choose between push-to-talk or continuous dictation
- Language Settings: Select your preferred language for dictation
- Audio Input: Configure your microphone settings
- Hotkeys: Customize activation shortcuts

## 🤝 Contributing

We welcome contributions!

## 📝 License

This project is licensed under the [BSD-3 License](LICENSE).

## 🙏 Acknowledgments

- [Decky Loader](https://github.com/SteamDeckHomebrew/decky-loader) team
- [nerd-dictation](https://github.com/ideasman42/nerd-dictation) for speech recognition
- All our contributors and users

---

For detailed technical documentation and development guides, please visit our [documentation directory](docs/).

# Project Layout

```src/
├── backend/          # Backend Python code for audio processing and dictation
├── docs/             # Documentation
├── py_modules/       # Python module dependencies
├── src/              # Frontend TypeScript/React code
├── tests/            # Test files
```

Key Files:
- `main.py`: Core plugin backend and dictation control
- `plugin.json`: Plugin metadata and configuration
- `package.json`: Node.js dependencies and scripts
- `tsconfig.json`: TypeScript configuration
- `rollup.config.js`: Build configuration
