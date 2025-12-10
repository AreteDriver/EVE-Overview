# EVE Overview - Linux Multi-Window Preview Tool

A powerful, EVE-O-Preview-style multi-window preview tool built for Linux using Python and PySide6. This application allows you to monitor multiple windows simultaneously with draggable, resizable preview frames, customizable hotkeys, and profile management.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## Features

### Core Functionality
- 🖼️ **Multi-Window Previews**: Display live previews of multiple windows simultaneously
- 🎯 **Low-Latency Capture**: Optimized window capture using X11 tools
- 📐 **Resizable & Draggable**: Freely position and resize preview frames
- ⌨️ **Global Hotkeys**: Activate windows with customizable keyboard shortcuts
- 💾 **Profile Presets**: Save and load different window layouts
- 🎨 **Clean, Modern UI**: Dark-themed interface with Fusion style

### Advanced Features
- 🔄 **Adjustable Refresh Rate**: Control FPS (1-60) for performance tuning
- 🔝 **Always On Top**: Keep previews visible above other windows
- 🎯 **Click to Activate**: Click preview to focus the source window
- 💡 **Smart Window Detection**: Automatically lists available windows
- 🗂️ **Profile Management**: Create, save, and switch between profiles
- ⚙️ **Persistent Settings**: Configurations saved automatically

## Requirements

### System Requirements
- **OS**: Linux (X11 or Wayland with XWayland)
- **Python**: 3.8 or higher
- **Display Server**: X11 (native support)

### System Dependencies
The application requires the following system utilities:

```bash
# Ubuntu/Debian
sudo apt-get install wmctrl xdotool imagemagick x11-apps

# Fedora/RHEL
sudo dnf install wmctrl xdotool ImageMagick xorg-x11-apps

# Arch Linux
sudo pacman -S wmctrl xdotool imagemagick xorg-xwd
```

### Python Dependencies
- PySide6 >= 6.6.0
- python-xlib >= 0.33
- Pillow >= 10.0.0
- pynput >= 1.7.6

## Installation

### From Source

1. **Clone the repository**:
   ```bash
   git clone https://github.com/AreteDriver/EVE-Overview.git
   cd EVE-Overview
   ```

2. **Install system dependencies** (see above)

3. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**:
   ```bash
   python src/main.py
   ```

### Quick Start Script

Create a launcher script:

```bash
#!/bin/bash
cd /path/to/EVE-Overview
source venv/bin/activate
python src/main.py
```

Make it executable:
```bash
chmod +x eve-overview.sh
```

## Usage

### Getting Started

1. **Launch the Application**:
   ```bash
   python src/main.py
   ```

2. **Add Windows to Monitor**:
   - Click "Refresh Window List" to scan for available windows
   - Select a window from the "Available Windows" list
   - Click "Add Selected Window" or double-click the window

3. **Arrange Preview Frames**:
   - Drag preview frames by their title bars
   - Resize using the size grip in the bottom-right corner
   - Right-click a preview to close it

4. **Activate Windows**:
   - Click on a preview frame to activate its source window
   - Set up hotkeys for quick keyboard activation

### Hotkey Configuration

1. Select a preview from the "Active Previews" list
2. Click "Edit Hotkey"
3. Enter a key combination (e.g., `Ctrl+Alt+1`)
4. The hotkey will activate the window when pressed globally

**Supported Key Formats**:
- `Ctrl+Alt+1` through `Ctrl+Alt+9`
- `Ctrl+Shift+F1` through `Ctrl+Shift+F12`
- `Super+1`, `Super+2`, etc.

### Profile Management

**Create a Profile**:
1. Click "New" in the Profile Management section
2. Enter a profile name
3. Add and arrange your windows
4. Click "Save" to save the current layout

**Load a Profile**:
- Select a profile from the dropdown menu
- The layout will be restored automatically

**Delete a Profile**:
- Select the profile to delete
- Click "Delete" (Default profile cannot be deleted)

### Settings

- **Refresh Rate**: Adjust the preview update frequency (1-60 FPS)
- **Always On Top**: Keep preview frames above other windows

## Project Structure

```
EVE-Overview/
├── src/
│   ├── main.py                 # Application entry point
│   └── eve_overview/
│       ├── __init__.py
│       ├── core/               # Core functionality
│       │   ├── window_capture.py    # Window capture system
│       │   ├── hotkey_manager.py    # Global hotkey handling
│       │   └── config_manager.py    # Configuration & profiles
│       ├── ui/                 # User interface
│       │   ├── main_window.py       # Main application window
│       │   └── preview_frame.py     # Preview frame widget
│       └── utils/              # Utility functions
├── requirements.txt            # Python dependencies
├── .gitignore
└── README.md
```

## Configuration

Configuration files are stored in `~/.config/eve-overview/`:

- `config.json`: Main application settings
- `profiles/`: Profile presets (JSON format)
- `eve-overview.log`: Application log file

### Configuration Format

Profiles are stored as JSON files with the following structure:

```json
{
  "name": "Default",
  "windows": [
    {
      "window_id": "0x123456",
      "window_title": "Example Window",
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

## Performance Optimization

### Tips for Best Performance

1. **Adjust Refresh Rate**: Lower FPS for better CPU usage
2. **Scale Factor**: Reduce preview size for faster capture
3. **Limit Previews**: Monitor only essential windows
4. **Window Selection**: Avoid previewing GPU-intensive applications

### System Resources

Typical resource usage:
- **Memory**: 50-100 MB per preview
- **CPU**: 2-5% per preview at 30 FPS
- **Network**: None (local only)

## Troubleshooting

### Common Issues

**"Command not found: wmctrl"**
- Install required system dependencies (see Installation)

**Hotkeys not working**
- Ensure no other application is using the same combination
- Try a different key combination
- Check system permissions for global hotkey access

**Preview not updating**
- Verify the window still exists
- Check if the window is minimized (may not capture)
- Try refreshing the window list

**Black/empty previews**
- Some applications block screen capture
- Try using a different capture tool (xwd vs import)
- Check window permissions

### Debug Mode

Enable debug logging:
```python
# In main.py, change:
logging.basicConfig(level=logging.DEBUG, ...)
```

Check logs at: `~/.config/eve-overview/eve-overview.log`

## Kaizen Improvements

This project follows Kaizen principles for continuous improvement:

### UI/UX Refinements
- ✅ Minimal, clean interface
- ✅ Intuitive drag-and-drop window arrangement
- ✅ One-click window activation
- ✅ Visual feedback for all actions
- ✅ Dark theme reduces eye strain

### Performance Optimizations
- ✅ Configurable refresh rates
- ✅ Efficient window capture caching
- ✅ Minimal memory footprint
- ✅ Fast profile switching

### Workflow Enhancements
- ✅ Quick hotkey setup
- ✅ Profile presets for different tasks
- ✅ Auto-save functionality
- ✅ Persistent window positions

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Acknowledgments

- Inspired by EVE-O-Preview for Windows
- Built with PySide6 (Qt for Python)
- Uses X11 tools for window management

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the troubleshooting section
- Review the configuration documentation

---

**Made with ❤️ for the EVE Online community and Linux users**
