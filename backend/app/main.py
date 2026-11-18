"""Phase-1 local-first Comic Studio API. No AI, authentication or cloud upload."""

from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

STYLES = [
    ("manhua-xianxia", "Manhua tiên hiệp"),
    ("manhua-romance", "Manhua ngôn tình"),
    ("manga-shonen", "Manga hành động"),
    ("manga-shojo", "Manga tình cảm"),
    ("webtoon-modern", "Webtoon hiện đại"),
    ("western-comic", "Comic phương Tây"),
    ("watercolor-fantasy", "Màu nước fantasy"),
    ("ink-monochrome", "Mực đen trắng"),
    ("chibi-comedy", "Chibi hài hước"),
    ("cinematic-semi-realism", "Bán hiện thực điện ảnh"),
]
MOODS = [
    ("balanced", "Cân bằng"), ("romantic", "Lãng mạn"),
    ("melancholic", "U buồn"), ("tragic", "Bi kịch"),
    ("dark", "Hắc ám"), ("horror", "Kinh dị"),
    ("mysterious", "Bí ẩn"), ("epic", "Hùng tráng"),
    ("comedic", "Hài hước"), ("healing", "Chữa lành"),
    ("action", "Hành động"),
]
MODES = [
    ("faithful", "Bám nguyên tác"),
    ("cinematic", "Điện ảnh"),
    ("scroll-webtoon", "Cuộn dọc Webtoon"),
    ("compact", "Cô đọng có kiểm soát"),
    ("creative", "Sáng tạo có phê duyệt"),
]
DEPARTMENTS = [
    {"id": "director", "name": "Giám đốc Studio", "phase": 1},
    {"id": "research", "name": "Nghiên cứu nguồn", "phase": 1},
    {"id": "script", "name": "Biên kịch", "phase": 2},
    {"id": "character", "name": "Mỹ thuật nhân vật", "phase": 1},
    {"id": "storyboard", "name": "Storyboard", "phase": 3},
    {"id": "render", "name": "Sản xuất tranh", "phase": 4},
    {"id": "editor", "name": "Biên tập", "phase": 4},
    {"id": "qc", "name": "Kiểm duyệt", "phase": 5},
    {"id": "skills", "name": "Tri thức & Skill", "phase": 6},
]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Store:
    def __init__(self, path: Path):
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    @contextmanager
    def connect(self):
        con = sqlite3.connect(str(self.path), timeout=15)
        con.row_factory = sqlite3.Row
        con.execute("PRAGMA foreign_keys = ON")
        try:
            yield con
            con.commit()
        except Exception:
            con.rollback()
            raise
        finally:
            con.close()

    def initialize(self):
        with self.connect() as con:
            con.executescript("""
                CREATE TABLE IF NOT EXISTS projects (
                    id TEXT PRIMARY KEY, title TEXT NOT NULL, synopsis TEXT NOT NULL,
                    source_type TEXT NOT NULL, rights_status TEXT NOT NULL,
                    style_id TEXT NOT NULL, mood_id TEXT NOT NULL,
                    mode_id TEXT NOT NULL, status TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS chapters (
                    id TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES projects(id),
                    chapter_number INTEGER NOT NULL CHECK(chapter_number > 0),
                    title TEXT NOT NULL, target_pages INTEGER NOT NULL CHECK(target_pages > 0),
                    status TEXT NOT NULL, created_at TEXT NOT NULL,
                    UNIQUE(project_id, chapter_number)
                );
                CREATE TABLE IF NOT EXISTS characters (
                    id TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES projects(id),
                    name TEXT NOT NULL, role TEXT NOT NULL, notes TEXT NOT NULL,
                    model_status TEXT NOT NULL, approved_version TEXT,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS beats (
                    id TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES projects(id),
                    beat_number INTEGER NOT NULL CHECK(beat_number > 0),
                    summary TEXT NOT NULL, source_locator TEXT NOT NULL,
                    verification_level TEXT NOT NULL, created_at TEXT NOT NULL,
                    UNIQUE(project_id, beat_number)
                );
                CREATE INDEX IF NOT EXISTS idx_chapters_project ON chapters(project_id);
                CREATE INDEX IF NOT EXISTS idx_characters_project ON characters(project_id);
                CREATE INDEX IF NOT EXISTS idx_beats_project ON beats(project_id);
            """)

    def all(self, sql: str, params: tuple = ()) -> list[dict]:
        with self.connect() as con:
            return [dict(row) for row in con.execute(sql, params).fetchall()]

    def one(self, sql: str, params: tuple = ()) -> dict | None:
        with self.connect() as con:
            item = con.execute(sql, params).fetchone()
            return dict(item) if item else None

    def insert(self, table: str, values: dict) -> dict:
        if table not in {"projects", "chapters", "characters", "beats"}:
            raise ValueError("Unexpected table")
        fields = list(values)
        columns = ", ".join(fields)
        placeholders = ", ".join("?" for _ in fields)
        with self.connect() as con:
            con.execute(
                f"INSERT INTO {table} ({columns}) VALUES ({placeholders})",
                tuple(values[field] for field in fields),
            )
        return values


class ProjectCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    synopsis: str = Field(default="", max_length=2000)
    source_type: Literal["original", "adaptation"] = "original"
    rights_status: Literal["unknown", "owned", "licensed", "public_domain"] = "unknown"
    style_id: str = "manhua-xianxia"
    mood_id: str = "balanced"
    mode_id: str = "faithful"


class ChapterCreate(BaseModel):
    chapter_number: int = Field(ge=1, le=100000)
    title: str = Field(min_length=1, max_length=160)
    target_pages: int = Field(default=24, ge=1, le=10000)


class CharacterCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    role: str = Field(default="Nhân vật", max_length=120)
    notes: str = Field(default="", max_length=3000)


class BeatCreate(BaseModel):
    beat_number: int = Field(ge=1, le=1000000)
    summary: str = Field(min_length=1, max_length=3000)
    source_locator: str = Field(default="", max_length=500)


def create_app(db_path: str | Path | None = None) -> FastAPI:
    if db_path is None:
        base_dir = Path(os.environ.get("COMIC_STUDIO_DATA_DIR", Path.home() / ".comic-studio-ai"))
        db_path = base_dir / "studio.db"
    store = Store(Path(db_path))
    app = FastAPI(title="Comic Studio AI — Local API", version="0.1.0")
    app.state.store = store
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
    )

    def require_project(project_id: str) -> dict:
        project = store.one("SELECT * FROM projects WHERE id = ?", (project_id,))
        if project is None:
            raise HTTPException(404, "Không tìm thấy dự án")
        return project

    @app.get("/api/health")
    def health():
        return {"status": "ok", "phase": 1, "ai_generation": False}

    @app.get("/api/catalog")
    def catalog():
        return {
            "styles": [{"id": i, "name": n} for i, n in STYLES],
            "moods": [{"id": i, "name": n} for i, n in MOODS],
            "modes": [{"id": i, "name": n} for i, n in MODES],
        }

    @app.get("/api/departments")
    def departments():
        return DEPARTMENTS

    @app.get("/api/projects")
    def list_projects():
        return store.all("SELECT * FROM projects ORDER BY created_at DESC, id DESC")

    @app.post("/api/projects", status_code=201)
    def create_project(payload: ProjectCreate):
        for field, options in (
            ("style_id", STYLES), ("mood_id", MOODS), ("mode_id", MODES)
        ):
            if getattr(payload, field) not in {entry[0] for entry in options}:
                raise HTTPException(422, f"Giá trị {field} không hợp lệ")
        return store.insert("projects", {
            "id": str(uuid4()), "title": payload.title.strip(),
            "synopsis": payload.synopsis, "source_type": payload.source_type,
            "rights_status": payload.rights_status, "style_id": payload.style_id,
            "mood_id": payload.mood_id, "mode_id": payload.mode_id,
            "status": "planning", "created_at": now_iso(),
        })

    @app.get("/api/projects/{project_id}")
    def get_project(project_id: str):
        return {
            **require_project(project_id),
            "chapters": store.all(
                "SELECT * FROM chapters WHERE project_id = ? ORDER BY chapter_number", (project_id,)
            ),
            "characters": store.all(
                "SELECT * FROM characters WHERE project_id = ? ORDER BY created_at, id", (project_id,)
            ),
            "beats": store.all(
                "SELECT * FROM beats WHERE project_id = ? ORDER BY beat_number", (project_id,)
            ),
        }

    @app.post("/api/projects/{project_id}/chapters", status_code=201)
    def create_chapter(project_id: str, payload: ChapterCreate):
        require_project(project_id)
        try:
            return store.insert("chapters", {
                "id": str(uuid4()), "project_id": project_id,
                "chapter_number": payload.chapter_number, "title": payload.title.strip(),
                "target_pages": payload.target_pages, "status": "draft",
                "created_at": now_iso(),
            })
        except sqlite3.IntegrityError:
            raise HTTPException(409, "Số chương đã tồn tại trong dự án") from None

    @app.post("/api/projects/{project_id}/characters", status_code=201)
    def create_character(project_id: str, payload: CharacterCreate):
        require_project(project_id)
        return store.insert("characters", {
            "id": str(uuid4()), "project_id": project_id,
            "name": payload.name.strip(), "role": payload.role,
            "notes": payload.notes, "model_status": "provisional",
            "approved_version": None, "created_at": now_iso(),
        })

    @app.post("/api/projects/{project_id}/beats", status_code=201)
    def create_beat(project_id: str, payload: BeatCreate):
        require_project(project_id)
        try:
            return store.insert("beats", {
                "id": str(uuid4()), "project_id": project_id,
                "beat_number": payload.beat_number,
                "summary": payload.summary.strip(),
                "source_locator": payload.source_locator.strip(),
                "verification_level": "unverified", "created_at": now_iso(),
            })
        except sqlite3.IntegrityError:
            raise HTTPException(409, "Mã beat đã tồn tại trong dự án") from None

    return app


app = create_app()
