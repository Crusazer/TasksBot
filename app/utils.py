import sqlite3
from datetime import datetime, timedelta

from config import settings
from core.repository.row_sql_query import CREATE_TASK_TABLE, CREATE_AUTO_AUTOUPDATE_TIMESTAMP


def prepare_database():
    """ Create new database if not exists and create trigger for autoupdate updated_at field. """
    with sqlite3.connect(settings.DB_NAME) as db:
        db.execute(CREATE_TASK_TABLE)
        db.execute(CREATE_AUTO_AUTOUPDATE_TIMESTAMP)
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
