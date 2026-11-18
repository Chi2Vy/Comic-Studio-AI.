# PRD — Comic Studio AI v0.1

**Cập nhật:** 2026-11-18 · **Hướng triển khai:** A — nền tảng vững, mở rộng theo giai đoạn.

## 1. Bài toán
Cần studio chuyển tiểu thuyết/kịch bản/ý tưởng sang manhua, manga, webtoon, comic; nhất quán cốt truyện, nhân vật, ngoại cảnh, thoại và khả năng chỉnh đúng vị trí. Hệ thống dùng giao diện web local-first, tránh phụ thuộc một nhà cung cấp AI.

## 2. Personas
- **Tác giả/chủ dự án:** gửi ý tưởng/tác phẩm, chọn số chap/trang/phong cách, duyệt sản phẩm.
- **Biên kịch/biên tập:** chỉnh diễn biến, lời thoại, storyboard.
- **Họa sĩ/QA:** khóa nhân vật, chỉnh panel, kiểm lỗi và ký duyệt.
Một người có thể đảm nhiệm mọi vai trò ở bản local.

## 3. Functional requirements
- **FR-01** Tạo nhiều dự án, ngăn trộn canon giữa dự án.
- **FR-02** Nhập TXT/DOCX/EPUB/PDF/link được phép sử dụng, lưu nguồn và trạng thái quyền. *Phase 2*.
- **FR-03** Nhập kịch bản có sẵn hoặc gợi ý thành kịch bản từ mô tả, lưu version. *Phase 2*.
- **FR-04** Story bible, timeline, beat ledger có locator/evidence/verification. *Phase 1 có lưu ledger thủ công; Phase 2 tự phân tích*.
- **FR-05** Chọn độc lập Style, Mood, Mode; override từng scene; không sửa canon. *Phase 1 cấu hình*.
- **FR-06** Character Bible: turnaround, expressions, trang phục, quan hệ, approved version. *Phase 3*.
- **FR-07** Tự chọn số chương và trang; kế hoạch mapping theo beat, không bỏ beat. *Phase 3*.
- **FR-08** Storyboard chi tiết scene/page/panel/bubble/camera. *Phase 3*.
- **FR-09** Sinh từng panel ảnh và render từng trang ở phân giải gốc; lớp thoại tách riêng. *Phase 4*.
- **FR-10** Chỉnh sửa bằng mask/layer/panel; bảo toàn mọi phần ngoài vùng duyệt, versioned diffs. *Phase 4*.
- **FR-11** QC G0–G6, có bằng chứng, không tự thay REVIEW thành PASS. *Phase 5*.
- **FR-12** Tiến độ, checkpoint, cảnh báo và xuất PNG/JPG/PDF/CBZ. *Phase 5*.
- **FR-13** Ghi nhớ phản hồi và skill version; đề xuất update và rollback, không tự chạy code lạ. *Phase 6*.
- **FR-14** Local Windows, có thể mở LAN/online sau khi có auth. *Phase 1 local; cloud future*.

## 4. Nguyên tắc
- Không trộn nguồn từ các project. Truyện dài chỉ verified khi đối chiếu thực sự, không suy đoán.
- G0–G6 là các cổng riêng, có phê duyệt rõ ràng; chất lượng không suy ra từ kích thước ảnh.
- Người dùng kiểm soát thay đổi canon, số trang đã khóa, phiên bản model sheet và phát hành.
- Link tham khảo dùng để phân tích đặc điểm *chung* khi hợp lệ; không mặc nhiên được quyền sao chép hoặc huấn luyện.

## 5. Phi chức năng
- **NFR-01** Dữ liệu mặc định local SQLite; không upload ngầm.
- **NFR-02** Không cần dịch vụ trả tiền để dùng tính năng quản lý Phase 1.
- **NFR-03** Mọi thay đổi có project_id, ID riêng, timestamp; về sau version và audit log.
- **NFR-04** Chạy thử tối thiểu Windows 10/11, Python 3.11+, Node 20+.
- **NFR-05** Không cấu hình máy chủ public khi thiếu auth/TLS/rate limit.
- **NFR-06** Tạo test cho các quy tắc không bỏ beat, khóa model, edit mask, QC và rights trước khi triển khai.

## 6. Out of scope Phase 1
Không chạy Ollama/ComfyUI, tự đọc truyện, tự tạo ảnh, tự QC thị giác, inpainting, scraper, auth cloud, thanh toán, marketplace hay huấn luyện mô hình.

## 7. Tiêu chí chấp nhận Phase 1
1. Có thể tạo 2 project độc lập, lập chapter/character/beat; API không lẫn project.
2. Mặc định beat mới `unverified`, nhân vật mới `provisional`, quyền nguồn `unknown`.
3. Giao diện đọc danh sách, chọn dự án, nhập dữ liệu tối thiểu và thể hiện các phòng ban.
4. API chạy trên máy local không cần key, có test CRUD + kiểm lỗi.
5. README hướng dẫn khởi động và cảnh báo repo Public.
