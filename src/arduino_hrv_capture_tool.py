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
import time
import pandas as pd
import datetime

# %% Record Data From Serial USB
port_name = '/dev/cu.usbmodem14201'
ser = serial.Serial(port_name, 9600)

timestamp_now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
signal_filename = 'heart_signal_' + timestamp_now + '.csv'
export_file = open(signal_filename, 'a')
export_file.write('timestamp,value\n')

# Sample for 30 seconds
# (100 samples/sec = 3000 iterations)
print("Starting...", end="")
for x in range(3000):
    output = str(time.time()) + "," + str(int(ser.readline())) + "\n"
    export_file.write(output)

print("Done!")
export_file.close()
ser.close()
# %% Load data and add local time information
data_df = pd.read_csv(signal_filename, low_memory=False)
data_df["local_time"] = pd.to_datetime(data_df.timestamp,
                                       unit='s',
                                       utc=True).dt.tz_convert(time.tzname[0])

data_df.to_csv(signal_filename, index=False)
