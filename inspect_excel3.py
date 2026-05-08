import pandas as pd
import json

file_path = 'CRM and Sales Pipelines.xlsx'
df = pd.read_excel(file_path, sheet_name='CRM_data')

info = {
    'Status_seq': df.groupby('Status sequence')['Status'].unique().to_dict(),
    'Stage_seq': df.groupby('Stage sequence')['Stage'].unique().to_dict(),
    'Max_Acq_Date': str(df['Lead acquisition date'].max()),
    'Max_Act_Date': str(df['Actual close date'].max()),
    'Max_Exp_Date': str(df['Expected close date'].max())
}

# Convert arrays to list for json serialization
for k, v in info['Status_seq'].items():
    info['Status_seq'][k] = v.tolist()

for k, v in info['Stage_seq'].items():
    info['Stage_seq'][k] = v.tolist()

print(json.dumps(info, indent=2))
