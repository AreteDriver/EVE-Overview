"""Configuration and profile management"""
import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import logging


@dataclass
class WindowConfig:
    """Configuration for a single window preview"""
    window_id: str
    window_title: str
    x: int
    y: int
    width: int
    height: int
    scale: float = 0.3
    hotkey: str = ""
    enabled: bool = True


@dataclass
class Profile:
    """Profile containing multiple window configurations"""
    name: str
    windows: List[WindowConfig]
    refresh_rate: int = 30  # FPS
    always_on_top: bool = True
    click_through: bool = False
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'windows': [asdict(w) for w in self.windows],
            'refresh_rate': self.refresh_rate,
            'always_on_top': self.always_on_top,
            'click_through': self.click_through
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Profile':
        """Create from dictionary"""
        windows = [WindowConfig(**w) for w in data.get('windows', [])]
        return cls(
            name=data.get('name', 'Default'),
            windows=windows,
            refresh_rate=data.get('refresh_rate', 30),
            always_on_top=data.get('always_on_top', True),
            click_through=data.get('click_through', False)
        )


class ConfigManager:
    """Manages application configuration and profiles"""
    
    def __init__(self, config_dir: Optional[Path] = None):
        self.logger = logging.getLogger(__name__)
        
        # Set config directory
        if config_dir is None:
            config_dir = Path.home() / '.config' / 'eve-overview'
        
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.profiles_dir = self.config_dir / 'profiles'
        self.profiles_dir.mkdir(exist_ok=True)
        
        self.config_file = self.config_dir / 'config.json'
        self.current_profile_name = 'Default'
        
        # Load or create default config
        self.config = self._load_config()
        
    def _load_config(self) -> Dict:
        """Load main configuration file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Failed to load config: {e}")
        
        # Default configuration
        return {
            'current_profile': 'Default',
            'last_profile': 'Default',
            'window_geometry': None,
            'theme': 'dark'
        }
    
    def _save_config(self):
        """Save main configuration file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save config: {e}")
    
    def get_profile_path(self, profile_name: str) -> Path:
        """Get path to profile file"""
        return self.profiles_dir / f"{profile_name}.json"
    
    def load_profile(self, profile_name: str) -> Optional[Profile]:
        """Load a profile by name
        
        Args:
            profile_name: Name of the profile
            
        Returns:
            Profile object or None if not found
        """
        profile_path = self.get_profile_path(profile_name)
        
        if not profile_path.exists():
            self.logger.warning(f"Profile '{profile_name}' not found")
            return None
        
        try:
            with open(profile_path, 'r') as f:
                data = json.load(f)
                return Profile.from_dict(data)
        except Exception as e:
            self.logger.error(f"Failed to load profile '{profile_name}': {e}")
            return None
    
    def save_profile(self, profile: Profile) -> bool:
        """Save a profile
        
        Args:
            profile: Profile to save
            
        Returns:
            True if successful
        """
        profile_path = self.get_profile_path(profile.name)
        
        try:
            with open(profile_path, 'w') as f:
                json.dump(profile.to_dict(), f, indent=2)
            self.logger.info(f"Saved profile '{profile.name}'")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save profile '{profile.name}': {e}")
            return False
    
    def delete_profile(self, profile_name: str) -> bool:
        """Delete a profile
        
        Args:
            profile_name: Name of profile to delete
            
        Returns:
            True if successful
        """
        if profile_name == 'Default':
            self.logger.warning("Cannot delete Default profile")
            return False
        
        profile_path = self.get_profile_path(profile_name)
        
        try:
            if profile_path.exists():
                profile_path.unlink()
                self.logger.info(f"Deleted profile '{profile_name}'")
                return True
        except Exception as e:
            self.logger.error(f"Failed to delete profile '{profile_name}': {e}")
        
        return False
    
    def list_profiles(self) -> List[str]:
        """Get list of all profile names
        
        Returns:
            List of profile names
        """
        profiles = []
        for file_path in self.profiles_dir.glob('*.json'):
            profiles.append(file_path.stem)
        
        # Ensure Default is in the list
        if 'Default' not in profiles:
            profiles.insert(0, 'Default')
        
        return sorted(profiles)
    
    def get_current_profile(self) -> Profile:
        """Get the current active profile
        
        Returns:
            Current profile or new Default profile
        """
        profile_name = self.config.get('current_profile', 'Default')
        profile = self.load_profile(profile_name)
        
        if profile is None:
            # Create new default profile
            profile = Profile(name='Default', windows=[])
            self.save_profile(profile)
        
        return profile
    
    def set_current_profile(self, profile_name: str):
        """Set the current active profile
        
        Args:
            profile_name: Name of profile to activate
        """
        self.config['current_profile'] = profile_name
        self.current_profile_name = profile_name
        self._save_config()
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a configuration setting
        
        Args:
            key: Setting key
            default: Default value if not found
            
        Returns:
            Setting value
        """
        return self.config.get(key, default)
    
    def set_setting(self, key: str, value: Any):
        """Set a configuration setting
        
        Args:
            key: Setting key
            value: Setting value
        """
        self.config[key] = value
        self._save_config()
