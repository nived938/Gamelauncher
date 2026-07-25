from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QFileDialog
)

import shutil
import os

from config import DATABASE_FILE, APP_NAME, APP_VERSION


class SettingsPage(QWidget):

    back_requested = Signal()


    def __init__(self):

        super().__init__()

        self.setup_ui()


    # ------------------------------------------------

    def setup_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            40,
            40,
            40,
            40
        )

        layout.setSpacing(20)


        title = QLabel(
            "Settings"
        )

        title.setStyleSheet("""
        font-size:32px;
        font-weight:bold;
        """)


        layout.addWidget(
            title
        )


        # Theme

        theme_title = QLabel(
            "Appearance"
        )

        theme_title.setStyleSheet("""
        font-size:20px;
        font-weight:bold;
        """)


        layout.addWidget(
            theme_title
        )


        theme_info = QLabel(
            "Current Theme: Dark Mode"
        )

        theme_info.setStyleSheet("""
        color:#A8B3C7;
        font-size:15px;
        """)


        layout.addWidget(
            theme_info
        )


        # Database Backup

        backup_title = QLabel(
            "Library Backup"
        )

        backup_title.setStyleSheet("""
        font-size:20px;
        font-weight:bold;
        """)


        layout.addWidget(
            backup_title
        )


        backup_button = QPushButton(
            "Create Database Backup"
        )


        backup_button.clicked.connect(
            self.backup_database
        )


        layout.addWidget(
            backup_button
        )


        # Clear Library

        clear_button = QPushButton(
            "Clear All Games"
        )


        clear_button.clicked.connect(
            self.clear_library
        )


        layout.addWidget(
            clear_button
        )


        layout.addStretch()


        # About

        about = QLabel(

            f"""
            {APP_NAME}

            Version: {APP_VERSION}

            A personal game launcher built with Python and PySide6.

            """
        )


        about.setStyleSheet("""
        color:#A8B3C7;
        font-size:14px;
        """)


        layout.addWidget(
            about
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



    # ------------------------------------------------

    def backup_database(self):

        destination, _ = QFileDialog.getSaveFileName(

            self,

            "Save Backup",

            "games_backup.db",

            "Database (*.db)"

        )


        if destination:

            shutil.copy(

                DATABASE_FILE,

                destination

            )


            QMessageBox.information(

                self,

                "Backup Complete",

                "Database backup created successfully."

            )



    # ------------------------------------------------

    def clear_library(self):

        answer = QMessageBox.question(

            self,

            "Confirm",

            "Delete all games from your library?"

        )


        if answer == QMessageBox.Yes:

            import sqlite3


            connection = sqlite3.connect(
                DATABASE_FILE
            )


            cursor = connection.cursor()


            cursor.execute(
                "DELETE FROM games"
            )


            connection.commit()

            connection.close()


            QMessageBox.information(

                self,

                "Library Cleared",

                "All games have been removed."

            )