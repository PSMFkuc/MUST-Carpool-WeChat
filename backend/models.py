"""
models.py — SQLite 数据模型（建表 + 示例数据）
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "carpool.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name  TEXT NOT NULL,
            phone TEXT UNIQUE NOT NULL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS routes (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            start   TEXT NOT NULL,
            end     TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL,
            start      TEXT NOT NULL,
            end        TEXT NOT NULL,
            hour       INTEGER NOT NULL,
            weekday    INTEGER NOT NULL,
            success    INTEGER NOT NULL,
            created_at TEXT DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()

    if c.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
        c.execute("INSERT INTO users (name, phone) VALUES ('张三','13800000001')")
        c.execute("INSERT INTO users (name, phone) VALUES ('李四','13800000002')")

        c.execute("INSERT INTO routes (user_id, start, end) VALUES (1,'科技园南区','高铁站')")
        c.execute("INSERT INTO routes (user_id, start, end) VALUES (1,'高铁站','科技园南区')")
        c.execute("INSERT INTO routes (user_id, start, end) VALUES (2,'大学城','体育中心')")

        sample = [
            (1, "科技园南区", "高铁站", 8, 0, 1),
            (1, "科技园南区", "高铁站", 8, 1, 1),
            (1, "科技园南区", "高铁站", 8, 2, 1),
            (1, "科技园南区", "高铁站", 8, 3, 0),
            (1, "科技园南区", "高铁站", 8, 4, 1),
            (1, "科技园南区", "高铁站", 9, 0, 1),
            (1, "科技园南区", "高铁站", 9, 1, 0),
            (2, "大学城",     "体育中心", 18, 5, 1),
            (2, "大学城",     "体育中心", 18, 6, 0),
            (2, "大学城",     "体育中心", 17, 5, 1),
        ]
        c.executemany(
            "INSERT INTO history (user_id, start, end, hour, weekday, success) VALUES (?,?,?,?,?,?)",
            sample,
        )
        conn.commit()

    conn.close()
