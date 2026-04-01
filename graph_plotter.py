import csv
from datetime import datetime
import matplotlib.pyplot as plt
call = input("File name: ")
with open(call, mode='r') as file:
    data = list(csv.reader(file))
    x = [row[0] for row in data]
    y = [row[2] for row in data]
    parsed_x = [datetime.strptime(t, "%H:%M:%S") for t in x]
    t_0 = parsed_x[0]
    relative = [((t-t_0).total_seconds())/3600 for t in parsed_x]
    plt.plot(relative,y)
    plt.title(f"{call} - Pressure v Time")
    plt.xlabel("Time/h")
    plt.ylabel("Pressure/mTORR")
    plt.show()
