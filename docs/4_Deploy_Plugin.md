# Deploying the Steam Deck Dictation Plugin

This guide covers deploying the plugin to your Steam Deck for testing and use.

## Configuration

### 1. Setup VSCode Settings
Edit `.vscode/settings.json`:
```json
{
    "deckip": "your.deck.ip.address",
    "deckport": "22",
    "deckuser": "deck",
    "deckpass": "your_password",
    "deckkey": "-i ${env:HOME}/.ssh/steamdeck_ed25519",
    "pluginname": "Decky Dictation",
    "python.analysis.extraPaths": [
    "./py_modules"
    ]

}
```

### 2. Prerequisites
- Ensure Decky Loader is installed on your Steam Deck
- Verify SSH access is configured (see Configure_Steam_Deck.md)
- Confirm the plugin has been built successfully

## Deployment Methods

### Automated Deployment (VSCode)
1. Open Command Palette (Ctrl+Shift+P)
2. Select "Tasks: Run Task"
3. Choose "builddeploy"

### Manual Deployment
1. Copy plugin to Steam Deck:
   ```bash
   scp out/decky-dictation.zip deck@<steam-deck-ip>:/home/deck/homebrew/plugins/
   ```

2. SSH into Steam Deck and extract:
   ```bash
   ssh deck@<steam-deck-ip>
   cd /home/deck/homebrew/plugins/
   unzip decky-dictation.zip
   ```

## Verification
1. Open Quick Access menu on Steam Deck
2. Open Decky settings
3. Navigate to Plugins section
4. Verify Decky Dictation appears and is enabled

## Troubleshooting
- Plugin not appearing: Restart Decky Loader
- Deployment fails: Check SSH configuration
- Plugin crashes: Check Steam Deck logs
