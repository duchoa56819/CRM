import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Cài đặt font và style
sns.set_theme(style="whitegrid", rc={"font.family": "sans-serif"})

file_path = 'CRM and Sales Pipelines.xlsx'
df = pd.read_excel(file_path, sheet_name='CRM_data')

# Prepare common data
df['Is_Won'] = df['Status'].isin(['Customer', 'Churned Customer'])
df['Is_Closed'] = df['Status'].isin(['Customer', 'Churned Customer', 'Disqualified']) | df['Stage'].isin(['Won', 'Lost'])
df['Days_to_Close'] = (df['Actual close date'] - df['Lead acquisition date']).dt.days

# 1. Dashboard: Org Size Performance (Win Rate & Sales Cycle)
org_perf = []
for size in df['Organization size'].unique():
    size_df = df[df['Organization size'] == size]
    closed = size_df[size_df['Is_Closed']]
    won = size_df[size_df['Is_Won']]
    win_rate = (len(won) / len(closed) * 100) if len(closed) > 0 else 0
    avg_days = size_df[size_df['Is_Won'] == True]['Days_to_Close'].mean()
    org_perf.append({'Org Size': size, 'Win Rate (%)': win_rate, 'Days to Close': avg_days})

org_df = pd.DataFrame(org_perf).sort_values(by='Win Rate (%)', ascending=False)

fig, ax1 = plt.subplots(figsize=(12, 6))
ax2 = ax1.twinx()

sns.barplot(data=org_df, x='Org Size', y='Win Rate (%)', ax=ax1, palette='Blues_d', alpha=0.8)
sns.lineplot(data=org_df, x='Org Size', y='Days to Close', ax=ax2, color='#e67e22', marker='o', linewidth=3, markersize=10, label='Days to Close')

ax1.set_title('Hiệu suất theo Quy mô Doanh nghiệp (Win Rate vs Chu kỳ bán hàng)', fontsize=15, fontweight='bold', pad=20)
ax1.set_ylabel('Tỷ lệ thắng (Win Rate %)', color='#2980b9', fontweight='bold')
ax2.set_ylabel('Thời gian chốt đơn (Ngày)', color='#e67e22', fontweight='bold')
ax1.set_ylim(0, 100)

plt.tight_layout()
plt.savefig('segment_performance.png', dpi=300)
plt.close()

# 2. Dashboard: Product & Revenue Analysis
prod_rev = df.groupby('Product')['Deal Value, $'].sum().reset_index().sort_values(by='Deal Value, $', ascending=False)

plt.figure(figsize=(10, 6))
colors = sns.color_palette('pastel')[0:3]
plt.pie(prod_rev['Deal Value, $'], labels=prod_rev['Product'], autopct='%1.1f%%', startangle=140, colors=colors, explode=(0.05, 0, 0))
plt.title('Cơ cấu Doanh thu theo dòng Sản phẩm', fontsize=15, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('product_revenue_pie.png', dpi=300)
plt.close()

# 3. Dashboard: ICP Heatmap (Org Size vs Product - Won Value)
icp_matrix = df[df['Is_Won'] == True].pivot_table(
    index='Organization size', 
    columns='Product', 
    values='Deal Value, $', 
    aggfunc='sum'
).fillna(0)

plt.figure(figsize=(12, 7))
sns.heatmap(icp_matrix, annot=True, fmt=',.0f', cmap='YlGnBu', cbar_kws={'label': 'Tổng Doanh thu ($)'})
plt.title('Ma trận ICP: Quy mô Khách hàng vs Sản phẩm (Doanh thu thực tế)', fontsize=15, fontweight='bold', pad=20)
plt.xlabel('Dòng sản phẩm', fontsize=12)
plt.ylabel('Quy mô Doanh nghiệp', fontsize=12)
plt.tight_layout()
plt.savefig('icp_heatmap.png', dpi=300)
plt.close()

print("New segmentation dashboards generated.")
