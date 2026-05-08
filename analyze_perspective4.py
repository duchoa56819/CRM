import pandas as pd
import numpy as np
import json

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

file_path = 'CRM and Sales Pipelines.xlsx'
df = pd.read_excel(file_path, sheet_name='CRM_data')

# Basic prep
df['Is_Won'] = df['Status'].isin(['Customer', 'Churned Customer'])
df['Is_Closed'] = df['Status'].isin(['Customer', 'Churned Customer', 'Disqualified']) | df['Stage'].isin(['Won', 'Lost'])

results = {}

# 1. Owner Workload vs. Performance
owner_stats = []
for owner in df['Owner'].unique():
    owner_df = df[df['Owner'] == owner]
    total_leads = len(owner_df)
    closed = owner_df[owner_df['Is_Closed']]
    won = owner_df[owner_df['Is_Won']]
    
    win_rate = (len(won) / len(closed) * 100) if len(closed) > 0 else 0
    total_rev = won['Deal Value, $'].sum()
    rev_per_lead = float(total_rev / total_leads) if total_leads > 0 else 0
    
    owner_stats.append({
        'Owner': owner,
        'Workload': total_leads,
        'Win_Rate': win_rate,
        'Revenue_per_Lead': rev_per_lead,
        'Total_Revenue': float(total_rev)
    })

results['Owner_Efficiency'] = sorted(owner_stats, key=lambda x: x['Workload'], reverse=True)

# 2. Portfolio Mix
bins = [0, 5000, 10000, 200000]
labels = ['Small', 'Medium', 'Large']
df['Deal_Size_Category'] = pd.cut(df['Deal Value, $'], bins=bins, labels=labels)

portfolio = df.groupby(['Owner', 'Deal_Size_Category'], observed=True).size().unstack(fill_value=0).to_dict(orient='index')
results['Portfolio_Mix'] = portfolio

# 3. Regional Efficiency
country_stats = []
for country in df['Country'].unique():
    c_df = df[df['Country'] == country]
    closed = c_df[c_df['Is_Closed']]
    won = c_df[c_df['Is_Won']]
    if len(closed) > 20: 
        country_stats.append({
            'Country': country,
            'Win_Rate': float(len(won) / len(closed) * 100),
            'Avg_Value': float(c_df['Deal Value, $'].mean())
        })

results['Country_Efficiency'] = sorted(country_stats, key=lambda x: x['Win_Rate'], reverse=True)[:5]

print(json.dumps(results, indent=2, cls=NpEncoder))
