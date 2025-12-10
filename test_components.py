#!/usr/bin/env python3
"""
Simple test script to verify EVE Overview components
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from eve_overview import __version__
        print(f"✓ eve_overview version {__version__}")
    except ImportError as e:
        print(f"✗ Failed to import eve_overview: {e}")
        return False
    
    try:
        from eve_overview.core.window_capture import WindowCapture
        print("✓ WindowCapture imported")
    except ImportError as e:
        print(f"✗ Failed to import WindowCapture: {e}")
        return False
    
    try:
        from eve_overview.core.hotkey_manager import HotkeyManager
        print("✓ HotkeyManager imported")
    except ImportError as e:
        # Expected to fail without X11
        if "platform is not supported" in str(e) or "DISPLAY" in str(e):
            print("⚠ HotkeyManager requires X11 (skipped in headless environment)")
            return "skip"
        print(f"✗ Failed to import HotkeyManager: {e}")
        return False
    
    try:
        from eve_overview.core.config_manager import ConfigManager, Profile, WindowConfig
        print("✓ ConfigManager imported")
    except ImportError as e:
        print(f"✗ Failed to import ConfigManager: {e}")
        return False
    
    try:
        from eve_overview.ui.preview_frame import PreviewFrame
        print("✓ PreviewFrame imported")
    except ImportError as e:
        print(f"✗ Failed to import PreviewFrame: {e}")
        return False
    
    try:
        from eve_overview.ui.main_window import MainWindow
        print("✓ MainWindow imported")
    except ImportError as e:
        print(f"✗ Failed to import MainWindow: {e}")
        return False
    
    return True


def test_config_manager():
    """Test ConfigManager functionality"""
    print("\nTesting ConfigManager...")
    
    try:
        from eve_overview.core.config_manager import ConfigManager, Profile, WindowConfig
        import tempfile
        
        # Create temporary config directory
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ConfigManager(config_dir=tmpdir)
            
            # Create a test profile
            test_profile = Profile(
                name="Test",
                windows=[
                    WindowConfig(
                        window_id="0x123",
                        window_title="Test Window",
                        x=100, y=100,
                        width=400, height=300
                    )
                ]
            )
            
            # Save profile
            if not config.save_profile(test_profile):
                print("✗ Failed to save profile")
                return False
            
            # Load profile
            loaded = config.load_profile("Test")
            if loaded is None:
                print("✗ Failed to load profile")
                return False
            
            if loaded.name != "Test":
                print("✗ Profile name mismatch")
                return False
            
            if len(loaded.windows) != 1:
                print("✗ Profile windows count mismatch")
                return False
            
            print("✓ ConfigManager working correctly")
            return True
            
    except Exception as e:
        print(f"✗ ConfigManager test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_hotkey_parser():
    """Test hotkey parsing"""
    print("\nTesting HotkeyManager...")
    
    try:
        from eve_overview.core.hotkey_manager import HotkeyManager
        
        manager = HotkeyManager()
        
        # Test parsing
        test_cases = [
            ("Ctrl+Alt+1", "<ctrl>+<alt>+1"),
            ("Ctrl+Shift+F1", "<ctrl>+<shift>+<f1>"),
            ("Super+A", "<cmd>+a"),
        ]
        
        for input_combo, expected in test_cases:
            result = manager.parse_key_combo(input_combo)
            if result != expected:
                print(f"✗ Parse failed: {input_combo} -> {result} (expected {expected})")
                return False
        
        print("✓ HotkeyManager parser working correctly")
        return True
        
    except ImportError as e:
        # Expected to fail without X11
        if "platform is not supported" in str(e) or "DISPLAY" in str(e):
            print("⚠ HotkeyManager requires X11 (skipped in headless environment)")
            return "skip"
        print(f"✗ HotkeyManager test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"✗ HotkeyManager test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("=" * 50)
    print("EVE Overview Component Tests")
    print("=" * 50)
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("ConfigManager", test_config_manager()))
    results.append(("HotkeyManager", test_hotkey_parser()))
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result is True)
    skipped = sum(1 for _, result in results if result == "skip")
    total = len(results)
    
    for test_name, result in results:
        if result is True:
            status = "✓ PASS"
        elif result == "skip":
            status = "⚠ SKIP"
        else:
            status = "✗ FAIL"
        print(f"{test_name:20s}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed, {skipped} skipped")
    
    failed = total - passed - skipped
    if failed == 0:
        print("\n✓ All non-skipped tests passed!")
        return 0
    else:
        print(f"\n✗ {failed} test(s) failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
