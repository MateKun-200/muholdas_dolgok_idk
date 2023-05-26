import georinex as gr
import numpy as np
import sys
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta

print(sys.argv[1])
# Path to the RINEX file
rinex_file = sys.argv[1]

if not os.path.isfile(rinex_file):
    print(f"Error: RINEX file '{rinex_file}' not found.")
    sys.exit(1)

start_date = '2023-03-04T11:00:00'
end_date = '2023-03-04T12:10:30'

start_datetime = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
end_datetime = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S")
time_diff = end_datetime - start_datetime
time_diff_seconds = time_diff.total_seconds()

seconds_array = np.arange(0, int(time_diff_seconds) + 2)

# Read the RINEX file
try:
    obs_data = gr.load(rinex_file, tlim=[
                       start_date, end_date], meas=['C1C', 'L1C'])
except Exception as e:
    print(f"Error occurred while reading the RINEX file: {str(e)}")
    sys.exit(1)
# Calculate C1C-L1C differences
c1c_values = obs_data['C1C']
l1c_values = obs_data['L1C']
c1c_l1c_diff = c1c_values - l1c_values


# Get unique satellite PRN numbers
satellite_prn = np.unique(obs_data.sv)

fig, ax = plt.subplots()

# basszuk össze a figure-t:
# todo új változó, hogy csak egyszer kelljen kiszánolni iterációnként az adathalmaz nagyságát
for sat in satellite_prn:
    index_of_satelite = np.where(obs_data.sv == sat)[0]
    diff_of_satellite_mes = np.empty(len(c1c_l1c_diff))
    times = np.empty(len(c1c_l1c_diff), dtype=object)
    print(f"satellite: '{sat}'")

    for time in range(len(c1c_l1c_diff)):
        actualdif_for_time_and_satellite = c1c_l1c_diff[time][index_of_satelite].values.ravel(
        )
        diff_of_satellite_mes[time] = actualdif_for_time_and_satellite
        times[time] = start_datetime + timedelta(seconds=time)

    print(diff_of_satellite_mes)
    print(times)
    plt.plot(times, diff_of_satellite_mes, label=sat)

plt.legend()
plt.show()

""" for sat in satellite_prn:
    index_of_satelite = np.where(obs_data.sv == sat)
    diff_of_satelite_mes = []
    times = []
    print(f"satelite:'{sat}'")
    for time in range(len(c1c_l1c_diff)):
        actualdif_for_time_and_satelite = c1c_l1c_diff[time][index_of_satelite]
        # print(f"time:{time}  c1c_l1c_diff:{actualdif_for_time_and_satelite[0]}")
        diff_of_satelite_mes.append(actualdif_for_time_and_satelite)
        times.append(start_datetime + timedelta(seconds=time))
    print(diff_of_satelite_mes)
    print(times)
    plt.plot(times, diff_of_satelite_mes, label=sat) """

"""ax.set_xlabel('Time')
ax.set_ylabel('C1C-L1C Differences')
ax.legend()
plt.show()"""

# Plot figure for each satellite
