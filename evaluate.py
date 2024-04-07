#from sklearn.metrics import r2_score
import os
import scipy
import pandas as pd
import yaml

with open("params.yaml", 'r') as f:
    params = yaml.safe_load(f)
year=params['year']

df_truth=[]
df_predict=[]

for filename in os.listdir(f'groundtruth/{year}'):
    df_truth.append(filename)

for filename in os.listdir(f'predicted/{year}'):
    df_predict.append(filename)

filepath=f'fieldlist/{year}/fields.txt'

fields=[]
with open(filepath, 'r') as file:
    for field in file:
        fields.append(field.strip())

out_folder=f'r2score/{year}'
os.makedirs(out_folder, exist_ok=True)
res=[]
truth_path=f'groundtruth/{year}'
predict_path=f'predicted/{year}'
for i in range(len(df_truth)):
    temp1=os.path.join(truth_path,df_truth[i])
    temp2=os.path.join(predict_path,df_predict[i])
    temp_ground=pd.read_csv(temp1)
    temp_predict=pd.read_csv(temp2)
    temp_predict=temp_predict[:len(temp_ground)]
    print(temp_predict)

    temp_predict['MonthlyMaximumTemperature']=temp_predict['DailyMaximumDryBulbTemperature']
    temp_predict['MonthlyMinimumTemperature']=temp_predict['DailyMinimumDryBulbTemperature']
    temp_predict=temp_predict.drop(columns=fields)
    print(temp_ground)
    print(temp_predict)
    _, _, rvalue1, _, _=scipy.stats.mstats.linregress(temp_ground['MonthlyMaximumTemperature'], temp_predict['MonthlyMaximumTemperature'])
    _, _, rvalue2, _, _=scipy.stats.mstats.linregress(temp_ground['MonthlyMinimumTemperature'], temp_predict['MonthlyMinimumTemperature'])

    r={}
    r['MonthlyMaximumTemperature']=rvalue1**2
    r['MonthlyMinimumTemperature']=rvalue2**2
    res.append({df_truth[i]:r})


file_path = os.path.join(out_folder, 'res.txt')

# Write the list to the file
with open(file_path, 'w') as f:
    for item in res:
        f.write("%s\n" % item)