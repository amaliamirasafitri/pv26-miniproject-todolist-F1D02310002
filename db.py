import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("todo.db")
        self.create_table()

    def create_table(self):
        # tabel task
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            category TEXT,
            priority TEXT,
            deadline TEXT,
            status TEXT DEFAULT 'Belum'
        )
        """)

        # tabel user
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
        """)
        self.conn.commit()

    # Task
    def add_task(self, data):
        self.conn.execute("""
        INSERT INTO tasks (title, description, category, priority, deadline)
        VALUES (?, ?, ?, ?, ?)
        """, data)
        self.conn.commit()

    def get_tasks(self):
        return self.conn.execute("SELECT * FROM tasks").fetchall()

    def delete_task(self, task_id):
        self.conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        self.conn.commit()

    def update_status(self, task_id, status):
        self.conn.execute("UPDATE tasks SET status=? WHERE id=?", (status, task_id))
        self.conn.commit()

    # Tambahan untuk update task
    def update_task(self, task_id, data):
        self.conn.execute("""
        UPDATE tasks
        SET title=?, description=?, category=?, priority=?, deadline=?
        WHERE id=?
        """, (*data, task_id))
        self.conn.commit()

    # User
    def register_user(self, username, password):
        try:
            self.conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            self.conn.commit()
            return True
        except:
            return False

    def login_user(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )
        return cursor.fetchone()