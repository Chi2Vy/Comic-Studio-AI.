# Roadmap — lựa chọn A (GPT Orchestration First)

**Quyết định mới:** Studio là công cụ quản lý thiết lập, skill, prompt, kết quả và QA cho GPT bên ngoài. Các hạng mục Ollama/ComfyUI/render worker phía dưới là **tùy chọn**, không phải hướng ưu tiên.

## MVP ưu tiên mới
- [ ] A1: Prompt Desk, prompt compiler theo project/chap/page/panel, template/Skill, copy/export, warnings.
- [ ] A2: Task ledger, prompt pack version, import kết quả GPT text/ảnh, link phạm vi và nguồn.
- [ ] A3: QC G0–G6 có chứng cứ, sinh lệnh sửa đúng panel/vùng, giữ bản đã khóa.
- [ ] A4: Feedback-to-Skill có duyệt, adapter chính thức tự động tùy chọn.

Chi tiết: [09-GPT-ORCHESTRATION.md](09-GPT-ORCHESTRATION.md).


## Phase 1 — Foundation [đang triển khai]
- [x] Khởi tạo repository, PRD, architecture, workflow, database, UI/QC, agent contracts.
- [x] API + SQLite cho project/chapter/character/beat.
- [x] Giao diện React quản lý project và thông tin sơ bộ.
- [ ] Chạy kiểm thử trên Windows thực tế; sửa khác biệt môi trường.
- [ ] CRUD sửa/xóa, sự kiện audit, backup/restore, migration versioned.
- [ ] Xác thực trước khi mở LAN/online.
**Exit:** Tạo 2 project không lẫn dữ liệu, demo quản lý đơn giản, chạy thử trên Windows.

## Phase 2 — Story intelligence
- [x] Nhập TXT/DOCX/EPUB/PDF text-layer với xác nhận quyền, giới hạn 8MB; phân đoạn tiêu đề chương (bước đầu).
- [ ] Chuẩn hóa và chỉnh sửa ranh giới chương; kiểm thử PDF/EPUB phức tạp và bổ sung OCR scan sau.
- [ ] Source ledger/chapter extraction/RAG theo project_id.
- [ ] Ollama adapter; biên kịch từ brief/script có sẵn; có evidence & verified flags.
- [ ] Xuất RESEARCH / BEATS / adaptation map; review UI.

## Phase 3 — Art bible & storyboard
- [ ] Character model sheet + approved versions, costume timeline.
- [ ] Scene bible, props, stage, palette.
- [ ] Page/chap budgeting, scene/page/panel editor, bubble ledger.

## Phase 4 — Visual production/editor
- [ ] ComfyUI adapter, job queue, render panel thành PNG/JPG gốc.
- [ ] Text layer tách biệt.
- [ ] Mask/inpaint, version/undo, hash outside edit-mask không đổi sau compositing.

## Phase 5 — QA/release
- [ ] G0–G6 machine checks + human reviews, compare source/scene.
- [ ] Workflow approvals, changelogs, export PNG/JPG/PDF/CBZ.

## Phase 6 — Learning/skills & hybrid
- [ ] Project memory, feedback trace, retrieval, offline eval set.
- [ ] Skill registry diff/approve/rollback và sandbox.
- [ ] Auth, encrypted sync, remote access, optional paid provider adapters.

### Nguyên tắc hoàn thành
Chỉ đánh dấu hoàn thành sau khi code đã commit và kiểm tra. Một bản demo quản lý không phải sản phẩm chuyển thể AI hoàn chỉnh.
