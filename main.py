import sys

from PySide6.QtWidgets import QApplication

from ui.launcher import LauncherWindow


def main():

    app = QApplication(sys.argv)

    window = LauncherWindow()

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()