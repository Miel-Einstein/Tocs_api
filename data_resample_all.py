
import os
import time

import pandas as pd
from scipy import signal, stats

from .models import *


def resample_csv(path):
    df_tocs={}
    tmin={}
    tmax={}
    df_fine={}
    for files in os.walk(path):
        for csv in files[2]:
            if csv.endswith('.csv'):
                df_tocs[csv]=pd.read_csv(os.path.join(files[0],csv),header=None, names=["time", "ax", "ay", "az", "temp"])

                df_tocs[csv]['time']=pd.to_datetime(df_tocs[csv]['time'])

                tmin[csv] = min(df_tocs[csv]['time'])
                tmax[csv] = max(df_tocs[csv]['time'])
               
                # now we get rid of isolated outliers using a median filter with window=3
               
                df_tocs[csv].ax = signal.medfilt(df_tocs[csv]['ax'])
                df_tocs[csv].ay = signal.medfilt(df_tocs[csv]['ay'])
                df_tocs[csv].az = signal.medfilt(df_tocs[csv]['az'])
    
                # # remove NaNs with interpolation
                # df_tocs[csv] = df_tocs[csv].interpolate(method='bfill')
               
                # transform in g-units
                
                g_unit = 2.0/(2.0**15.0)
                df_tocs[csv]['ax'] = df_tocs[csv]['ax'].multiply(g_unit)
                df_tocs[csv]['ay'] = df_tocs[csv]['ay'].multiply(g_unit)
                df_tocs[csv]['az'] = df_tocs[csv]['az'].multiply(g_unit)

                # add mean normalized columns
                mx = df_tocs[csv]['ax'].mean()
                my = df_tocs[csv]['ay'].mean()
                mz = df_tocs[csv]['az'].mean()
                df_tocs[csv]['axm'] = df_tocs[csv]['ax']-mx
                df_tocs[csv]['aym'] = df_tocs[csv]['ay']-my
                df_tocs[csv]['azm'] = df_tocs[csv]['az']-mz                                
                
                df_fine[csv] = df_tocs[csv].resample("38ms", on="time").mean()
                # Interpolating missing values using linear interpolation

                df_fine[csv] = df_fine[csv].interpolate()
                df_fine[csv]['temp'] = df_fine[csv]['temp'].div(256) + 25.0
    for index, row in df_fine[csv].iterrows():
        time=row['time']
        ax=row['ax']
        az=row['az']
        ay=row['ay']
        temp=row['temp']
    
        TocsCSVRow.objects.create(time=time,ax=ax,az=az,ay=ay,temp=temp)
    print(df_fine)


    # for i,j in zip(df_tocs.values(),df_fine.values()):
    #   print(i['ax'][0],"with finale ",j['ax'][0])

resample_csv(r'C:\Users\casa\Documents\all')

# autmate resample for new csv only 


# def check_for_new_files(directory_path):
#     # Get the initial list of files in the directory
#     initial_files = set(os.listdir(directory_path))

#     while True:
#         # Wait for some time before checking again
#         time.sleep(60)  # Adjust the interval as needed (e.g., 60 seconds)

#         # Get the current list of files in the directory
#         current_files = set(os.listdir(directory_path))

#         # Find the new files by comparing the current and initial lists
#         new_files = current_files - initial_files

#         if new_files:
#             print("New files detected:")
#             resample_csv(new_files)

#             # Update the initial list for the next iteration
#             initial_files = current_files
#         else:
#             print('not file added')
# # Example usage: Specify the directory path you want to monitor
# directory_path = r'C:\Users\casa\Documents\all'
# check_for_new_files(directory_path)

