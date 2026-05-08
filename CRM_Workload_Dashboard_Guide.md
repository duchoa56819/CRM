# 👥 Dashboard & DAX: Khối lượng công việc & Hiệu suất vùng miền

Góc nhìn thứ 4 tập trung vào **con người (Sales Owners)** và **vùng địa lý (Geography)**. Mục tiêu là để trả lời câu hỏi: *"Chúng ta có đang giao quá nhiều việc cho một người không?"* và *"Vùng đất nào đang mang lại hiệu quả chốt đơn tốt nhất?"*

---

## 📈 Trực quan hóa (Dashboards)

````carousel
![Workload vs Efficiency](C:/Users/Tuan/.gemini/antigravity/brain/7aaf4099-8e8c-41d6-a94e-091361527c2e/artifacts/workload_efficiency.png)
<!-- slide -->
![Cơ cấu danh mục Owner Portfolio](C:/Users/Tuan/.gemini/antigravity/brain/7aaf4099-8e8c-41d6-a94e-091361527c2e/artifacts/owner_portfolio.png)
<!-- slide -->
![Hiệu suất theo Quốc gia](C:/Users/Tuan/.gemini/antigravity/brain/7aaf4099-8e8c-41d6-a94e-091361527c2e/artifacts/regional_efficiency.png)
````

---

## 🔢 Công thức DAX cho Hiệu suất & Phân bổ

### 1. Số lượng Lead đang quản lý (Workload)
```dax
Active Leads count = COUNTROWS('CRM_data')
```

### 2. Doanh thu trung bình trên mỗi Lead (Revenue per Lead)
*Chỉ số này giúp biết một nhân viên "tận dụng" tệp khách được giao tốt đến mức nào:*
```dax
Revenue per Lead = DIVIDE([Total Revenue], [Active Leads count], 0)
```

### 3. Hiệu suất Vùng miền (Country Rank)
```dax
Country Win Rate Rank = 
RANKX(ALL('CRM_data'[Country]), [Win Rate %], , DESC)
```

---

## 💡 Giải thích ý nghĩa Quản trị (Perspective)

1.  **Mối tương quan Workload - Win Rate:** 
    *   Hãy nhìn vào biểu đồ Scatter. Nếu một Sales Owner có số lượng Lead quá lớn (như Laura Thompson với 749 leads) nhưng Win Rate vẫn ổn định, đó là một nhân sự cực kỳ xuất sắc. 
    *   Tuy nhiên, nếu số Lead tăng mà Win Rate giảm mạnh, đó là dấu hiệu của việc **quá tải**. Bạn nên san sẻ bớt Lead cho những người có Workload thấp hơn (như Sarah Davis hay Kevin Anderson) để tăng tỷ lệ chốt tổng thể.
2.  **Portfolio Mix (Cơ cấu danh mục):** Biểu đồ này cho biết khẩu vị bán hàng của từng người. 
    *   *Laura Thompson* và *Jessica Martinez* đang gánh vác phần lớn các Deal lớn (>10k). 
    *   *David Wilson* chủ yếu tập trung vào các Deal nhỏ. Điều này giúp bạn phân loại ai nên là người tiếp nhận các "Cá mập" (Enterprise leads) và ai nên xử lý các "Cá con" (SMB leads).
3.  **Regional Efficiency (Hiệu quả vùng miền):** **Netherlands (Hà Lan)** đang có tỷ lệ thắng vượt trội (65.8%). Đây là tín hiệu cho bộ phận Marketing: *"Hãy dồn thêm ngân sách quảng cáo vào Hà Lan vì tỷ lệ chốt ở đây đang tốt nhất"*.

---
> [!TIP]
> **Hành động đề xuất:** Cân nhắc điều chuyển bớt Lead từ nhóm đang quá tải sang nhóm có Workload thấp nhưng Win Rate cao (như Kevin Anderson) để tối ưu hóa doanh thu mà không cần tuyển thêm người. Bạn cũng nên nghiên cứu tại sao thị trường Hà Lan lại có tỷ lệ thắng cao như vậy để áp dụng cho các quốc gia khác.
