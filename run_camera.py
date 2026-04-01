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

# Image name numbering convention
i = 1

# Continous image taking loop
while True:
    try:
        time.sleep(2)
        capture_time = datetime.now()
        time_stamp = capture_time.strftime("%H:%M:%S")
        
        # File name generator
        image_name = f"read_pressure_{i}.jpg"
        img_path = os.path.join('./sample_images', image_name)
        i += 1
        
        picam2.capture_file(img_path)
            
        results = recognition_module(img_path, time_stamp)
        print(results)

        with open(log_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(results)

        with open(log_file, mode="r") as file:
            data = list(csv.reader(file))
        
        if len(data) > 2:
            value = data[1][1]
            last_point = data[-1][2]
            second_point = data[-2][2]

            if value and value[0] in ['m','M','™']:
                remove = False

                def is_number(val):
                    try:
                        float(val)
                        return True
                    except ValueError:
                        return False

                if '.' in last_point and '.' not in second_point:
                    remove = True
                elif '.' in last_point and '.' in second_point:
                    if float(last_point) - float(second_point) > 10:
                        remove = True
                    elif float(second_point) - float(last_point) > 10: 
                        remove = True

                if not is_number(last_point):
                    remove = True
                        
                if remove:
                    data.pop()

                    with open(log_file, mode='w', newline="") as file:
                        writer = csv.writer(file)
                        writer.writerows(data)
                        
        os.remove(img_path)
        time.sleep(5)
        
    except KeyboardInterrupt:
        print('\nProcess interupted - exiting the logging process')
        break
        
    except Exception as e:
        print(e)
        break
