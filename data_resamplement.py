#!./env/bin/python3

# use line below for generic servers
#!/usr/bin/env python3

# v. 2023.05.23 

import glob
import os
from datetime import datetime as dt
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import signal, stats

df_tocs = pd.read_csv("./tocs.csv", header=None, names=["time", "ax", "ay", "az", "temp"])

df_tocs['time'] = pd.to_datetime(df_tocs['time'])

tmin = min(df_tocs['time'])
tmax = max(df_tocs['time'])

# save also a copy of the data as read from the sensor
#df_tocs_raw = df_tocs.copy();
#df_tocs_raw.to_csv('tocs_raw.csv')

# now get rid of isolated outliers using a median filter with window=3
df_tocs.ax = signal.medfilt(df_tocs['ax'])
df_tocs.ay = signal.medfilt(df_tocs['ay'])
df_tocs.az = signal.medfilt(df_tocs['az'])

# remove NaNs with interpolation
# df_tocs = df_tocs.interpolate(method='bfill')

# transform in g-units
g_unit = 2.0/(2.0**15.0)
df_tocs['ax'] = df_tocs['ax'].multiply(g_unit)
df_tocs['ay'] = df_tocs['ay'].multiply(g_unit)
df_tocs['az'] = df_tocs['az'].multiply(g_unit)

# add mean normalized columns
mx = df_tocs['ax'].mean()
my = df_tocs['ay'].mean()
mz = df_tocs['az'].mean()
df_tocs['axm'] = df_tocs['ax']-mx
df_tocs['aym'] = df_tocs['ay']-my
df_tocs['azm'] = df_tocs['az']-mz

df_fine = df_tocs.resample("38ms", on="time").mean()
df_fine = df_fine.interpolate()
df_fine['temp'] = df_fine['temp'].div(256) + 25.0

# get mod of vector
mod = (df_fine.axm**2+df_fine.aym**2+df_fine.azm**2)**0.5
# standard deviation in mg
stdval = mod.std()*1000
tdel = tmax-tmin
tds = tdel.total_seconds()

if tds > 3:
    df_fine.to_csv('tocs.csv')
else:
    df_fine.to_csv('NO_LOAD_tocs.csv')

with open('events.csv', 'w') as f:
    print(f'{tmin},{tmax},{stdval},{tds}', file=f)
#    print(f'{tmin},{tmax},{stdval},{mx},{my},{mz},{tds}', file=f)
