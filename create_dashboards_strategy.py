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

# 1. Dashboard: Industry-Product Win Rate Matrix (Heatmap)
matrix = df[df['Is_Closed'] == True].pivot_table(
    index='Industry', 
    columns='Product', 
    values='Is_Won', 
    aggfunc='mean'
) * 100

plt.figure(figsize=(14, 10))
sns.heatmap(matrix, annot=True, fmt='.1f', cmap='RdYlGn', cbar_kws={'label': 'Tỷ lệ thắng (%)'})
plt.title('Ma trận Chiến lược: Tỷ lệ thắng theo Ngành & Sản phẩm', fontsize=15, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('strategic_matrix.png', dpi=300)
plt.close()

# 2. Dashboard: Revenue Pareto (Industry-Product)
rev_combo = df[df['Is_Won'] == True].groupby(['Industry', 'Product'])['Deal Value, $'].sum().sort_values(ascending=False).head(10).reset_index()
rev_combo['Combo'] = rev_combo['Industry'] + " (" + rev_combo['Product'] + ")"

plt.figure(figsize=(12, 6))
sns.barplot(data=rev_combo, x='Deal Value, $', y='Combo', palette='viridis')
plt.title('Top 10 Cặp Ngành - Sản phẩm mang lại Doanh thu lớn nhất', fontsize=15, fontweight='bold', pad=20)
plt.xlabel('Tổng doanh thu đã chốt ($)')
plt.tight_layout()
plt.savefig('pareto_combos.png', dpi=300)
plt.close()

# 3. Dashboard: Industry Efficiency (Cycle vs Win Rate)
df['Days_to_Close'] = (df['Actual close date'] - df['Lead acquisition date']).dt.days
ind_eff = df[df['Is_Won'] == True].groupby('Industry').agg({
    'Is_Won': 'count', # Using count as a proxy for scale
    'Days_to_Close': 'mean'
}).reset_index()

# Add win rate
win_rates = (df.groupby('Industry')['Is_Won'].sum() / df[df['Is_Closed'] == True].groupby('Industry')['Is_Won'].count() * 100).reset_index()
ind_eff = ind_eff.merge(win_rates, on='Industry')
ind_eff.columns = ['Industry', 'Count', 'Avg_Cycle', 'Win_Rate']

plt.figure(figsize=(12, 6))
sns.scatterplot(data=ind_eff, x='Avg_Cycle', y='Win_Rate', size='Count', hue='Industry', sizes=(100, 1000), alpha=0.6, palette='Set1')
plt.title('Phân tích Hiệu quả Ngành: Tốc độ chốt đơn vs. Tỷ lệ thắng', fontsize=15, fontweight='bold', pad=20)
plt.xlabel('Thời gian chốt đơn trung bình (Ngày)')
plt.ylabel('Tỷ lệ thắng (%)')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., title='Ngành')
plt.tight_layout()
plt.savefig('industry_efficiency.png', dpi=300)
plt.close()

print("Perspective 6 dashboards generated.")
