import os
import sys


def file_reader(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    rinex_file = os.path.join(script_dir, filename)
    if not os.path.isfile(rinex_file):
        print(f"Error: RINEX file '{rinex_file}' not found.")
    else:
        return rinex_file
