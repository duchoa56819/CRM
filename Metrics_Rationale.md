# 🧠 Giải thích tư duy lựa chọn Metrics (Chỉ số) trong CRM

Trong một Dashboard phân tích CRM, việc "vẽ gì" không quan trọng bằng "tại sao lại vẽ nó". Dưới đây là phần giải thích chi tiết ý nghĩa kinh doanh (Business Logic) đằng sau việc lựa chọn các chỉ số (Metrics) trong báo cáo vừa rồi.

---

## 1. Nhóm chỉ số Sức khỏe Pipeline (Pipeline Health)
Mục tiêu của nhóm này là trả lời câu hỏi: *"Dòng chảy khách hàng của chúng ta có đang khỏe mạnh không?"*

*   **Conversion Rate (Tỷ lệ chuyển đổi tổng thể):** Đây là nhịp tim của doanh nghiệp. Nhìn vào tỷ lệ này (11.6%), quản lý biết được để có 1 hợp đồng thì cần bơm vào bao nhiêu Leads.
*   **Funnel Analysis (Phân tích phễu & Nút thắt cổ chai):** Không ai mất khách hàng ở mọi bước. Phễu giúp phát hiện *Lỗ rò rỉ (Leakage)* lớn nhất nằm ở đâu. Khi thấy lượng lớn kẹt ở **Opportunity**, quản lý biết ngay vấn đề không nằm ở Marketing (đã mang về Lead) mà nằm ở khâu chốt giá / thương lượng của Sales.
*   **Lead Distribution (Top Quốc gia & Ngành):** Tiền Marketing có hạn. Nhờ chỉ số này, đội Marketing sẽ biết nên dồn tiền quảng cáo vào thị trường nào (Ý, Pháp) và ngành nào (Logistics) thay vì rải rác mù quáng.

---

## 2. Nhóm chỉ số Đánh giá đội ngũ Sales
Mục tiêu là đánh giá *hiệu năng thực sự* thay vì chỉ nhìn vào "Bề nổi" là tổng tiền.

*   **Sự kết hợp giữa Doanh thu ($) và Win Rate (%):** 
    *   *Tại sao không chỉ đo Doanh thu?* Vì một nhân viên có thể cực kỳ may mắn vớ được 1 deal khổng lồ nhưng lại để rớt 99 deal khác.
    *   *Win Rate* phản ánh kỹ năng và sự ổn định. Ví dụ: Laura mang về nhiều tiền nhất, nhưng Kevin mới là người có kỹ năng chốt sale sắc bén nhất (Win Rate > 63%).
*   **Response Time (Days to Close vs Churn):** *"Thời gian giết chết mọi thỏa thuận" (Time kills all deals)*. Bằng cách so sánh thời gian của khách hàng Active và khách hàng Churn, chúng ta chứng minh được bằng số liệu chứ không phải cảm tính: Việc ngâm deal lâu tỷ lệ thuận với việc mất khách.

---

## 3. Nhóm chỉ số Dự báo doanh thu (Forecasting)
Mục tiêu là giúp Giám đốc Tài chính (CFO) biết tháng sau công ty có bao nhiêu tiền để chi tiêu.

*   **Pipeline Value vs. Expected Revenue (Dự báo theo xác suất):** 
    *   *Pipeline Value* ($6.4M) là con số "ảo tưởng", là tổng tất cả số tiền đang nằm trong phễu nếu chốt được 100%.
    *   *Expected Revenue* ($2.8M) là con số "thực tế", được nhân với xác suất (Probability %) theo từng giai đoạn. Đây là con số sống còn để lập kế hoạch tài chính.
*   **Accuracy Check (Delay Days - Độ trễ):** Đội Sales thường mắc hội chứng *"Đôi mắt màu hồng"* (quá lạc quan về ngày khách hàng sẽ chuyển tiền). Việc đo lường % deal trễ hạn giúp điều chỉnh sự kỳ vọng và "nắn" lại thói quen đặt ngày Close Date bừa bãi của Sales.

---

## 4. Nhóm phân tích Lost Opportunity (Cơ hội thất bại)
Mục tiêu là: *"Học từ thất bại để không lặp lại."*

*   **Chia Lost Deals theo Industry (Ngành) và Product (Sản phẩm):** Nếu ta mất rải rác thì do lỗi của Sales. Nhưng nếu ta mất cục bộ (VD: 45% rớt ở sản phẩm SAAS và chủ yếu rớt ở ngành Logistics), thì đây là **lỗi của Sản phẩm hoặc Product-Market Fit**. Nó báo hiệu cho bộ phận Product Development (Phát triển sản phẩm) rằng tính năng phần mềm SAAS của chúng ta đang không đáp ứng được quy trình của các công ty vận tải tại Châu Âu.

> [!NOTE]
> **Tổng kết:** Việc chọn Metrics không phải là cố gắng hiển thị tất cả các cột trong file Excel, mà là kết nối các điểm dữ liệu lại với nhau để kể một câu chuyện kinh doanh, từ đó đưa ra **Actionable Insights** (Các hành động cụ thể để cải thiện).
