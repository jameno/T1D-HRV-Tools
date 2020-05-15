#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arduino HRV Capture Tool
========================
:File: arduino_hrv_capture_tool.py
:Description: Captures Arduino HRV data from a USB serial port
:Version: 0.0.1
:Created: 2020-02-16
:Authors: Jason Meno (jameno)
:Dependencies: A .csv containing Tidepool CGM device data
:License: BSD-2-Clause
"""
import serial
import numpy as np
import time
import pandas as pd
import datetime
import sys
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

# %% Record Data From Serial USB
port_name = '/dev/cu.usbmodem14201'
ser = serial.Serial(port_name, 9600)

timestamp_now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
signal_filename = 'heart_signal_' + timestamp_now + '.csv'
#export_file = open(signal_filename, 'a')
#export_file.write('timestamp,value\n')

# Sampling (100 samples/sec)
run_seconds = 180
n_samples = 100 * run_seconds

animation_duration = run_seconds
inhale_symbol = "O"
exhale_symbol = "."
inhale_seconds = 5
exhale_seconds = 5
field_width = 70

inhale_marker_times = np.linspace(0, inhale_seconds, field_width)
inhale_symbol_num = np.ceil(
    (np.sin(np.linspace(-np.pi / 2, np.pi / 2, field_width)) + 1) * field_width / 2
)

exhale_marker_times = np.linspace(
    inhale_seconds, inhale_seconds + exhale_seconds, field_width
)
exhale_symbol_num = inhale_symbol_num * -1 + field_width  # Inverse Signal

start_time = time.time()
diff_time = time.time() - start_time
mod_time = diff_time % inhale_seconds
previous_marker_time = 0

breath_status = "inhale"
print_ready = False

signal_data = []
breath_data = []

print("Starting...", end="")
for x in range(n_samples):
    #output = str(time.time()) + "," + str(int(ser.readline())) + "\n"
    signal = int(ser.readline())
    signal_data.append((time.time(), signal))

    # scaled_signal = int(signal/10)
    # output_string = "Signal: [" + 'O'*scaled_signal + '.'*(100-scaled_signal) + "] "
    # sys.stdout.write("\r" + output_string)
    # sys.stdout.flush()
    #export_file.write(output)

    if breath_status == ">>> INHALE >>>":
        status = 1000
        marker_time = np.where(inhale_marker_times >= mod_time)[0][0]

        if marker_time > previous_marker_time:
            inhale_num = int(inhale_symbol_num[marker_time])
            exhale_num = field_width - inhale_num
            print_ready = True
            previous_marker_time = marker_time

        diff_time = time.time() - start_time
        mod_time = diff_time % (inhale_seconds + exhale_seconds)

        if mod_time > inhale_seconds:
            breath_status = "<<< exhale <<<"
            previous_marker_time = 0

    else:
        status = 0
        marker_time = np.where(exhale_marker_times >= mod_time)[0][0]

        if marker_time > previous_marker_time:
            inhale_num = int(exhale_symbol_num[marker_time])
            exhale_num = field_width - inhale_num
            print_ready = True
            previous_marker_time = marker_time

        diff_time = time.time() - start_time
        mod_time = diff_time % (inhale_seconds + exhale_seconds)

        if mod_time < inhale_seconds:
            breath_status = ">>> INHALE >>>"
            previous_marker_time = 0

    if print_ready:
        breath_data.append((time.time(), inhale_num, status))
        state = inhale_symbol * inhale_num + exhale_symbol * exhale_num
        output_string = breath_status + " [" + state + "] " + breath_status
        sys.stdout.write("\r" + output_string)
        sys.stdout.flush()
        print_ready = False

print("Done!")
# export_file.close()
ser.close()
# %% Load data and add local time information
#data_df = pd.read_csv(signal_filename, low_memory=False)
#data_df["local_time"] = pd.to_datetime(data_df.timestamp,
#                                       unit='s',
#                                       utc=True).dt.tz_convert(time.tzname[0])
#
#data_df.to_csv(signal_filename, index=False)


# %% Merge signals into one dataframe
signal_data = pd.DataFrame(signal_data, columns=['timestamp', 'value'])
breath_data = pd.DataFrame(breath_data, columns=['timestamp', 'stage', 'status'])
data = pd.concat([signal_data, breath_data], sort=False)
data["local_time"] = pd.to_datetime(data['timestamp'],
                                       unit='s',
                                       utc=True).dt.tz_convert(time.tzname[0])
data.sort_values('local_time', ascending=True, inplace=True)
data[['stage','status']] = data[['stage','status']].fillna(method='ffill')
data = data[data['value'].notnull().values]

# %% Viz peaks
#signal_data = pd.DataFrame(signal_data)
#signal_sample = signal_data[1]
#peaks, thing = find_peaks(signal_sample, distance=50)
peaks, thing = find_peaks(data['value'], distance=50)
plt.plot(data['value'])
plt.plot(peaks, data['value'][peaks], "x")

# %% HRV
pd.Series(peaks).diff().rolling(3, center=True).mean().plot(figsize=(15,5))
pd.Series(data['stage'][peaks].values/2+60).plot(figsize=(15,5))

# %% Viz peaks smoothed
data['smoothed_value'] = data['value'].rolling(1, center=True).mean()
peaks, thing = find_peaks(data['smoothed_value'], distance=50)
#plt.plot(signal_smoothed)
data['smoothed_value'].plot(figsize=(10,5))
#plt.plot(peaks, pd.Series(signal_smoothed)[peaks], "x")
data['smoothed_value'][peaks].plot(figsize=(10,5),style="x")
# %% HRV
pd.Series(peaks).diff().plot(figsize=(10,5))

# %% Ratio between inhale and exhale HRV
hrv = pd.Series(peaks).diff()
inhale_hrv = hrv[data['status'][peaks].values == 1000]
exhale_hrv = hrv[data['status'][peaks].values == 0]

# %%
inhale_hrv.hist(bins=25, label='inhale')
exhale_hrv.hist(bins=25, label='exhale')
plt.legend()