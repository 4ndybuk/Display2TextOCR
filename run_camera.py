#!/usr/bin/env python3
"""
"""

import os
import time
import csv
from picamera2 import Picamera2, Preview
from datetime import datetime
# Live data plotting imports
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np

# OCR module script
from recognition_module import recognition_module

# Setting up the Pi camera
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start_preview(Preview.NULL)
picam2.start()

# Create a log file
log_file = f"{datetime.now().strftime('%Y-%m-%d')}_pressure_log.csv"

# Create a live plot
style.use('fivethirtyeight')
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

# Function to yield processed data points for live plotting
def animate(frame):
    try:
        with open(log_file, 'r') as file:
            reader = csv.reader(file)
            plot_data = list(reader)

            # Wait until the log fills with enough data
            if len(plot_data) < 2:
                return
                
            # Converting parsed datetime object to hours
            def convert_to_hours(x):
                parsed = datetime.strptime(x, "%H:%M:%S")
                hours = parsed.hour + parsed.minute/60 + parsed.second/3600
                return float(round(hours, 3))

            # Converting pressure values relative to the unit scale (TORR and mTORR)
            def scale_to_units(y):
                fY = float(y[1])
                if y[0][0] in ['m', 'M', '™']:
                    mY = fY / 1000
                    return round(mY, 6)
                else:
                    return fY
                    
            x_points = [convert_to_hours(x[0]) for x in plot_data if len(plot_data) > 1]
            y_points = [scale_to_units(y[1:]) for y in plot_data if len(plot_data) > 1]

            # Numpy array of points for relative axis scaling
            np_x = np.array(x_points)
            np_y = np.array(y_points)

            ax1.clear()
            ax1.plot(np_x-np_x[0], np_y)
            
    except Exception as e:
        print("Plot error:", e)

# Live plot animation
ani_plot = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()

# Image name numbering convention
i = 1

# Continous image taking loop
while True:
    try:
        time.sleep(2)
        capture_time = datetime.now()
        time_stamp = capture_time.strftime("%H:%M:%S")
        
        # File name generator (OPTIONAL: used for storinf images in a folder)
        image_name = f"read_pressure_{i}.jpg"
        img_path = os.path.join('./sample_images', image_name)
        i += 1
        
        picam2.capture_file(img_path)

        # Image recognition for results
        results = recognition_module(img_path, time_stamp)
        print(results)

        with open(log_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(results)

        with open(log_file, mode="r") as file:
            data = list(csv.reader(file))

        # Filtering out potential false readings for loss of decimal point
        if len(data) > 2:
            if data[-1][1][0] in ['m', 'M', '™'] and data[-1][1] != "":
                if '.' in data[-2][2] and '.' not in data[-1][2]:
                    data = data[:-1]

                    # Overwrite filtered data in the log file
                    with open(log_file, mode='w', newline="") as file:
                        writer = csv.writer(file)
                        writer.writerows(data)

        # OPTIONAL: comment os.remove() to begin saving images
        os.remove(img_path)
        time.sleep(60)
        
    except KeyboardInterrupt:
        print('\nProcess interupted - exiting and saving the logging process')
        break
        
    except Exception as e:
        print(e)
        break
