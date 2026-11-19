"""存储模块：SQLite 落库、去重、查询。schema 见同目录 schema.sql。"""
import sqlite3
from pathlib import Path

SCHEMA = Path(__file__).with_name("schema.sql")


def connect(db_path="radar.db"):
    conn = sqlite3.connect(db_path)
    conn.executescript(SCHEMA.read_text(encoding="utf-8"))
    return conn


def upsert(conn, items, now):
    """按 url 去重：新条目插入并返回，旧条目只刷新热度。返回 [(id, item), ...] 新增列表"""
    new = []
    for it in items:
        row = conn.execute("SELECT id FROM items WHERE url = ?", (it["url"],)).fetchone()
        if row is None:
            cur = conn.execute(
                "INSERT INTO items(source, title, url, heat, extra, fetched_at)"
                " VALUES(?,?,?,?,?,?)",
                (it["source"], it["title"], it["url"], it["heat"], it["extra"], now),
            )
            new.append((cur.lastrowid, it))
        else:
            conn.execute(
                "UPDATE items SET heat=?, extra=?, fetched_at=? WHERE url=?",
                (it["heat"], it["extra"], now, it["url"]),
            )
    conn.commit()
    return new


def pending(conn):
    """还没有 AI 摘要的条目"""
    cur = conn.execute(
        "SELECT id, source, title, url, heat, extra"
        " FROM items WHERE summary IS NULL OR summary = ''"
    )
    cols = ("id", "source", "title", "url", "heat", "extra")
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def set_summary(conn, item_id, summary, now):
    conn.execute(
        "UPDATE items SET summary=?, summarized_at=? WHERE id=?", (summary, now, item_id)
    )
    conn.commit()


def recent(conn, limit=60):
    cur = conn.execute(
        "SELECT source, title, url, heat, extra, summary, fetched_at"
        " FROM items ORDER BY fetched_at DESC, id DESC LIMIT ?",
        (limit,),
    )
    cols = ("source", "title", "url", "heat", "extra", "summary", "fetched_at")
    return [dict(zip(cols, r)) for r in cur.fetchall()]
