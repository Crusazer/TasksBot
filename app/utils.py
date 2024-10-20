import sqlite3

from config import settings


def prepare_database():
    with sqlite3.connect(settings.DB_NAME) as db:
        db.execute(
            """CREATE TABLE IF NOT EXISTS task
            (id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            status INTEGER NOT NULL,
            deadline TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )"""
        )
        db.execute(
            """
            CREATE TRIGGER IF NOT EXISTS update_timestamp
            AFTER UPDATE ON task
            FOR EACH ROW
            BEGIN
            UPDATE task SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
            END;
            """
        )
        db.commit()
