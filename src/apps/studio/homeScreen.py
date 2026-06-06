"""
homeScreen.py — Écran d'accueil Chronik AI
Architecture : HomeScreen est un widget autonome monté dans MainWindow.
"""

from PySide6.QtWidgets import (
    QPushButton, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QFrame, QScrollArea, QSizePolicy, QLineEdit,
    QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QTimer, QDateTime
from PySide6.QtGui import QColor, QFont
from style import AppFont, Colors
from apps.watcher import Tracker
import threading


# ─── Tracker ─────────────────────────────────────────────────────────────────

def start_watcher(stop_event: threading.Event, tracker: Tracker):
    """Lance le Tracker dans un thread dédié."""

    # Arrêt propre quand stop_event est déclenché
    def watch():
        while not stop_event.is_set():
            tracker.run_session()

    watch()

# ─── Helpers ─────────────────────────────────────────────────────────────────

def make_shadow(color: str = "#000000", blur: int = 20, offset=(0, 4)) -> QGraphicsDropShadowEffect:
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(blur)
    shadow.setColor(QColor(color))
    shadow.setOffset(*offset)
    return shadow


def h_divider() -> QFrame:
    line = QFrame()
    line.setObjectName("divider")
    line.setFrameShape(QFrame.Shape.HLine)
    line.setFixedHeight(1)
    return line

# ─── Tracker button ───────────────────────────────────────────────────────────────
class TrackerButton(QPushButton):
    def __init__(self, label: str, parent=None):
        super().__init__(label, parent)
        self.setObjectName("button")
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFont(AppFont.body(size=13))
        self.setFixedHeight(42)
        self.event = threading.Event()
        self.tracker = None
        self.watcher_thread = None
        self.is_running = False
    
    def _run_watcher(self):
        self.tracker = Tracker(
            replay=True,
            duration=60,
            verbose=True,
            idle_threshold=1,
        )
        self.event.clear()

        self.watcher_thread = threading.Thread(
            target=start_watcher,
            args=(self.event, self.tracker),
            name="watcher",
            daemon=True,
        )
        self.watcher_thread.start()
        self.is_running = True
        self.setText("Stop Watcher")
        print("[watcher] actif")

    def _stop_watcher(self):
        if self.tracker is not None:
            self.tracker.should_stop = True
            try:
                self.tracker.stop()
            except Exception:
                pass

        self.event.set()
        self.is_running = False
        self.setText("Start Watcher")
        print("[watcher] arrêté")

    def toggle(self):
        if self.is_running:
            self._stop_watcher()
        else:
            self._run_watcher()
        

# ─── Stat Card ───────────────────────────────────────────────────────────────

class StatCard(QWidget):
    def __init__(self, icon: str, label: str, value: str, card_id: str, accent: str, parent=None):
        super().__init__(parent)
        self.setObjectName(card_id)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(110)
        self.setGraphicsEffect(make_shadow(accent, blur=24, offset=(0, 6)))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(6)

        top = QHBoxLayout()
        icon_lbl = QLabel(icon)
        icon_lbl.setFont(AppFont.from_config(size=22))
        value_lbl = QLabel(value)
        value_lbl.setFont(AppFont.heading(size=26))
        value_lbl.setStyleSheet(f"color: {accent};")
        top.addWidget(icon_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        #top.addStretch()
        top.addWidget(value_lbl, alignment=Qt.AlignmentFlag.AlignCenter)

        text_lbl = QLabel(label)
        text_lbl.setFont(AppFont.caption(size=11))
        text_lbl.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")

        layout.addLayout(top)
        layout.addWidget(text_lbl)


# ─── Activity Item ────────────────────────────────────────────────────────────

class ActivityItem(QWidget):
    def __init__(self, icon: str, title: str, subtitle: str, time_str: str, parent=None):
        super().__init__(parent)
        self.setObjectName("activity_item")
        self.setFixedHeight(64)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(12)

        icon_lbl = QLabel(icon)
        icon_lbl.setFont(AppFont.from_config(size=20))
        icon_lbl.setFixedWidth(32)

        text_col = QVBoxLayout()
        text_col.setSpacing(2)
        title_lbl = QLabel(title)
        title_lbl.setFont(AppFont.body(size=12))
        title_lbl.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        sub_lbl = QLabel(subtitle)
        sub_lbl.setFont(AppFont.caption(size=10))
        sub_lbl.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        text_col.addWidget(title_lbl)
        text_col.addWidget(sub_lbl)

        time_lbl = QLabel(time_str)
        time_lbl.setFont(AppFont.caption(size=10))
        time_lbl.setStyleSheet(f"color: {Colors.TEXT_MUTED};")
        time_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        layout.addWidget(icon_lbl)
        layout.addLayout(text_col, stretch=1)
        layout.addWidget(time_lbl)


# ─── HomeScreen ──────────────────────────────────────────────────────────────

class HomeScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("content_area")
        self._build_ui()
        self._start_clock()

    # ── Construction ──────────────────────────────────────────────────────────

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 32, 32, 32)
        root.setSpacing(24)

        root.addLayout(self._header_section())
        root.addWidget(self._search_bar())
        root.addLayout(self._stats_section())
        root.addWidget(self._activity_section())
        root.addStretch()

    def _header_section(self) -> QHBoxLayout:
        layout = QHBoxLayout()

        left = QVBoxLayout()
        left.setSpacing(4)

        self.greeting_lbl = QLabel(self._greeting())
        self.greeting_lbl.setObjectName("title_label")
        self.greeting_lbl.setFont(AppFont.display(size=26))

        self.clock_lbl = QLabel()
        self.clock_lbl.setObjectName("subtitle_label")
        self.clock_lbl.setFont(AppFont.body(size=12))
        self._update_clock()

        left.addWidget(self.greeting_lbl)
        left.addWidget(self.clock_lbl)
        layout.addLayout(left)
        layout.addStretch()

        # Button
        button = TrackerButton(label='Start Watcher')
        button.clicked.connect(button.toggle)
        layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignVCenter)
        # Badge "Aujourd'hui actif"
        
        badge = QLabel("● Session active")
        badge.setFont(AppFont.caption(size=10))
        badge.setStyleSheet(
            f"color: {Colors.ACCENT_3}; background: rgba(107,203,119,0.15);"
            f"border-radius: 10px; padding: 4px 12px;"
        )
        if button.is_running:
            layout.addWidget(badge, alignment=Qt.AlignmentFlag.AlignVCenter)
        return layout

    def _search_bar(self) -> QLineEdit:
        bar = QLineEdit()
        bar.setObjectName("search_bar")
        bar.setPlaceholderText("🔍  Rechercher dans vos captures…")
        bar.setFont(AppFont.body(size=12))
        bar.setFixedHeight(42)
        return bar

    def _stats_section(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        #layout.setSpacing(16)

        stats = [
            #("📸", "Captures aujourd'hui",  "0",   "stat_card_red",   Colors.ACCENT_1),
            ("🗂️",  "Sessions mémorisées",   "1000",   "stat_card_blue",  Colors.ACCENT_4),
            ("⚡",  "Actions détectées",     "1000",   "stat_card_green", Colors.ACCENT_3),
            ("🕐",  "Temps de suivi",        "1000", "stat_card_gold",  Colors.ACCENT_2),
        ]
        for icon, label, value, obj_name, accent in stats:
            card = StatCard(icon, label, value, obj_name, accent)
            layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)

        return layout

    def _activity_section(self) -> QWidget:
        container = QWidget()
        container.setObjectName("card")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        header = QHBoxLayout()
        title = QLabel("📋  Activité récente")
        title.setFont(AppFont.heading(size=14))
        title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        see_all = QLabel("Tout voir →")
        see_all.setFont(AppFont.caption(size=11))
        see_all.setStyleSheet(f"color: {Colors.ACCENT_4}; cursor: pointer;")
        see_all.setCursor(Qt.CursorShape.PointingHandCursor)
        header.addWidget(title)
        header.addStretch()
        header.addWidget(see_all)

        layout.addLayout(header)
        layout.addWidget(h_divider())

        # Placeholder items
        empty = QLabel("Aucune activité capturée pour l'instant.\nChronik AI commence à surveiller dès que vous travaillez. ✨")
        empty.setFont(AppFont.body(size=12))
        empty.setStyleSheet(f"color: {Colors.TEXT_MUTED};")
        empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty.setFixedHeight(80)
        layout.addWidget(empty)

        return container

    # ── Clock ─────────────────────────────────────────────────────────────────

    def _start_clock(self):
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_clock)
        self._timer.start(1000)

    def _update_clock(self):
        now = QDateTime.currentDateTime()
        self.clock_lbl.setText(now.toString("dddd d MMMM yyyy  •  hh:mm:ss"))

    @staticmethod
    def _greeting() -> str:
        hour = QDateTime.currentDateTime().time().hour()
        if hour < 12:
            return "Bonjour, Utilisateur 👋"
        elif hour < 18:
            return "Bon après-midi, Utilisateur ☀️"
        else:
            return "Bonsoir, Utilisateur 🌙"