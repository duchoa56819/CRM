# 📖 Sổ tay Phân tích Dữ liệu CRM: Từ Dữ liệu Thô đến Quyết định Chiến lược

Tài liệu này là một "kim chỉ nam" hướng dẫn bạn từng bước quy trình phân tích bất kỳ một bộ dữ liệu CRM nào, đồng thời cung cấp một hệ thống "Từ điển Metrics" (Chỉ số) ánh xạ trực tiếp đến các "nỗi đau" (Pain points) của doanh nghiệp.

---

## PHẦN 1: QUY TRÌNH 5 BƯỚC PHÂN TÍCH DỮ LIỆU CRM CHUẨN

### Bước 1: Xác định Mục tiêu Kinh doanh (Define Business Goals)
Đừng vội nhảy vào vẽ biểu đồ ngay. Hãy bắt đầu bằng cách ngồi với Giám đốc Sales (CSO) hoặc CEO để hỏi:
- *Chúng ta đang gặp vấn đề gì nhất?* (Chạy quảng cáo tốn kém nhưng chốt kém? Sales than phiền lead rác? Hay hay hụt doanh thu cuối tháng?)
- *Quyết định nào sẽ được đưa ra sau báo cáo này?* (Cắt giảm nhân sự, đổi kịch bản sales, hay dồn ngân sách marketing cho sản phẩm khác?)

### Bước 2: Chuẩn bị & Làm sạch dữ liệu (Data Preparation & Cleaning)
Một bộ dữ liệu CRM tiêu chuẩn cần có các trường (cột) cốt lõi sau:
1. **Định danh:** Lead ID, Organization, Industry, Country.
2. **Quy trình:** Status (Trạng thái), Stage (Giai đoạn phễu), Owner (Nhân viên phụ trách).
3. **Giá trị:** Deal Value ($), Probability (Xác suất chốt %).
4. **Thời gian:** Lead Acquisition Date (Ngày nhận lead), Expected Close Date (Ngày dự kiến chốt), Actual Close Date (Ngày thực tế chốt/rớt).

*Các công việc làm sạch:*
- Lọc bỏ các Deal "ảo" (Test data).
- Xử lý các dòng bị thiếu `Actual Close Date` (đối với những Deal đã có Status là Customer hoặc Lost).
- Đồng nhất định dạng tiền tệ và ngày tháng.

### Bước 3: Tính toán cột phụ (Feature Engineering)
Dữ liệu gốc thường không đủ để ra insight, bạn cần tạo thêm các cột như:
- **Sales Cycle (Chu kỳ bán hàng):** `Actual Close Date` - `Lead Acquisition Date` (Bao nhiêu ngày để chốt 1 deal?).
- **Delay Days (Số ngày trễ hạn):** `Actual Close Date` - `Expected Close Date` (Khách hứa nhưng bao lâu sau mới trả tiền?).
- **Outcome (Kết quả):** Phân loại rõ ràng 3 tệp `Open` (Đang xử lý), `Won` (Thắng), `Lost/Disqualified` (Thua/Hủy).

### Bước 4: Khám phá & Trực quan hóa (EDA)
Bắt đầu vẽ biểu đồ trả lời các câu hỏi:
- Nhìn tổng quan: Phễu rớt nhiều nhất ở đâu?
- Nhìn chi tiết: Ai là người bán giỏi nhất? Ngành nào đem lại nhiều tiền nhất?
*(Tham khảo phần Metrics bên dưới để biết nên vẽ gì).*

### Bước 5: Đưa ra Actionable Insights (Khuyến nghị hành động)
Data không có ý nghĩa nếu không dẫn đến hành động. 
- *Thay vì nói:* "Tỷ lệ rớt ở giai đoạn Opportunity là 50%".
- *Hãy nói:* "Tỷ lệ rớt ở Opportunity lên tới 50%. Khuyến nghị: Tổ chức buổi training tuần tới để đào tạo lại kỹ năng đàm phán giá (Objection Handling) cho team Sales."

---

## PHẦN 2: TỪ ĐIỂN METRICS TƯƠNG ỨNG VỚI CÁC BÀI TOÁN DOANH NGHIỆP

Dưới đây là cách chọn đúng loại "thuốc" (Metric) cho đúng "bệnh" (Vấn đề doanh nghiệp).

### Vấn đề 1: Marketing đổ lỗi cho Sales chốt dở, Sales đổ lỗi cho Marketing chạy "Lead rác"
**Bài toán:** Đánh giá chất lượng Lead và hiệu năng phễu chuyển đổi.
**Các Metrics sử dụng:**
1. **Lead-to-Customer Conversion Rate (Tỷ lệ chuyển đổi tổng):** Đánh giá chung sức khỏe toàn hệ thống.
2. **Funnel Drop-off Rate (Tỷ lệ rụng theo từng phễu):** 
   - Rụng nhiều ở bước đầu (Mới tiếp cận -> Phân loại): Lead rác, Marketing làm sai target.
   - Rụng nhiều ở bước cuối (Gửi báo giá -> Chốt): Lỗi do Sales yếu kỹ năng đàm phán hoặc giá quá cao.
3. **MQL to SQL Ratio:** Tỷ lệ Leads từ Marketing (MQL) được Sales chấp nhận (SQL).

### Vấn đề 2: Ai cũng làm việc bận rộn nhưng doanh thu lẹt đẹt
**Bài toán:** Đánh giá năng lực thực sự và quản trị thời gian của đội Sales.
**Các Metrics sử dụng:**
1. **Win Rate vs. Revenue (Tỷ lệ thắng & Doanh thu thực tế):** Nhìn Win Rate để đánh giá kỹ năng, nhìn Revenue để xem quy mô Deal.
2. **Average Sales Cycle Length (Chu kỳ chốt sale trung bình):** Nếu thời gian chốt quá dài, nhân viên đang bị "ngâm" quá lâu với các khách hàng không tiềm năng.
3. **Lead Response Time:** Khách hàng để lại form, bao lâu Sales gọi? (Thường response dưới 5 phút tỷ lệ win tăng gấp 9 lần).
4. **Activity Metrics:** Số cuộc gọi, số email, số cuộc họp tạo ra / ngày.

### Vấn đề 3: Cuối tháng Sếp hỏi "Tháng sau có bao nhiêu tiền?", Sales trả lời cảm tính
**Bài toán:** Quản trị rủi ro dòng tiền và độ chính xác của Dự báo (Forecasting).
**Các Metrics sử dụng:**
1. **Unweighted Pipeline Value:** Tổng giá trị tất cả các deals đang mở (Phản ánh "ước mơ").
2. **Weighted Pipeline Value (Expected Revenue):** `Deal Value` × `Probability %`. (Phản ánh "thực tế" dòng tiền CFO có thể tin tưởng).
3. **Pipeline Coverage Ratio:** Bằng Tổng Pipeline / Chỉ tiêu (Quota) của tháng. Thường phải duy trì tỷ lệ 3x (Phễu phải lớn gấp 3 lần chỉ tiêu thì mới an toàn chốt đủ số).
4. **Forecast Accuracy / Slippage Rate:** Tỷ lệ các deal bị dời ngày chốt (Close Date) sang tháng sau. Giúp "nắn" lại thói quen hứa hẹn hão huyền của Sales.

### Vấn đề 4: Chốt được nhiều nhưng mất đi cũng nhiều
**Bài toán:** Phân tích lý do thất bại và vấn đề gắn kết sản phẩm.
**Các Metrics sử dụng:**
1. **Lost Reasons Breakdown (Tỷ trọng lý do thất bại):** Phân chia theo: *Giá cao, Đổi ý chọn đối thủ, Thiếu tính năng, Chăm sóc kém.*
2. **Lost Deals by Segment:** Ngành nào, khu vực nào, sản phẩm nào rớt nhiều nhất? Nếu sản phẩm A rớt tới 60% vì "Thiếu tính năng", đó là tín hiệu SOS gửi cho đội Product Development.
3. **Churn Rate vs. Time-to-Churn:** Khách ký hợp đồng rồi nhưng hủy sau 1-2 tháng? Lỗi nằm ở khâu Customer Success (Chăm sóc khách hàng) hoặc Onboarding (Hướng dẫn sử dụng).

---
**💡 Lời khuyên cuối:** Một báo cáo Data Analysis CRM thành công là báo cáo khiến Giám đốc phải nói: *"Chúng ta phải thay đổi quy trình ngay ngày mai"*, chứ không phải là báo cáo khiến họ trầm trồ *"Biểu đồ này nhìn đẹp quá!"*.
