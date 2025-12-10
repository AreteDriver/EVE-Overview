"""Main application window"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QLabel, QComboBox, QSpinBox, QGroupBox,
    QLineEdit, QCheckBox, QMessageBox, QDialog, QFormLayout,
    QDialogButtonBox, QListWidgetItem
)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QAction
import logging
from typing import Dict, Optional

from ..core.window_capture import WindowCapture
from ..core.hotkey_manager import HotkeyManager
from ..core.config_manager import ConfigManager, Profile, WindowConfig
from .preview_frame import PreviewFrame


class HotkeyDialog(QDialog):
    """Dialog for editing hotkey bindings"""
    
    def __init__(self, current_combo: str = "", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Hotkey")
        self.combo_value = current_combo
        
        layout = QVBoxLayout()
        
        # Instructions
        label = QLabel("Enter key combination (e.g., Ctrl+Alt+1):")
        layout.addWidget(label)
        
        # Input
        self.combo_input = QLineEdit(current_combo)
        self.combo_input.setPlaceholderText("Ctrl+Alt+1")
        layout.addWidget(self.combo_input)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def get_combo(self) -> str:
        """Get the entered combo"""
        return self.combo_input.text().strip()


class MainWindow(QMainWindow):
    """Main application window for EVE Overview"""
    
    def __init__(self):
        super().__init__()
        
        self.logger = logging.getLogger(__name__)
        
        # Core components
        self.window_capture = WindowCapture()
        self.hotkey_manager = HotkeyManager()
        self.config_manager = ConfigManager()
        
        # Preview frames
        self.preview_frames: Dict[str, PreviewFrame] = {}
        
        # Current profile
        self.current_profile: Optional[Profile] = None
        
        # Setup UI
        self._setup_ui()
        
        # Load current profile
        self._load_current_profile()
        
        # Start hotkey manager
        self.hotkey_manager.start()
        
        # Timer for refreshing window list
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self._refresh_window_list)
        self.refresh_timer.start(5000)  # Refresh every 5 seconds
        
    def _setup_ui(self):
        """Setup the main UI"""
        self.setWindowTitle("EVE Overview - Multi-Window Preview")
        self.setMinimumSize(800, 600)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Profile section
        profile_group = QGroupBox("Profile Management")
        profile_layout = QHBoxLayout()
        
        self.profile_combo = QComboBox()
        self.profile_combo.currentTextChanged.connect(self._on_profile_changed)
        profile_layout.addWidget(QLabel("Profile:"))
        profile_layout.addWidget(self.profile_combo, 1)
        
        self.new_profile_btn = QPushButton("New")
        self.new_profile_btn.clicked.connect(self._create_new_profile)
        profile_layout.addWidget(self.new_profile_btn)
        
        self.save_profile_btn = QPushButton("Save")
        self.save_profile_btn.clicked.connect(self._save_current_profile)
        profile_layout.addWidget(self.save_profile_btn)
        
        self.delete_profile_btn = QPushButton("Delete")
        self.delete_profile_btn.clicked.connect(self._delete_profile)
        profile_layout.addWidget(self.delete_profile_btn)
        
        profile_group.setLayout(profile_layout)
        main_layout.addWidget(profile_group)
        
        # Settings section
        settings_group = QGroupBox("Settings")
        settings_layout = QFormLayout()
        
        self.refresh_rate_spin = QSpinBox()
        self.refresh_rate_spin.setRange(1, 60)
        self.refresh_rate_spin.setValue(30)
        self.refresh_rate_spin.setSuffix(" FPS")
        settings_layout.addRow("Refresh Rate:", self.refresh_rate_spin)
        
        self.always_on_top_check = QCheckBox()
        self.always_on_top_check.setChecked(True)
        settings_layout.addRow("Always On Top:", self.always_on_top_check)
        
        settings_group.setLayout(settings_layout)
        main_layout.addWidget(settings_group)
        
        # Window list section
        window_group = QGroupBox("Available Windows")
        window_layout = QVBoxLayout()
        
        # Refresh button
        refresh_btn_layout = QHBoxLayout()
        self.refresh_windows_btn = QPushButton("Refresh Window List")
        self.refresh_windows_btn.clicked.connect(self._refresh_window_list)
        refresh_btn_layout.addWidget(self.refresh_windows_btn)
        refresh_btn_layout.addStretch()
        window_layout.addLayout(refresh_btn_layout)
        
        # Window list
        self.window_list = QListWidget()
        self.window_list.itemDoubleClicked.connect(self._on_window_double_clicked)
        window_layout.addWidget(self.window_list)
        
        # Add window button
        self.add_window_btn = QPushButton("Add Selected Window")
        self.add_window_btn.clicked.connect(self._add_selected_window)
        window_layout.addWidget(self.add_window_btn)
        
        window_group.setLayout(window_layout)
        main_layout.addWidget(window_group)
        
        # Active previews section
        previews_group = QGroupBox("Active Previews")
        previews_layout = QVBoxLayout()
        
        self.previews_list = QListWidget()
        self.previews_list.itemDoubleClicked.connect(self._on_preview_double_clicked)
        previews_layout.addWidget(self.previews_list)
        
        # Preview control buttons
        preview_btn_layout = QHBoxLayout()
        
        self.remove_preview_btn = QPushButton("Remove")
        self.remove_preview_btn.clicked.connect(self._remove_selected_preview)
        preview_btn_layout.addWidget(self.remove_preview_btn)
        
        self.edit_hotkey_btn = QPushButton("Edit Hotkey")
        self.edit_hotkey_btn.clicked.connect(self._edit_preview_hotkey)
        preview_btn_layout.addWidget(self.edit_hotkey_btn)
        
        self.show_preview_btn = QPushButton("Show/Hide")
        self.show_preview_btn.clicked.connect(self._toggle_preview)
        preview_btn_layout.addWidget(self.show_preview_btn)
        
        previews_layout.addLayout(preview_btn_layout)
        
        previews_group.setLayout(previews_layout)
        main_layout.addWidget(previews_group)
        
        # Initial window list refresh
        self._refresh_window_list()
        
        # Load profiles
        self._load_profiles()
        
    def _load_profiles(self):
        """Load available profiles into combo box"""
        self.profile_combo.clear()
        profiles = self.config_manager.list_profiles()
        self.profile_combo.addItems(profiles)
        
        # Select current profile
        current = self.config_manager.get_setting('current_profile', 'Default')
        index = self.profile_combo.findText(current)
        if index >= 0:
            self.profile_combo.setCurrentIndex(index)
    
    def _load_current_profile(self):
        """Load the current profile"""
        self.current_profile = self.config_manager.get_current_profile()
        
        # Update settings
        self.refresh_rate_spin.setValue(self.current_profile.refresh_rate)
        self.always_on_top_check.setChecked(self.current_profile.always_on_top)
        
        # Clear existing previews
        for frame in list(self.preview_frames.values()):
            frame.close()
        self.preview_frames.clear()
        self.previews_list.clear()
        
        # Load windows from profile
        for window_config in self.current_profile.windows:
            if window_config.enabled:
                self._create_preview_from_config(window_config)
    
    def _save_current_profile(self):
        """Save the current profile"""
        if not self.current_profile:
            return
        
        # Update profile settings
        self.current_profile.refresh_rate = self.refresh_rate_spin.value()
        self.current_profile.always_on_top = self.always_on_top_check.isChecked()
        
        # Update window configurations
        self.current_profile.windows = []
        for window_id, frame in self.preview_frames.items():
            geom = frame.get_geometry_dict()
            
            # Get hotkey if registered
            hotkey = ""
            for hk_name, hk_combo in self.hotkey_manager.get_hotkeys().items():
                if hk_name == f"preview_{window_id}":
                    hotkey = hk_combo
                    break
            
            window_config = WindowConfig(
                window_id=window_id,
                window_title=frame.window_title,
                x=geom['x'],
                y=geom['y'],
                width=geom['width'],
                height=geom['height'],
                scale=frame.scale_factor,
                hotkey=hotkey,
                enabled=frame.isVisible()
            )
            self.current_profile.windows.append(window_config)
        
        # Save to disk
        if self.config_manager.save_profile(self.current_profile):
            QMessageBox.information(
                self,
                "Profile Saved",
                f"Profile '{self.current_profile.name}' saved successfully!"
            )
    
    def _create_new_profile(self):
        """Create a new profile"""
        from PySide6.QtWidgets import QInputDialog
        
        name, ok = QInputDialog.getText(
            self,
            "New Profile",
            "Enter profile name:"
        )
        
        if ok and name:
            # Create new profile
            new_profile = Profile(name=name, windows=[])
            if self.config_manager.save_profile(new_profile):
                self._load_profiles()
                self.profile_combo.setCurrentText(name)
    
    def _delete_profile(self):
        """Delete the current profile"""
        if not self.current_profile or self.current_profile.name == 'Default':
            QMessageBox.warning(
                self,
                "Cannot Delete",
                "Cannot delete the Default profile."
            )
            return
        
        reply = QMessageBox.question(
            self,
            "Delete Profile",
            f"Are you sure you want to delete profile '{self.current_profile.name}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.config_manager.delete_profile(self.current_profile.name):
                self._load_profiles()
                self.profile_combo.setCurrentText('Default')
    
    def _on_profile_changed(self, profile_name: str):
        """Handle profile change"""
        if profile_name:
            self.config_manager.set_current_profile(profile_name)
            self._load_current_profile()
    
    def _refresh_window_list(self):
        """Refresh the list of available windows"""
        self.window_list.clear()
        windows = self.window_capture.get_window_list()
        
        for window_id, window_title in windows:
            # Skip our own windows
            if 'EVE Overview' in window_title or 'Preview' in window_title:
                continue
            
            item = QListWidgetItem(f"{window_title} [{window_id}]")
            item.setData(Qt.ItemDataRole.UserRole, window_id)
            self.window_list.addItem(item)
    
    def _on_window_double_clicked(self, item: QListWidgetItem):
        """Handle double-click on window list"""
        self._add_selected_window()
    
    def _add_selected_window(self):
        """Add selected window to previews"""
        item = self.window_list.currentItem()
        if not item:
            return
        
        window_id = item.data(Qt.ItemDataRole.UserRole)
        window_title = item.text().split('[')[0].strip()
        
        # Check if already added
        if window_id in self.preview_frames:
            QMessageBox.information(
                self,
                "Already Added",
                f"Window '{window_title}' is already in previews."
            )
            return
        
        # Create preview frame
        self._create_preview(window_id, window_title)
    
    def _create_preview(self, window_id: str, window_title: str):
        """Create a new preview frame"""
        frame = PreviewFrame(window_id, window_title)
        frame.set_refresh_rate(self.refresh_rate_spin.value())
        
        # Connect signals
        frame.closed.connect(self._on_preview_closed)
        frame.activated.connect(self._on_preview_activated)
        frame.request_update = lambda: self._update_preview(window_id)
        
        # Show frame
        frame.show()
        frame.start_preview()
        
        # Store frame
        self.preview_frames[window_id] = frame
        
        # Add to list
        list_item = QListWidgetItem(f"{window_title} [{window_id}]")
        list_item.setData(Qt.ItemDataRole.UserRole, window_id)
        self.previews_list.addItem(list_item)
        
        self.logger.info(f"Created preview for window '{window_title}'")
    
    def _create_preview_from_config(self, config: WindowConfig):
        """Create preview from configuration"""
        frame = PreviewFrame(config.window_id, config.window_title)
        frame.set_refresh_rate(self.current_profile.refresh_rate)
        frame.set_scale(config.scale)
        
        # Set geometry
        frame.move(config.x, config.y)
        frame.resize(config.width, config.height)
        
        # Connect signals
        frame.closed.connect(self._on_preview_closed)
        frame.activated.connect(self._on_preview_activated)
        frame.request_update = lambda: self._update_preview(config.window_id)
        
        # Register hotkey if specified
        if config.hotkey:
            self._register_preview_hotkey(config.window_id, config.hotkey)
        
        # Show frame
        frame.show()
        frame.start_preview()
        
        # Store frame
        self.preview_frames[config.window_id] = frame
        
        # Add to list
        list_item = QListWidgetItem(f"{config.window_title} [{config.window_id}]")
        list_item.setData(Qt.ItemDataRole.UserRole, config.window_id)
        self.previews_list.addItem(list_item)
    
    def _update_preview(self, window_id: str):
        """Update a preview with captured window image"""
        if window_id not in self.preview_frames:
            return
        
        frame = self.preview_frames[window_id]
        image = self.window_capture.capture_window(window_id, frame.scale_factor)
        
        if image:
            frame.update_preview(image)
    
    def _on_preview_closed(self, window_id: str):
        """Handle preview frame closed"""
        if window_id in self.preview_frames:
            # Unregister hotkey
            self.hotkey_manager.unregister_hotkey(f"preview_{window_id}")
            
            # Remove from dict
            del self.preview_frames[window_id]
            
            # Remove from list
            for i in range(self.previews_list.count()):
                item = self.previews_list.item(i)
                if item.data(Qt.ItemDataRole.UserRole) == window_id:
                    self.previews_list.takeItem(i)
                    break
    
    def _on_preview_activated(self, window_id: str):
        """Handle preview clicked - activate the window"""
        self.window_capture.activate_window(window_id)
    
    def _on_preview_double_clicked(self, item: QListWidgetItem):
        """Handle double-click on preview list"""
        self._edit_preview_hotkey()
    
    def _remove_selected_preview(self):
        """Remove selected preview"""
        item = self.previews_list.currentItem()
        if not item:
            return
        
        window_id = item.data(Qt.ItemDataRole.UserRole)
        if window_id in self.preview_frames:
            self.preview_frames[window_id].close()
    
    def _toggle_preview(self):
        """Toggle preview visibility"""
        item = self.previews_list.currentItem()
        if not item:
            return
        
        window_id = item.data(Qt.ItemDataRole.UserRole)
        if window_id in self.preview_frames:
            frame = self.preview_frames[window_id]
            if frame.isVisible():
                frame.hide()
            else:
                frame.show()
    
    def _edit_preview_hotkey(self):
        """Edit hotkey for selected preview"""
        item = self.previews_list.currentItem()
        if not item:
            return
        
        window_id = item.data(Qt.ItemDataRole.UserRole)
        
        # Get current hotkey
        current_combo = ""
        for hk_name, hk_combo in self.hotkey_manager.get_hotkeys().items():
            if hk_name == f"preview_{window_id}":
                current_combo = self.hotkey_manager.format_key_combo(hk_combo)
                break
        
        # Show dialog
        dialog = HotkeyDialog(current_combo, self)
        if dialog.exec() == QDialog.Accepted:
            combo = dialog.get_combo()
            if combo:
                self._register_preview_hotkey(window_id, combo)
    
    def _register_preview_hotkey(self, window_id: str, combo: str):
        """Register a hotkey for a preview"""
        # Parse combo
        parsed_combo = self.hotkey_manager.parse_key_combo(combo)
        
        # Create callback
        def activate_callback():
            self.window_capture.activate_window(window_id)
        
        # Register
        hk_name = f"preview_{window_id}"
        if self.hotkey_manager.register_hotkey(hk_name, parsed_combo, activate_callback):
            self.logger.info(f"Registered hotkey '{combo}' for window {window_id}")
        else:
            QMessageBox.warning(
                self,
                "Hotkey Error",
                f"Failed to register hotkey '{combo}'. Make sure it's not already in use."
            )
    
    def closeEvent(self, event):
        """Handle application close"""
        # Save current state
        self._save_current_profile()
        
        # Stop hotkey manager
        self.hotkey_manager.stop()
        
        # Close all preview frames
        for frame in list(self.preview_frames.values()):
            frame.close()
        
        super().closeEvent(event)
