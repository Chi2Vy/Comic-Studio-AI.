# GPT Orchestration First — Đặc tả trọng tâm v1.0

**Quyết định ngày 18/11/2026:** Comic Studio là bộ điều hành chuyển thể truyện dựa trên GPT/AI bên ngoài. Studio chủ yếu **giữ dữ liệu, công cụ, skill, thiết lập đã khóa, câu lệnh, prompt, kết quả, bản sửa và kiểm duyệt**. Studio KHÔNG cần tích hợp mô hình AI tạo nội dung bên trong hoặc chạy GPU.

## 1. Phân công trách nhiệm

| Thành phần | Trách nhiệm |
| --- | --- |
| Comic Studio | Quản lý tiểu thuyết, nguồn/locator, Story Bible, Beat Ledger, Character Bible, Style/Mood/Mode, quy tắc G0–G6, Prompt Templates, Skill Registry, tasks, phiên bản và tiến độ |
| GPT/AI bên ngoài | Phân tích nguồn, biên kịch, storyboard, xây dựng hồ sơ nhân vật, dựng hoặc sửa hình, gợi ý QC theo prompt/ảnh/nguồn Studio chuẩn bị |
| Người dùng | Thiết lập nguyên tác/phong cách, chọn hướng sáng tạo, xét duyệt model/storyboard/trang/QC và quyền xuất bản |

**Giới hạn:** Prompt tốt không bảo đảm GPT tuân thủ 100%. Studio phải ghi nhận khác biệt, kiểm tra ràng buộc và yêu cầu duyệt; không tự công bố AI đã thực hiện khi chỉ mới tạo/copy prompt.

## 2. Chu trình điều phối

1. **Nạp nguồn:** tiểu thuyết, kịch bản, brief hoặc tệp tham khảo có quyền sử dụng; gắn project_id, file hash, source locator, verification_level.
2. **Khóa thiết lập dự án:** source version, canon, nhân vật và ngoại cảnh, timeline trang phục/vật phẩm, style/mood/mode, độ trung thành, ngân sách chap/trang và các ngoại lệ đã duyệt.
3. **Chọn tác vụ:** nghiên cứu, chuyển thể kịch bản, model sheet, storyboard, panel art, QA, sửa đúng vị trí.
4. **Prompt Compiler:** tìm trích đoạn nguồn và hồ sơ đã duyệt phù hợp tác vụ/scope; tổng hợp template theo phòng ban; chặn mâu thuẫn và cảnh báo dữ liệu chưa được xác minh.
5. **Prompt Pack:** manifest (project/task/versions/scope/dependency hashes); instruction (mục tiêu, ràng buộc, tham chiếu); expected output (định dạng/đối tượng); QA checklist.
6. **Giao việc với GPT:** mặc định **Copy Prompt / Export Pack** để người dùng gửi vào ChatGPT; **không** tuyên bố đã tự gửi. Kết nối chính thức tự động chỉ là tùy chọn về sau, có kiểm soát chi phí/quyền.
7. **Nhập kết quả GPT:** paste văn bản hoặc import file/ảnh, gắn vào task_id/pack_id, lưu bản nháp, giữ provenance và phiên bản.
8. **Kiểm duyệt:** chạy kiểm tra cấu trúc, thiếu beat/nhân vật/xưng hô/timeline, evidence G0–G6, nhận định của người dùng; không đạt thì đề xuất lệnh sửa.
9. **Sửa cục bộ:** xác định chap/page/panel/layer/mask/line và phiên bản gốc, chỉ thay đúng phạm vi đã duyệt, không phá panel/trang không liên quan.

## 3. Quy tắc lắp ghép Prompt

Thứ tự ưu tiên theo tính ràng buộc:
- Quyền tác phẩm, quy tắc an toàn và giới hạn nhà cung cấp AI.
- Canon và bản nguồn đã verified, đúng thời điểm trong timeline.
- Character Bible / Scene Bible / Costume version đã approved.
- Scope tác vụ, page/panel budget, yêu cầu sửa của người dùng.
- Skill và template đã duyệt cho từng công đoạn.
- Sự sáng tạo trong phạm vi cho phép.

**Nguồn chưa verified:** không tự nhận là đúng nguyên tác; prompt nêu rõ điểm chưa chắc chắn. Không ép GPT sáng tạo tình tiết để lấp lỗ hổng. Không nhét toàn bộ tiểu thuyết vào mọi prompt nếu chỉ cần vài trích đoạn.

## 4. Các kiểu lệnh ưu tiên

- RESEARCH_SOURCE: trích sự kiện/nhân vật/địa điểm và vị trí chứng cứ.
- SCRIPT_ADAPT: chuyển văn xuôi thành scene/dialogue với beat_ids và source_locators.
- DESIGN_CHARACTER: tạo mô tả/model sheet theo đúng Canon/Character Bible.
- PLAN_STORYBOARD: phân bổ chap/trang/panel, kiểm tra cover từng beat.
- DRAW_PANEL: yêu cầu tạo một panel với tài liệu nhân vật/bối cảnh đã khóa.
- REVIEW_QC: đối chiếu kết quả với nguồn, hình, lỗi tiếng Việt và G0–G6.
- REPAIR_SCOPE: sửa đúng trang/panel/vùng/text layer, bắt buộc liệt kê các yếu tố phải giữ nguyên.

Mỗi prompt có mã project/task/pack, loại tác vụ, scope, input versions, rules, expected-output format, uncertainties, acceptance checks và hướng dẫn khi thiếu dữ liệu.

## 5. Dữ liệu bổ sung

- ProjectBibleVersion, CanonFact, CharacterReferenceVersion, StyleProfile
- SkillDefinition + version + approvals; PromptTemplate + version
- Task (project_id, department, kind, chapter_id/page_id/panel_id/region, status)
- PromptPack (task_id, input_hashes, instructions, context references, generated_at)
- ExternalAIResult (pack_id, received_at, text/file/artifact_ref, source/provider note, status)
- QCReview (result/version, gate, findings, evidence, decision, reviewer)
- RepairRequest (source result, target region, required invariants, next prompt pack)

Không trộn dữ liệu giữa hai dự án. Kết quả đã approved được giữ bất biến, thay đổi phải tạo version mới.

## 6. Prompt Desk — màn hình trung tâm mới

- Chọn dự án, chap/page/panel, nhiệm vụ và phiên bản Skill.
- Chọn chế độ: bám sát nguồn / sáng tạo có kiểm soát; tải setting đã khóa tự động.
- Hiện những dữ liệu còn thiếu và nguồn đã đối chiếu.
- Nút **Tạo gói lệnh → Xem trước → Sao chép / Xuất tệp**.
- Nút **Nhập kết quả GPT** (dán text hoặc tải ảnh/file từ máy) → gắn đúng task → xem diff → QC → duyệt / tạo prompt sửa.
- Nhật ký các prompt và phiên bản AI đã nhận; lịch sử thao tác.

Phần cứng của Studio chỉ cần đủ chạy web/SQLite và làm việc với file; GPU tạo ảnh local không bắt buộc.

## 7. Kênh gửi lệnh

**A — Manual, mặc định, không phí API:** Studio biên soạn prompt, người dùng sao chép vào ChatGPT, sau đó đưa kết quả về Studio. Một website độc lập không tự điều khiển hội thoại ChatGPT đang mở chỉ nhờ gói ChatGPT.

**B — Tích hợp được hỗ trợ, tùy chọn:** Dùng API/connector chính thức nếu có quyền và ngân sách. Cần consent, lưu request ID, retries, lỗi; chi phí API có thể riêng với gói ChatGPT. Không xây chức năng giả 'Gửi ngay cho GPT'.

**C — Codex:** Dùng trong VS Code để phát triển mã nguồn Studio, không phải mặc định đóng vai engine vẽ truyện.

## 8. Lộ trình ưu tiên đã đổi

- **MVP A1:** Deterministic Prompt Builder + templates/Skill + copy/export + warnings (không cần mô hình AI).
- **MVP A2:** Task/PromptPack ledger, nhập kết quả GPT và map đúng scope/version, lưu local.
- **MVP A3:** QC G0–G6 dựa trên chứng cứ và lệnh repair cục bộ với ảnh/metadata tham chiếu.
- **MVP A4:** Thư viện kỹ năng tự rút kinh nghiệm có duyệt; kết nối GPT tự động tùy chọn, không phải chức năng bắt buộc.

### Tiêu chí test
- Context truyện A không được trộn vào prompt truyện B.
- Thông tin chưa verified không được khẳng định là verified.
- Mọi prompt có task ID, scope, input version; thiếu thiết lập quan trọng có cảnh báo.
- Import kết quả phải gắn đúng pack; không thể gắn nhầm chap/page/panel.
- Thay đổi panel 3 không tự cập nhật lại panel 1/2/4/5.
- QC thiếu evidence không được tự thành PASS.
