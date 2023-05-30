
import os
import unittest
from matplotlib import pyplot as plt

import numpy as np
import xarray

# flexes sszkriptjeim 💩
from file_reader import file_reader
from date_daemon import distance_in_sec

import georinex as gr
from datetime import datetime, timedelta
import time

very_start_date = '2023-03-04T11:02:00'
small_end_date = '2023-03-04T11:06:00'
very_end_date = '2023-03-04T15:01:00'
one_end_date = '2023-03-04T11:51:00'
file_name = "PildoBox20923063l.obs"


class SatelliteDataTests(unittest.TestCase):

    def test_file_visible(self):
        self.assertIsNotNone(file_reader(
            file_name), "file is not located in folder")

    def test_date_counter(self):
        ellapsed_time = distance_in_sec(very_start_date, small_end_date)
        self.assertEqual(len(ellapsed_time), 31)
        print(ellapsed_time)

    def test_load_data_in_memory(self):
        start_timestamp = time.time()
        obs_file = file_reader(file_name)
        obs_data = gr.load(
            obs_file, tlim=[very_start_date, small_end_date], meas=['C1C', 'L1C'])
        end_timestamp = time.time()
        print(
            f"time needed to load the data is {end_timestamp-start_timestamp} second")
        self.assertIsNotNone(obs_data)
        print(obs_data)

    def test_load_time_in_memory(self):
        obs_file = file_reader(file_name)
        obs_data = gr.load(
            obs_file, tlim=[very_start_date, small_end_date], meas=['C1C', 'L1C'])
        self.assertIsNotNone(obs_data.time)

    def test_extract_variables_from_data(self):
        obs_file = file_reader(file_name)
        obs_data = gr.load(
            obs_file, tlim=[very_start_date, small_end_date], meas=['C1C', 'L1C'])
        self.assertIsNotNone(obs_data['C1C'])
        self.assertIsNotNone(obs_data['L1C'])

    def test_variables_has_same_dimension(self):
        obs_file = file_reader(file_name)
        obs_data = gr.load(
            obs_file, tlim=[very_start_date, small_end_date], meas=['C1C', 'L1C'])
        c1c_data = obs_data['C1C']
        l1c_data = obs_data['L1C']
        len1 = len(c1c_data[0])
        len2 = len(l1c_data[0])
        a = 10

    def test_if_diff_can_counted(self):
        obs_file = file_reader(file_name)
        obs_data = gr.load(
            obs_file, tlim=[very_start_date, small_end_date], meas=['C1C', 'L1C'])
        c1c_data = obs_data['C1C']
        l1c_data = obs_data['L1C']
        c1c_l1c_diff = c1c_data - l1c_data
        self.assertIsNotNone(c1c_l1c_diff)
        a = 10

    def test_if_can_get_header_values_of_file(self):
        obs_file = file_reader(file_name)
        hdr = gr.rinexheader(obs_file)
        a = 10

    def test_if_can_get_data_for_one_set_of_satellite(self):
        start_timestamp = time.time()
        obs_file = file_reader(file_name)
        obs_data = gr.load(
            obs_file, tlim=[very_start_date, small_end_date], meas=['C1C', 'L1C'], use="E")
        end_timestamp = time.time()
        ellapsed = end_timestamp - start_timestamp
        a = 10

    def test_if_can_be_plotted(self):  # nem jó b*zdmeg 💩
        obs_file = file_reader(file_name)
        start_datetime = datetime.strptime(
            very_start_date, "%Y-%m-%dT%H:%M:%S")
        obs_data = gr.load(
            obs_file, tlim=[very_start_date, very_end_date], meas=['C1C', 'L1C'], use="E")
        c1c_values = obs_data['C1C']
        l1c_values = obs_data['L1C']
        c1c_l1c_diff = c1c_values - l1c_values
        satellite_prn = np.unique(obs_data.sv)
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
        a = 10

    def test_if_can_be_plotted_second_try(self):
        obs_file = file_reader(file_name)
        obs_data = gr.load(
            obs_file, tlim=[very_start_date, very_end_date], meas=['C1C', 'L1C'], use="E")
        e04_satellite = obs_data.sel(sv='E04').dropna(dim='time', how='all')
        c1c_values = e04_satellite['C1C']
        l1c_values = e04_satellite['L1C']
        c1c_l1c_diff = c1c_values - l1c_values
        plt.plot(c1c_l1c_diff.time, c1c_l1c_diff)
        plt.show()
        a = 10

    def test_for_converting_obs_into_netcdf(self):
        obs_file = file_reader(file_name)
        obs_data = gr.load(
            obs_file, tlim=[very_start_date, very_end_date], meas=['C1C', 'L1C'], use="E")
        obs_data.to_netcdf('process.nc')
        a = 10

    def test_if_saved_netcdf_is_readable(self):
        obs = xarray.open_dataset('process.nc')
        self.assertIsNotNone(obs)
        a = 10

    def test_experiment_of_the_reading_speeds(self):
        # mi a gyorsabb?
        # kiolvasni egy .obs fájlból
        # vagy kiolvasni egy .nc fájlból
        # győzzön a győztes
        start_timestamp_obs = time.time()
        obs_file = file_reader(file_name)
        obs_data = gr.load(
            obs_file, tlim=[very_start_date, small_end_date], meas=['C1C', 'L1C'], use="E")
        end_timestamp_obs = time.time()
        start_timestamp_nc = time.time()
        obs = xarray.open_dataset('process.nc')
        end_timestamp_nc = time.time()
        nc_time = end_timestamp_nc - start_timestamp_nc
        obs_time = end_timestamp_obs - start_timestamp_obs
        a = 10

    def test_checking_units(self):
        obs = xarray.open_dataset('process.nc')
        obs_C1C = obs["C1C"]
        # Constants
        c = 299792458  # Speed of light in meters per second
        l1_frequency = 1575.42e6  # L1 frequency in Hz
        # Convert C1C observations to meters
        wavelength = c / l1_frequency  # Calculate the wavelength in meters
        # Multiply the observations by the wavelength
        obs_C1C_meters = obs_C1C * wavelength
        a = 10

    def test_checking_C1C_to_meter(self):
        obs = xarray.open_dataset('process.nc')
        obs_C1C = obs["C1C"]
        c = 299792458
        l1_frequency = 1575.42e6
        wavelength = c / l1_frequency
        obs_C1C_meters = obs_C1C * wavelength
        a = 10

    def test_checking_L1C_to_meter(self):
        obs = xarray.open_dataset('process.nc')
        obs_L1C = obs["L1C"]
        c = 299792458
        l1_frequency = 1227.6e6
        wavelength = c / l1_frequency
        obs_L1C_meter = obs_L1C * wavelength
        a = 10

    def test_if_can_be_plotted_with_meters(self):
        obs_data = xarray.open_dataset('process.nc')
        e04_satellite = obs_data.sel(sv='E04').dropna(dim='time', how='all')
        c1c_values = e04_satellite['C1C']
        l1c_values = e04_satellite['L1C']

        c = 299792458
        l1_frequency = 1575.42e6
        l2_frequency = 1227.6e6
        wavelength_l1 = c / l1_frequency
        wavelength_l2 = c / l2_frequency
        c1c_values_meter = c1c_values * wavelength_l1
        l1c_values_meter = l1c_values * wavelength_l2
        c1c_l1c_diff = c1c_values_meter - l1c_values_meter

        plt.plot(c1c_l1c_diff.time, c1c_l1c_diff)
        plt.show()
        a = 10


if __name__ == '__main__':
    unittest.main()
