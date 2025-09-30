import sqlite3
from datetime import datetime
from typing import List, Dict, Optional


class QuestionDatabase:
    """Database manager for storing and retrieving questions."""

    def __init__(self, db_path: str = "questions.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                difficulty INTEGER DEFAULT 3,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

    def add_question(self, subject: str, question: str, answer: str, difficulty: int = 3):
        """Add a new question to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO questions (subject, question, answer, difficulty)
            VALUES (?, ?, ?, ?)
        """, (subject, question, answer, difficulty))

        conn.commit()
        question_id = cursor.lastrowid
        conn.close()
        return question_id

    def get_questions(self, subject: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """Retrieve questions from the database."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if subject:
            cursor.execute("""
                SELECT * FROM questions
                WHERE subject = ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (subject, limit))
        else:
            cursor.execute("""
                SELECT * FROM questions
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,))

        rows = cursor.fetchall()
        questions = [dict(row) for row in rows]
        conn.close()
        return questions

    def get_random_questions(self, subject: Optional[str] = None, count: int = 5) -> List[Dict]:
        """Get random questions for practice."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if subject:
            cursor.execute("""
                SELECT * FROM questions
                WHERE subject = ?
                ORDER BY RANDOM()
                LIMIT ?
            """, (subject, count))
        else:
            cursor.execute("""
                SELECT * FROM questions
                ORDER BY RANDOM()
                LIMIT ?
            """, (count,))

        rows = cursor.fetchall()
        questions = [dict(row) for row in rows]
        conn.close()
        return questions
