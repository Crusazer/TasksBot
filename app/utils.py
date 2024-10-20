import sqlite3
from datetime import datetime, timedelta

from config import settings


def prepare_database():
    """ Create new database if not exists and create trigger for autoupdate updated_at field. """
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


def convert_time_to_utc(time: datetime | str) -> datetime:
    """ Utils function to convert local time to UTC """
    if isinstance(time, str):
        time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    return time - timedelta(hours=settings.TIME_ZONE)


def convert_time_to_local(time: datetime | str) -> datetime:
    """ Utils function to convert UTC time to local """
    if isinstance(time, str):
        time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    return time + timedelta(hours=settings.TIME_ZONE)
