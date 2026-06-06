from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtCore import Qt


# ─── Palette ────────────────────────────────────────────────────────────────
class Colors:
    BG_DARK       = "#0F0F1A"
    BG_CARD       = "#16162A"
    BG_SIDEBAR    = "#12121F"

    ACCENT_1      = "#FF6B6B"   # coral-red
    ACCENT_2      = "#FFD93D"   # golden yellow
    ACCENT_3      = "#6BCB77"   # mint green
    ACCENT_4      = "#4D96FF"   # electric blue
    ACCENT_PURPLE = "#C77DFF"   # violet

    TEXT_PRIMARY  = "#F0F0FF"
    TEXT_SECONDARY= "#8888AA"
    TEXT_MUTED    = "#44445A"

    GRADIENT_1    = "qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 #FF6B6B,stop:1 #C77DFF)"
    GRADIENT_2    = "qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #4D96FF,stop:1 #6BCB77)"
    GRADIENT_SIDE = "qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #12121F,stop:1 #0F0F1A)"


# ─── Fonts ───────────────────────────────────────────────────────────────────
class AppFont:
    class Weight:
        Regular = QFont.Weight.Normal
        Medium  = QFont.Weight.Medium
        Bold    = QFont.Weight.Bold
        Black   = QFont.Weight.Black

    @staticmethod
    def from_config(size: int = 13, weight=QFont.Weight.Normal, family: str = "Segoe UI") -> QFont:
        font = QFont(family, size)
        font.setWeight(weight)
        font.setHintingPreference(QFont.HintingPreference.PreferFullHinting)
        return font

    @staticmethod
    def display(size: int = 28) -> QFont:
        return AppFont.from_config(size=size, weight=QFont.Weight.Black)

    @staticmethod
    def heading(size: int = 16) -> QFont:
        return AppFont.from_config(size=size, weight=QFont.Weight.Bold)

    @staticmethod
    def body(size: int = 12) -> QFont:
        return AppFont.from_config(size=size, weight=QFont.Weight.Normal)

    @staticmethod
    def caption(size: int = 10) -> QFont:
        return AppFont.from_config(size=size, weight=QFont.Weight.Normal)


# ─── Stylesheet ──────────────────────────────────────────────────────────────
APP_STYLESHEET = f"""
/* ── Root ── */
QMainWindow, QWidget {{
    background-color: {Colors.BG_DARK};
    color: {Colors.TEXT_PRIMARY};
    font-family: "Segoe UI";
}}

/* ── Sidebar ── */
#sidebar {{
    background: {Colors.BG_SIDEBAR};
    border-right: 1px solid {Colors.TEXT_MUTED};
    min-width: 220px;
    max-width: 220px;
}}

/* ── Nav Buttons ── */
#nav_btn {{
    background: transparent;
    color: {Colors.TEXT_SECONDARY};
    border: none;
    border-radius: 10px;
    padding: 10px 18px;
    text-align: left;
    font-size: 13px;
}}
#nav_btn:hover {{
    background: rgba(255,107,107,0.12);
    color: {Colors.ACCENT_1};
}}
#nav_btn[active="true"] {{
    background: rgba(255,107,107,0.18);
    color: {Colors.ACCENT_1};
    font-weight: bold;
    border-left: 3px solid {Colors.ACCENT_1};
}}

/* ── Content Area ── */
#content_area {{
    background: {Colors.BG_DARK};
    padding: 30px;
}}

/* ── Cards ── */
#card {{
    background: {Colors.BG_CARD};
    border-radius: 16px;
    border: 1px solid {Colors.TEXT_MUTED};
    padding: 20px;
}}
#card:hover {{
    border: 1px solid {Colors.ACCENT_4};
}}

/* ── Stat Cards ── */
#stat_card_red   {{ background: rgba(255,107,107,0.15); border: 1px solid {Colors.ACCENT_1}; border-radius: 14px; }}
#stat_card_blue  {{ background: rgba(77,150,255,0.15);  border: 1px solid {Colors.ACCENT_4}; border-radius: 14px; }}
#stat_card_green {{ background: rgba(107,203,119,0.15); border: 1px solid {Colors.ACCENT_3}; border-radius: 14px; }}
#stat_card_gold  {{ background: rgba(255,217,61,0.15);  border: 1px solid {Colors.ACCENT_2}; border-radius: 14px; }}

/* ── Logo Label ── */
#logo_label {{
    color: {Colors.ACCENT_1};
    font-size: 20px;
    font-weight: 900;
    padding: 20px 18px 10px 18px;
    letter-spacing: 2px;
}}

/* ── Title ── */
#title_label {{
    color: {Colors.TEXT_PRIMARY};
    font-size: 26px;
    font-weight: 900;
}}

/* ── Subtitle ── */
#subtitle_label {{
    color: {Colors.TEXT_SECONDARY};
    font-size: 12px;
}}

/* ── Section Header ── */
#section_header {{
    color: {Colors.TEXT_SECONDARY};
    font-size: 10px;
    letter-spacing: 2px;
    padding: 16px 18px 4px 18px;
}}

/* ── Divider ── */
#divider {{
    background: {Colors.TEXT_MUTED};
    max-height: 1px;
    margin: 6px 18px;
}}

/* ── Scrollbar ── */
QScrollBar:vertical {{
    background: {Colors.BG_DARK};
    width: 6px;
    border-radius: 3px;
}}
QScrollBar::handle:vertical {{
    background: {Colors.TEXT_MUTED};
    border-radius: 3px;
    min-height: 30px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}

/* ── Search Bar ── */
#search_bar {{
    background: {Colors.BG_CARD};
    color: {Colors.TEXT_PRIMARY};
    border: 1px solid {Colors.TEXT_MUTED};
    border-radius: 10px;
    padding: 8px 14px;
    font-size: 12px;
}}
#search_bar:focus {{
    border: 1px solid {Colors.ACCENT_4};
    outline: none;
}}

/* ── Activity Item ── */
#activity_item {{
    background: {Colors.BG_CARD};
    border-radius: 10px;
    padding: 10px 14px;
    border: 1px solid transparent;
}}
#activity_item:hover {{
    border: 1px solid {Colors.ACCENT_PURPLE};
}}

/* Button */
#button {{
    border: 1px solid transparent;
    background: rgba(107,203,119,0.15);
    border-radius: 10px; padding: 4px 12px;
    color: {Colors.ACCENT_3}
}}
#button:hover {{
    border-radius: 10px; padding: 4px 12px;
    border: 1px solid {Colors.ACCENT_3};
}}
"""