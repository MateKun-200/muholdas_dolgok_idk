import os
import georinex as gr
import numpy as np
import sys
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from matplotlib.dates import DateFormatter
import xarray

# RINEX fájl megadása parancssorból
rinex_file = sys.argv[1]
selected_satellite = sys.argv[2]


file_name_nc = os.path.splitext(rinex_file)[0] + ".nc"
# ha van .nc ugyanolyan néven abban a mappában
if not os.path.isfile(file_name_nc):
    print("netCDF fájl nem található")
    print(f"adatok betöltése {rinex_file} rinex fileból...")
    obs_data = gr.load(rinex_file,  meas=[
        'L1C', 'L2W'], use="G")
    print("adatok konvertálása netCDF formátumra...")
    obs_data.to_netcdf(file_name_nc)
    print(f"adatok mentve az alábbi fájlba: {file_name_nc}")

else:
    print(f"{file_name_nc} fájlból adatok kiolvasása...")
    obs_data = xarray.open_dataset(file_name_nc)


# Geometriamentes lineáris kombinációk számítása (GPS)
lambda1 = 0.1903  # L1 hullámhossz
lambda2 = 0.2442  # L2 hullámhossz

c1c_values = obs_data['L1C']  # L1 C/A pszeudotávolság
c2l_values = obs_data['L2W']  # L2 Z pszeudotávolság
c1c_c2l_diff = ((c1c_values*lambda1) - (c2l_values*lambda2))

# GPS műholdak adatainak plottolás az idő (UTC) függvényében
satellite_prn = np.unique(obs_data.sv)
fig, ax = plt.subplots()

if (selected_satellite is not None):  # felhasználó adott-e meg műholdat
    if (np.isin(selected_satellite, satellite_prn)):  # van-e ilyen műhold/a megadott érvényes-e
        current_satellite = c1c_c2l_diff.sel(
            sv=selected_satellite).dropna(dim='time', how='all')
        plt.plot(current_satellite.time, current_satellite,
                 label=selected_satellite)
    else:
        print("Nincs ilyen műhold")
else:  # ha nem ad meg semmit a felhasználó
    for sat in satellite_prn:
        current_satellite = c1c_c2l_diff.sel(
            sv=sat).dropna(dim='time', how='all')
        plt.plot(current_satellite.time, current_satellite, label=sat)
# plot
plt.xlabel('Time')
date_formatter = DateFormatter("%H:%M")
ax.xaxis.set_major_formatter(date_formatter)
plt.xticks(rotation=90)
plt.ylabel('Geometry-free Linear Combination (L1-L2)')
plt.title('Satellite Data')
plt.legend()
plt.savefig('satellite_plot.png')
print("grafikon mentve az alábbi néven: satellite_plot.png")
