CREATE_TASK = " INSERT INTO task (user_id, description, status, deadline) VALUES (?, ?, ?, ?)"
GET_TASK_BY_ID = "SELECT * FROM task WHERE id = ?"
GET_TASKS_BY_USER_ID = " SELECT * FROM task WHERE user_id = ?"
DELETE_TASK_BY_ID = "DELETE FROM task WHERE id = ?"
UPDATE_TASK_BY_ID = "UPDATE task SET description = ?, deadline = ? WHERE id = ?"
COMPLETE_TASK_BY_ID = "UPDATE task SET status = ? WHERE id = ?"

CREATE_TASK_TABLE = """CREATE TABLE IF NOT EXISTS task
            (id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            status INTEGER NOT NULL,
            deadline TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )"""

CREATE_AUTO_AUTOUPDATE_TIMESTAMP = """
            CREATE TRIGGER IF NOT EXISTS update_timestamp
            AFTER UPDATE ON task
            FOR EACH ROW
            BEGIN
            UPDATE task SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
            END;
            """
