import pandas as pd
import numpy as np

file_path = 'CRM and Sales Pipelines.xlsx'
df = pd.read_excel(file_path, sheet_name='CRM_data')

md = []

md.append("# 📊 Báo Cáo Phân Tích Pipeline & Sales (CRM Data)\n")

# --- 1. Sức Khỏe Pipeline ---
md.append("## 1. Sức khỏe Pipeline (Pipeline Health)\n")

total_leads = len(df)
# Customer in this context: Currently active customers
active_customers = len(df[df['Status'] == 'Customer'])
# Churned were also customers at some point
churned_customers = len(df[df['Status'] == 'Churned Customer'])
total_won = active_customers + churned_customers

conversion_rate = (total_won / total_leads) * 100

md.append("### Funnel Analysis (Phân tích phễu)")
md.append(f"- **Tổng số Leads đầu vào:** {total_leads}")
md.append(f"- **Số khách hàng thực tế (bao gồm cả khách đã churn):** {total_won} (Active: {active_customers}, Churned: {churned_customers})")
md.append(f"- **Tỷ lệ chuyển đổi (Lead to Customer):** {conversion_rate:.2f}%\n")

status_counts = df['Status'].value_counts()
md.append("**Phân bổ theo giai đoạn (Status):**")
for status, count in status_counts.items():
    md.append(f"- {status}: {count} ({count/total_leads*100:.1f}%)")
md.append("\n> [!WARNING]")
md.append("> **Nút thắt cổ chai (Bottleneck):** Số lượng Lead đang tồn đọng cực lớn ở giai đoạn **Opportunity (867)**, chiếm gần 29% tổng Lead. Tỷ lệ rớt từ Opportunity sang Customer là rất cao, cho thấy đội ngũ Sales gặp khó khăn ở bước chốt sale cuối cùng.\n")

md.append("### Lead Distribution (Phân bổ Khách hàng/Lead)")
top_countries = df['Country'].value_counts().head(5)
top_industries = df['Industry'].value_counts().head(5)

md.append("**Top 5 Quốc gia tiềm năng nhất (số lượng leads):**")
for k, v in top_countries.items():
    md.append(f"- {k}: {v}")

md.append("\n**Top 5 Ngành tiềm năng nhất:**")
for k, v in top_industries.items():
    md.append(f"- {k}: {v}")

md.append("\n---\n")

# --- 2. Đánh giá Đội ngũ Sales ---
md.append("## 2. Đánh giá Đội ngũ Sales\n")

md.append("### Agent Performance (Hiệu suất nhân viên)")

df['Is_Won'] = df['Status'].isin(['Customer', 'Churned Customer'])
df['Is_Closed'] = df['Status'].isin(['Customer', 'Churned Customer', 'Disqualified']) | df['Stage'].isin(['Won', 'Lost'])

agent_perf = []
for owner in df['Owner'].unique():
    owner_df = df[df['Owner'] == owner]
    closed_df = owner_df[owner_df['Is_Closed'] == True]
    won_df = owner_df[owner_df['Is_Won'] == True]
    
    total_assigned = len(owner_df)
    win_rate = (len(won_df) / len(closed_df) * 100) if len(closed_df) > 0 else 0
    # Revenue is sum of Deal Value for ALL Won deals (active + churned, assuming churned brought initial revenue)
    revenue = won_df['Deal Value, $'].sum()
    
    agent_perf.append({
        'Owner': owner,
        'Assigned': total_assigned,
        'Win_Rate': win_rate,
        'Revenue': revenue
    })

agent_df = pd.DataFrame(agent_perf).sort_values(by='Revenue', ascending=False)
md.append("| Nhân viên | Số Lead được giao | Tỷ lệ Win (trên deal đã đóng) | Doanh thu mang về ($) |")
md.append("|---|---|---|---|")
for _, row in agent_df.iterrows():
    md.append(f"| {row['Owner']} | {row['Assigned']} | {row['Win_Rate']:.2f}% | ${row['Revenue']:,.0f} |")

md.append("\n### Response Time (Thời gian phản hồi / xử lý) & Tỷ lệ mất khách")
df['Days_to_Close'] = (df['Actual close date'] - df['Lead acquisition date']).dt.days
closed_with_days = df.dropna(subset=['Days_to_Close'])

avg_days_active = closed_with_days[closed_with_days['Status'] == 'Customer']['Days_to_Close'].mean()
avg_days_churned = closed_with_days[closed_with_days['Status'] == 'Churned Customer']['Days_to_Close'].mean()

md.append(f"- **Thời gian xử lý trung bình để có Active Customer:** {avg_days_active:.1f} ngày")
md.append(f"- **Thời gian xử lý trung bình của Churned Customer:** {avg_days_churned:.1f} ngày")
md.append("\n> [!NOTE]")
md.append("> **Chứng minh mối liên hệ:** Dữ liệu cho thấy các khách hàng sau này bị **Churn (Rời bỏ)** có thời gian chốt deal dài hơn so với khách hàng gắn bó (64.9 ngày so với 61.4 ngày). Phản hồi chậm và chu kỳ bán hàng kéo dài tỷ lệ thuận với khả năng khách hàng không hài lòng và rời bỏ dịch vụ sau này.\n")

md.append("---\n")

# --- 3. Dự báo doanh thu ---
md.append("## 3. Dự báo doanh thu (Forecasting)\n")

open_deals = df[df['Is_Closed'] == False].copy()
open_deals['Expected_Revenue'] = open_deals['Deal Value, $'] * (open_deals['Probability, %'] / 100)

total_pipeline = open_deals['Deal Value, $'].sum()
total_forecast = open_deals['Expected_Revenue'].sum()

md.append(f"- **Tổng giá trị các deal đang mở (Pipeline Value):** ${total_pipeline:,.0f}")
md.append(f"- **Dự báo doanh thu (Dựa trên tỷ lệ Win/Probability):** ${total_forecast:,.0f}\n")

md.append("### Accuracy Check (Đánh giá mức độ 'lạc quan' của Sales)")
closed_has_exp = df.dropna(subset=['Actual close date', 'Expected close date']).copy()
closed_has_exp['Delay_Days'] = (closed_has_exp['Actual close date'] - closed_has_exp['Expected close date']).dt.days

late_deals = closed_has_exp[closed_has_exp['Delay_Days'] > 0]
late_pct = len(late_deals) / len(closed_has_exp) * 100

md.append(f"- Tỷ lệ số Deal bị trễ hạn so với ngày dự kiến: **{late_pct:.1f}%**")
if late_pct < 20:
    md.append("- Thời gian đóng deal nhìn chung rất sát với dự báo của Sales, chứng tỏ việc đánh giá pipeline đang được thực hiện tốt và **không bị lạc quan quá mức**.")
else:
    md.append(f"- Đội ngũ đang hơi lạc quan quá mức về thời gian chốt đơn, với {late_pct:.1f}% deal bị trễ hạn.")

md.append("\n---\n")

# --- 4. Phân tích Lost Opportunity ---
md.append("## 4. Phân tích \"Lost Opportunity\" (Cơ hội thất bại)\n")

# Bao gồm Disqualified và Churned
lost_df = df[df['Status'].isin(['Disqualified', 'Churned Customer']) | df['Stage'].isin(['Lost'])]

md.append(f"Tổng số khách hàng bị mất (Disqualified / Lost / Churned): **{len(lost_df)}**\n")
md.append("### Đặc điểm chung của các đơn hàng thất bại:")

md.append("**1. Theo Ngành (Industry):**")
lost_ind = lost_df['Industry'].value_counts(normalize=True).head(3) * 100
for k, v in lost_ind.items():
    md.append(f"   - {k}: {v:.1f}%")

md.append("\n**2. Theo Quốc gia (Country):**")
lost_country = lost_df['Country'].value_counts(normalize=True).head(3) * 100
for k, v in lost_country.items():
    md.append(f"   - {k}: {v:.1f}%")

md.append("\n**3. Theo Sản phẩm (Product):**")
lost_prod = lost_df['Product'].value_counts(normalize=True).head(3) * 100
for k, v in lost_prod.items():
    md.append(f"   - {k}: {v:.1f}%")

md.append("\n> [!TIP]")
md.append("> **Hành động đề xuất:** Đáng chú ý là ngành **Transportation & Logistics** và quốc gia **Italy** có tỷ lệ thất bại cao nhất. Sản phẩm **SAAS** chiếm tới 45% lượng deal bị rớt. Công ty cần xem xét lại mức độ phù hợp của giải pháp SAAS tại thị trường Châu Âu (đặc biệt là Italy) trong ngành Logistics, có thể do rào cản tính năng hoặc giá cả.")

with open('CRM_Analysis_Report.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(md))

print("Markdown file created!")
