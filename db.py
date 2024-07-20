import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self._create_users_table()

    def _create_users_table(self):
        with self.connection:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    full_name TEXT NOT NULL
                )
            ''')

    def add(self, user_id: int, user_fullname: str):
        with self.connection:   # Bu qator //self.connection// yordamida ma'lumotlar bazasiga ulanishni ochadi va bu kontekst menejer yordamida amalga oshiriladi. Bu usul ulanishni avtomatik ravishda yopadi, hatto funksiyada xatolik yuz bersa ham.
            return self.cursor.execute(
                "INSERT INTO users (user_id, full_name) VALUES (?, ?)",
                (user_id, user_fullname)
            )

    def get_all_users(self):
        with self.connection:
            return self.cursor.execute("SELECT user_id, full_name FROM users").fetchall()

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchmany(1)
            return bool(len(result))

# Usage
# DB_URL = os.getenv('DB_URL')
# database = Database(DB_URL)
