# Comic Studio AI

**Local-first GPT orchestration studio**: công cụ điều hành quá trình chuyển thể bằng GPT/AI bên ngoài, quản lý thiết lập, Skill, prompt, nguồn, QC và các bản sửa. Không bắt buộc tích hợp hay chạy mô hình AI bên trong.

> Trạng thái: **Phase 1 — foundation (prototype)**. Chưa tích hợp mô hình LLM, sinh ảnh, OCR, inpainting hoặc tự động xuất bản. Không khẳng định các chức năng đó đã hoạt động.

## Bắt đầu nhanh

Cần Python 3.11+ và Node.js 20+.

### 1. API

```bash
cd backend
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

API: http://127.0.0.1:8000/docs — dữ liệu SQLite lưu ở `~/.comic-studio-ai/studio.db` (có thể đặt biến môi trường `COMIC_STUDIO_DATA_DIR`).

### 2. Giao diện

```bash
cd frontend
npm install
npm run dev
```

Mở http://localhost:5173. Máy local chạy hai terminal. Chưa có xác thực người dùng; **không mở cổng ra Internet/LAN** ở phiên bản này.

### 3. Kiểm thử API

```bash
cd backend
pip install -r requirements-dev.txt
pytest -q
```

## Trọng tâm sản phẩm

Bắt đầu từ **Prompt Desk**: chọn dự án/phạm vi/skill, tự chuẩn bị gói lệnh, sao chép sang ChatGPT, nhập kết quả về và kiểm duyệt. Xem [đặc tả điều phối GPT](docs/09-GPT-ORCHESTRATION.md). Các model local/GPU/API tích hợp là tùy chọn, không thuộc lõi.

## Phạm vi bản đầu
- Tạo/list dự án; quản lý chương, nhân vật, beat nguồn và trạng thái xác minh.
- Nhập bản thảo TXT/DOCX/EPUB/PDF có lớp văn bản trong mục **Nghiên cứu nguồn**; tự nhận diện tiêu đề chương và xem nội dung cục bộ. Giới hạn 8 MB/tệp; chưa có AI biên kịch hoặc OCR.
- Bộ phận Studio, Style/Mood/Mode có cấu hình mẫu.
- Chạy local, không cần khóa API, dữ liệu từng truyện được tách theo `project_id`.
- Chưa tạo tranh hay tự động đọc/viết nội dung bằng AI. Khu vực AI trên giao diện chỉ là vị trí dành cho giai đoạn sau.

## Tài liệu và quản trị

- [PRD](docs/01-PRD.md) · [Kiến trúc](docs/02-ARCHITECTURE.md) · [Workflow](docs/03-WORKFLOW.md) · [Dữ liệu](docs/04-DATABASE.md)
- [AI Agents](docs/05-AI-AGENTS.md) · [QC](docs/06-QUALITY-GATES.md) · [Giao diện](docs/07-UI-UX.md) · [Roadmap](docs/08-ROADMAP.md)
- [Quy tắc cộng tác Codex](AGENTS.md) · [Quyết định](docs/DECISIONS.md)

### Tích hợp bộ ZIP v2.0
Bộ `ComicStudio_TatCaSkill_DuAn_QC_v2_2026-11-18.zip` là **nguồn quy tắc nghiệp vụ**, không phải code đã triển khai. Những phần được kế thừa gồm: Story/Beat ledger, Character Bible, Style/Mood/Mode, G0–G6 và checkpoint. Không đẩy bản thảo tiểu thuyết, tranh tham khảo, ảnh bị loại hay tệp được bảo hộ lên repo Public.

## Bản quyền
Mã nguồn và tài liệu khởi tạo không cấp phép quyền chuyển thể/phân phối bất kỳ tác phẩm nào. Tác giả vận hành hệ thống chịu trách nhiệm kiểm tra giấy phép nguồn và tài sản hình ảnh trước công bố.
