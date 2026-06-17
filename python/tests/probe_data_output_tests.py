import os
import sys
import time
import re

test_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(test_dir)

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


from probe_data_output.probe_data_output import ProbeDataOutput


class ProbeDataOutputTests:

    probe_data_output = ProbeDataOutput()

    


    def TEST_probe_session_start(self):
        """Tests the start and creation of the probe data output session."""
        print("Starting Test Probe Session...")
        self.probe_data_output.start_probe_output_session()

        print("Completed test probe session creation.")

    def TEST_probe_session_record_probe_data(self):
        """Tests the recording of probe readings and adding the results to the probe output."""

        print("Starting probe test recording...")
        test_float_input = float(input("Test Value: "))
        self.probe_data_output.record_new_probe_reading(test_float_input)

        print("Completed test probe recording.")



probe_data_output_tests = ProbeDataOutputTests()

# probe_data_output_tests.TEST_probe_session_start()

probe_data_output_tests.TEST_probe_session_record_probe_data()