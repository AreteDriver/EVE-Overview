"""Hotkey management system"""
from typing import Callable, Dict, Optional
from pynput import keyboard
from PySide6.QtCore import QObject, Signal
import logging


class HotkeyManager(QObject):
    """Manages global hotkeys for window activation"""
    
    hotkey_triggered = Signal(str)  # Signal emitted with hotkey name
    
    def __init__(self):
        super().__init__()
        self.hotkeys: Dict[str, Dict] = {}  # hotkey_name -> {combo: str, callback: callable}
        self.listener: Optional[keyboard.GlobalHotKeys] = None
        self.current_keys = set()
        self.logger = logging.getLogger(__name__)
        
    def register_hotkey(self, name: str, key_combo: str, callback: Callable) -> bool:
        """Register a new hotkey
        
        Args:
            name: Unique identifier for the hotkey
            key_combo: Key combination (e.g., '<ctrl>+<alt>+1')
            callback: Function to call when hotkey is pressed
            
        Returns:
            True if registration successful
        """
        try:
            # Store hotkey info
            self.hotkeys[name] = {
                'combo': key_combo,
                'callback': callback
            }
            
            # Restart listener with updated hotkeys
            self._restart_listener()
            self.logger.info(f"Registered hotkey '{name}': {key_combo}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to register hotkey '{name}': {e}")
            return False
    
    def unregister_hotkey(self, name: str) -> bool:
        """Unregister a hotkey
        
        Args:
            name: Hotkey identifier
            
        Returns:
            True if successful
        """
        if name in self.hotkeys:
            del self.hotkeys[name]
            self._restart_listener()
            self.logger.info(f"Unregistered hotkey '{name}'")
            return True
        return False
    
    def get_hotkeys(self) -> Dict[str, str]:
        """Get all registered hotkeys
        
        Returns:
            Dict mapping hotkey names to key combinations
        """
        return {name: info['combo'] for name, info in self.hotkeys.items()}
    
    def _restart_listener(self):
        """Restart the hotkey listener with current hotkeys"""
        # Stop existing listener
        if self.listener:
            try:
                self.listener.stop()
            except:
                pass
        
        if not self.hotkeys:
            return
        
        # Create mapping for GlobalHotKeys
        hotkey_map = {}
        for name, info in self.hotkeys.items():
            combo = info['combo']
            callback = info['callback']
            
            # Wrap callback to emit signal
            # Use default arguments to capture current values
            def make_callback(cb=callback, hk_name=name):
                def wrapper():
                    cb()
                    self.hotkey_triggered.emit(hk_name)
                return wrapper
            
            hotkey_map[combo] = make_callback()
        
        try:
            # Start new listener
            self.listener = keyboard.GlobalHotKeys(hotkey_map)
            self.listener.start()
        except Exception as e:
            self.logger.error(f"Failed to start hotkey listener: {e}")
    
    def start(self):
        """Start listening for hotkeys"""
        self._restart_listener()
    
    def stop(self):
        """Stop listening for hotkeys"""
        if self.listener:
            try:
                self.listener.stop()
                self.listener = None
            except:
                pass
    
    def parse_key_combo(self, combo_string: str) -> str:
        """Parse a human-readable key combo to pynput format
        
        Args:
            combo_string: String like 'Ctrl+Alt+1' or 'Ctrl+Shift+F1'
            
        Returns:
            pynput format string like '<ctrl>+<alt>+1'
        """
        # Map common key names to pynput format
        key_map = {
            'ctrl': '<ctrl>',
            'control': '<ctrl>',
            'alt': '<alt>',
            'shift': '<shift>',
            'super': '<cmd>',
            'win': '<cmd>',
            'cmd': '<cmd>',
        }
        
        parts = combo_string.lower().split('+')
        formatted_parts = []
        
        for part in parts:
            part = part.strip()
            if part in key_map:
                formatted_parts.append(key_map[part])
            elif len(part) == 1:
                # Single character
                formatted_parts.append(part)
            elif part.startswith('f') and part[1:].isdigit():
                # Function keys
                formatted_parts.append(f'<{part}>')
            else:
                # Other special keys
                formatted_parts.append(f'<{part}>')
        
        return '+'.join(formatted_parts)
    
    def format_key_combo(self, pynput_combo: str) -> str:
        """Format pynput key combo to human-readable format
        
        Args:
            pynput_combo: pynput format like '<ctrl>+<alt>+1'
            
        Returns:
            Human readable format like 'Ctrl+Alt+1'
        """
        # Remove angle brackets and capitalize
        parts = pynput_combo.split('+')
        formatted_parts = []
        
        for part in parts:
            part = part.strip('<>').capitalize()
            if part == 'Cmd':
                part = 'Super'
            formatted_parts.append(part)
        
        return '+'.join(formatted_parts)
