import pandas as pd
import os
import numpy as np
import yaml

with open("params.yaml", 'r') as f:
    params=yaml.safe_load(f)

datafolder='downloaded_files/2003'
outputfolder='groundtruth/2003'
os.makedirs(outputfolder, exist_ok=True)

year=params['year']

monthly_columns=['MonthlyMaximumTemperature', 'MonthlyMinimumTemperature']
daily_columns=['DailyMaximumDryBulbTemperature','DailyMinimumDryBulbTemperature']
field_list=f'fieldlist/{year}'
os.makedirs(field_list, exist_ok=True)
for filename in os.listdir(datafolder):
    if filename.endswith('.csv'):
        file_path=os.path.join(datafolder, filename)
        df=pd.read_csv(file_path)
        df_dropped=df.dropna(subset=monthly_columns, axis=0)
        df_dropped['MONTH']=pd.to_datetime(df_dropped['DATE']).dt.month
        df_dropped=df_dropped[['MONTH']+monthly_columns]
        output_file_path = os.path.join(outputfolder, f'{os.path.splitext(filename)[0]}_dropped.csv')
        df_dropped.to_csv(output_file_path, index=False)


with open(os.path.join(field_list, 'fields.txt'), 'w') as f:
    for item in daily_columns:
        f.write("%s\n" % item)


