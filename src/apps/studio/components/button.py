

from PySide6.QtWidgets import (
    QPushButton, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QFrame, QScrollArea, QSizePolicy, QLineEdit,
    QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QTimer, QDateTime
from PySide6.QtGui import QColor, QFont

from style import AppFont, Colors

class Button(QPushButton):
    def __init__(self, label: str, parent=None):
        super().__init__(label, parent)
        self.setObjectName("button")
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFont(AppFont.body(size=13))
        self.setFixedHeight(42)