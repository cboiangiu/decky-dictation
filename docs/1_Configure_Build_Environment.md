# Configuring Your Build Environment

This guide will walk you through setting up your development environment for the Steam Deck Dictation Plugin.

## Prerequisites

### Automated Setup (VSCode)
If you're using VSCode, you can use our pre-configured tasks:
1. Open the command palette (Ctrl+Shift+P)
2. Select "Tasks: Run Task"
3. Select "setup"

### Manual Setup (Recommended)
Follow these steps for a complete understanding of the build environment:

#### Core Dependencies
1. **Node.js and npm**
   ```bash
   sudo pacman -S nodejs-lts-jod npm
   ```

2. **pnpm v9**
   ```bash
   sudo npm i -g pnpm@9
   ```

3. **Docker**
   ```bash
   sudo pacman -S docker
   ```

#### Decky CLI Setup
1. Download the Decky CLI tool:
   ```bash
   curl -L --create-dirs -o "$(pwd)"/cli/decky "https://github.com/SteamDeckHomebrew/cli/releases/latest/download/decky-linux-x86_64"
   ```

2. Make it executable:
   ```bash
   chmod +x "$(pwd)"/cli/decky
   ```

#### Project Dependencies
1. Install project dependencies:
   ```bash
   pnpm i
   ```

2. Update Decky UI library:
   ```bash
   pnpm update @decky/ui --latest
   ```

## Verification
Run the VSCode setup task to verify your installation:
1. Press Ctrl+Shift+P
2. Select "Tasks: Run Task"
3. Choose "setup"

If everything is installed correctly, you'll see messages indicating steps were skipped because components are already installed.

## Troubleshooting
- If Docker fails to start: `sudo systemctl start docker`
- If pnpm installation fails: Clear npm cache with `npm cache clean --force`
- For permission issues: Ensure your user is in the docker group