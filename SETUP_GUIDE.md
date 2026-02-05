# Complete PaperMC Minecraft Server Setup Guide

A comprehensive guide to setting up a Minecraft Java server with plugin support using PaperMC on macOS.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Server Setup](#server-setup)
4. [Configuration](#configuration)
5. [Plugin Installation](#plugin-installation)
6. [Network Setup](#network-setup)
7. [Advanced Options](#advanced-options)
8. [Best Practices & Troubleshooting](#best-practices--troubleshooting)

---

## Introduction

**PaperMC** is a high-performance Minecraft server software that supports Spigot and Bukkit plugins. It offers better performance and more features than vanilla Minecraft servers.

### Why PaperMC?
- ✅ Supports Spigot, Bukkit, and Paper plugins
- ✅ Better performance than vanilla servers
- ✅ Active development and community support
- ✅ Built-in optimizations for large servers

---

## Prerequisites

Before starting, ensure you have:

1. **Java 21** (required for Minecraft 1.20.4+)
2. **macOS** with Terminal access
3. **At least 2GB RAM** available (4GB+ recommended)
4. **Stable internet connection**

### Check Java Version

```bash
java -version
```

If Java is not installed or version is too old, install it:

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Java 21
brew install openjdk@21

# Link Java
sudo ln -sfn /opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-21.jdk
```

---

## Server Setup

### Step 1: Create Server Directory

```bash
# Navigate to your Documents folder
cd ~/Documents

# Create server directory
mkdir -p "Server Minecraft"
cd "Server Minecraft"
```

### Step 2: Download PaperMC

Visit [PaperMC Downloads](https://papermc.io/downloads/paper) to find the latest version, or use this command:

```bash
# Download Paper for Minecraft 1.21.4 (latest stable as of Feb 2026)
# Replace version numbers as needed
curl -o paper.jar https://api.papermc.io/v2/projects/paper/versions/1.21.4/builds/latest/downloads/paper-1.21.4-latest.jar
```

> [!TIP]
> To get the latest version URL, visit https://papermc.io/downloads/paper and copy the download link.

### Step 3: Create Start Script

Create a file named `start.sh`:

```bash
cat > start.sh << 'EOF'
#!/bin/bash

# PaperMC Server Start Script
# Adjust RAM allocation as needed

java -Xms2G -Xmx4G -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 \
-XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch \
-XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M \
-XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 \
-XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 \
-XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem \
-XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs \
-Daikars.new.flags=true -jar paper.jar --nogui

echo "Server stopped. Press any key to exit..."
read
EOF

# Make the script executable
chmod +x start.sh
```

> [!IMPORTANT]
> **RAM Allocation Explained:**
> - `-Xms2G`: Minimum RAM (2GB)
> - `-Xmx4G`: Maximum RAM (4GB)
> - Adjust based on your available RAM and player count
> - Recommended: 1GB per 5-10 players

### Step 4: Accept EULA

First run to generate files:

```bash
./start.sh
```

The server will stop and ask you to accept the EULA. Edit the file:

```bash
# Open eula.txt
nano eula.txt
```

Change `eula=false` to `eula=true`, then save (Ctrl+O, Enter, Ctrl+X).

### Step 5: Start the Server

```bash
./start.sh
```

Wait for the message: `Done! For help, type "help"`

The server is now running! Type `stop` to shut it down gracefully.

---

## Configuration

### Server Properties

The `server.properties` file controls server behavior. Here's an optimized configuration:

```bash
# Stop the server first
# Then edit server.properties
nano server.properties
```

**Recommended Settings:**

```properties
# Basic Settings
server-name=My PaperMC Server
motd=§6Welcome to My Server! §ePlaying on PaperMC
server-port=25565
max-players=20
online-mode=true
difficulty=normal
gamemode=survival

# Performance Settings
view-distance=10
simulation-distance=8
max-tick-time=60000
network-compression-threshold=256

# World Settings
level-name=world
level-seed=
allow-nether=true
allow-flight=false
pvp=true
spawn-protection=16
spawn-monsters=true
spawn-animals=true
spawn-npcs=true

# Advanced Settings
enable-command-block=false
enable-rcon=false
white-list=false
enforce-whitelist=false
resource-pack=
resource-pack-sha1=
```

> [!NOTE]
> **Key Settings Explained:**
> - `view-distance`: Lower values improve performance (8-12 recommended)
> - `simulation-distance`: Affects mob spawning and crop growth
> - `online-mode=true`: Requires legitimate Minecraft accounts
> - `white-list`: Enable for private servers

### Paper Configuration

PaperMC has additional config files for advanced optimization:

**config/paper-global.yml** - Global server settings
**config/paper-world-defaults.yml** - Default world settings

These are auto-generated with sensible defaults. Modify only if needed.

---

## Plugin Installation

### Understanding Plugin Compatibility

PaperMC supports plugins from:
- ✅ **Paper** plugins (best performance)
- ✅ **Spigot** plugins (fully compatible)
- ✅ **Bukkit** plugins (fully compatible)
- ❌ **Forge/Fabric** mods (NOT compatible - different system)

### Where to Find Plugins

1. **SpigotMC Resources**: https://www.spigotmc.org/resources/
2. **Bukkit Dev**: https://dev.bukkit.org/
3. **PaperMC Forums**: https://forums.papermc.io/
4. **Hangar (Paper)**: https://hangar.papermc.io/

> [!WARNING]
> Only download plugins from trusted sources. Malicious plugins can compromise your server.

### Installing Plugins

#### Step 1: Create Plugins Folder

The `plugins/` folder is auto-created on first run. If not:

```bash
mkdir -p plugins
```

#### Step 2: Download Plugin JAR Files

Download `.jar` files from trusted sources and place them in the `plugins/` folder.

```bash
# Example: Download to plugins folder
cd plugins
# Download your plugin .jar here
cd ..
```

#### Step 3: Restart Server

```bash
# Stop server (type 'stop' in console)
# Then start again
./start.sh
```

Plugins load automatically on startup.

### Essential Plugins Examples

#### 1. EssentialsX (Core Commands & Features)

**Download**: https://essentialsx.net/downloads.html

```bash
cd plugins
# Download EssentialsX, EssentialsXChat, EssentialsXSpawn
curl -L -o EssentialsX.jar "https://github.com/EssentialsX/Essentials/releases/latest/download/EssentialsX-2.20.1.jar"
curl -L -o EssentialsXChat.jar "https://github.com/EssentialsX/Essentials/releases/latest/download/EssentialsXChat-2.20.1.jar"
curl -L -o EssentialsXSpawn.jar "https://github.com/EssentialsX/Essentials/releases/latest/download/EssentialsXSpawn-2.20.1.jar"
cd ..
```

**Configuration** (`plugins/Essentials/config.yml`):

```yaml
# Example Essentials config snippet
nickname-prefix: '~'
max-nick-length: 15
ignore-colors-in-max-nick-length: false
currency-symbol: '$'
starting-balance: 100
command-costs:
  sethome: 0
  home: 0
teleport-cooldown: 5
teleport-delay: 3
```

#### 2. LuckPerms (Permissions Management)

**Download**: https://luckperms.net/download

```bash
cd plugins
curl -L -o LuckPerms.jar "https://download.luckperms.net/1556/bukkit/loader/LuckPerms-Bukkit-5.4.141.jar"
cd ..
```

**Basic Commands**:

```bash
# In-game or console commands
lp user <player> permission set essentials.home true
lp group admin create
lp group admin permission set * true
lp user <player> parent add admin
```

**Configuration** (`plugins/LuckPerms/config.yml`):

```yaml
# Storage method (h2, mysql, mariadb, postgresql, mongodb, sqlite)
storage-method: h2

# Server name (for multi-server setups)
server: global

# Sync interval (minutes)
sync-minutes: 3

# Web editor
web-editor-url-pattern: 'https://editor.luckperms.net/'
```

#### 3. WorldEdit (World Editing Tool)

```bash
cd plugins
curl -L -o WorldEdit.jar "https://dev.bukkit.org/projects/worldedit/files/latest"
cd ..
```

#### 4. Vault (Economy API - Required by many plugins)

```bash
cd plugins
curl -L -o Vault.jar "https://github.com/MilkBowl/Vault/releases/download/1.7.3/Vault.jar"
cd ..
```

### Managing Plugins

#### List Installed Plugins

In server console:
```
plugins
```

#### Reload Plugins

```
# Reload all plugins (use cautiously)
reload confirm

# Reload specific plugin (if supported)
essentials reload
```

> [!CAUTION]
> Using `/reload` can cause issues. Restart the server instead when possible.

#### Remove Plugins

1. Stop the server
2. Delete the plugin `.jar` from `plugins/` folder
3. Optionally delete the plugin's data folder
4. Start the server

```bash
# Example: Remove EssentialsX
rm plugins/EssentialsX.jar
rm -rf plugins/Essentials/
```

### Troubleshooting Plugin Issues

#### Plugin Not Loading

1. **Check console for errors** during startup
2. **Verify compatibility**: Check plugin page for supported Minecraft versions
3. **Check dependencies**: Some plugins require others (e.g., Vault)
4. **File permissions**: Ensure `.jar` files are readable

```bash
# Fix permissions
chmod 644 plugins/*.jar
```

#### Plugin Errors

Common issues:
- **Missing dependencies**: Install required plugins
- **Outdated plugin**: Update to latest version
- **Config errors**: Check YAML syntax (no tabs, proper spacing)
- **Conflicts**: Two plugins trying to do the same thing

**Check logs**:
```bash
# View latest log
tail -f logs/latest.log

# Search for errors
grep ERROR logs/latest.log
```

---

## Network Setup

### Finding Your Local IP

```bash
# Get local IP address
ipconfig getifaddr en0
# or
ifconfig | grep "inet " | grep -v 127.0.0.1
```

### Finding Your Public IP

```bash
# Get public IP
curl ifconfig.me
# or
curl icanhazip.com
```

### Port Forwarding

To allow friends to connect, you must forward port **25565** on your router.

#### General Steps:

1. **Access Router Admin Panel**
   - Open browser to `192.168.1.1` or `192.168.0.1`
   - Login (check router label for credentials)

2. **Find Port Forwarding Section**
   - Usually under: Advanced → Port Forwarding, NAT, or Virtual Servers

3. **Create Port Forward Rule**
   - **Service Name**: Minecraft Server
   - **External Port**: 25565
   - **Internal Port**: 25565
   - **Internal IP**: Your Mac's local IP (from above)
   - **Protocol**: TCP/UDP or Both

4. **Save and Restart Router** (if required)

> [!IMPORTANT]
> **Security Note**: Port forwarding exposes your server to the internet. Use a strong whitelist and keep plugins updated.

#### Router-Specific Guides:

- **Netgear**: Advanced → Advanced Setup → Port Forwarding
- **TP-Link**: Advanced → NAT Forwarding → Virtual Servers
- **Linksys**: Security → Apps and Gaming → Port Range Forwarding
- **ASUS**: WAN → Virtual Server / Port Forwarding

### Connecting to Your Server

#### Local Network (Same WiFi):
```
<local-ip>:25565
Example: 192.168.1.100:25565
```

#### Internet (Friends):
```
<public-ip>:25565
Example: 203.0.113.45:25565
```

> [!TIP]
> If using default port 25565, players can omit `:25565` and just use the IP.

### Testing Connectivity

Use online tools to verify port forwarding:
- https://mcsrvstat.us/
- https://www.yougetsignal.com/tools/open-ports/

---

## Advanced Options

### Dynamic DNS (DDNS)

Your public IP may change. DDNS provides a stable hostname.

#### Popular Free DDNS Services:
- **No-IP**: https://www.noip.com/
- **DuckDNS**: https://www.duckdns.org/
- **Dynu**: https://www.dynu.com/

#### Setup Example (DuckDNS):

1. Create account at https://www.duckdns.org/
2. Create a domain (e.g., `myminecraft.duckdns.org`)
3. Install update client on your Mac:

```bash
# Create update script
mkdir -p ~/duckdns
cd ~/duckdns
echo "echo url=\"https://www.duckdns.org/update?domains=myminecraft&token=YOUR_TOKEN&ip=\" | curl -k -o ~/duckdns/duck.log -K -" > duck.sh
chmod +x duck.sh

# Test it
./duck.sh

# Add to crontab for auto-updates
crontab -e
# Add this line:
*/5 * * * * ~/duckdns/duck.sh >/dev/null 2>&1
```

Players can now connect using: `myminecraft.duckdns.org`

### Running Server in Background

#### Option 1: Using `screen`

```bash
# Install screen
brew install screen

# Start server in screen session
screen -S minecraft
./start.sh

# Detach: Press Ctrl+A, then D
# Reattach: screen -r minecraft
# List sessions: screen -ls
```

#### Option 2: Using `tmux`

```bash
# Install tmux
brew install tmux

# Start server in tmux session
tmux new -s minecraft
./start.sh

# Detach: Press Ctrl+B, then D
# Reattach: tmux attach -t minecraft
# List sessions: tmux ls
```

#### Option 3: Create Launch Agent (Auto-start on boot)

Create `~/Library/LaunchAgents/com.minecraft.server.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.minecraft.server</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/YOUR_USERNAME/Documents/Server Minecraft/start.sh</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/YOUR_USERNAME/Documents/Server Minecraft</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/YOUR_USERNAME/Documents/Server Minecraft/logs/stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/YOUR_USERNAME/Documents/Server Minecraft/logs/stderr.log</string>
</dict>
</plist>
```

Load it:
```bash
launchctl load ~/Library/LaunchAgents/com.minecraft.server.plist
```

### Backup Strategy

Regular backups are essential!

```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="$HOME/Documents/Server Minecraft/backups"
DATE=$(date +%Y-%m-%d_%H-%M-%S)
SERVER_DIR="$HOME/Documents/Server Minecraft"

mkdir -p "$BACKUP_DIR"

# Backup world and plugins
tar -czf "$BACKUP_DIR/backup_$DATE.tar.gz" \
    -C "$SERVER_DIR" \
    world world_nether world_the_end plugins server.properties

echo "Backup created: backup_$DATE.tar.gz"

# Keep only last 7 backups
cd "$BACKUP_DIR"
ls -t backup_*.tar.gz | tail -n +8 | xargs rm -f
EOF

chmod +x backup.sh

# Run backup
./backup.sh

# Schedule daily backups (add to crontab)
crontab -e
# Add: 0 3 * * * /Users/YOUR_USERNAME/Documents/Server\ Minecraft/backup.sh
```

---

## Best Practices & Troubleshooting

### Best Practices

1. **Regular Updates**
   - Update PaperMC regularly for security and performance
   - Update plugins to match server version
   - Backup before updating

2. **Performance Optimization**
   - Use Aikar's flags (included in start script)
   - Lower view-distance for better performance
   - Use Paper's optimizations in config files
   - Monitor TPS (ticks per second) - should be 20

3. **Security**
   - Enable whitelist for private servers
   - Use strong operator passwords
   - Keep plugins minimal (only what you need)
   - Regular backups
   - Monitor logs for suspicious activity

4. **Player Management**
   - Use LuckPerms for permissions
   - Set up ranks and groups
   - Create spawn protection
   - Configure anti-grief plugins

### Common Issues & Solutions

#### Server Won't Start

**Symptom**: Server crashes immediately or won't start

**Solutions**:
```bash
# Check Java version
java -version  # Should be 21+

# Check for port conflicts
lsof -i :25565

# Review error logs
cat logs/latest.log

# Reduce RAM if insufficient
# Edit start.sh: Change -Xmx4G to -Xmx2G
```

#### Low TPS / Lag

**Symptom**: Server running slowly, TPS below 20

**Solutions**:
- Reduce `view-distance` in server.properties
- Limit entity spawning in paper-world-defaults.yml
- Remove laggy plugins
- Allocate more RAM
- Use `/timings` command to identify lag sources

```bash
# In-game command
/timings on
# Wait a few minutes
/timings paste
# Share the URL to analyze lag
```

#### Players Can't Connect

**Symptom**: "Connection timed out" or "Unable to connect"

**Solutions**:
1. Verify server is running
2. Check port forwarding is correct
3. Verify firewall isn't blocking
4. Test with local IP first
5. Confirm public IP is current

```bash
# Allow through macOS firewall
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/bin/java
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --unblockapp /usr/bin/java
```

#### Plugin Conflicts

**Symptom**: Plugins not working, errors in console

**Solutions**:
1. Remove plugins one by one to identify conflict
2. Check plugin compatibility
3. Update all plugins
4. Read plugin documentation for known conflicts

#### Out of Memory Errors

**Symptom**: `java.lang.OutOfMemoryError`

**Solutions**:
```bash
# Increase max RAM in start.sh
# Change -Xmx4G to -Xmx6G or higher
nano start.sh

# Monitor memory usage
# In-game: /tps or /memory (if plugin installed)
```

### Useful Commands

#### Server Console Commands

```bash
# Player management
op <player>              # Give operator status
deop <player>            # Remove operator status
whitelist add <player>   # Add to whitelist
whitelist remove <player> # Remove from whitelist
ban <player>             # Ban player
pardon <player>          # Unban player

# Server management
stop                     # Stop server gracefully
save-all                 # Save world data
save-off                 # Disable auto-save
save-on                  # Enable auto-save
list                     # List online players
difficulty <level>       # Change difficulty
gamemode <mode> <player> # Change gamemode

# Performance
tps                      # Check server TPS (if plugin installed)
timings                  # Performance profiling
```

#### Essential EssentialsX Commands

```bash
/spawn                   # Teleport to spawn
/sethome <name>          # Set home location
/home <name>             # Teleport to home
/tpa <player>            # Request teleport
/tpaccept                # Accept teleport request
/warp <name>             # Teleport to warp
/setwarp <name>          # Create warp point
```

### Performance Monitoring

Monitor your server's health:

```bash
# Check TPS in-game (requires plugin)
/tps

# View timings report
/timings paste

# Monitor system resources
# In separate terminal:
top -pid $(pgrep -f paper.jar)
```

### Getting Help

- **PaperMC Docs**: https://docs.papermc.io/
- **PaperMC Discord**: https://discord.gg/papermc
- **SpigotMC Forums**: https://www.spigotmc.org/forums/
- **r/admincraft**: https://reddit.com/r/admincraft

---

## Quick Reference

### File Structure

```
Server Minecraft/
├── paper.jar                 # Server software
├── start.sh                  # Start script
├── eula.txt                  # EULA agreement
├── server.properties         # Main config
├── bukkit.yml               # Bukkit config
├── spigot.yml               # Spigot config
├── config/
│   ├── paper-global.yml     # Paper global config
│   └── paper-world-defaults.yml
├── plugins/                 # Plugin folder
│   ├── PluginName.jar
│   └── PluginName/          # Plugin data
├── world/                   # Overworld
├── world_nether/            # Nether
├── world_the_end/           # End
├── logs/                    # Server logs
└── backups/                 # Backups (create this)
```

### RAM Recommendations

| Players | Minimum RAM | Recommended RAM |
|---------|-------------|-----------------|
| 1-5     | 2GB         | 3GB            |
| 5-10    | 3GB         | 4GB            |
| 10-20   | 4GB         | 6GB            |
| 20-50   | 6GB         | 8GB            |
| 50+     | 8GB+        | 12GB+          |

### Port Reference

| Service | Port  | Protocol |
|---------|-------|----------|
| Minecraft | 25565 | TCP/UDP |
| RCON    | 25575 | TCP     |
| Query   | 25565 | UDP     |

---

## Conclusion

You now have a fully functional PaperMC server with plugin support! 

**Next Steps:**
1. Install your favorite plugins
2. Configure permissions with LuckPerms
3. Set up port forwarding
4. Invite friends to play
5. Regular backups and updates

**Remember:**
- Keep your server updated
- Backup regularly
- Monitor performance
- Have fun!

Happy crafting! 🎮⛏️
