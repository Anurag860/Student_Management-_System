import sqlite3
from utils.crypto import encrypt_name, decrypt_name

class SQLiteDB:
    def __init__(self, db_path):
        self.db_path = db_path
        self._create_student_table()
        self._create_users_table()  # Call it during initialization

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _create_student_table(self):
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    age INTEGER,
                    course TEXT
                )
            """)

    def _create_users_table(self):
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            """)

    def add_student(self, student):
        with self._connect() as conn:
            encrypted_name = encrypt_name(student['name'])
            conn.execute("INSERT INTO students VALUES (?, ?, ?, ?)",
                         (student['id'], encrypted_name, student['age'], student['course']))

    def get_all_students(self):
        with self._connect() as conn:
            students = conn.execute("SELECT * FROM students").fetchall()
            return [(s[0], decrypt_name(s[1]), s[2], s[3]) for s in students]

    def get_student_by_id(self, student_id):
        with self._connect() as conn:
            s = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
            if s:
                return (s[0], decrypt_name(s[1]), s[2], s[3])
            return None

    def update_student(self, student):
        with self._connect() as conn:
            encrypted_name = encrypt_name(student['name'])
            conn.execute("UPDATE students SET name = ?, age = ?, course = ? WHERE id = ?",
                         (encrypted_name, student['age'], student['course'], student['id']))

    def delete_student(self, student_id):
        with self._connect() as conn:
            conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
