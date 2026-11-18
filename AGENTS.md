# Hướng dẫn cho Codex / AI contributors

0. **Tôn chỉ đã chốt:** Studio điều phối GPT/AI ngoài ứng dụng bằng Prompt Packs, không xây local model/GPU pipeline như công cụ chính. Manual copy/import là luồng mặc định, không tự điều khiển ChatGPT web UI hoặc dùng API key khi chưa có phê duyệt. Xem docs/09-GPT-ORCHESTRATION.md.
1. Làm theo `docs/01-PRD.md` và `docs/08-ROADMAP.md`; không báo chức năng đã hoàn tất nếu chưa có code và test.
2. Nguồn truyện, ảnh nhân vật, trang tranh, bản thảo và checkpoint từng tác phẩm là dữ liệu riêng: **KHÔNG** commit vào repository Public. Kiểm tra `git status` trước khi push.
3. Không tự thay đổi canon; mỗi beat cần `source_locator` và `verification_level`. Thiếu nguồn = `unverified`; AI suy luận không trở thành verified.
4. Tạo hình chưa có model sheet approved => `provisional`. Không tự đánh dấu PASS kiểm duyệt G0–G6.
5. Bất kỳ thao tác sửa ảnh nào trong các giai đoạn tiếp theo phải dựa trên panel/layer/version; không tái tạo toàn bộ trang đã duyệt để sửa một vùng.
6. Viết test cho endpoint và luật nghiệp vụ mới; lưu migrations khi đổi schema.
7. API giai đoạn 1 chỉ được dùng ở `127.0.0.1`, chưa có auth. Không đề xuất public deploy trước khi có xác thực và bảo vệ file nguồn.
8. Trước khi thêm AI: định nghĩa adapter, cách lưu bằng chứng, timeout/retry, chi phí ước lượng và cơ chế duyệt thủ công.
9. Nên mở PR nhỏ theo một milestone; cập nhật docs và ghi rõ phạm vi chưa có.
