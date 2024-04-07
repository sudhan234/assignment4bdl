import pandas as pd
import numpy as np
import os
import re
import yaml

with open("params.yaml", 'r') as f:
    params = yaml.safe_load(f)

year=params['year']
datafolder=f"downloaded_files/{year}"
output_folder=f'predicted/{year}'
os.makedirs(output_folder, exist_ok=True)


filepath=f'fieldlist/{year}/fields.txt'

fields=[]
with open(filepath, 'r') as file:
    for field in file:
        fields.append(field.strip())



for filename in os.listdir(datafolder):
    if filename.endswith('.csv'):
        filepath=os.path.join(datafolder, filename)
        df=pd.read_csv(filepath)
        df_dropped=df.dropna(subset=fields, axis=0)
        df_dropped['MONTH']=pd.to_datetime(df_dropped['DATE']).dt.month
        for i in fields:
            df_dropped[i]=df_dropped[i].astype(str).str.replace('[a-zA-Z]', '', regex=True)
        df_dropped.replace({'':np.nan}, inplace=True)

        df_dropped=df_dropped.dropna(subset=fields, axis=0)
        for i in fields:
            df_dropped[i]=df_dropped[i].astype(float)
        d={}
        for i in fields:
            d[i] = df_dropped.groupby('MONTH',as_index=False)[i].mean()
        output_file_path = os.path.join(output_folder, f'{os.path.splitext(filename)[0]}_filtered.csv')
        concat_list=[]
        for i in fields:
            concat_list.append(d[i].set_index('MONTH'))
        concat_df=pd.concat(concat_list, axis=1)
        #print(concat_df)
        concat_df.to_csv(output_file_path, index=True)
