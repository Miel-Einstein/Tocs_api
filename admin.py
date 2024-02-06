import os

import pandas as pd
from django.contrib import admin

from .models import *

admin.site.register(TocsCSVRow)
admin.site.register(TocsEvent)

# create final df creates a final dataframe with all the csv inside every files  
def create_final_df(path):
    L=[]
    for files in os.walk(path):
        for csv in files[2]:
            if csv.endswith('.csv'):
                final_df = pd.read_csv(os.path.join(files[0], csv), header=None, names=["time", "ax", "az", "ay", "temp"]
                                 )
                
            id_sensor=(os.path.splitext(csv)[0].split("-")[1])  
            df=final_df.assign(id_sensor=id_sensor)
            L.append(df)
    final_df=pd.concat(L,ignore_index=True) 
    return final_df

create_final_df(r'C:\Users\casa\Documents\all')


# now let us create a dataframe by id_sensor 
df={}
L_ax=[]
L_az=[]
L_ay=[]

try:
    for x,y in create_final_df(r'C:\Users\casa\Documents\all').groupby("id_sensor"):
       df[x]=y.reset_index(drop=True)
       df[x]['time']=pd.to_datetime(df[x]['time'])

    # for index, row in df[x].iterrows():
    #     time=row['time']
    #     ax=row['ax']
    #     az=row['az']
    #     ay=row['ay']
    #     temp=row['temp']
    #     sensor_id=row['id_sensor']
    #     if pd.isna(time):
    #         time = None
    #     Sensor.objects.create(time=time,ax=ax,az=az,ay=ay,temp=temp,sensor_id=sensor_id)

except Exception as e:
    print(e)          


    
#     # valore medio by tree or sensor_id di x,z,y
#     val_mean_id_sensor_x =df[x]['ax'].mean()
#     val_mean_id_sensor_z =df[x]['az'].mean()
#     val_mean_id_sensor_y =df[x]['ay'].mean()
    
#     L_ax.append(val_mean_id_sensor_x)
#     L_az.append(val_mean_id_sensor_z)
#     L_ay.append(val_mean_id_sensor_y)
    

# for d,x,z,y  in zip(df,L_ax,L_az,L_ay): # d stands for dataframe 
#     # mean value 
#     df[d]['val_mean_id_sensor_x']=x
#     df[d]['val_mean_id_sensor_z']=z
#     df[d]['val_mean_id_sensor_y']=y
#     #razio value
#     df[d]['val_razio_id_sensor_x']=df[d]['ax']-x
#     df[d]['val_razio_id_sensor_z']=df[d]['az']-z
#     df[d]['val_razio_id_sensor_y']=df[d]['ay']-y
    

          

# #to call it we do df['id_sensor'] exemple :



# print(df['68_b6_b3_2a_f3_70'])

# #in your  ipynb code first import df  exemple : from ilaria_utils import df
