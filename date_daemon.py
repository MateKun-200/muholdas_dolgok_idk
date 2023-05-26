from datetime import datetime
import numpy as np


def distance_in_sec(start_date, end_date):
    start_datetime = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
    end_datetime = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S")
    time_diff = end_datetime - start_datetime
    time_diff_seconds = time_diff.total_seconds()
    seconds_array = np.arange(0, int(time_diff_seconds)+1)
    return seconds_array
