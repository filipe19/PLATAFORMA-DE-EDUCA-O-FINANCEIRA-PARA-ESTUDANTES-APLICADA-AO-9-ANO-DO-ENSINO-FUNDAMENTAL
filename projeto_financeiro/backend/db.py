# backend/db.py
import sqlite3
import json


SCHEMA = """
CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kind TEXT,
    payload TEXT,
    created_at DATETIME DEFAULT (datetime('now','localtime'))
);
"""


def init_db(path: str = './data.db'):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.executescript(SCHEMA)
    conn.commit()
    conn.close()


def save_submission(path: str, kind: str, payload: dict):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute('INSERT INTO submissions (kind, payload) VALUES (?,?)', (kind, json.dumps(payload, ensure_ascii=False)))
    conn.commit()
    conn.close()


def get_submissions(path: str):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute('SELECT id, kind, payload, created_at FROM submissions ORDER BY created_at DESC')
    rows = c.fetchall()
    conn.close()
    out = []
    for r in rows:
        try:
            payload = json.loads(r[2])
        except Exception:
            payload = r[2]
        out.append({"id": r[0], "kind": r[1], "payload": payload, "created_at": r[3]})
    return out