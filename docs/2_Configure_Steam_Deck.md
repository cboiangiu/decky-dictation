# Configuring Your Steam Deck for Development

This guide covers the necessary steps to prepare your Steam Deck for plugin development and deployment.

## Initial Setup

### Enable Developer Mode
1. Switch to Desktop Mode:
   - Press the STEAM button
   - Select Power
   - Choose "Switch to Desktop"

### Configure SSH Access
1. Open Konsole
2. Set a password for the deck user:
   ```bash
   passwd
   ```
   Remember this password for future use!

3. Enable SSH server:
   ```bash
   sudo systemctl enable sshd --now
   ```

4. Find your Steam Deck's IP address:
   ```bash
   ip addr | grep inet | grep wlan0
   ```

## SSH Key Setup (From Development Machine)

1. Generate SSH key:
   ```bash
   ssh-keygen -t ed25519 -C "Steam Deck" -f ~/.ssh/steamdeck_ed25519
   ```

2. Copy key to Steam Deck:
   ```bash
   ssh-copy-id -i ~/.ssh/steamdeck_ed25519.pub deck@<steam-deck-ip>
   ```

3. Test SSH connection:
   ```bash
   ssh -i ~/.ssh/steamdeck_ed25519 deck@<steam-deck-ip>
   ```

## Security Hardening

1. Disable password authentication:
   ```bash
   sudo nano /etc/ssh/sshd_config
   ```
   Set: `PasswordAuthentication no`

2. Restart SSH service:
   ```bash
   sudo systemctl restart sshd
   ```

## Verification
- Test SSH connection again
- Ensure Decky Loader is installed (see [Decky installation guide](https://wiki.deckbrew.xyz/en/user-guide/install))

## Troubleshooting
- If SSH connection fails, verify the IP address and network connectivity
- For permission issues, ensure the password was set correctly
- If SSH key doesn't work, verify the key was copied correctly

Instructions above from here: 
https://gist.github.com/andygeorge/eee2825fa6446b629745ea92e862593a
https://shendrick.net/Gaming/2022/05/30/sshonsteamdeck.html