import sqlite3
from os import path

class SqlDb:
    def __init__(self, db_file='database.db'):
        # Check if the db file exists
        self.db_file = db_file

        if path.exists(self.db_file):
            print(f"{self.db_file} exists in the current directory.")
        else:
            self.init_db()

    def db_conn(self):
        """Returns a new database connection."""
        return sqlite3.connect(self.db_file)

    def init_db(self):
        """Initializes the database by creating the notes table if it doesn't exist."""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                desc TEXT NOT NULL,
                isImp BOOLEAN DEFAULT 0
            )
            """)
            conn.commit()

