import os
import re
import sys
import time

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

    def TEST_manual_voltage_read(self):
        """An interactive test that allows manual control over voltage reading."""
        print("\n--- Manual Voltage Read Test Menu ---")

        # Step 1: Initiate the probe reader setup
        self.probe_data_reader.setup_charge_reading()
        print("Probe charging sequence initiated.")

        while True:
            print("---------------Options---------------")
            print("q - Quit Test Session")
            print("test - Immediately read and print voltage")

            user_input = input("What would you like to do?: ")

            if user_input == "q":
                print("Test session terminated.")
                break
            elif user_input == "test":
                print("Reading immediate probe value...")
                try:
                    probe_reading_value = (
                        self.probe_data_reader.read_voltage_value_channelless()
                    )

                    print("Probe Reading Test Value: ", probe_reading_value, "\n")
                except Exception as e:
                    print("Error reading voltage during 'test' mode: ", e, "\n")

            else:
                print("Unknown command. Please enter 'q' or 'test'.")


probe_reader_testing = ProbeReadTests()

# probe_reader_testing.TEST_read_out_probe_value()
probe_reader_testing.TEST_manual_voltage_read()
