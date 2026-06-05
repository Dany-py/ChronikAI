"""
main.py — Point d'entrée Chronik AI
Architecture : MainWindow orchestre Sidebar + ContentStack.
Chaque écran est un QWidget indépendant monté dans un QStackedWidget.
"""

import sys
import os
#from src.main import VERSION

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QHBoxLayout, QVBoxLayout, QLabel,
    QPushButton, QStackedWidget, QFrame,
    QSizePolicy, QSpacerItem
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QFont, QColor

from style import AppFont, Colors, APP_STYLESHEET
from homeScreen import HomeScreen


# ─── Placeholder Screens ──────────────────────────────────────────────────────

def _placeholder(icon: str, name: str) -> QWidget:
    w = QWidget()
    w.setObjectName("content_area")
    layout = QVBoxLayout(w)
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    lbl_icon = QLabel(icon)
    lbl_icon.setFont(AppFont.from_config(size=48))
    lbl_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

    lbl_name = QLabel(name)
    lbl_name.setFont(AppFont.heading(size=18))
    lbl_name.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
    lbl_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

    lbl_wip = QLabel("En cours de développement…")
    lbl_wip.setFont(AppFont.caption(size=11))
    lbl_wip.setStyleSheet(f"color: {Colors.TEXT_MUTED};")
    lbl_wip.setAlignment(Qt.AlignmentFlag.AlignCenter)

    layout.addWidget(lbl_icon)
    layout.addWidget(lbl_name)
    layout.addWidget(lbl_wip)
    return w


# ─── Nav Button ───────────────────────────────────────────────────────────────

class NavButton(QPushButton):
    def __init__(self, icon: str, label: str, parent=None):
        super().__init__(f"  {icon}  {label}", parent)
        self.setObjectName("nav_btn")
        self.setCheckable(False)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFont(AppFont.body(size=13))
        self.setFixedHeight(42)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def set_active(self, active: bool):
        self.setProperty("active", "true" if active else "false")
        self.style().unpolish(self)
        self.style().polish(self)


# ─── Sidebar ─────────────────────────────────────────────────────────────────

class Sidebar(QWidget):
    NAV_ITEMS = [
        ("🏠", "Accueil"),
        #("📸", "Captures"),
        ("🗂️",  "Sessions"),
        #("📊", "Statistiques"),
        #("🔍", "Recherche"),
        ("⚙️",  "Paramètres"),
    ]

    def __init__(self, on_navigate, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self._on_navigate = on_navigate
        self._buttons: list[NavButton] = []
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Logo
        logo = QLabel("CHRONIK-AI")
        logo.setObjectName("logo_label")
        logo.setFont(AppFont.from_config(size=16, weight=QFont.Weight.Black))
        layout.addWidget(logo)

        # Divider
        div = QFrame()
        div.setObjectName("divider")
        div.setFrameShape(QFrame.Shape.HLine)
        div.setFixedHeight(1)
        layout.addWidget(div)

        # Section header
        nav_hdr = QLabel("NAVIGATION")
        nav_hdr.setObjectName("section_header")
        nav_hdr.setFont(AppFont.caption(size=9))
        layout.addWidget(nav_hdr)

        # Nav buttons
        for i, (icon, label) in enumerate(self.NAV_ITEMS):
            btn = NavButton(icon, label)
            btn.clicked.connect(lambda _, idx=i: self._navigate(idx))
            self._buttons.append(btn)
            layout.addWidget(btn)
            if i == 4:  # separator before Paramètres
                sp = QSpacerItem(0, 12, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
                layout.addSpacerItem(sp)
                sep_hdr = QLabel("SYSTÈME")
                sep_hdr.setObjectName("section_header")
                sep_hdr.setFont(AppFont.caption(size=9))
                layout.addWidget(sep_hdr)

        layout.addStretch()

        # Version badge
        ver = QLabel(f"v1.0.0")  #VERSION
        ver.setFont(AppFont.caption(size=9))
        ver.setStyleSheet(f"color: {Colors.TEXT_MUTED}; padding: 12px 18px;")
        layout.addWidget(ver)

        self._navigate(0)

    def _navigate(self, index: int):
        for i, btn in enumerate(self._buttons):
            btn.set_active(i == index)
        self._on_navigate(index)


# ─── MainWindow ───────────────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chronik AI")
        self.setMinimumSize(1000, 700)
        self._build_ui()

    def _build_ui(self):
        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)

        main_layout = QHBoxLayout(root)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ── Stack of screens ──────────────────────────────────────────────────
        self._stack = QStackedWidget()
        self._stack.setObjectName("content_area")

        screens = [
            HomeScreen(),
            #_placeholder("📸", "Captures"),
            _placeholder("🗂️",  "Sessions"),
            #_placeholder("📊", "Statistiques"),
            #_placeholder("🔍", "Recherche"),
            _placeholder("⚙️",  "Paramètres"),
        ]
        for screen in screens:
            self._stack.addWidget(screen)

        # ── Sidebar ───────────────────────────────────────────────────────────
        sidebar = Sidebar(on_navigate=self._stack.setCurrentIndex)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self._stack, stretch=1)


# ─── Entry Point ─────────────────────────────────────────────────────────────

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLESHEET)

    icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon-1.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()