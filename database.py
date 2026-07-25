"""
PowerPlay Launcher
SQLite Database Manager
"""

import sqlite3
from config import DATABASE_FILE


class Database:

    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_FILE)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

        self.create_tables()

    # -------------------------------------------------
    # Create Tables
    # -------------------------------------------------

    def create_tables(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS games(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            description TEXT,

            cover TEXT,

            exe TEXT,

            folder TEXT,

            cpu TEXT,

            gpu TEXT,

            ram TEXT,

            storage TEXT,

            play_time INTEGER DEFAULT 0,

            last_played TEXT,

            favorite INTEGER DEFAULT 0

        )
        """)

        self.connection.commit()

    # -------------------------------------------------
    # Add Game
    # -------------------------------------------------

    def add_game(
        self,
        name,
        description,
        cover,
        exe,
        folder,
        cpu="",
        gpu="",
        ram="",
        storage=""
    ):

        self.cursor.execute(
            """
            INSERT INTO games(

                name,
                description,
                cover,
                exe,
                folder,
                cpu,
                gpu,
                ram,
                storage

            )

            VALUES(?,?,?,?,?,?,?,?,?)

            """,

            (
                name,
                description,
                cover,
                exe,
                folder,
                cpu,
                gpu,
                ram,
                storage
            )

        )

        self.connection.commit()

    # -------------------------------------------------
    # Get All Games
    # -------------------------------------------------

    def get_games(self):

        self.cursor.execute("""

        SELECT *

        FROM games

        ORDER BY name

        """)

        return self.cursor.fetchall()

    # -------------------------------------------------
    # Get One Game
    # -------------------------------------------------

    def get_game(self, game_id):

        self.cursor.execute(

            """

            SELECT *

            FROM games

            WHERE id=?

            """,

            (game_id,)

        )

        return self.cursor.fetchone()

    # -------------------------------------------------
    # Update Game
    # -------------------------------------------------

    def update_game(

        self,

        game_id,

        name,

        description,

        cover,

        exe,

        folder

    ):

        self.cursor.execute(

            """

            UPDATE games

            SET

            name=?,

            description=?,

            cover=?,

            exe=?,

            folder=?

            WHERE id=?

            """,

            (

                name,

                description,

                cover,

                exe,

                folder,

                game_id

            )

        )

        self.connection.commit()

    # -------------------------------------------------
    # Update Requirements
    # -------------------------------------------------

    def update_requirements(

        self,

        game_id,

        cpu,

        gpu,

        ram,

        storage

    ):

        self.cursor.execute(

            """

            UPDATE games

            SET

            cpu=?,

            gpu=?,

            ram=?,

            storage=?

            WHERE id=?

            """,

            (

                cpu,

                gpu,

                ram,

                storage,

                game_id

            )

        )

        self.connection.commit()

    # -------------------------------------------------
    # Favorite
    # -------------------------------------------------

    def set_favorite(

        self,

        game_id,

        favorite

    ):

        self.cursor.execute(

            """

            UPDATE games

            SET favorite=?

            WHERE id=?

            """,

            (

                favorite,

                game_id

            )

        )

        self.connection.commit()

    # -------------------------------------------------
    # Delete
    # -------------------------------------------------

    def delete_game(

        self,

        game_id

    ):

        self.cursor.execute(

            """

            DELETE FROM games

            WHERE id=?

            """,

            (game_id,)

        )

        self.connection.commit()

    # -------------------------------------------------
    # Update Play Time
    # -------------------------------------------------

    def update_play_time(

        self,

        game_id,

        minutes

    ):

        self.cursor.execute(

            """

            UPDATE games

            SET play_time=play_time+?

            WHERE id=?

            """,

            (

                minutes,

                game_id

            )

        )

        self.connection.commit()

    # -------------------------------------------------
    # Close
    # -------------------------------------------------

    def close(self):

        self.connection.close()

    def delete_game(self, game_id):

        self.cursor.execute(
            "DELETE FROM games WHERE id = ?",
            (game_id,)
        )

        self.connection.commit()