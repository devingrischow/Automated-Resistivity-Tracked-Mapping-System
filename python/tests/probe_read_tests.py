import os
import sys
import time
import re


test_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(test_dir)

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


from probe_reading.probe_reading import ProbeReading

class ProbeReadTests:

    probe_data_reader = ProbeReading()


    def TEST_read_out_probe_value(self):
        """Tests the creation, and use of reading out probe voltage data"""

        print("Starting Test Probe Reading Session...")

        self.probe_data_reader.setup_charge_reading()

        probe_reading_value = self.probe_data_reader.read_voltage_value_channelless()

        print("Probe Reading Test Value: ", probe_reading_value)



probe_reader_testing = ProbeReadTests()

probe_reader_testing.TEST_read_out_probe_value()