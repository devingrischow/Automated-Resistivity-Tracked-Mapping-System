
import os
import sys
import time
import re


test_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(test_dir)

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


from probe_reading.probe_reading import ProbeReading


class ProbeReadOutputTests:

    probe_data_reader = ProbeReading()

    