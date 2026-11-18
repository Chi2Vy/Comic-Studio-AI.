# UI/UX Studio — phác thảo và chức năng

## Trọng tâm UI mới: Prompt Desk

Tạo gói lệnh GPT (không gọi AI): chọn project, loại việc, chap/page/panel, Skill và bản nguồn; trình biên soạn phải hiển thị setting đã khóa và cảnh báo thiếu dữ liệu. Các hành động minh bạch: **Tạo prompt**, **Sao chép**, **Xuất gói**, **Nhập kết quả**, **QC**, **Tạo lệnh sửa**. Không dùng nút giả 'Run GPT' hay 'Gửi GPT' nếu chưa có tích hợp hỗ trợ. Xem [09-GPT-ORCHESTRATION.md](09-GPT-ORCHESTRATION.md).

## Bố cục
- Sidebar: Tổng quan, Biên kịch, Nghiên cứu, Nhân vật, Storyboard, Dựng tranh, Biên tập, Kiểm duyệt, AI & Skill.
- Topbar: tên studio, dự án hiện tại, trạng thái local và quyền nguồn.
- Dashboard: dự án, chapters, characters, beat ledger, số hạng mục review.
- Form dự án: title, synopsis, origin/adaptation, rights, Style/Mood/Mode.
- Chi tiết dự án: form thêm chapter/character/beat, danh sách có trạng thái và source locator.

## Phase 1 reality
Màn hình React này **chỉ quản lý dữ liệu**. Trang sản xuất ảnh và AI là placeholder, không được có nút giả báo thành công.

## Editor Phase 4
- Cây page → panel → layer/text; mask/brush/crop/transform; lock approved.
- Khi sửa mask: giữ original, apply diff vào đúng layer; compare, approve rồi commit version.
- Hai thao tác khác nhau: regenerate panel và edit mask; mặc định edit mask, không rerender nguyên trang.
- Thoại quản lý text layer Unicode; hỗ trợ sửa chính tả không đụng art.

## Tiếp cận
Điều hướng bằng bàn phím, nhãn form rõ, màu trạng thái kèm text, layout hỗ trợ màn hình laptop, không giấu lỗi API.
