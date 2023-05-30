import georinex as gr

very_start_date = '2023-03-04T11:02:00'
small_end_date = '2023-03-04T11:06:00'
rinex_file = "PildoBox20923063l.obs"

obs_data = gr.load(rinex_file, tlim=[very_start_date, small_end_date], meas=[
                   'L1C', 'L2W'], use="G")
obs_data.to_netcdf('ha_ezt_latod_a_mappaban_mukodik.nc')
