# ⚖️ Dashboard & DAX: Hiệu chuẩn Xác suất & Quản trị Rủi ro

Góc nhìn thứ 5 là góc nhìn **"Hậu trường" (Backstage)**. Chúng ta không chỉ nhìn vào con số Sales báo cáo, mà chúng ta đi kiểm chứng xem **độ tin cậy (Reliability)** của các báo cáo đó đến đâu. Đây là cấp độ cao nhất trong phân tích CRM: *Phân tích tâm lý và rủi ro.*

---

## 📈 Trực quan hóa (Dashboards)

````carousel
![Hiệu chuẩn Xác suất: Dự báo vs Thực tế](C:/Users/Tuan/.gemini/antigravity/brain/7aaf4099-8e8c-41d6-a94e-091361527c2e/artifacts/prob_calibration.png)
<!-- slide -->
![Chỉ số Lạc quan (Bias Index)](C:/Users/Tuan/.gemini/antigravity/brain/7aaf4099-8e8c-41d6-a94e-091361527c2e/artifacts/sales_bias.png)
<!-- slide -->
![Bản đồ Rủi ro Pipeline](C:/Users/Tuan/.gemini/antigravity/brain/7aaf4099-8e8c-41d6-a94e-091361527c2e/artifacts/risk_scatter.png)
````

---

## 🔢 Công thức DAX cho Rủi ro & Hiệu chuẩn

### 1. Chỉ số Lạc quan (Optimism Bias)
*Công thức đo độ lệch giữa niềm tin của Sales và thực tế chốt đơn:*
```dax
Optimism Bias = AVERAGE('CRM_data'[Probability, %]) - [Win Rate %]
```
> *Giải thích:* Nếu chỉ số này > 0, nhân viên đang quá lạc quan (hứa nhiều làm ít). Nếu < 0, nhân viên đang quá thận trọng (giấu bài).

### 2. Giá trị rủi ro (At-Risk Pipeline)
*Xác định các Deal giá trị cao nhưng xác suất chốt do Sales đánh giá lại thấp:*
```dax
High Value Low Prob = 
IF(
    'CRM_data'[Deal Value, $] > 10000 && 'CRM_data'[Probability, %] < 40,
    "🔴 Rủi ro cao",
    "Bình thường"
)
```

### 3. Tỷ lệ thắng lịch sử theo Stage (Historical Stage Probability)
*Dùng để thay thế cho xác suất cảm tính của Sales:*
```dax
Historical Stage Prob = 
CALCULATE(
    [Win Rate %],
    ALL('CRM_data'),
    'CRM_data'[Stage] = EARLIER('CRM_data'[Stage])
)
```

---

## 💡 Giải thích ý nghĩa Quản trị (Perspective)

1.  **Sự sai lệch của Xác suất (Calibration Gap):** 
    *   Hãy nhìn vào biểu đồ hiệu chuẩn. Nhóm Deal được Sales đánh giá xác suất cực thấp (0-20%) thực tế lại có tỷ lệ thắng lên tới **56%**. 
    *   **Insight:** Điều này chứng tỏ cột `Probability` đang bị đánh giá một cách **cảm tính hoặc sai quy trình**. Đội ngũ Sales có xu hướng hạ thấp kỳ vọng để gây bất ngờ khi chốt được đơn.
2.  **Bias Index (Chỉ số tâm lý):** 
    *   **Kevin Anderson (-18.0):** Là người "giấu bài" nhiều nhất. Anh ấy luôn báo cáo xác suất thấp nhưng thực tế lại chốt đơn rất "khủng".
    *   **David Wilson (+6.4):** Là người lạc quan nhất. Anh ấy thường đánh giá xác suất cao hơn so với năng lực thực tế của mình.
    *   **Quản trị:** Sếp Sales cần biết điều này để khi nghe David báo cáo thì nên trừ hao đi, còn khi nghe Kevin báo cáo thì nên tự tin cộng thêm vào.
3.  **Risk Scatter (Bản đồ rủi ro):** Biểu đồ này giúp bạn "soi" những Deal "Cá mập" đang nằm ở vùng xác suất thấp. Đây chính là nơi sếp cần nhảy vào hỗ trợ Sales để đẩy xác suất chốt đơn lên cao hơn.

---
> [!TIP]
> **Hành động đề xuất:** Cần chuẩn hóa lại cách tính `Probability`. Thay vì để Sales tự điền, hãy gán cứng xác suất theo giai đoạn (ví dụ: Proposal sent = 60%, Nurturing = 30%) để dự báo tài chính được chính xác hơn. Bạn cũng nên dùng chỉ số Bias để đào tạo lại tư duy lập kế hoạch cho những nhân viên quá lạc quan.
