import board

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time

import busio

class ProbeReading:

    """Variable that handles voltage change detection"""

    i2c = None
    voltage_channel = None
    ads = None

    def setup_charge_reading(self, ads_gain = 4): # Try Gain Values of 2, 4, 8, or 16
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