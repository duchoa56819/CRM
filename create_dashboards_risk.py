import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Cài đặt font và style
sns.set_theme(style="whitegrid", rc={"font.family": "sans-serif"})

file_path = 'CRM and Sales Pipelines.xlsx'
df = pd.read_excel(file_path, sheet_name='CRM_data')

# Basic prep
df['Is_Won'] = df['Status'].isin(['Customer', 'Churned Customer'])
df['Is_Closed'] = df['Status'].isin(['Customer', 'Churned Customer', 'Disqualified']) | df['Stage'].isin(['Won', 'Lost'])

# 1. Dashboard: Probability Calibration
bins = [0, 20, 40, 60, 80, 101]
labels = ['0-20%', '21-40%', '41-60%', '61-80%', '81-100%']
df['Prob_Bucket'] = pd.cut(df['Probability, %'], bins=bins, labels=labels, right=False)

cal_data = []
for bucket in labels:
    bucket_df = df[df['Prob_Bucket'] == bucket]
    closed = bucket_df[bucket_df['Is_Closed']]
    won = bucket_df[bucket_df['Is_Won']]
    actual_rate = (len(won) / len(closed) * 100) if len(closed) > 0 else 0
    cal_data.append({'Probability Bucket': bucket, 'Actual Win Rate (%)': actual_rate})

cal_df = pd.DataFrame(cal_data)

plt.figure(figsize=(10, 6))
ax = sns.barplot(data=cal_df, x='Probability Bucket', y='Actual Win Rate (%)', palette='YlOrRd')
plt.axhline(50, color='blue', linestyle='--', label='Đường chuẩn 50%')
plt.title('Hiệu chuẩn Xác suất: Dự đoán vs. Thực tế', fontsize=15, fontweight='bold', pad=20)
plt.ylabel('Tỷ lệ thắng thực tế (%)')
plt.legend()
plt.tight_layout()
plt.savefig('prob_calibration.png', dpi=300)
plt.close()

# 2. Dashboard: Owner Bias (Optimism vs Pessimism)
bias_stats = []
for owner in df['Owner'].unique():
    owner_df = df[df['Owner'] == owner]
    closed = owner_df[owner_df['Is_Closed']]
    won = owner_df[owner_df['Is_Won']]
    actual_win_rate = (len(won) / len(closed) * 100) if len(closed) > 0 else 0
    avg_prob = owner_df['Probability, %'].mean()
    bias_stats.append({'Owner': owner, 'Avg Assigned Prob': avg_prob, 'Actual Win Rate': actual_win_rate})

b_df = pd.DataFrame(bias_stats)
b_df['Bias'] = b_df['Avg Assigned Prob'] - b_df['Actual Win Rate']
b_df = b_df.sort_values(by='Bias')

plt.figure(figsize=(12, 6))
colors = ['#e74c3c' if x > 0 else '#2ecc71' for x in b_df['Bias']]
plt.barh(b_df['Owner'], b_df['Bias'], color=colors)
plt.axvline(0, color='black', linewidth=1)
plt.title('Chỉ số "Lạc quan" của Sales (Bias Index)', fontsize=15, fontweight='bold', pad=20)
plt.xlabel('Độ lệch: Dự báo - Thực tế (Dương = Lạc quan quá mức, Âm = Thận trọng)')
plt.tight_layout()
plt.savefig('sales_bias.png', dpi=300)
plt.close()

# 3. Dashboard: Deal Value vs Probability Scatter
plt.figure(figsize=(12, 7))
sns.scatterplot(data=df[df['Is_Closed'] == False], x='Probability, %', y='Deal Value, $', hue='Status', alpha=0.6, s=100)
plt.title('Bản đồ Rủi ro: Giá trị đơn hàng vs. Xác suất (Deals đang mở)', fontsize=15, fontweight='bold', pad=20)
plt.xlabel('Xác suất chốt đơn (%)')
plt.ylabel('Giá trị đơn hàng ($)')
plt.tight_layout()
plt.savefig('risk_scatter.png', dpi=300)
plt.close()

print("Perspective 5 dashboards generated.")
