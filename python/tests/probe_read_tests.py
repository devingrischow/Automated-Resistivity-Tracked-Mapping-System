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

        probe_read_value_from_channel = self.probe_data_reader.read_voltage_value_from_channel(self.probe_data_reader.voltage_channel)
        print("Probe Reading from channel Test Value: ", probe_read_value_from_channel, "\n")

    def TEST_no_metal_on_probe(self):
        """A test that checks if no metal is in the way of the probe.
        Test will be complete once it detects no metal is in the way or near the probe."""
        print("Starting No Metal On Probe Test...")

        self.probe_data_reader.setup_charge_reading()

        # After Setting Up Charge Reading, Set up and call "wait_for_low_voltage"
        self.probe_data_reader.wait_for_low_voltage(self.probe_data_reader.voltage_channel)

        print("Wait for low voltage test exited! Low enough voltage detected during short time")


    #TODO - Write Test Function for Testing if Metal is in the way
    def TEST_metal_on_probe(self):
        """
        A test that checks whether metal is in the way of the probe.
        Test will complete once it detects metal is in the way of the probe for a given duration
        """
        print("Starting Metal On Probe Detection Test...")

        self.probe_data_reader.setup_charge_reading()

        # After Setting up the charge reading, set up and call "wait_for_active_voltage_readings" for active reading
        self.probe_data_reader.wait_for_active_voltage_readings(self.probe_data_reader.voltage_channel)

        print("Wait for active voltage test exited! Minimum Enough Voltage detected during the test to exit the wait")


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

                    probe_read_value_from_channel = self.probe_data_reader.read_voltage_value_from_channel(self.probe_data_reader.voltage_channel)
                    print("Probe Reading from channel Test Value: ", probe_read_value_from_channel, "\n")
                except Exception as e:
                    print("Error reading voltage during 'test' mode: ", e, "\n")

            else:
                print("Unknown command. Please enter 'q' or 'test'.")


probe_reader_testing = ProbeReadTests()

# probe_reader_testing.TEST_read_out_probe_value()
# probe_reader_testing.TEST_no_metal_on_probe()
probe_reader_testing.TEST_metal_on_probe()


# Manual Test
#probe_reader_testing.TEST_manual_voltage_read()
