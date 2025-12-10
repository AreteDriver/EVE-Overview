# Example Profiles

This directory contains example profile configurations for EVE Overview.

## Using Example Profiles

1. Copy the desired example to your profiles directory:
   ```bash
   cp examples/Gaming.json ~/.config/eve-overview/profiles/
   ```

2. Launch EVE Overview and select the profile from the dropdown

3. Update window IDs to match your actual windows:
   - Click "Refresh Window List"
   - Note the window IDs (shown in brackets)
   - Edit the profile JSON file with correct IDs
   - Reload the profile

## Available Examples

### Gaming.json
Perfect for multi-account gaming (EVE Online, etc.)
- 3 game client windows
- Arranged vertically on second monitor
- Hotkeys: Ctrl+Alt+1, 2, 3
- 30 FPS for smooth updates

### Development.json
Ideal for monitoring development processes
- Terminal window
- Log viewer
- Application output
- Hotkeys: Ctrl+Alt+T, L, O
- 20 FPS for reduced CPU usage

## Creating Custom Profiles

1. Start EVE Overview
2. Add windows you want to monitor
3. Arrange them as desired
4. Set up hotkeys
5. Save with a custom name
6. Profile saved to `~/.config/eve-overview/profiles/`

## Profile Structure

```json
{
  "name": "ProfileName",
  "windows": [
    {
      "window_id": "0x123456",      // X11 window ID
      "window_title": "Window Name", // Display title
      "x": 100,                      // X position
      "y": 100,                      // Y position
      "width": 400,                  // Width in pixels
      "height": 300,                 // Height in pixels
      "scale": 0.3,                  // Scale factor (0.1-1.0)
      "hotkey": "<ctrl>+<alt>+1",   // Global hotkey
      "enabled": true                // Active/inactive
    }
  ],
  "refresh_rate": 30,                // FPS (1-60)
  "always_on_top": true,             // Keep previews on top
  "click_through": false             // (Future feature)
}
```

## Tips

- Start with low refresh rates (15-20 FPS) and increase if needed
- Use smaller scale factors (0.2-0.3) for better performance
- Assign logical hotkeys (sequential numbers for related windows)
- Test layouts before saving to avoid overlapping windows

## Sharing Profiles

To share a profile:
1. Export from `~/.config/eve-overview/profiles/`
2. Edit to remove personal window IDs
3. Share the JSON file

To use a shared profile:
1. Copy to `~/.config/eve-overview/profiles/`
2. Update window IDs to match your system
3. Load in EVE Overview
