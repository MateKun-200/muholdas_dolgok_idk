import georinex as gr
import numpy as np
import sys
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from matplotlib.dates import DateFormatter

# RINEX fájl megadása parancssorból
rinex_file = sys.argv[1]
satellite = sys.argv[2]
print('RINEX file:', rinex_file)
print('Satellite:', satellite)
print('Loading...')

# Időkeret beállítása
start_date = '2023-03-04T11:00:00'
end_date = '2023-03-04T12:00:00'

start_datetime = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
end_datetime = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S")
time_diff = end_datetime - start_datetime
time_diff_seconds = time_diff.total_seconds()

seconds_array = np.arange(0, int(time_diff_seconds) + 2)

# RINEX fájl megfelelő adatainak beolvasása
obs_data = gr.load(rinex_file, tlim=[start_date, end_date], meas=['C1C', 'C2W'], use="G")

# Geometriamentes lineáris kombinációk számítása (GPS)
lambda1 = 0.1903  # L1 hullámhossz
lambda2 = 0.2442  # L2 hullámhossz
c1c_values = obs_data['C1C']  # L1 C/A pszeudotávolság
c2l_values = obs_data['C2W']  # L2 Z pszeudotávolság
c1c_c2l_diff = ((c1c_values / lambda1) - (c2l_values / lambda2))

# GPS műholdak adatainak számítása for ciklussal és plottolás az idő (UTC) függvényében
index_of_satellite = np.where(obs_data.sv == satellite)[0]
diff_of_satellite_mes = np.empty(len(c1c_c2l_diff))
times = np.empty(len(c1c_c2l_diff), dtype=object)

for time in range(len(c1c_c2l_diff)):
    actual_diff_for_time_and_satellite = c1c_c2l_diff[time][index_of_satellite].values.ravel()
    diff_of_satellite_mes[time] = actual_diff_for_time_and_satellite
    times[time] = start_datetime + timedelta(seconds=time)

fig, ax = plt.subplots()
plt.plot(times, diff_of_satellite_mes, label=satellite)
plt.xlabel('Time')
date_formatter = DateFormatter("%H:%M")
ax.xaxis.set_major_formatter(date_formatter)
plt.xticks(rotation=90)
plt.ylabel('Geometry-free Linear Combination (L1-L2)')
plt.title('Data for Satellite ' + satellite)

plt.legend()
plt.show()
