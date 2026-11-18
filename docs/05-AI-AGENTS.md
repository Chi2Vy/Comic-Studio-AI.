# Role/Task Templates để điều phối GPT bên ngoài

Không có yêu cầu chạy 9 mô hình AI bên trong. Mỗi agent trong bảng dưới đây là **role + prompt template + quy tắc đầu vào/đầu ra**, được Prompt Compiler dùng để giao nhiệm vụ cho GPT bên ngoài. Chỉ truy hồi dữ liệu theo project_id. Xem [đặc tả](09-GPT-ORCHESTRATION.md).

| Agent | Đầu vào | Đầu ra | Bất biến |
|---|---|---|---|
| Director | tiến độ, approvals, QC | task plan, next_action | không tự publish |
| Researcher | nguồn đã được phép, locator | evidence, beat/source ledger | không nói đã đọc khi chưa đọc |
| Scriptwriter | verified beats, brief | scene/script/dialogue | không thay canon tùy tiện |
| Character Designer | canon_facts, timeline | model sheet proposals | chưa approve = provisional |
| Storyboard Artist | beats, page budget | panels, cameras, bubbles | không bỏ beat trọng yếu |
| Renderer | approved model, storyboard | từng panel/layer art | không render mosaic fake |
| Editor | asset/version, mask | local edit version | ngoài mask giữ nguyên |
| QC Reviewer | evidence và assets | G0–G6 verdict | thiếu bằng chứng = not_ready |
| Skill Curator | feedback, tools, releases | đề xuất skill diff | không tự execute code ngoài |

## Chuẩn metadata
`project_id, task_id, input_hashes, prompt_template_version, adapter_name, adapter_version, output_hash, proposed_at, review_status`.

## Cách 'tự học' có kiểm soát
1. Ghi lại correction và lời duyệt có provenance;
2. Truy hồi các quy tắc đã duyệt khi tác vụ tương tự;
3. Đề xuất chỉnh prompt/workflow qua diff;
4. So sánh bộ test, chỉ áp dụng sau khi người dùng duyệt;
5. Có rollback; không tự huấn luyện hay tự viết/chạy skill không tin cậy.

## Quyền tham khảo
Chỉ phân tích đặc điểm phong cách chung từ nguồn hợp lệ. Không giả định rằng link truyện = quyền tải toàn bộ hoặc tái tạo tranh/cốt truyện để phát hành.
