import board

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time

import busio

class ProbeReading:

    """Variable that handles voltage change detection"""
    voltage_change_detector = None

    def setup_charge_reading(self, ads_gain = 4): # Try Gain Values of 2, 4, 8, or 16
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c)

        self.voltage_change_detector = AnalogIn(ads, ADS.P0, ADS.P1) # Differential between A0 and A1
        
        ads.gain = ads_gain 