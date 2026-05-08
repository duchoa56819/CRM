# 📊 Báo Cáo Phân Tích Pipeline & Sales (CRM Data)

## 1. Sức khỏe Pipeline (Pipeline Health)

### Funnel Analysis (Phân tích phễu)
- **Tổng số Leads đầu vào:** 3000
- **Số khách hàng thực tế (bao gồm cả khách đã churn):** 348 (Active: 171, Churned: 177)
- **Tỷ lệ chuyển đổi (Lead to Customer):** 11.60%

**Phân bổ theo giai đoạn (Status):**
- Opportunity: 867 (28.9%)
- Qualified: 567 (18.9%)
- Sales Accepted: 528 (17.6%)
- New: 513 (17.1%)
- Churned Customer: 177 (5.9%)
- Disqualified: 177 (5.9%)
- Customer: 171 (5.7%)

> [!WARNING]
> **Nút thắt cổ chai (Bottleneck):** Số lượng Lead đang tồn đọng cực lớn ở giai đoạn **Opportunity (867)**, chiếm gần 29% tổng Lead. Tỷ lệ rớt từ Opportunity sang Customer là rất cao, cho thấy đội ngũ Sales gặp khó khăn ở bước chốt sale cuối cùng.

### Lead Distribution (Phân bổ Khách hàng/Lead)
**Top 5 Quốc gia tiềm năng nhất (số lượng leads):**
- Italy: 620
- France: 422
- Germany: 420
- Switzerland: 392
- Portugal: 371

**Top 5 Ngành tiềm năng nhất:**
- Transportation & Logistics: 528
- Banking and Finance: 404
- IT & IT Services: 387
- Government Administration Healthcare: 253
- Professional Services  & Consulting: 232

---

## 2. Đánh giá Đội ngũ Sales

### Agent Performance (Hiệu suất nhân viên)
| Nhân viên | Số Lead được giao | Tỷ lệ Win (trên deal đã đóng) | Doanh thu mang về ($) |
|---|---|---|---|
| Laura Thompson | 749 | 56.71% | $218,624 |
| Michael Brown | 483 | 50.00% | $177,109 |
| Jessica Martinez | 511 | 58.10% | $145,299 |
| Emily Johnson | 275 | 50.00% | $115,032 |
| Kevin Anderson | 240 | 63.46% | $80,248 |
| John Smith | 259 | 40.30% | $75,652 |
| Sarah Davis | 249 | 50.00% | $73,028 |
| David Wilson | 234 | 36.73% | $46,283 |

### Response Time (Thời gian phản hồi / xử lý) & Tỷ lệ mất khách
- **Thời gian xử lý trung bình để có Active Customer:** 61.4 ngày
- **Thời gian xử lý trung bình của Churned Customer:** 64.9 ngày

> [!NOTE]
> **Chứng minh mối liên hệ:** Dữ liệu cho thấy các khách hàng sau này bị **Churn (Rời bỏ)** có thời gian chốt deal dài hơn so với khách hàng gắn bó (64.9 ngày so với 61.4 ngày). Phản hồi chậm và chu kỳ bán hàng kéo dài tỷ lệ thuận với khả năng khách hàng không hài lòng và rời bỏ dịch vụ sau này.

---

## 3. Dự báo doanh thu (Forecasting)

- **Tổng giá trị các deal đang mở (Pipeline Value):** $6,445,454
- **Dự báo doanh thu (Dựa trên tỷ lệ Win/Probability):** $2,893,848

### Accuracy Check (Đánh giá mức độ 'lạc quan' của Sales)
- Tỷ lệ số Deal bị trễ hạn so với ngày dự kiến: **11.5%**
- Thời gian đóng deal nhìn chung rất sát với dự báo của Sales, chứng tỏ việc đánh giá pipeline đang được thực hiện tốt và **không bị lạc quan quá mức**.

---

## 4. Phân tích "Lost Opportunity" (Cơ hội thất bại)

Tổng số khách hàng bị mất (Disqualified / Lost / Churned): **415**

### Đặc điểm chung của các đơn hàng thất bại:
**1. Theo Ngành (Industry):**
   - Transportation & Logistics: 16.4%
   - Banking and Finance: 14.2%
   - IT & IT Services: 10.1%

**2. Theo Quốc gia (Country):**
   - Italy: 21.9%
   - Switzerland: 14.2%
   - France: 13.5%

**3. Theo Sản phẩm (Product):**
   - SAAS: 43.6%
   - Services: 40.2%
   - Custom solution: 16.1%

> [!TIP]
> **Hành động đề xuất:** Đáng chú ý là ngành **Transportation & Logistics** và quốc gia **Italy** có tỷ lệ thất bại cao nhất. Sản phẩm **SAAS** chiếm tới 45% lượng deal bị rớt. Công ty cần xem xét lại mức độ phù hợp của giải pháp SAAS tại thị trường Châu Âu (đặc biệt là Italy) trong ngành Logistics, có thể do rào cản tính năng hoặc giá cả.
