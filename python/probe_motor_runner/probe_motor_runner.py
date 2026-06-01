import os
import sys


mod_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(mod_dir)

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from motor_movement.motor_movement_management import MotorMovementManagement
from probe_reading.probe_reading import ProbeReading

class ProbeMotorRunner:
    """This is main running function where comining motor movements and probe operations meet."""

    # ========================= CONFIGURATION =========================

    motor_movement_manager = MotorMovementManagement()
    probe_reading = ProbeReading()


    increment_by_amount = 0.5        # Increment By amount (MM)

    # ==================== Active Status Variables =====================
    
    
    ser_probe_motor = None

    probe_runner_active = False

    
    def __activate_probe_runner_status():
        """When called, handles settings that need to be turned on for the probe runner main function."""
        probe_runner_active = True

    def __deactivate_probe_runner_status():
        """When called, handles settings that need to be turned off for the probe runner to stop effectively"""



    def __probe_runner(self, motor_ser):
        print("PROBE RUNNING...")
        """Probe runner, when called, handles the iteration of probes scaning & movement behavior. Tracks position and action from current activities"""

        # EVERY ITERATION inside of PROBE RUNNER SHOULD REPRESENT AN INCHING MOVEMENT

        while self.probe_runner_active:
            print("Probe runner active! Iterating...")

            


    def start_tracked_test(self):
        """Function called to start the entire process of incremental probing"""


        # Initalize the Probe Reader
        self.probe_reading.setup_charge_reading()

        # Initalize and prepare motor mover
        self.ser_probe_motor = self.motor_movement_manager.open_and_get_serial_connection()


        # Call the runner

        self.tracked_probe_runner()

    


