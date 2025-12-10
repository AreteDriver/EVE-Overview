# Changelog

All notable changes to EVE Overview will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-10

### Added
- Initial release of EVE Overview for Linux
- Multi-window preview system with live capture
- Draggable and resizable preview frames
- Global hotkey system for window activation
- Profile management (create, save, load, delete)
- Configuration persistence
- Adjustable refresh rate (1-60 FPS)
- Always-on-top window mode
- Click-to-activate functionality
- Window list auto-refresh
- Dark theme UI with Fusion style
- Comprehensive documentation
- Setup automation script
- Component testing suite
- Desktop entry for system integration

### Core Features
- **Window Capture**: X11-based window capture using wmctrl, xdotool, and ImageMagick
- **Hotkey Manager**: Global keyboard shortcuts using pynput
- **Config Manager**: JSON-based profile and settings storage
- **Preview Frames**: Custom Qt widgets with drag, resize, and click support
- **Main Window**: Complete control interface for managing previews

### Documentation
- README with full installation and usage guide
- QUICKSTART guide for new users
- Example configurations
- Troubleshooting section
- Performance optimization tips

### Performance
- Low-latency window capture
- Configurable refresh rates
- Efficient memory usage
- Optimized for multi-window scenarios

### Kaizen Improvements
- Clean, minimal UI design
- Intuitive drag-and-drop interface
- One-click window activation
- Visual feedback for all actions
- Auto-save on profile changes
- Persistent window positions

### Dependencies
- PySide6 >= 6.6.0 (Qt for Python)
- python-xlib >= 0.33 (X11 bindings)
- Pillow >= 10.0.0 (Image processing)
- pynput >= 1.7.6 (Global hotkeys)

### System Requirements
- Linux with X11 or Wayland/XWayland
- Python 3.8 or higher
- wmctrl, xdotool, ImageMagick, x11-apps

---

## Future Enhancements (Roadmap)

### Planned for v1.1.0
- [ ] Click-through mode (interact with windows through previews)
- [ ] Custom opacity settings for previews
- [ ] Grid layout auto-arrangement
- [ ] Import/export profiles
- [ ] Thumbnail/icon view mode
- [ ] Window grouping by application
- [ ] Minimized window support
- [ ] Screenshot capability

### Planned for v1.2.0
- [ ] Wayland native support (without X11)
- [ ] Multi-monitor awareness
- [ ] Window filters and search
- [ ] Custom themes/styling
- [ ] Plugins/extensions system
- [ ] Remote window support
- [ ] Performance statistics
- [ ] Notification integration

### Community Requests
- Submit feature requests via GitHub Issues
- Vote on proposed features
- Contribute code via Pull Requests

---

## Version History

- **1.0.0** (2024-12-10): Initial release

---

For detailed changes and commits, see the [Git history](https://github.com/AreteDriver/EVE-Overview/commits/).
