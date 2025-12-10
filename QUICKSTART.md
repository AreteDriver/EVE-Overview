# Quick Start Guide

## Installation

### 1. Install System Dependencies

```bash
# Ubuntu/Debian
sudo apt-get install wmctrl xdotool imagemagick x11-apps

# Fedora/RHEL
sudo dnf install wmctrl xdotool ImageMagick xorg-x11-apps

# Arch Linux
sudo pacman -S wmctrl xdotool imagemagick xorg-xwd
```

### 2. Run Setup

```bash
./setup.sh
```

This will:
- Check Python version (3.8+)
- Verify system dependencies
- Create a virtual environment
- Install Python packages
- Create a launcher script

### 3. Launch the Application

```bash
./eve-overview.sh
```

Or manually:
```bash
source venv/bin/activate
python src/main.py
```

## First-Time Setup

### Step 1: Add Windows

1. Click "Refresh Window List"
2. Select a window from the list
3. Click "Add Selected Window" or double-click

### Step 2: Arrange Previews

- **Move**: Drag the title bar
- **Resize**: Drag the bottom-right corner
- **Close**: Right-click the preview

### Step 3: Set Hotkeys

1. Select a preview from "Active Previews"
2. Click "Edit Hotkey"
3. Enter a key combination (e.g., `Ctrl+Alt+1`)
4. Press anywhere to activate the window using the hotkey

### Step 4: Save Your Layout

1. Click "Save" to save the current profile
2. Or click "New" to create a new profile with a custom name

## Common Use Cases

### Gaming (EVE Online, Multi-Window Games)

1. Launch all game clients
2. Add each client window to EVE Overview
3. Arrange previews on a second monitor or edge of screen
4. Set hotkeys `Ctrl+Alt+1`, `Ctrl+Alt+2`, etc.
5. Save as "Gaming" profile

### Development/Monitoring

1. Add terminal, log viewer, and application windows
2. Arrange in a monitoring layout
3. Set refresh rate to 15-20 FPS for lower CPU usage
4. Save as "Development" profile

### Video Production

1. Add preview windows for different cameras/sources
2. Arrange in grid layout
3. Use hotkeys to quickly switch between sources
4. Save as "Video Production" profile

## Keyboard Shortcuts

### Global Hotkeys (Customizable)
- `Ctrl+Alt+1-9`: Activate windows 1-9
- `Ctrl+Shift+F1-F12`: Activate windows using function keys

### Application Controls
- **Double-click window**: Add to previews
- **Double-click preview**: Edit hotkey
- **Right-click preview**: Close preview
- **Left-click preview**: Activate source window

## Performance Tips

### Optimize Refresh Rate
- **Low CPU**: 10-15 FPS
- **Balanced**: 20-30 FPS (default)
- **Smooth**: 40-60 FPS

### Reduce Preview Size
- Smaller previews = less data to capture
- Use resize grip to find optimal size

### Limit Active Previews
- Only monitor windows you need
- Close unused previews

## Troubleshooting

### Preview Not Updating
```bash
# Check if window still exists
wmctrl -l

# Refresh window list in application
```

### Hotkey Not Working
- Try a different key combination
- Check if another app uses the same hotkey
- Restart the application

### Black/Empty Preview
- Some apps block screen capture
- Try minimizing/restoring the window
- Check window permissions

### High CPU Usage
- Reduce refresh rate
- Reduce number of active previews
- Check for GPU-intensive source windows

## Advanced Configuration

### Manual Profile Editing

Profiles are stored in: `~/.config/eve-overview/profiles/`

Example profile structure:
```json
{
  "name": "MyProfile",
  "windows": [
    {
      "window_id": "0x3200001",
      "window_title": "Terminal",
      "x": 100,
      "y": 100,
      "width": 400,
      "height": 300,
      "scale": 0.3,
      "hotkey": "<ctrl>+<alt>+1",
      "enabled": true
    }
  ],
  "refresh_rate": 30,
  "always_on_top": true,
  "click_through": false
}
```

### Custom Hotkey Format

Use pynput format for custom hotkeys:
- Modifiers: `<ctrl>`, `<alt>`, `<shift>`, `<cmd>`
- Keys: `a-z`, `0-9`, `<f1>`-`<f12>`
- Combine with `+`: `<ctrl>+<alt>+1`

## Tips & Tricks

### Multi-Monitor Setup
1. Move main window to primary monitor
2. Arrange previews on secondary monitor
3. Use "Always On Top" to keep previews visible

### Quick Switching
1. Assign sequential hotkeys (1-9) to your most-used windows
2. Practice the hotkey combinations
3. Muscle memory develops quickly

### Profile per Activity
- Create separate profiles for different activities
- Switch profiles via dropdown
- Each profile remembers window positions and hotkeys

## System Integration

### Desktop Entry

Install desktop entry:
```bash
# Edit paths in eve-overview.desktop
cp eve-overview.desktop ~/.local/share/applications/
```

### Autostart

Add to autostart:
```bash
mkdir -p ~/.config/autostart
cp eve-overview.desktop ~/.config/autostart/
```

## Getting Help

- Check logs: `~/.config/eve-overview/eve-overview.log`
- Run tests: `python test_components.py`
- GitHub Issues: Report bugs or request features

## Next Steps

1. Experiment with different layouts
2. Create profiles for different workflows
3. Customize hotkeys to your preference
4. Fine-tune refresh rates for your system

---

**Enjoy your multi-window preview experience!**
