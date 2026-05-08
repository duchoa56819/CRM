# 📅 Dashboard & DAX: Tính chu kỳ & Thời điểm vàng

Góc nhìn thứ 7 tập trung vào **Thời gian (Time dimension)**. Chúng ta đi tìm những "thời điểm vàng" trong tuần và trong năm để trả lời câu hỏi: *"Khi nào là lúc khách hàng dễ chốt đơn nhất?"* và *"Chúng ta nên tập trung nỗ lực Sales vào thứ mấy?"*

---

## 📈 Trực quan hóa (Dashboards)

````carousel
![Tính chu kỳ theo Tháng](C:/Users/Tuan/.gemini/antigravity/brain/7aaf4099-8e8c-41d6-a94e-091361527c2e/artifacts/seasonal_win_rate.png)
<!-- slide -->
![Hiệu suất theo Thứ trong tuần](C:/Users/Tuan/.gemini/antigravity/brain/7aaf4099-8e8c-41d6-a94e-091361527c2e/artifacts/daily_win_rate.png)
<!-- slide -->
![Nhu cầu Sản phẩm theo Tháng](C:/Users/Tuan/.gemini/antigravity/brain/7aaf4099-8e8c-41d6-a94e-091361527c2e/artifacts/seasonal_product_demand.png)
````

---

## 🔢 Công thức DAX cho Tính chu kỳ

### 1. Phân loại Thứ trong tuần (Day of Week)
```dax
Day Name = FORMAT('CRM_data'[Lead acquisition date], "dddd")
```

### 2. Tỷ lệ thắng theo Thứ (Win Rate by Day)
```dax
Win Rate by Day = 
CALCULATE(
    [Win Rate %],
    ALLEXCEPT('CRM_data', 'CRM_data'[Day Name])
)
```

### 3. Chỉ số Mùa vụ (Seasonality Index)
*So sánh hiệu suất của tháng hiện tại với trung bình cả năm:*
```dax
Seasonality Index = 
DIVIDE(
    [Win Rate %],
    CALCULATE([Win Rate %], ALL('CRM_data')),
    0
)
```

---

## 💡 Giải thích ý nghĩa Quản trị (Perspective)

1.  **Tháng Hai bùng nổ (February Peak):** 
    *   Dữ liệu cho thấy tỷ lệ thắng của các Lead nhận vào trong **tháng 2** cao đột biến (**65.4%**), so với mức trung bình 45-50% của các tháng khác.
    *   **Insight:** Có thể do đầu năm khách hàng có ngân sách mới và nhu cầu thay đổi mạnh mẽ. Đây là thời điểm doanh nghiệp nên dồn toàn lực (All-in) cho các chiến dịch Marketing.
2.  **Ngày vàng Thứ Năm (Golden Thursday):** 
    *   Các Lead nhận vào ngày **Thứ Năm** có tỷ lệ chốt đơn tốt nhất (**58.8%**). Trong khi đó, các Lead nhận vào Chủ Nhật và Thứ Ba có tỷ lệ thấp nhất.
    *   **Insight:** Điều này gợi ý rằng tâm lý khách hàng doanh nghiệp thường cởi mở nhất vào cuối tuần (Thứ Năm, Thứ Sáu). Marketing nên cân nhắc đẩy mạnh chạy quảng cáo vào chiều Thứ Tư để đón đầu lượng Lead chất lượng vào Thứ Năm.
3.  **Sự dịch chuyển nhu cầu Sản phẩm:** 
    *   Biểu đồ Heatmap cho thấy sản phẩm **Services** có nhu cầu tăng vọt vào **tháng 3** (283 leads), trong khi **SAAS** lại khá ổn định qua các tháng.
    *   **Quản trị:** Đội ngũ cung ứng dịch vụ cần chuẩn bị nhân sự sẵn sàng cho cao điểm vào tháng 3 hàng năm.

---
> [!TIP]
> **Hành động đề xuất:** Hãy điều chỉnh lịch trực Hotline và xử lý Lead của đội Sales. Ưu tiên những nhân sự "thiện chiến" nhất trực vào ngày **Thứ Năm và Thứ Sáu** để tối ưu hóa tỷ lệ chốt từ những Lead chất lượng cao này. Ngược lại, ngày Thứ Ba và Chủ Nhật có thể dành cho việc đào tạo hoặc xử lý giấy tờ.
