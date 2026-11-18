# Quyết định kiến trúc (ADR)

## ADR-001: Local-first, hybrid optional
Ưu tiên tài nguyên offline và SQLite, sau này thêm sync/cloud khi có quyền và auth. Tránh chi phí API bắt buộc.

## ADR-002: Một model, nhiều vai trò
9 phòng ban là vai trò nghiệp vụ; có thể dùng chung các mô hình AI thông qua adapter. Không triển khai 9 GPU pipelines riêng.

## ADR-003: G0–G6 hard gates
QC cần evidence và approval; không tự chấm pass vì ảnh tạo thành công.

## ADR-004: Reference bundle
Bộ ZIP v2.0 chỉ dùng làm nguồn yêu cầu/kiểm thử. Kho public không chứa tiểu thuyết, tranh bị loại, model draft, storyboard của dự án có bản quyền.

## ADR-005: Đi từ dữ liệu trước AI
Phase 1 làm project/chapters/character/beat trước. Chạy local không key. Rồi mới tiếp ingestion, engine, visual.

## ADR-006: Repository name
GitHub hiện đặt tên `Chi2Vy/Comic-Studio-AI.` (có dấu chấm ở cuối). Không tự đổi tên repository.

## ADR-007: GPT orchestration first (2026-11-18)
Comic Studio là nơi giữ canon, setting, skill, prompt templates, version, result intake và QC. GPT là trình thực thi bên ngoài; mặc định copy/export prompt và import kết quả thủ công. Không tự triển khai model/GPU pipeline; adapter AI API là tùy chọn, cần quyền và ngân sách.
