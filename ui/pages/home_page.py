from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLineEdit,
    QScrollArea,
)

from database import Database
from ui.widgets.game_card import GameCard


class HomePage(QWidget):

    add_game_requested = Signal()

    game_selected = Signal(int)

    def __init__(self):

        super().__init__()

        self.db = Database()

        self.cards = []

        self.setup_ui()

        self.load_games()

    # ----------------------------------------

    def setup_ui(self):

        root = QVBoxLayout(self)

        root.setContentsMargins(25, 25, 25, 25)

        root.setSpacing(20)

        # Header

        header = QHBoxLayout()

        title = QLabel("My Library")

        title.setStyleSheet("""
        font-size:30px;
        font-weight:bold;
        """)

        self.search = QLineEdit()

        self.search.setPlaceholderText("Search games...")

        self.search.textChanged.connect(
            self.filter_games
        )

        self.search.setFixedHeight(40)

        self.search.setMaximumWidth(350)

        header.addWidget(title)

        header.addStretch()

        header.addWidget(self.search)

        root.addLayout(header)

        # Scroll Area

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(True)

        self.scroll.setFrameShape(
            QScrollArea.NoFrame
        )

        container = QWidget()

        self.grid = QGridLayout(container)

        self.grid.setSpacing(25)

        self.scroll.setWidget(container)

        root.addWidget(self.scroll)

        # Bottom

        bottom = QHBoxLayout()

        self.add_button = QPushButton("+ Add Game")

        self.add_button.setFixedSize(170, 45)

        self.add_button.clicked.connect(
            self.add_game_requested.emit
        )

        bottom.addWidget(self.add_button)

        bottom.addStretch()

        root.addLayout(bottom)

    # ----------------------------------------

    def clear_cards(self):

        while self.grid.count():

            item = self.grid.takeAt(0)

            if item.widget():

                item.widget().deleteLater()

        self.cards.clear()

    # ----------------------------------------

    def load_games(self):

        self.clear_cards()

        games = self.db.get_games()

        row = 0

        col = 0

        for game in games:

            card = GameCard(

                game["id"],

                game["name"],

                game["cover"]

            )

            card.clicked.connect(

                self.game_selected.emit

            )

            self.cards.append(card)

            self.grid.addWidget(

                card,

                row,

                col

            )

            col += 1

            if col == 5:

                col = 0

                row += 1

    # ----------------------------------------

    def refresh(self):

        self.load_games()

    # ----------------------------------------

    def filter_games(self):

        text = self.search.text().lower()

        for card in self.cards:

            visible = text in card.title_text.lower()

            card.setVisible(visible)