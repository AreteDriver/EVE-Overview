# EVE Overview - Technical Documentation

## Architecture Overview

### Component Hierarchy

```
EVE Overview
├── Main Application (main.py)
│   └── Qt Application with dark theme
├── Core Components (core/)
│   ├── WindowCapture: X11 window capture
│   ├── HotkeyManager: Global keyboard shortcuts
│   └── ConfigManager: Profile & settings persistence
└── UI Components (ui/)
    ├── MainWindow: Control interface
    └── PreviewFrame: Draggable preview widgets
```

### Data Flow

```
User Action → MainWindow → Core Components → System
                ↓                 ↓
         PreviewFrame ← WindowCapture → X11
                ↓
         Update Display
```

## Core Components

### 1. WindowCapture (window_capture.py)

**Purpose**: Interface with X11 for window enumeration and capture

**Key Methods**:
- `get_window_list()`: Enumerate all windows
- `capture_window(window_id, scale)`: Capture window screenshot
- `activate_window(window_id)`: Focus a window

**System Dependencies**:
- `wmctrl`: Window management
- `xdotool`: Window control (fallback)
- `import` (ImageMagick): Screenshot capture
- `xwd` + `convert`: Screenshot capture (fallback)

**Implementation Details**:
- Uses subprocess for system tool execution
- Implements fallback chains for reliability
- Converts images to PIL format for Qt display
- Supports both hex (wmctrl) and decimal (xdotool) window IDs

### 2. HotkeyManager (hotkey_manager.py)

**Purpose**: Register and manage global keyboard shortcuts

**Key Methods**:
- `register_hotkey(name, combo, callback)`: Register new hotkey
- `unregister_hotkey(name)`: Remove hotkey
- `parse_key_combo(combo_string)`: Convert human-readable to pynput format
- `format_key_combo(pynput_combo)`: Convert pynput format to human-readable

**Implementation Details**:
- Uses `pynput` for global hotkey detection
- Signals emitted via Qt when hotkeys triggered
- Automatic listener restart when hotkeys change
- Proper closure handling for callback references

**Supported Key Formats**:
```python
# Human readable
"Ctrl+Alt+1"
"Ctrl+Shift+F1"
"Super+A"

# pynput format (internal)
"<ctrl>+<alt>+1"
"<ctrl>+<shift>+<f1>"
"<cmd>+a"
```

### 3. ConfigManager (config_manager.py)

**Purpose**: Persist profiles and application settings

**Key Methods**:
- `load_profile(name)`: Load profile from disk
- `save_profile(profile)`: Save profile to disk
- `delete_profile(name)`: Remove profile
- `list_profiles()`: Get all profile names
- `get_current_profile()`: Get active profile
- `set_current_profile(name)`: Switch active profile

**Storage Structure**:
```
~/.config/eve-overview/
├── config.json          # Main settings
├── eve-overview.log     # Application log
└── profiles/            # Profile storage
    ├── Default.json
    ├── Gaming.json
    └── Development.json
```

**Profile Format**:
```json
{
  "name": "Gaming",
  "windows": [
    {
      "window_id": "0x3200001",
      "window_title": "EVE Online",
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

## UI Components

### 1. MainWindow (main_window.py)

**Purpose**: Primary control interface

**Sections**:
1. **Profile Management**: Create, load, save, delete profiles
2. **Settings**: Refresh rate, always-on-top
3. **Window List**: Available windows to monitor
4. **Active Previews**: Currently monitored windows

**Key Features**:
- Auto-refresh window list every 5 seconds
- Double-click to add/edit
- Right-click preview to close
- Automatic profile saving on close

**Signal Connections**:
```python
preview.closed → _on_preview_closed()
preview.activated → _on_preview_activated()
preview.geometry_changed → (auto-save trigger)
```

### 2. PreviewFrame (preview_frame.py)

**Purpose**: Individual window preview widget

**Features**:
- Frameless, always-on-top window
- Draggable title bar
- Resizable via size grip
- Click to activate source window
- Right-click to close
- Auto-update timer

**Layout**:
```
┌─────────────────────────┐
│ Window Title (draggable)│
├─────────────────────────┤
│                         │
│   Preview Image         │
│                         │
│                    [≡]  │ ← Size grip
└─────────────────────────┘
```

**Update Mechanism**:
```python
Timer (30 FPS) → request_update() 
              → capture_window() 
              → update_preview(image)
              → display
```

## Performance Considerations

### Optimization Strategies

1. **Configurable Refresh Rate**
   - Default: 30 FPS
   - Low CPU: 10-15 FPS
   - Smooth: 60 FPS
   - Impact: Linear with number of previews

2. **Image Scaling**
   - Capture at reduced resolution
   - Default scale: 0.3 (30%)
   - Reduces capture time and memory

3. **Capture Timeout**
   - 1 second timeout per capture
   - Prevents hanging on problematic windows
   - Graceful degradation on failures

4. **Lazy Updates**
   - Only update visible previews
   - Stop updates when minimized
   - Resume on show

### Resource Usage

**Per Preview** (at 30 FPS, 0.3 scale):
- CPU: 2-5%
- Memory: 50-100 MB
- Disk I/O: Minimal (config saves only)

**Recommended Limits**:
- 1-5 previews: Excellent performance
- 6-10 previews: Good performance
- 11+ previews: Consider reducing FPS or scale

## Kaizen Principles Applied

### 1. Minimize Friction
- One-click window addition
- Auto-save on changes
- Persistent layouts
- Smart defaults

### 2. Iterative Refinement
- Multiple fallback capture methods
- Graceful error handling
- Progressive feature loading
- Modular architecture

### 3. User Experience
- Dark theme reduces eye strain
- Visual feedback for all actions
- Intuitive drag-and-drop
- Clear status indicators

### 4. Continuous Improvement
- Extensible architecture
- Plugin-ready design
- Configuration flexibility
- Profile system for iteration

## Security Considerations

### Input Validation
- Window IDs validated before use
- File paths sanitized
- JSON parsing with error handling
- Subprocess timeouts enforced

### Process Isolation
- No elevated privileges required
- Sandboxed subprocess execution
- Read-only window capture
- User-space only operations

### Data Protection
- Local-only storage
- No network communication
- No sensitive data in logs
- User-controlled config location

## Extension Points

### Adding New Capture Methods

```python
class WindowCapture:
    def capture_window(self, window_id, scale):
        # Try new method
        result = self._capture_new_method(window_id, scale)
        if result:
            return result
        
        # Fallback to existing methods
        return self._capture_window_xwd(window_id, scale)
```

### Adding New Hotkey Modifiers

```python
class HotkeyManager:
    def parse_key_combo(self, combo_string):
        key_map = {
            'ctrl': '<ctrl>',
            'newmod': '<newmod>',  # Add here
        }
        # ... rest of implementation
```

### Adding Profile Export/Import

```python
class ConfigManager:
    def export_profile(self, profile_name, export_path):
        profile = self.load_profile(profile_name)
        with open(export_path, 'w') as f:
            json.dump(profile.to_dict(), f)
    
    def import_profile(self, import_path):
        with open(import_path, 'r') as f:
            data = json.load(f)
            profile = Profile.from_dict(data)
            self.save_profile(profile)
```

## Testing Strategy

### Unit Tests
- Component import verification
- Configuration save/load cycles
- Hotkey parsing logic
- Window ID format handling

### Integration Tests
- Profile switching
- Multi-window capture
- Hotkey registration
- UI signal connections

### Manual Testing
- Window drag/resize
- Hotkey activation
- Profile persistence
- System tool availability

## Troubleshooting Guide

### Common Issues and Solutions

**Issue**: Preview not updating
- **Cause**: Window minimized or destroyed
- **Solution**: Check window existence, refresh window list

**Issue**: Hotkey not working
- **Cause**: Conflict with system hotkey
- **Solution**: Try different key combination

**Issue**: High CPU usage
- **Cause**: Too many previews or high FPS
- **Solution**: Reduce refresh rate or preview count

**Issue**: Black preview
- **Cause**: Application blocks screen capture
- **Solution**: Some apps (DRM content) can't be captured

### Debug Logging

Enable debug output:
```python
# In main.py
logging.basicConfig(level=logging.DEBUG)
```

Log location: `~/.config/eve-overview/eve-overview.log`

## Future Enhancements

### Planned Features
1. Click-through mode
2. Grid auto-arrangement
3. Window grouping
4. Wayland native support
5. Plugin system

### Architecture Changes Needed
- Abstraction layer for display server (X11/Wayland)
- Plugin manager for extensions
- Event system for inter-component communication
- Theme engine for customization

---

**Version**: 1.0.0  
**Last Updated**: 2024-12-10  
**Maintainer**: EVE Overview Contributors
