# Quality Gates G0–G6 — kế thừa bộ ZIP v2.0

**G0 Source:** nguồn/chương xác minh, locator + beat, không tự dựng nguồn.
**G1 Script:** thứ tự sự kiện, người nói, xưng hô, nhịp cảm xúc, không đổi canon.
**G2 Model:** nhân vật, tạo hình, costume, thương tích theo timeline, model sheet approved.
**G3 Storyboard:** đúng đường đọc, có balloon plan, camera hợp cảnh, đủ beat.
**G4 Render:** từng trang nguyên gốc không phóng từ mosaic, không méo chi, đúng panel, phân giải nguồn.
**G5 Proof:** tách art/text, dấu tiếng Việt chính xác, bubble/speaker, legibility ở tỷ lệ đọc.
**G6 Continuity:** so trang liền nhau và toàn chap, trang phục/props/time, phê duyệt rõ.

## Điểm tham khảo từ REVIEW_MATRIX của gói v2
- Canon/Beat >= 4/5 và không sai sự kiện cốt lõi
- Character >= 4.5/5, model sheet approved
- Storyboard >= 4/5
- Render >= 4.5/5, kiểm 100%
- Text = 5/5 trước xuất bản
- Continuity >= 4.5/5

Lỗi BLOCK: sai canon, sai chính tả, sai nhân vật, ảnh mosaic cắt phóng, giải phẫu nghiêm trọng, bỏ beat quan trọng. Kể cả điểm tổng cao vẫn REJECT.

## Khả năng máy và người
Tự động (Phase 5): kiểm file tồn tại, độ phân giải, format, hash trùng, thứ tự, ledger đầy đủ, bubble mapping.
Phải thẩm định hình/chữ/ngữ nghĩa: người xem hoặc mô hình hỗ trợ và người chịu trách nhiệm ký duyệt. OCR/AI không đảm bảo 100%.

## Trạng thái
`not_ready | needs_review | pass | reject`, luôn lưu evidence + reviewed_by + timestamp + version. Thiếu ảnh hoặc quyền xem nguồn => not_ready, không có PASS giả.
