# Quy trình 9 phòng ban

## Phòng ban
1. Giám đốc Studio: phân công, cảnh báo, phê duyệt ở các checkpoint.
2. Nghiên cứu nguồn: ingestion, quyền, index, source ledger, spoiler.
3. Biên kịch: beat, adaptation map, script, thoại có người nói.
4. Mỹ thuật: model sheet, palette, costume/timeline, scene bible.
5. Storyboard: chapter/page/panel plan, camera, bubble positions, page budget.
6. Sản xuất: từng panel riêng, layers, art PNG/JPG nguyên gốc.
7. Biên tập: sửa đúng mask/layer, lưu version, không ghi đè approved.
8. Kiểm duyệt: QA G0–G6 kèm evidence và người duyệt.
9. Kho tri thức & Skill: dự án, phản hồi, skill versions, rollback có duyệt.

## Đầu ra chuẩn mỗi đơn vị
`RESEARCH.md → BEATS.csv → ADAPTATION_MAP.csv → STORYBOARD.md → image/layers → QC.md → APPROVALS.md`.

## Checkpoint
- Source `unverified | toc_only | skim_checked | chapter_checked | cross_checked`.
- Sản phẩm `draft | provisional | review | approved | rejected`. Không suy ra approved từ việc có file.
- Sau mỗi công đoạn lưu `PROGRESS.json` hoặc trạng thái tương đương trong DB; báo rõ `next_action`.
- Thay đổi request không mặc nhiên tác động trang đã approved; cần bản sửa/version & kiểm tra dependency.

## Page budget
Tổng trang/chương đã khóa là bất biến cho tới khi chủ dự án approve thay đổi. Phân bố theo arc/beat và nhịp kể; không chia đều cơ học, không xóa beat nguồn để vừa ngân sách.

## Chữ tiếng Việt
Render art tách bubble/text; lấy thoại từ ledger có người nói; font Unicode, proof 100% và liên kết balloon_id → panel_id → line_id.
