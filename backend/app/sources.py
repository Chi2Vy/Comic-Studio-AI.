"""Local, project-scoped manuscript ingestion. Never sends text to AI services."""
from __future__ import annotations

import hashlib
import io
import posixpath
import re
import sqlite3
import zipfile
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import PureWindowsPath
from uuid import uuid4
from xml.etree import ElementTree as ET

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

MAX_UPLOAD_BYTES = 8 * 1024 * 1024
MAX_EXTRACTED_CHARS = 2_000_000
MAX_ZIP_UNCOMPRESSED = 32 * 1024 * 1024
MAX_ZIP_ENTRIES = 1500
ALLOWED_EXTENSIONS = {".txt", ".docx", ".epub", ".pdf"}
CHAPTER_HEADING = re.compile(
    r"^\s{0,3}((?:Chương|Chapter)\s+(?:\d{1,5}|[IVXLCDM]{1,8})\b[^\r\n]{0,90})\s*$",
    re.I | re.M,
)

class IngestError(Exception):
    pass

class HTMLText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style"}:
            self.skip += 1
        if tag in {"p", "div", "br", "h1", "h2", "h3", "li"}:
            self.parts.append("\n")
    def handle_endtag(self, tag):
        if tag in {"script", "style"} and self.skip:
            self.skip -= 1
        if tag in {"p", "div", "h1", "h2", "h3", "li"}:
            self.parts.append("\n")
    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)

def _safe_zip(data: bytes) -> zipfile.ZipFile:
    try:
        archive = zipfile.ZipFile(io.BytesIO(data))
        entries = archive.infolist()
        if len(entries) > MAX_ZIP_ENTRIES or sum(e.file_size for e in entries) > MAX_ZIP_UNCOMPRESSED:
            archive.close()
            raise IngestError("Tệp nén vượt giới hạn an toàn")
        return archive
    except (OSError, zipfile.BadZipFile) as exc:
        raise IngestError("Tệp DOCX/EPUB không hợp lệ") from exc

def _decode(data: bytes) -> str:
    for encoding in ("utf-8-sig", "cp1258"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            pass
    raise IngestError("Không thể đọc bảng mã văn bản")

def _docx(data: bytes) -> str:
    with _safe_zip(data) as z:
        if "word/document.xml" not in z.namelist():
            raise IngestError("Thiếu nội dung DOCX")
        root = ET.fromstring(z.read("word/document.xml"))
        w = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
        paragraphs = []
        for p in root.iter(w + "p"):
            text = "".join(n.text or "" for n in p.iter(w + "t"))
            if text.strip():
                paragraphs.append(text)
        return "\n".join(paragraphs)

def _epub(data: bytes) -> str:
    with _safe_zip(data) as z:
        try:
            container = ET.fromstring(z.read("META-INF/container.xml"))
            rf = next(e for e in container.iter() if e.tag.endswith("rootfile"))
            opf_path = rf.attrib["full-path"]
            if opf_path.startswith("/") or ".." in opf_path.split("/"):
                raise IngestError("EPUB có đường dẫn không hợp lệ")
            opf = ET.fromstring(z.read(opf_path))
            manifest = {}
            spine = []
            for e in opf.iter():
                if e.tag.endswith("item") and "id" in e.attrib and "href" in e.attrib:
                    manifest[e.attrib["id"]] = (e.attrib["href"], e.attrib.get("media-type", ""))
                if e.tag.endswith("itemref") and "idref" in e.attrib:
                    spine.append(e.attrib["idref"])
            parts = []
            for ref in spine[:1000]:
                if ref not in manifest:
                    continue
                href, kind = manifest[ref]
                if kind not in {"application/xhtml+xml", "text/html"}:
                    continue
                path = posixpath.normpath(posixpath.join(posixpath.dirname(opf_path), href.split("#")[0]))
                if path.startswith("../") or path.startswith("/"):
                    raise IngestError("EPUB có đường dẫn không hợp lệ")
                if path not in z.namelist():
                    continue
                parser = HTMLText()
                parser.feed(z.read(path).decode("utf-8-sig"))
                parts.append("".join(parser.parts))
            if not parts:
                raise IngestError("Không tìm thấy văn bản trong EPUB")
            return "\n".join(parts)
        except (ET.ParseError, KeyError, StopIteration, UnicodeDecodeError, zipfile.BadZipFile) as exc:
            raise IngestError("EPUB không hợp lệ hoặc không đọc được") from exc

def _pdf(data: bytes) -> str:
    try:
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(data), strict=False)
        if len(reader.pages) > 500:
            raise IngestError("PDF vượt 500 trang; hãy chia tệp trước khi nhập")
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except IngestError:
        raise
    except Exception as exc:
        raise IngestError("Không đọc được PDF hoặc PDF cần mật khẩu") from exc

def extract_text(data: bytes, extension: str) -> str:
    if extension == ".txt":
        text = _decode(data)
    elif extension == ".docx":
        text = _docx(data)
    elif extension == ".epub":
        text = _epub(data)
    elif extension == ".pdf":
        text = _pdf(data)
    else:
        raise IngestError("Chỉ hỗ trợ TXT, DOCX, EPUB, PDF")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = "\n".join(line.rstrip() for line in text.splitlines()).strip()
    if not text:
        raise IngestError("Tệp không có chữ có thể trích xuất; PDF ảnh cần OCR ở phiên bản sau")
    if len(text) > MAX_EXTRACTED_CHARS:
        raise IngestError("Văn bản quá dài; hãy chia thành nhiều tệp")
    return text

def chapters_from_text(text: str) -> list[dict]:
    matches = list(CHAPTER_HEADING.finditer(text))
    if len(matches) > 2000:
        raise IngestError("Có quá nhiều tiêu đề chương cần xác minh")
    boundaries = []
    if not matches:
        boundaries.append(("Toàn văn (chưa nhận diện chương)", 0, len(text)))
    else:
        if matches[0].start() > 0 and text[:matches[0].start()].strip():
            boundaries.append(("Lời mở đầu", 0, matches[0].start()))
        for idx, match in enumerate(matches):
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
            boundaries.append((match.group(1).strip(), match.start(), end))
    return [
        {"segment_index": i + 1, "heading": title, "start_char": start,
         "end_char": end, "char_count": end - start, "preview": text[start:end].strip()[:300]}
        for i, (title, start, end) in enumerate(boundaries)
    ]

def create_source_router(store) -> APIRouter:
    router = APIRouter(prefix="/api/projects/{project_id}/sources", tags=["sources"])
    with store.connect() as con:
        con.executescript("""
            CREATE TABLE IF NOT EXISTS source_documents (
                id TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES projects(id),
                filename TEXT NOT NULL, format TEXT NOT NULL, file_hash TEXT NOT NULL,
                text_content TEXT NOT NULL, character_count INTEGER NOT NULL,
                segment_count INTEGER NOT NULL, created_at TEXT NOT NULL,
                UNIQUE(project_id, file_hash)
            );
            CREATE INDEX IF NOT EXISTS idx_source_project ON source_documents(project_id);
        """)

    def require_project(project_id: str) -> dict:
        project = store.one("SELECT * FROM projects WHERE id = ?", (project_id,))
        if not project:
            raise HTTPException(404, "Không tìm thấy dự án")
        return project
    def get_source(project_id: str, source_id: str) -> dict:
        source = store.one(
            "SELECT * FROM source_documents WHERE project_id = ? AND id = ?",
            (project_id, source_id),
        )
        if not source:
            raise HTTPException(404, "Không tìm thấy tệp nguồn trong dự án")
        return source
    def metadata(source: dict) -> dict:
        return {k: source[k] for k in (
            "id", "project_id", "filename", "format", "file_hash",
            "character_count", "segment_count", "created_at"
        )}

    @router.get("")
    def list_sources(project_id: str):
        require_project(project_id)
        return store.all(
            "SELECT id, project_id, filename, format, file_hash, character_count, "
            "segment_count, created_at FROM source_documents WHERE project_id=? "
            "ORDER BY created_at DESC, id DESC", (project_id,)
        )

    @router.post("", status_code=201)
    async def upload_source(
        project_id: str,
        file: UploadFile = File(...),
        confirm_rights: bool = Form(...),
    ):
        project = require_project(project_id)
        if not confirm_rights:
            raise HTTPException(422, "Cần xác nhận có quyền xử lý bản thảo")
        if project["rights_status"] == "unknown":
            raise HTTPException(409, "Hãy xác nhận tình trạng quyền nguồn của dự án trước khi nhập")
        filename = PureWindowsPath(file.filename or "").name.replace("/", "_")[:200]
        extension = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(415, "Chỉ hỗ trợ TXT, DOCX, EPUB, PDF")
        data = await file.read(MAX_UPLOAD_BYTES + 1)
        await file.close()
        if len(data) > MAX_UPLOAD_BYTES:
            raise HTTPException(413, "Tệp vượt giới hạn 8 MB")
        if not data:
            raise HTTPException(422, "Tệp trống")
        try:
            content = extract_text(data, extension)
            segments = chapters_from_text(content)
        except IngestError as exc:
            raise HTTPException(422, str(exc)) from exc
        file_hash = hashlib.sha256(data).hexdigest()
        record = {
            "id": str(uuid4()), "project_id": project_id, "filename": filename,
            "format": extension.lstrip("."), "file_hash": file_hash,
            "text_content": content, "character_count": len(content),
            "segment_count": len(segments),
            "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
        try:
            with store.connect() as con:
                con.execute(
                    "INSERT INTO source_documents (id,project_id,filename,format,file_hash,"
                    "text_content,character_count,segment_count,created_at) "
                    "VALUES (:id,:project_id,:filename,:format,:file_hash,:text_content,"
                    ":character_count,:segment_count,:created_at)", record,
                )
        except sqlite3.IntegrityError:
            raise HTTPException(409, "Tệp này đã có trong dự án") from None
        return {**metadata(record), "segments": segments}

    @router.get("/{source_id}")
    def source_detail(project_id: str, source_id: str):
        source = get_source(project_id, source_id)
        return {
            **metadata(source),
            "preview": source["text_content"][:5000],
            "segments": chapters_from_text(source["text_content"]),
        }

    @router.get("/{source_id}/segments/{segment_index}")
    def read_segment(project_id: str, source_id: str, segment_index: int):
        source = get_source(project_id, source_id)
        segments = chapters_from_text(source["text_content"])
        if segment_index < 1 or segment_index > len(segments):
            raise HTTPException(404, "Không tìm thấy chương nguồn")
        segment = segments[segment_index - 1]
        return {"source_id": source_id, **segment,
                "content": source["text_content"][segment["start_char"]:segment["end_char"]]}

    return router
