# Building the Steam Deck Dictation Plugin

This guide covers the process of building the plugin for deployment.

## Automated Build (VSCode)
The simplest method is using VSCode's built-in task:
1. Open Command Palette (Ctrl+Shift+P)
2. Select "Tasks: Run Task"
3. Choose "Build Plugin"

## Manual Build Process

### Prerequisites
1. Ensure Docker is running:
   ```bash
   sudo systemctl start docker
   ```

2. Configure VSCode settings:
   ```bash
   cp .vscode/settings.default.json .vscode/settings.json
   ```

### Build Steps
1. Build the plugin:
   ```bash
   sudo ./cli/decky plugin build $(pwd)
   ```

The build process:
1. Builds backend components in Docker
2. Compiles frontend TypeScript/React code
3. Packages everything into a distributable zip

### Build Output
- Backend files: `backend/out/`
- Frontend files: `dist/`
- Final plugin: `out/`

## Build Configuration
- Backend configuration: `backend/src/`
- Frontend configuration: `tsconfig.json`
- Build settings: `rollup.config.js`

## Troubleshooting
- If Docker fails: Check Docker service status
- For build errors: Check logs in `build.log`
- For TypeScript errors: Review `tsconfig.json`