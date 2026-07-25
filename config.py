"""
PowerPlay Launcher
Configuration File
"""

import os

# --------------------------------------------------
# APP INFORMATION
# --------------------------------------------------

APP_NAME = "PowerPlay Launcher"
APP_VERSION = "1.0.0"

# --------------------------------------------------
# WINDOW
# --------------------------------------------------

WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 900

MIN_WIDTH = 1200
MIN_HEIGHT = 700

# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ASSETS_DIR = os.path.join(BASE_DIR, "assets")

ICONS_DIR = os.path.join(ASSETS_DIR, "icons")

IMAGES_DIR = os.path.join(ASSETS_DIR, "images")

COVERS_DIR = os.path.join(BASE_DIR, "covers")

DATABASE_DIR = os.path.join(BASE_DIR, "database")

DATABASE_FILE = os.path.join(
    DATABASE_DIR,
    "games.db"
)

# Create folders automatically

os.makedirs(COVERS_DIR, exist_ok=True)
os.makedirs(DATABASE_DIR, exist_ok=True)

# --------------------------------------------------
# COLORS
# --------------------------------------------------

BACKGROUND = "#0D1117"

SURFACE = "#161B22"

CARD = "#1C2128"

CARD_HOVER = "#252C36"

ACCENT = "#3B82F6"

ACCENT_HOVER = "#60A5FA"

SUCCESS = "#22C55E"

DANGER = "#EF4444"

WARNING = "#F59E0B"

TEXT = "#FFFFFF"

TEXT_SECONDARY = "#A8B3C7"

BORDER = "#30363D"

# --------------------------------------------------
# GAME CARD
# --------------------------------------------------

CARD_WIDTH = 220

CARD_HEIGHT = 320

CARD_RADIUS = 18

COVER_WIDTH = 200

COVER_HEIGHT = 250

# --------------------------------------------------
# BUTTONS
# --------------------------------------------------

BUTTON_HEIGHT = 46

BUTTON_RADIUS = 12

# --------------------------------------------------
# ANIMATION
# --------------------------------------------------

HOVER_ANIMATION = 180

PAGE_ANIMATION = 250

CARD_SCALE = 1.04

# --------------------------------------------------
# FONTS
# --------------------------------------------------

FONT = "Segoe UI"

TITLE_SIZE = 28

SUBTITLE_SIZE = 18

BODY_SIZE = 13

SMALL_SIZE = 11