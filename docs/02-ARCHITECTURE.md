# Kiến trúc Local-first

## Điều chỉnh kiến trúc 18/11/2026

**Ưu tiên mới:** React + FastAPI + SQLite làm Prompt Compiler / Task Ledger / Skill Registry / Canon Ledger / Result Intake / QC Review cho GPT bên ngoài. Ollama, ComfyUI, Job Worker, model-serving và kết nối API trở thành tùy chọn giai đoạn sau, không phải mục tiêu xây dựng lõi. Xem [đặc tả GPT-Orchestration](09-GPT-ORCHESTRATION.md).

## Kiến trúc mục tiêu
```
React/Vite UI ──HTTP── FastAPI BFF/API ── SQLite (Phase 1)
                         │
                         ├── Source ingestion / RAG (Phase 2)
                         ├── Story agent / adapters Ollama/API (Phase 2)
                         ├── Character & Storyboard services (Phase 3)
                         ├── Job queue ── ComfyUI / render workers (Phase 4)
                         ├── QC rules + review dashboard (Phase 5)
                         └── Skill registry/sandbox + feedback (Phase 6)
```
Hiện tại chưa có AI worker hoặc queue; sơ đồ trên là **kiến trúc mục tiêu**, không phải thành phần đã chạy.

## Mục tiêu kỹ thuật
- **Backend** Python 3.11+, FastAPI, Pydantic 2, sqlite3 stdlib ở Phase 1.
- **Frontend** React + TypeScript + Vite, TypeScript strict, CSS thuần trước để tránh thư viện dư.
- **Lưu trữ** `COMIC_STUDIO_DATA_DIR` là đường dẫn local ngoài git; `studio.db` không commit.
- **Định danh** UUID dạng text cho project/chapter/character/beat, FK có bật.
- **Tách biệt** project_id ở mọi truy vấn con; không để yêu cầu của project A truy hồi project B.
- **API v1** `GET /api/health`, `GET /api/catalog`, `GET/POST /api/projects`, `GET /api/projects/{id}`, `POST /api/projects/{id}/chapters|characters|beats`.
- **Triển khai local** hai process dev, backend bind 127.0.0.1, frontend dev proxy tới backend; chưa có auth.

## Thiết kế adapter AI tương lai
Mỗi tác vụ mô tả `task_id, project_id, input_ids, model_adapter, model_version, prompt_version, rights, expected_output_schema, budget, timeout, review_status`; worker trả về artifact có checksum và nguồn. Dữ liệu approved bất biến trừ thao tác tạo version mới.

## Bảo mật & bản quyền
- Tuyệt đối không commit dữ liệu truyện gốc/tranh tham chiếu riêng tư. Gitignore chỉ là lớp bảo vệ bổ sung.
- Link không phải giấy phép. Cần xác nhận rights trước thao tác chia sẻ/xuất bản công khai.
- Trước khi mở LAN: auth, session, CSRF/CORS, file upload limits, path validation, TLS khi online, audit.
- Skill bên ngoài chỉ được xem như nguồn không tin cậy: xem diff, xác thực, thử trong sandbox và yêu cầu approve.
