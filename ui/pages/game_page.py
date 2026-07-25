from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QMessageBox
)

import subprocess
import os

from database import Database



class GamePage(QWidget):

    back_requested = Signal()

    requirements_requested = Signal()

    game_deleted = Signal()


    def __init__(self):

        super().__init__()

        self.db = Database()

        self.game_id = None

        self.game = None

        self.setup_ui()



    # -------------------------------------------------

    def setup_ui(self):

        main = QVBoxLayout(self)

        main.setContentsMargins(
            40,
            40,
            40,
            40
        )

        main.setSpacing(
            25
        )


        # Back

        top_bar = QHBoxLayout()

        back = QPushButton("← Back")
        back.clicked.connect(self.back_requested.emit)

        delete = QPushButton("🗑 Delete Game")

        delete.setStyleSheet("""
        QPushButton{
            background:#D32F2F;
            color:white;
            border:none;
            border-radius:10px;
            padding:10px 20px;
            font-weight:bold;
        }

        QPushButton:hover{
            background:#F44336;
        }
        """)

        delete.clicked.connect(
            self.delete_game
        )

        top_bar.addWidget(back)

        top_bar.addStretch()

        top_bar.addWidget(delete)

        main.addLayout(top_bar)


        # Top section

        top = QHBoxLayout()

        top.setSpacing(
            30
        )


        # Cover

        self.cover = QLabel(
            "No Cover"
        )

        self.cover.setFixedSize(
            300,
            420
        )

        self.cover.setAlignment(
            Qt.AlignCenter
        )

        self.cover.setStyleSheet("""
        background:#161B22;
        border-radius:20px;
        """)


        top.addWidget(
            self.cover
        )



        # Info

        info = QVBoxLayout()


        self.title = QLabel(
            "Game Name"
        )

        self.title.setStyleSheet("""
        font-size:34px;
        font-weight:bold;
        """)



        self.description = QLabel(
            "Description"
        )

        self.description.setWordWrap(
            True
        )

        self.description.setStyleSheet("""
        font-size:16px;
        color:#A8B3C7;
        """)



        self.play_button = QPushButton(
            "▶ Launch Game"
        )

        self.play_button.clicked.connect(
            self.launch_game
        )



        self.folder_button = QPushButton(
            "📁 Open Game Folder"
        )

        self.folder_button.clicked.connect(
            self.open_folder
        )



        info.addWidget(
            self.title
        )

        info.addSpacing(
            20
        )

        info.addWidget(
            self.description
        )

        info.addStretch()

        info.addWidget(
            self.play_button
        )

        info.addWidget(
            self.folder_button
        )


        top.addLayout(
            info
        )


        main.addLayout(
            top
        )



        # Requirements Box


        box = QFrame()


        box.setStyleSheet("""
        
        QFrame{

            background:#161B22;

            border-radius:20px;

        }

        """)


        req_layout = QVBoxLayout(
            box
        )


        req_title = QLabel(
            "System Requirements"
        )


        req_title.setStyleSheet("""
        font-size:22px;
        font-weight:bold;
        """)


        req_layout.addWidget(
            req_title
        )



        self.cpu = QLabel()

        self.gpu = QLabel()

        self.ram = QLabel()

        self.storage = QLabel()



        req_layout.addWidget(
            self.cpu
        )

        req_layout.addWidget(
            self.gpu
        )

        req_layout.addWidget(
            self.ram
        )

        req_layout.addWidget(
            self.storage
        )



        edit = QPushButton(
            "Add / Edit Requirements"
        )


        edit.clicked.connect(
            self.open_requirements
        )


        req_layout.addWidget(
            edit
        )


        main.addWidget(
            box
        )



        self.setStyleSheet("""
        
        QWidget{

            background:#0D1117;

            color:white;

        }


        QPushButton{

            background:#3B82F6;

            color:white;

            border:none;

            border-radius:12px;

            padding:12px;

            font-weight:bold;

        }


        QPushButton:hover{

            background:#60A5FA;

        }

        """)



    # -------------------------------------------------

    def load_game(
        self,
        game_id
    ):

        self.game_id = game_id


        self.game = self.db.get_game(
            game_id
        )


        if not self.game:

            return



        self.title.setText(
            self.game["name"]
        )


        self.description.setText(

            self.game["description"]

            if self.game["description"]

            else

            "No description available."

        )



        # Cover

        image = QPixmap(
            self.game["cover"]
        )


        if not image.isNull():

            self.cover.setPixmap(

                image.scaled(

                    300,

                    420,

                    Qt.KeepAspectRatioByExpanding,

                    Qt.SmoothTransformation

                )

            )


        else:

            self.cover.setText(
                "No Cover"
            )



        # Requirements


        self.cpu.setText(

            "CPU: "

            + (self.game["cpu"] or "Not Added")

        )


        self.gpu.setText(

            "GPU: "

            + (self.game["gpu"] or "Not Added")

        )


        self.ram.setText(

            "RAM: "

            + (self.game["ram"] or "Not Added")

        )


        self.storage.setText(

            "Storage: "

            + (self.game["storage"] or "Not Added")

        )



    # -------------------------------------------------

    def launch_game(self):

        if not self.game:

            return


        exe = self.game["exe"]


        if os.path.exists(exe):

            subprocess.Popen(
                exe
            )

        else:

            QMessageBox.warning(

                self,

                "Error",

                "Game executable was not found."

            )



    # -------------------------------------------------

    def open_folder(self):

        if not self.game:

            return


        folder = self.game["folder"]


        if os.path.exists(folder):

            os.startfile(
                folder
            )



    # -------------------------------------------------

    def open_requirements(self):

        self.requirements_requested.emit()

    def delete_game(self):

        if not self.game:

            return

        answer = QMessageBox.question(

            self,

            "Delete Game",

            f"Delete '{self.game['name']}' from your library?",

            QMessageBox.Yes | QMessageBox.No

        )

        if answer != QMessageBox.Yes:

            return

        self.db.delete_game(
            self.game_id
        )

        self.game_deleted.emit()