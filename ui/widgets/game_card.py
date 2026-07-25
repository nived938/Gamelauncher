from PySide6.QtCore import (
    Qt,
    Signal,
    QPropertyAnimation,
    QEasingCurve,
    QRect,
)

from PySide6.QtGui import (
    QPixmap,
    QColor,
)

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QGraphicsDropShadowEffect,
)


from config import *


class GameCard(QWidget):

    clicked = Signal(int)

    play_clicked = Signal(int)


    def __init__(
        self,
        game_id,
        title,
        cover_path
    ):

        super().__init__()

        self.game_id = game_id

        self.title_text = title

        self.cover_path = cover_path

        self.setFixedSize(
            250,
            380
        )

        self.setCursor(
            Qt.PointingHandCursor
        )

        self.setMouseTracking(True)

        self.setup_ui()

        self.setup_animations()


    # ---------------------------------------------------------

    def setup_ui(self):

        # ==========================
        # Card Background
        # ==========================

        self.card = QWidget(self)

        self.card.setGeometry(
            0,
            0,
            250,
            380
        )

        self.card.setStyleSheet(f"""
        QWidget{{
            background:{CARD};
            border-radius:22px;
        }}
        """)


        # ==========================
        # Shadow
        # ==========================

        self.shadow = QGraphicsDropShadowEffect()

        self.shadow.setBlurRadius(30)

        self.shadow.setOffset(
            0,
            8
        )

        self.shadow.setColor(
            QColor(
                0,
                0,
                0,
                160
            )
        )

        self.card.setGraphicsEffect(
            self.shadow
        )


        # ==========================
        # Cover
        # ==========================

        self.cover = QLabel(
            self.card
        )

        self.cover.setGeometry(
            15,
            15,
            220,
            280
        )

        self.cover.setAlignment(
            Qt.AlignCenter
        )

        self.cover.setStyleSheet("""
        background:#1A1A1A;
        border-radius:18px;
        """)


        pix = QPixmap(
            self.cover_path
        )

        if not pix.isNull():

            self.cover.setPixmap(

                pix.scaled(

                    self.cover.size(),

                    Qt.KeepAspectRatioByExpanding,

                    Qt.SmoothTransformation

                )

            )

        else:

            self.cover.setText(
                "No Cover"
            )


        # ==========================
        # Dark Overlay
        # ==========================

        self.overlay = QWidget(
            self.cover
        )

        self.overlay.setGeometry(
            0,
            0,
            self.cover.width(),
            self.cover.height()
        )

        self.overlay.setStyleSheet("""
        background:rgba(0,0,0,0);
        border-radius:18px;
        """)

                # ==========================
        # Play Button
        # ==========================

        self.play_button = QPushButton(
            "▶ PLAY",
            self.overlay
        )

        self.play_button.setGeometry(
            25,
            215,
            170,
            46
        )

        self.play_button.setCursor(
            Qt.PointingHandCursor
        )

        self.play_button.setStyleSheet(f"""
        QPushButton{{
            background:{ACCENT};
            color:white;
            border:none;
            border-radius:14px;
            font-size:15px;
            font-weight:bold;
        }}

        QPushButton:hover{{
            background:{ACCENT_HOVER};
        }}

        QPushButton:pressed{{
            background:#2563EB;
        }}
        """)

        self.play_button.clicked.connect(
            lambda: self.play_clicked.emit(self.game_id)
        )



        # ==========================
        # Game Title
        # ==========================

        self.title = QLabel(
            self.title_text,
            self.card
        )

        self.title.setGeometry(
            15,
            310,
            220,
            48
        )

        self.title.setWordWrap(True)

        self.title.setAlignment(
            Qt.AlignCenter
        )

        self.title.setStyleSheet("""
        color:white;
        background:transparent;
        font-size:16px;
        font-weight:700;
        """)



    # ---------------------------------------------------------

    def setup_animations(self):

        # Card zoom

        self.card_anim = QPropertyAnimation(
            self.card,
            b"geometry"
        )

        self.card_anim.setDuration(
            180
        )

        self.card_anim.setEasingCurve(
            QEasingCurve.OutCubic
        )


        # Cover zoom

        self.cover_anim = QPropertyAnimation(
            self.cover,
            b"geometry"
        )

        self.cover_anim.setDuration(
            180
        )

        self.cover_anim.setEasingCurve(
            QEasingCurve.OutCubic
        )


        # Play button slide

        self.play_anim = QPropertyAnimation(
            self.play_button,
            b"geometry"
        )

        self.play_anim.setDuration(
            180
        )

        self.play_anim.setEasingCurve(
            QEasingCurve.OutBack
        )


        self.play_button.setGeometry(
            25,
            245,
            170,
            46
        )

        # ---------------------------------------------------------

    def enterEvent(self, event):

        # Show overlay
        self.overlay.setStyleSheet("""
        background:rgba(0,0,0,110);
        border-radius:18px;
        """)

        # Stronger blue glow
        self.shadow.setBlurRadius(45)

        self.shadow.setOffset(0, 12)

        self.shadow.setColor(
            QColor(
                59,
                130,
                246,
                160
            )
        )

        # Card slightly grows
        self.card_anim.stop()

        self.card_anim.setStartValue(
            self.card.geometry()
        )

        self.card_anim.setEndValue(
            QRect(
                -4,
                -4,
                258,
                388
            )
        )

        self.card_anim.start()

        # Cover grows a little
        self.cover_anim.stop()

        self.cover_anim.setStartValue(
            self.cover.geometry()
        )

        self.cover_anim.setEndValue(
            QRect(
                12,
                12,
                226,
                286
            )
        )

        self.cover_anim.start()

        # Play button slides upward
        self.play_anim.stop()

        self.play_anim.setStartValue(
            self.play_button.geometry()
        )

        self.play_anim.setEndValue(
            QRect(
                25,
                215,
                170,
                46
            )
        )

        self.play_anim.start()

        super().enterEvent(event)

    # ---------------------------------------------------------

    def leaveEvent(self, event):

        self.overlay.setStyleSheet("""
        background:rgba(0,0,0,0);
        border-radius:18px;
        """)

        self.shadow.setBlurRadius(30)

        self.shadow.setOffset(0, 8)

        self.shadow.setColor(
            QColor(
                0,
                0,
                0,
                160
            )
        )

        self.card_anim.stop()

        self.card_anim.setStartValue(
            self.card.geometry()
        )

        self.card_anim.setEndValue(
            QRect(
                0,
                0,
                250,
                380
            )
        )

        self.card_anim.start()

        self.cover_anim.stop()

        self.cover_anim.setStartValue(
            self.cover.geometry()
        )

        self.cover_anim.setEndValue(
            QRect(
                15,
                15,
                220,
                280
            )
        )

        self.cover_anim.start()

        self.play_anim.stop()

        self.play_anim.setStartValue(
            self.play_button.geometry()
        )

        self.play_anim.setEndValue(
            QRect(
                25,
                245,
                170,
                46
            )
        )

        self.play_anim.start()

        super().leaveEvent(event)

    # ---------------------------------------------------------

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:

            # Don't open the game page if the Play button was clicked
            if not self.play_button.geometry().contains(event.pos()):

                self.clicked.emit(
                    self.game_id
                )

        super().mousePressEvent(event)