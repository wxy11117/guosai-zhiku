"""SQLite persistence for workflows and asynchronous job state."""

from __future__ import annotations

import json
import re
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "modelscore.sqlite3"
SAFE_ID = re.compile(r"^[A-Za-z0-9_-]{1,80}$")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA journal_mode=WAL")
    connection.execute("PRAGMA busy_timeout=10000")
    return connection


@contextmanager
def _db():
    connection = _connect()
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def init_db(recover_jobs: bool = False) -> None:
    with _db() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS workflows (
                id TEXT PRIMARY KEY,
                sort_order INTEGER NOT NULL,
                payload TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                payload TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """
        )
        if recover_jobs:
            rows = connection.execute("SELECT id, payload FROM jobs").fetchall()
            for row in rows:
                payload = json.loads(row["payload"])
                if payload.get("status") not in {"completed", "failed"}:
                    payload.update({
                        "status": "failed", "progress": 100,
                        "message": "服务重启前任务未完成", "error": "任务因本地服务重启而中断，请重新提交。",
                    })
                    connection.execute(
                        "UPDATE jobs SET payload = ?, updated_at = ? WHERE id = ?",
                        (json.dumps(payload, ensure_ascii=False), _now(), row["id"]),
                    )


def _validate_workflow(item: dict) -> dict:
    if not isinstance(item, dict):
        raise ValueError("工作流必须是对象")
    workflow_id = str(item.get("id", ""))
    if not SAFE_ID.fullmatch(workflow_id):
        raise ValueError("工作流 ID 无效")
    encoded = json.dumps(item, ensure_ascii=False)
    if len(encoded.encode("utf-8")) > 1_500_000:
        raise ValueError("单个工作流数据超过 1.5 MB")
    return item


def list_workflows() -> list[dict]:
    init_db()
    with _db() as connection:
        rows = connection.execute("SELECT payload FROM workflows ORDER BY sort_order ASC, updated_at DESC").fetchall()
    return [json.loads(row["payload"]) for row in rows]


def sync_workflows(items: list[dict]) -> list[dict]:
    if not isinstance(items, list) or len(items) > 200:
        raise ValueError("工作流列表无效或超过 200 条")
    clean = [_validate_workflow(item) for item in items]
    now = _now()
    init_db()
    with _db() as connection:
        keep_ids = [item["id"] for item in clean]
        if keep_ids:
            placeholders = ",".join("?" for _ in keep_ids)
            connection.execute(f"DELETE FROM workflows WHERE id NOT IN ({placeholders})", keep_ids)
        else:
            connection.execute("DELETE FROM workflows")
        for order, item in enumerate(clean):
            payload = json.dumps(item, ensure_ascii=False)
            connection.execute(
                """
                INSERT INTO workflows(id, sort_order, payload, created_at, updated_at)
                VALUES(?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    sort_order = excluded.sort_order,
                    payload = excluded.payload,
                    updated_at = excluded.updated_at
                """,
                (item["id"], order, payload, now, now),
            )
    return clean


def save_job(job_id: str, payload: dict) -> None:
    if not SAFE_ID.fullmatch(job_id):
        raise ValueError("任务 ID 无效")
    now = _now()
    init_db()
    encoded = json.dumps(payload, ensure_ascii=False)
    with _db() as connection:
        connection.execute(
            """
            INSERT INTO jobs(id, payload, created_at, updated_at) VALUES(?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET payload = excluded.payload, updated_at = excluded.updated_at
            """,
            (job_id, encoded, now, now),
        )


def get_job(job_id: str) -> dict | None:
    if not SAFE_ID.fullmatch(job_id):
        return None
    init_db()
    with _db() as connection:
        row = connection.execute("SELECT payload FROM jobs WHERE id = ?", (job_id,)).fetchone()
    return json.loads(row["payload"]) if row else None
