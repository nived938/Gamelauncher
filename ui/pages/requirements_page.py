from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QLineEdit,
    QFormLayout,
    QMessageBox
)

from database import Database



class RequirementsPage(QWidget):

    back_requested = Signal()

    saved = Signal()


    def __init__(self):

        super().__init__()

        self.db = Database()

        self.game_id = None

        self.setup_ui()



    # ---------------------------------------------

    def setup_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            50,
            50,
            50,
            50
        )

        layout.setSpacing(25)



        title = QLabel(
            "System Requirements"
        )

        title.setStyleSheet("""
        font-size:32px;
        font-weight:bold;
        """)


        layout.addWidget(
            title
        )



        self.form = QFormLayout()



        self.cpu_input = QLineEdit()

        self.gpu_input = QLineEdit()

        self.ram_input = QLineEdit()

        self.storage_input = QLineEdit()



        self.cpu_input.setPlaceholderText(
            "Example: Intel i5 10400"
        )

        self.gpu_input.setPlaceholderText(
            "Example: RTX 3060"
        )

        self.ram_input.setPlaceholderText(
            "Example: 16 GB"
        )

        self.storage_input.setPlaceholderText(
            "Example: 100 GB SSD"
        )



        self.form.addRow(
            "CPU",
            self.cpu_input
        )

        self.form.addRow(
            "GPU",
            self.gpu_input
        )

        self.form.addRow(
            "RAM",
            self.ram_input
        )

        self.form.addRow(
            "Storage",
            self.storage_input
        )



        layout.addLayout(
            self.form
        )


        layout.addStretch()



        self.save_button = QPushButton(
            "Save Requirements"
        )


        self.back_button = QPushButton(
            "← Back"
        )


        self.save_button.clicked.connect(
            self.save_requirements
        )


        self.back_button.clicked.connect(
            self.back
        )



        layout.addWidget(
            self.save_button
        )

        layout.addWidget(
            self.back_button
        )



        self.setStyleSheet("""
        
        QWidget{

            background:#0D1117;
            color:white;

        }


        QLineEdit{

            background:#161B22;

            border:1px solid #30363D;

            border-radius:12px;

            padding:12px;

            color:white;

        }


        QPushButton{

            background:#3B82F6;

            border:none;

            border-radius:12px;

            padding:12px;

            color:white;

            font-weight:bold;

        }


        QPushButton:hover{

            background:#60A5FA;

        }

        """)



    # ---------------------------------------------

    def load_game(
        self,
        game_id
    ):

        self.game_id = game_id


        game = self.db.get_game(
            game_id
        )


        if game:

            self.cpu_input.setText(
                game["cpu"] or ""
            )

            self.gpu_input.setText(
                game["gpu"] or ""
            )

            self.ram_input.setText(
                game["ram"] or ""
            )

            self.storage_input.setText(
                game["storage"] or ""
            )



    # ---------------------------------------------

    def save_requirements(self):

        if not self.game_id:

            return



        self.db.update_requirements(

            self.game_id,

            self.cpu_input.text(),

            self.gpu_input.text(),

            self.ram_input.text(),

            self.storage_input.text()

        )


        QMessageBox.information(

            self,

            "Saved",

            "System requirements updated."

        )


        self.saved.emit()

        self.back()



    # ---------------------------------------------

    def back(self):

        self.back_requested.emit()