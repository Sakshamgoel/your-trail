import json
import pandas as pd
import sys

df = pd.read_csv('./src/utils/trail_data.csv')
df.drop(df.columns[0], axis = 1, inplace = True)


latitude = sys.argv[1]
longitude = sys.argv[2]
distance = sys.argv[3]
difficulty = sys.argv[4]

lst = []

for index, row in df.iterrows():
    if(float(row['distance']) > float(distance)):
        lst.append(index)
        continue
    
    if(int(row['difficulty']) > float(difficulty)):
        lst.append(index)
        continue
    
updated_data = df.drop(lst)

df.to_json('./src/utils/result.json')

print('Success')
