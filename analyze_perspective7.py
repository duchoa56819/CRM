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

# New Temporal Columns
df['Acq_Month'] = df['Lead acquisition date'].dt.month
df['Acq_Month_Name'] = df['Lead acquisition date'].dt.month_name()
df['Acq_DayOfWeek'] = df['Lead acquisition date'].dt.day_name()

results = {}

# 1. Win Rate by Month of Acquisition
month_eff = []
for month in df['Acq_Month_Name'].unique():
    m_df = df[df['Acq_Month_Name'] == month]
    closed = m_df[m_df['Is_Closed']]
    won = m_df[m_df['Is_Won']]
    win_rate = (len(won) / len(closed) * 100) if len(closed) > 0 else 0
    month_eff.append({
        'Month': month,
        'Win_Rate': win_rate,
        'Lead_Count': len(m_df)
    })
results['Monthly_Performance'] = month_eff

# 2. Win Rate by Day of Week
day_eff = []
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
for day in day_order:
    d_df = df[df['Acq_DayOfWeek'] == day]
    closed = d_df[d_df['Is_Closed']]
    won = d_df[d_df['Is_Won']]
    win_rate = (len(won) / len(closed) * 100) if len(closed) > 0 else 0
    day_eff.append({
        'Day': day,
        'Win_Rate': win_rate,
        'Lead_Count': len(d_df)
    })
results['Daily_Performance'] = day_eff

# 3. Decision Window Analysis
# How long does it take for a deal to be WON vs LOST?
won_days = df[df['Is_Won'] == True]['Days_to_Close'].mean()
lost_days = df[(df['Is_Closed'] == True) & (df['Is_Won'] == False)]['Days_to_Close'].mean()

results['Decision_Window'] = {
    'Avg_Days_to_Won': won_days,
    'Avg_Days_to_Lost': lost_days
}

# 4. Seasonal Product Demand
# Which product is popular in which month?
seasonal_prod = df.groupby(['Acq_Month_Name', 'Product']).size().unstack(fill_value=0).to_dict(orient='index')
results['Seasonal_Product_Demand'] = seasonal_prod

print(json.dumps(results, indent=2, cls=NpEncoder))
