# Dữ liệu — phiên bản 0.1 và lộ trình

## Implemented Phase 1
**projects**: id PK, title, synopsis, source_type (original|adaptation), rights_status (unknown|owned|licensed|public_domain), style_id, mood_id, mode_id, status, created_at.

**chapters**: id PK, project_id FK, chapter_number UNIQUE theo project, title, target_pages, status, created_at.

**characters**: id PK, project_id FK, name, role, notes, model_status mặc định provisional, approved_version NULL, created_at.

**beats**: id PK, project_id FK, beat_number, summary, source_locator, verification_level mặc định unverified, created_at.

Mọi API con kiểm tra `project_id` tồn tại và query trong phạm vi đó; không tự gán `verified`.

## Planned tables
- `sources, source_segments, citations` — bản nguồn, mốc chương, chứng cứ và quyền.
- `story_facts, character_states, relations, timeline_events` — canon với phạm vi thời gian/spoiler.
- `adaptation_maps, scenes, pages, panels, dialogue, balloons` — screenplay và hình.
- `artifacts, artifact_versions, layer_versions, edit_masks, asset_hashes` — chỉnh cục bộ có lịch sử.
- `qc_checks, qc_evidence, approvals` — mỗi gate G0–G6.
- `jobs, ai_runs, adapters, skill_versions, feedback` — worker, budget, tracing, learning.

## Migration strategy
Phase 1 dùng `CREATE TABLE IF NOT EXISTS`; trước khi thêm/cập nhật schema production cần migration có phiên bản, backup và test. Không đổi cấu trúc trực tiếp làm mất dữ liệu.
