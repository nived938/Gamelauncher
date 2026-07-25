from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QStackedWidget,
    QFrame,
)

from config import *

from ui.pages.home_page import HomePage
from ui.pages.add_game_page import AddGamePage
from ui.pages.game_page import GamePage
from ui.pages.settings_page import SettingsPage
from ui.pages.requirements_page import RequirementsPage



class LauncherWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setup_window()

        self.build_ui()


    # ------------------------------------------------

    def setup_window(self):

        self.setWindowTitle(
            APP_NAME
        )

        self.resize(
            WINDOW_WIDTH,
            WINDOW_HEIGHT
        )

        self.setMinimumSize(
            MIN_WIDTH,
            MIN_HEIGHT
        )


    # ------------------------------------------------

    def build_ui(self):

        central = QWidget()

        self.setCentralWidget(
            central
        )


        root = QHBoxLayout(
            central
        )

        root.setContentsMargins(
            0,
            0,
            0,
            0
        )

        root.setSpacing(0)



        # ============================
        # SIDEBAR
        # ============================


        sidebar = QFrame()

        sidebar.setFixedWidth(
            240
        )


        sidebar_layout = QVBoxLayout(
            sidebar
        )


        sidebar_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )


        sidebar_layout.setSpacing(
            20
        )


        logo = QLabel(
            "POWERPLAY"
        )


        logo.setFont(
            QFont(
                FONT,
                20,
                QFont.Bold
            )
        )


        sidebar_layout.addWidget(
            logo
        )



        self.menu = QListWidget()


        self.menu.addItem(
            QListWidgetItem(
                "🏠 Home"
            )
        )


        self.menu.addItem(
            QListWidgetItem(
                "➕ Add Game"
            )
        )


        self.menu.addItem(
            QListWidgetItem(
                "⚙ Settings"
            )
        )


        self.menu.setCurrentRow(
            0
        )


        sidebar_layout.addWidget(
            self.menu
        )


        sidebar_layout.addStretch()



        version = QLabel(
            f"v{APP_VERSION}"
        )


        version.setAlignment(
            Qt.AlignCenter
        )


        sidebar_layout.addWidget(
            version
        )



        # ============================
        # PAGES
        # ============================


        self.pages = QStackedWidget()



        self.home = HomePage()


        self.add_game = AddGamePage()


        self.game_page = GamePage()


        self.requirements = RequirementsPage()


        self.settings = SettingsPage()



        self.pages.addWidget(
            self.home
        )


        self.pages.addWidget(
            self.add_game
        )


        self.pages.addWidget(
            self.game_page
        )


        self.pages.addWidget(
            self.requirements
        )


        self.pages.addWidget(
            self.settings
        )



        root.addWidget(
            sidebar
        )


        root.addWidget(
            self.pages
        )



        # ============================
        # CONNECTIONS
        # ============================


        self.menu.currentRowChanged.connect(
            self.menu_changed
        )


        # Home

        self.home.add_game_requested.connect(
            self.open_add_game
        )


        self.home.game_selected.connect(
            self.open_game
        )

        # Delete Game

        self.game_page.game_deleted.connect(
            self.game_deleted
        )



        # Add Game

        self.add_game.back_requested.connect(
            self.open_home
        )


        self.add_game.game_added.connect(
            self.game_added
        )



        # Game Page

        self.game_page.back_requested.connect(
            self.open_home
        )


        self.game_page.requirements_requested.connect(
            self.open_requirements
        )



        # Requirements

        self.requirements.back_requested.connect(
            self.back_from_requirements
        )


        self.requirements.saved.connect(
            self.refresh_game_page
        )



        # Settings

        self.settings.back_requested.connect(
            self.open_home
        )



        # ============================
        # STYLE
        # ============================


        self.setStyleSheet(f"""

        QMainWindow{{
            background:{BACKGROUND};
        }}


        QWidget{{
            background:{BACKGROUND};
            color:{TEXT};
            font-family:{FONT};
        }}


        QFrame{{
            background:{SURFACE};
            border-right:1px solid {BORDER};
        }}


        QListWidget{{
            background:transparent;
            border:none;
            outline:none;
        }}


        QListWidget::item{{
            padding:14px;
            border-radius:10px;
            margin:5px;
            font-size:15px;
        }}


        QListWidget::item:selected{{
            background:{ACCENT};
        }}


        QListWidget::item:hover{{
            background:{CARD_HOVER};
        }}

        """)



    # ------------------------------------------------

    def menu_changed(
        self,
        index
    ):

        if index == 0:

            self.open_home()


        elif index == 1:

            self.open_add_game()


        elif index == 2:

            self.pages.setCurrentWidget(
                self.settings
            )



    # ------------------------------------------------

    def open_home(self):

        self.home.refresh()


        self.pages.setCurrentWidget(
            self.home
        )


        self.menu.setCurrentRow(
            0
        )



    # ------------------------------------------------

    def open_add_game(self):

        self.pages.setCurrentWidget(
            self.add_game
        )


        self.menu.setCurrentRow(
            1
        )



    # ------------------------------------------------

    def open_game(
        self,
        game_id
    ):

        self.game_page.load_game(
            game_id
        )


        self.pages.setCurrentWidget(
            self.game_page
        )



    # ------------------------------------------------

    def open_requirements(self):

        self.requirements.load_game(
            self.game_page.game_id
        )


        self.pages.setCurrentWidget(
            self.requirements
        )



    # ------------------------------------------------

    def back_from_requirements(self):

        self.game_page.load_game(
            self.game_page.game_id
        )


        self.pages.setCurrentWidget(
            self.game_page
        )



    # ------------------------------------------------

    def refresh_game_page(self):

        self.game_page.load_game(
            self.game_page.game_id
        )



    # ------------------------------------------------

    def game_added(self):

        self.home.refresh()

        self.open_home()

    def game_deleted(self):

        self.home.refresh()

        self.open_home()