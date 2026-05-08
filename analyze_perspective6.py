import pandas as pd
import numpy as np
import json

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer): return int(obj)
        if isinstance(obj, np.floating): return float(obj)
        if isinstance(obj, np.ndarray): return obj.tolist()
        return super(NpEncoder, self).default(obj)

file_path = 'CRM and Sales Pipelines.xlsx'
df = pd.read_excel(file_path, sheet_name='CRM_data')

# Basic prep
df['Is_Won'] = df['Status'].isin(['Customer', 'Churned Customer'])
df['Is_Closed'] = df['Status'].isin(['Customer', 'Churned Customer', 'Disqualified']) | df['Stage'].isin(['Won', 'Lost'])
df['Days_to_Close'] = (df['Actual close date'] - df['Lead acquisition date']).dt.days

results = {}

# 1. Industry-Product Win Rate Matrix
matrix_data = []
for industry in df['Industry'].unique():
    for product in df['Product'].unique():
        subset = df[(df['Industry'] == industry) & (df['Product'] == product)]
        closed = subset[subset['Is_Closed']]
        won = subset[subset['Is_Won']]
        if len(closed) > 5: # Only significant combos
            win_rate = (len(won) / len(closed) * 100)
            avg_val = won['Deal Value, $'].mean() if len(won) > 0 else 0
            matrix_data.append({
                'Industry': industry,
                'Product': product,
                'Win_Rate': win_rate,
                'Avg_Value': avg_val,
                'Total_Won': len(won)
            })

results['Strategic_Matrix'] = sorted(matrix_data, key=lambda x: x['Win_Rate'], reverse=True)

# 2. Industry Efficiency (Cycle Time vs. Win Rate)
industry_eff = []
for industry in df['Industry'].unique():
    i_df = df[df['Industry'] == industry]
    closed = i_df[i_df['Is_Closed']]
    won = i_df[i_df['Is_Won']]
    if len(closed) > 10:
        avg_cycle = won['Days_to_Close'].mean() if len(won) > 0 else 0
        win_rate = (len(won) / len(closed) * 100)
        industry_eff.append({
            'Industry': industry,
            'Win_Rate': win_rate,
            'Avg_Cycle': avg_cycle
        })
results['Industry_Efficiency'] = industry_eff

# 3. Market Concentration (Pareto Analysis)
# Which 20% of Industry-Product combos bring 80% of revenue?
revenue_by_combo = df[df['Is_Won'] == True].groupby(['Industry', 'Product'])['Deal Value, $'].sum().sort_values(ascending=False).reset_index()
total_won_revenue = revenue_by_combo['Deal Value, $'].sum()
revenue_by_combo['Cumulative_Pct'] = revenue_by_combo['Deal Value, $'].cumsum() / total_won_revenue * 100
results['Pareto_Top_Combos'] = revenue_by_combo.head(10).to_dict(orient='records')

print(json.dumps(results, indent=2, cls=NpEncoder))
