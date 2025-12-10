"""Window capture functionality for X11/Linux"""
import subprocess
from typing import Optional, Tuple, List
from PIL import Image
import io


class WindowCapture:
    """Handles window capture on Linux using xwd and ImageMagick"""
    
    def __init__(self):
        self.cached_windows = {}
        
    def get_window_list(self) -> List[Tuple[str, str]]:
        """Get list of all windows with their IDs and titles
        
        Returns:
            List of tuples (window_id, window_title)
        """
        try:
            # Use wmctrl to get window list
            result = subprocess.run(
                ['wmctrl', '-l'],
                capture_output=True,
                text=True,
                timeout=2
            )
            
            windows = []
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        parts = line.split(None, 3)
                        if len(parts) >= 4:
                            window_id = parts[0]
                            window_title = parts[3]
                            windows.append((window_id, window_title))
            
            return windows
        except (subprocess.TimeoutExpired, FileNotFoundError):
            # Fallback to xdotool if wmctrl not available
            return self._get_windows_xdotool()
    
    def _get_windows_xdotool(self) -> List[Tuple[str, str]]:
        """Fallback method using xdotool"""
        try:
            result = subprocess.run(
                ['xdotool', 'search', '--onlyvisible', '--name', ''],
                capture_output=True,
                text=True,
                timeout=2
            )
            
            windows = []
            if result.returncode == 0:
                for window_id in result.stdout.strip().split('\n'):
                    if window_id:
                        title = self._get_window_title(window_id)
                        windows.append((window_id, title))
            
            return windows
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return []
    
    def _get_window_title(self, window_id: str) -> str:
        """Get window title by ID"""
        try:
            result = subprocess.run(
                ['xdotool', 'getwindowname', window_id],
                capture_output=True,
                text=True,
                timeout=1
            )
            return result.stdout.strip() if result.returncode == 0 else "Unknown"
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return "Unknown"
    
    def capture_window(self, window_id: str, scale: float = 1.0) -> Optional[Image.Image]:
        """Capture a window by its ID
        
        Args:
            window_id: X11 window ID
            scale: Scale factor for the captured image
            
        Returns:
            PIL Image or None if capture failed
        """
        try:
            # Use import (ImageMagick) for reliable window capture
            result = subprocess.run(
                ['import', '-window', window_id, '-silent', 'png:-'],
                capture_output=True,
                timeout=1
            )
            
            if result.returncode == 0 and result.stdout:
                img = Image.open(io.BytesIO(result.stdout))
                
                # Scale if needed
                if scale != 1.0:
                    new_size = (int(img.width * scale), int(img.height * scale))
                    img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                return img
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            pass
        
        # Fallback to xwd + convert
        return self._capture_window_xwd(window_id, scale)
    
    def _capture_window_xwd(self, window_id: str, scale: float = 1.0) -> Optional[Image.Image]:
        """Fallback capture using xwd"""
        try:
            # Capture with xwd
            xwd_result = subprocess.run(
                ['xwd', '-id', window_id, '-silent'],
                capture_output=True,
                timeout=1
            )
            
            if xwd_result.returncode != 0:
                return None
            
            # Convert to PNG
            convert_result = subprocess.run(
                ['convert', 'xwd:-', 'png:-'],
                input=xwd_result.stdout,
                capture_output=True,
                timeout=1
            )
            
            if convert_result.returncode == 0 and convert_result.stdout:
                img = Image.open(io.BytesIO(convert_result.stdout))
                
                if scale != 1.0:
                    new_size = (int(img.width * scale), int(img.height * scale))
                    img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                return img
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            pass
        
        return None
    
    def activate_window(self, window_id: str) -> bool:
        """Activate/focus a window by its ID
        
        Args:
            window_id: X11 window ID
            
        Returns:
            True if successful
        """
        try:
            # Try wmctrl first
            result = subprocess.run(
                ['wmctrl', '-i', '-a', window_id],
                capture_output=True,
                timeout=1
            )
            if result.returncode == 0:
                return True
            
            # Fallback to xdotool
            result = subprocess.run(
                ['xdotool', 'windowactivate', window_id],
                capture_output=True,
                timeout=1
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
