import os
import sqlite3
from typing import Dict, List, Optional

DB_PATH = os.getenv("DATABASE_URL", "data.db")

# If using in-memory DB for tests, keep a single shared connection
_shared_conn: Optional[sqlite3.Connection] = None


def _get_conn() -> sqlite3.Connection:
    global _shared_conn
    if DB_PATH in (":memory", ":memory:"):
        if _shared_conn is None:
            _shared_conn = sqlite3.connect(":memory:", check_same_thread=False)
            _shared_conn.row_factory = sqlite3.Row
        return _shared_conn
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed INTEGER NOT NULL DEFAULT 0
        )
        """
    )
    conn.commit()
    if DB_PATH not in (":memory:", ":memory"):
        conn.close()


def create_todo(title: str, description: Optional[str], completed: bool) -> Dict:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO todos (title, description, completed) VALUES (?, ?, ?)",
        (title, description, int(completed)),
    )
    conn.commit()
    todo_id = cur.lastrowid
    if DB_PATH not in (":memory:", ":memory"):
        conn.close()
    return {"id": todo_id, "title": title, "description": description, "completed": completed}


def list_todos() -> List[Dict]:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, title, description, completed FROM todos")
    rows = cur.fetchall()
    if DB_PATH not in (":memory:", ":memory"):
        conn.close()
    return [dict(id=row[0], title=row[1], description=row[2], completed=bool(row[3])) for row in rows]


def get_todo(todo_id: int) -> Optional[Dict]:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, title, description, completed FROM todos WHERE id = ?", (todo_id,))
    row = cur.fetchone()
    if DB_PATH not in (":memory:", ":memory"):
        conn.close()
    if not row:
        return None
    return dict(id=row[0], title=row[1], description=row[2], completed=bool(row[3]))


def update_todo(todo_id: int, title: str, description: Optional[str], completed: bool) -> Optional[Dict]:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE todos SET title = ?, description = ?, completed = ? WHERE id = ?",
        (title, description, int(completed), todo_id),
    )
    conn.commit()
    if DB_PATH not in (":memory:", ":memory"):
        conn.close()
    return get_todo(todo_id)


def delete_todo(todo_id: int) -> bool:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    deleted = cur.rowcount > 0
    if DB_PATH not in (":memory:", ":memory"):
        conn.close()
    return deleted
