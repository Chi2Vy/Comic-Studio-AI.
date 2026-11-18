# Nhập bản thảo nguồn (Phase 2 — bước 1)

- Chấp nhận tệp TXT, DOCX, EPUB (spine XHTML) và PDF có lớp văn bản; chưa hỗ trợ PDF scan OCR hay nội dung từ URL.
- Tối đa 8 MB/tệp, 2.000.000 ký tự văn bản, tối đa 500 trang PDF; DOCX/EPUB bị giới hạn cả dung lượng giải nén.
- Người dùng xác nhận có quyền xử lý nguồn và dự án có rights_status khác unknown.
- Text được trích xuất và lưu trong SQLite ở thư mục local của backend, không commit vào GitHub, không gọi API AI.
- Nhận diện tiêu đề Chương N / Chapter N bằng quy tắc đơn giản; kết quả là **đề xuất phân đoạn**, chưa phải kiểm chứng nguồn và không tự sinh Beat.
- Dữ liệu bản thảo chỉ có thể xem theo project ID và source ID tương ứng. Đọc từ máy đang chạy API, chưa có xác thực người dùng; KHÔNG đưa API ra Internet/LAN.

## Routes

- POST /api/projects/{project_id}/sources (multipart: file, confirm_rights=true)
- GET /api/projects/{project_id}/sources
- GET /api/projects/{project_id}/sources/{source_id} (preview + segment metadata)
- GET /api/projects/{project_id}/sources/{source_id}/segments/{segment_index} (full text segment)

## Hạn chế dự kiến

Trích xuất bảng, ngắt dòng PDF, EPUB lạ và nhận diện tên chương có thể sai; cần có editor soát lại các ranh giới. Giới hạn upload không thay thế quét malware. Trước khi mở LAN/Internet cần auth, encryption phù hợp, rate limits, audit và kiểm soát quyền truy cập.
