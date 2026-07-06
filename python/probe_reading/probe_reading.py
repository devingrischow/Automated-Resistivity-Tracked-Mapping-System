import board

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time

import busio

class ProbeReading:

    """
    Notes:

    - Output format of the Tests:
    {
        "test_date":1780597131,
        "readings":[
            {
            "time":1780597131,
            "voltage":5.2
            },
            {
            "time":1780597369,
            "voltage":2.6
            }
        ]
    }

    - Output to json format, file created at test start

    """
    

    """Variable that handles voltage change detection"""

    i2c = None
    voltage_channel = None
    ads = None

    def __create_test_output_file():
        """
        When Called, creates the output file the test information will be written to.00
        """

    def __write_probe_output_value(self, value):
        """
        Function Dedicated to writing the output of the given value to the output file of the tests status.
        """

    def __read_probe_and_write_output(self, channel):
        """
        Reads the current voltage from the Probe Channel, and outputs it/ saves it to file.
        """
        print("Reading Probe Value...")

        current_voltage = channel.voltage

        print("READ PROBE! Writing Output.")


    def read_voltage_value_channelless(self):
        return self.voltage_channel.voltage



    def setup_charge_reading(self, ads_gain = 4): # Try Gain Values of 2, 4, 8, or 16
        """
        Handle Test Start Setup of the probe systems. 
        """

        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1115(self.i2c)

        self.voltage_channel = AnalogIn(self.ads, ADS.P0, ADS.P1) # Differential between A0 and A1
        
        self.ads.gain = ads_gain


    def wait_for_low_voltage(self, channel, duration=5.0, threshold=0.01):
        """
        Blocks Execution & Operations until the voltage has been near 0V/Given Voltage Threshold for a coninuous duration.
        """

        print("Waiting for voltage to drop...")

        zero_start_time = None

        while True:
            current_voltage = channel.voltage

            if abs(current_voltage) <= threshold:
                if zero_start_time is None:
                    # Once the threshold reaches 0V for the first time, start the timer 
                    zero_start_time = time.time()

                elif time.time() - zero_start_time >= threshold:
                    print("Voltage has been 0V for Safe Duration...")
                    return
            else:
                # VOLTAGE IS NOT 0, RESET TIMER 
                zero_start_time = None

            # Poll every 100ms to balance accuracy and CPU usage
            time.sleep(0.1)


    def wait_for_active_voltage_readings(self, channel, duration=5.0, threshold=0.5):
        """
        Blocks Motor Movements and Actions until the voltage is consistently above the threshold for positive valid readings
        """

        print("Waiting for voltage to stay above threshold to allow for probe reading...")

        reading_start_time = None

        while True:
            current_voltage = channel.voltage

            if abs(current_voltage) > threshold:
                if reading_start_time is None:
                    # Start the timer the first time it crosses above zero
                    reading_start_time = time.time()
                elif time.time() - reading_start_time >= duration:
                    print("Voltage Above 0, Pins Are able to Read...")
                    return
            else:
                # If the value drops to low during reading, assume the button was released, and prevent phantom reading
                reading_start_time = None

            # Poll every 100ms to balance accuracy and CPU usage
            time.sleep(0.1)



    def start_and_take_safety_probe_reading(self, channel):
        """
        Function That handles safely reading the probe voltages.

        Works primarily through waiting for the voltage to be consistent above 0 for a duration, once that is reached the reader reads the value and outputs it.
        """

        print("Starting Saftey Probe Reading...")

        print("Waiting for voltage to be above zero reading...")
        self.wait_for_active_voltage_readings(channel)

        print("Voltage above zero, taking reading...")

        



