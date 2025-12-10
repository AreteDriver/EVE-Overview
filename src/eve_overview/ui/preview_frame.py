"""Preview window widget for displaying captured windows"""
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QSizeGrip
from PySide6.QtCore import Qt, QTimer, QPoint, Signal, QSize
from PySide6.QtGui import QPixmap, QImage, QPainter, QColor, QPen, QCursor
from PIL import Image
from typing import Optional
import logging


class PreviewFrame(QFrame):
    """Draggable, resizable preview frame for a window"""
    
    closed = Signal(str)  # Signal emitted when frame is closed, with window_id
    activated = Signal(str)  # Signal emitted when preview is clicked, with window_id
    geometry_changed = Signal()  # Signal emitted when geometry changes
    
    def __init__(self, window_id: str, window_title: str, parent=None):
        super().__init__(parent)
        
        self.window_id = window_id
        self.window_title = window_title
        self.logger = logging.getLogger(__name__)
        
        # State
        self.is_dragging = False
        self.drag_start_pos = QPoint()
        self.scale_factor = 0.3
        self.refresh_rate = 30  # FPS
        
        # Setup UI
        self._setup_ui()
        
        # Timer for updating preview
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.request_update)
        
    def _setup_ui(self):
        """Setup the UI components"""
        # Frame style
        self.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.setLineWidth(2)
        self.setStyleSheet("""
            PreviewFrame {
                background-color: #2b2b2b;
                border: 2px solid #555;
            }
            PreviewFrame:hover {
                border: 2px solid #888;
            }
        """)
        
        # Make frameless and always on top
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        
        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(0)
        
        # Title label
        self.title_label = QLabel(self.window_title)
        self.title_label.setStyleSheet("""
            QLabel {
                background-color: #1e1e1e;
                color: #ffffff;
                padding: 4px;
                font-size: 10px;
                font-weight: bold;
            }
        """)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setMaximumHeight(24)
        layout.addWidget(self.title_label)
        
        # Image label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background-color: #1a1a1a;")
        self.image_label.setScaledContents(True)
        self.image_label.setMinimumSize(100, 100)
        layout.addWidget(self.image_label)
        
        # Resize grip
        self.size_grip = QSizeGrip(self)
        self.size_grip.setStyleSheet("""
            QSizeGrip {
                background-color: #555;
                width: 16px;
                height: 16px;
            }
        """)
        
        self.setLayout(layout)
        
        # Default size
        self.resize(400, 300)
        
    def set_scale(self, scale: float):
        """Set the scale factor for the preview
        
        Args:
            scale: Scale factor (0.1 to 1.0)
        """
        self.scale_factor = max(0.1, min(1.0, scale))
        
    def set_refresh_rate(self, fps: int):
        """Set the refresh rate
        
        Args:
            fps: Frames per second (1 to 60)
        """
        self.refresh_rate = max(1, min(60, fps))
        if self.update_timer.isActive():
            self.update_timer.start(1000 // self.refresh_rate)
    
    def update_preview(self, image: Image.Image):
        """Update the preview with a new image
        
        Args:
            image: PIL Image to display
        """
        if image is None:
            return
        
        try:
            # Convert PIL Image to QPixmap
            image_rgb = image.convert('RGB')
            data = image_rgb.tobytes('raw', 'RGB')
            qimage = QImage(
                data,
                image_rgb.width,
                image_rgb.height,
                image_rgb.width * 3,
                QImage.Format.Format_RGB888
            )
            pixmap = QPixmap.fromImage(qimage)
            
            # Update label
            self.image_label.setPixmap(pixmap)
            
        except Exception as e:
            self.logger.error(f"Failed to update preview: {e}")
    
    def start_preview(self):
        """Start the preview update timer"""
        interval = 1000 // self.refresh_rate
        self.update_timer.start(interval)
        self.logger.info(f"Started preview for '{self.window_title}' at {self.refresh_rate} FPS")
    
    def stop_preview(self):
        """Stop the preview update timer"""
        self.update_timer.stop()
        self.logger.info(f"Stopped preview for '{self.window_title}'")
    
    def request_update(self):
        """Request a preview update (to be connected to capture system)"""
        # This should be connected to the window capture system
        pass
    
    def mousePressEvent(self, event):
        """Handle mouse press for dragging and activation"""
        if event.button() == Qt.MouseButton.LeftButton:
            # Check if clicking on title bar for dragging
            if self.title_label.geometry().contains(event.pos()):
                self.is_dragging = True
                self.drag_start_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
                event.accept()
            else:
                # Click on preview activates the window
                self.activated.emit(self.window_id)
                event.accept()
        elif event.button() == Qt.MouseButton.RightButton:
            # Right-click to close
            self.close()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging"""
        if self.is_dragging and event.buttons() & Qt.MouseButton.LeftButton:
            new_pos = event.globalPosition().toPoint() - self.drag_start_pos
            self.move(new_pos)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = False
            self.geometry_changed.emit()
            event.accept()
    
    def resizeEvent(self, event):
        """Handle resize event"""
        super().resizeEvent(event)
        
        # Position size grip in bottom-right corner
        grip_size = self.size_grip.sizeHint()
        self.size_grip.move(
            self.width() - grip_size.width(),
            self.height() - grip_size.height()
        )
        
        self.geometry_changed.emit()
    
    def closeEvent(self, event):
        """Handle close event"""
        self.stop_preview()
        self.closed.emit(self.window_id)
        super().closeEvent(event)
    
    def get_geometry_dict(self):
        """Get geometry as dictionary
        
        Returns:
            Dict with x, y, width, height
        """
        return {
            'x': self.x(),
            'y': self.y(),
            'width': self.width(),
            'height': self.height()
        }
