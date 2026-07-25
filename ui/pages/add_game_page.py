from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QMessageBox,
)

import os
import shutil

from database import Database
from config import COVERS_DIR


class AddGamePage(QWidget):

    game_added = Signal()

    back_requested = Signal()


    def __init__(self):

        super().__init__()

        self.db = Database()

        self.cover_path = ""

        self.exe_path = ""

        self.setup_ui()


    # -------------------------------------------------

    def setup_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            40,
            40,
            40,
            40
        )

        layout.setSpacing(18)


        # Title

        title = QLabel(
            "Add New Game"
        )

        title.setStyleSheet("""
        font-size:32px;
        font-weight:bold;
        """)

        layout.addWidget(title)


        # Cover Preview

        self.cover_preview = QLabel(
            "No Cover"
        )

        self.cover_preview.setFixedSize(
            220,
            300
        )

        self.cover_preview.setAlignment(
            Qt.AlignCenter
        )

        self.cover_preview.setStyleSheet("""
        background:#1C2128;
        border:2px dashed #3B82F6;
        border-radius:18px;
        color:#A8B3C7;
        font-size:16px;
        """)


        layout.addWidget(
            self.cover_preview,
            alignment=Qt.AlignCenter
        )


        self.cover_button = QPushButton(
            "Upload Cover Image"
        )

        self.cover_button.clicked.connect(
            self.choose_cover
        )


        layout.addWidget(
            self.cover_button
        )


        # Game Name

        self.name_input = QLineEdit()

        self.name_input.setPlaceholderText(
            "Game Name"
        )

        layout.addWidget(
            self.name_input
        )


        # Description

        self.description_input = QTextEdit()

        self.description_input.setPlaceholderText(
            "Game Description"
        )

        self.description_input.setFixedHeight(
            120
        )

        layout.addWidget(
            self.description_input
        )


        # EXE

        exe_layout = QHBoxLayout()


        self.exe_input = QLineEdit()

        self.exe_input.setPlaceholderText(
            "Game executable (.exe)"
        )


        browse = QPushButton(
            "Browse"
        )

        browse.clicked.connect(
            self.choose_exe
        )


        exe_layout.addWidget(
            self.exe_input
        )

        exe_layout.addWidget(
            browse
        )


        layout.addLayout(
            exe_layout
        )


        layout.addStretch()


        # Buttons

        buttons = QHBoxLayout()


        back = QPushButton(
            "← Back"
        )

        save = QPushButton(
            "Save Game"
        )


        back.clicked.connect(
            self.back_requested.emit
        )


        save.clicked.connect(
            self.save_game
        )


        buttons.addWidget(
            back
        )

        buttons.addStretch()

        buttons.addWidget(
            save
        )


        layout.addLayout(
            buttons
        )


        self.setStyleSheet("""
        
        QWidget{
            color:white;
            background:#0D1117;
            font-size:14px;
        }

        QLineEdit,
        QTextEdit{

            background:#161B22;

            border:1px solid #30363D;

            border-radius:12px;

            padding:12px;

            color:white;

        }


        QPushButton{

            background:#3B82F6;

            color:white;

            border:none;

            border-radius:12px;

            padding:12px 20px;

            font-weight:bold;

        }


        QPushButton:hover{

            background:#60A5FA;

        }

        """)


    # -------------------------------------------------

    def choose_cover(self):

        file, _ = QFileDialog.getOpenFileName(

            self,

            "Choose Cover",

            "",

            "Images (*.png *.jpg *.jpeg *.webp)"

        )


        if file:

            self.cover_path = file


            image = QPixmap(file)


            self.cover_preview.setPixmap(

                image.scaled(

                    220,
                    300,
                    Qt.KeepAspectRatioByExpanding,
                    Qt.SmoothTransformation

                )

            )


    # -------------------------------------------------

    def choose_exe(self):

        file, _ = QFileDialog.getOpenFileName(

            self,

            "Choose Game Executable",

            "",

            "Executable (*.exe)"

        )


        if file:

            self.exe_path = file

            self.exe_input.setText(
                file
            )


    # -------------------------------------------------

    def save_game(self):

        name = self.name_input.text().strip()

        description = (
            self.description_input
            .toPlainText()
            .strip()
        )


        if not name:

            QMessageBox.warning(
                self,
                "Missing Information",
                "Please enter a game name."
            )

            return


        if not self.exe_path:

            QMessageBox.warning(
                self,
                "Missing Information",
                "Please select the game executable."
            )

            return



        # Copy cover into launcher folder

        saved_cover = ""


        if self.cover_path:

            filename = os.path.basename(self.cover_path)

            destination = os.path.join(
                COVERS_DIR,
                filename
            )

            # Normalize both paths
            source = os.path.abspath(self.cover_path)
            destination = os.path.abspath(destination)

            # Only copy if they are different files
            if source != destination:
                shutil.copy(source, destination)

            saved_cover = destination



        # Find game folder

        folder = os.path.dirname(
            self.exe_path
        )


        self.db.add_game(

            name,

            description,

            saved_cover,

            self.exe_path,

            folder

        )


        QMessageBox.information(

            self,

            "Success",

            "Game added successfully!"

        )


        self.clear_form()


        self.game_added.emit()



    # -------------------------------------------------

    def clear_form(self):

        self.name_input.clear()

        self.description_input.clear()

        self.exe_input.clear()

        self.cover_preview.setText(
            "No Cover"
        )

        self.cover_preview.setPixmap(
            QPixmap()
        )

        self.cover_path = ""

        self.exe_path = ""