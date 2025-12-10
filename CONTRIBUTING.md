# Contributing to EVE Overview

Thank you for your interest in contributing to EVE Overview! This document provides guidelines and information for contributors.

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Linux with X11 (Wayland support planned)
- Git
- System dependencies: wmctrl, xdotool, ImageMagick, x11-apps

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/EVE-Overview.git
   cd EVE-Overview
   ```

2. **Set Up Development Environment**
   ```bash
   ./setup.sh
   source venv/bin/activate
   ```

3. **Verify Installation**
   ```bash
   python test_components.py
   ```

## Development Workflow

### Making Changes

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Follow the existing code style
   - Add docstrings to new functions/classes
   - Update documentation as needed

3. **Test Your Changes**
   ```bash
   # Run component tests
   python test_components.py
   
   # Test the application
   python src/main.py
   ```

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Description of changes"
   ```

5. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Style Guidelines

### Python Style
- Follow PEP 8
- Use type hints where possible
- Maximum line length: 100 characters
- Use meaningful variable names

**Example**:
```python
def capture_window(self, window_id: str, scale: float = 1.0) -> Optional[Image.Image]:
    """Capture a window by its ID
    
    Args:
        window_id: X11 window ID
        scale: Scale factor for the captured image
        
    Returns:
        PIL Image or None if capture failed
    """
    # Implementation
```

### Documentation
- Add docstrings to all public methods
- Use Google-style docstrings
- Keep README and documentation up to date
- Add inline comments for complex logic

### Qt/PySide6
- Use signals for inter-component communication
- Keep UI and logic separated
- Follow Qt naming conventions
- Use layouts instead of absolute positioning

## Project Structure

```
EVE-Overview/
├── src/
│   ├── main.py                 # Entry point
│   └── eve_overview/
│       ├── core/               # Core functionality
│       │   ├── window_capture.py
│       │   ├── hotkey_manager.py
│       │   └── config_manager.py
│       ├── ui/                 # UI components
│       │   ├── main_window.py
│       │   └── preview_frame.py
│       └── utils/              # Utility functions
├── requirements.txt
├── setup.sh
└── test_components.py
```

## Adding Features

### New Capture Method

1. Add method to `WindowCapture` class
2. Implement fallback chain
3. Add error handling
4. Test with various window types

### New UI Component

1. Create new file in `ui/` directory
2. Inherit from appropriate Qt widget
3. Use signals for communication
4. Add to main window as needed

### New Configuration Option

1. Add to `Profile` or `WindowConfig` dataclass
2. Update `to_dict()` and `from_dict()` methods
3. Add UI controls in `MainWindow`
4. Test save/load cycle

## Testing

### Component Tests

Run existing tests:
```bash
python test_components.py
```

### Manual Testing Checklist

- [ ] Window capture works with multiple window types
- [ ] Hotkeys register and activate correctly
- [ ] Profiles save and load without errors
- [ ] Preview frames are draggable and resizable
- [ ] Application starts without errors
- [ ] Configuration persists between runs

### Testing on Different Environments

Please test on:
- Different Linux distributions (Ubuntu, Fedora, Arch)
- Different desktop environments (GNOME, KDE, XFCE)
- X11 and Wayland (with XWayland)

## Reporting Issues

### Bug Reports

Include:
- Operating system and version
- Desktop environment
- Python version
- Steps to reproduce
- Expected vs actual behavior
- Error messages or logs

### Feature Requests

Include:
- Use case description
- Proposed behavior
- Why this would be useful
- Any implementation ideas

## Code Review Process

1. Submit pull request
2. Automated checks run
3. Maintainer reviews code
4. Address feedback if any
5. Merge when approved

### What We Look For

- Code quality and style
- Test coverage
- Documentation updates
- Backward compatibility
- Performance impact

## Areas Needing Help

### High Priority
- [ ] Wayland native support
- [ ] Unit test coverage
- [ ] Performance profiling
- [ ] Additional capture methods

### Medium Priority
- [ ] Click-through mode implementation
- [ ] Grid layout auto-arrangement
- [ ] Profile import/export
- [ ] Theme customization

### Low Priority (Nice to Have)
- [ ] Window grouping
- [ ] Minimized window support
- [ ] Remote window support
- [ ] Custom window filters

## Documentation

### Updating Documentation

When making changes, update:
- README.md - User-facing documentation
- TECHNICAL.md - Architecture and implementation details
- QUICKSTART.md - Getting started guide
- Inline docstrings - Code documentation

### Documentation Style

- Clear and concise
- Examples for complex features
- Screenshots for UI changes
- Code snippets for technical docs

## Community Guidelines

### Be Respectful
- Treat others with respect
- Welcome newcomers
- Provide constructive feedback
- Assume good intentions

### Communication
- Use GitHub issues for bugs and features
- Be clear and specific
- Provide examples
- Follow up on discussions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

- Open an issue for questions
- Check existing issues and documentation
- Reach out to maintainers

## Recognition

Contributors will be recognized in:
- CHANGELOG.md for their contributions
- GitHub contributors page
- Release notes for significant features

---

Thank you for contributing to EVE Overview!
