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


    increment_by_amount = 0.5                               # Increment By amount (MM)

    # ==================== Active Status Variables =====================
    
    
    ser_probe_motor = None

    probe_runner_active = False

    curr_x_pos = 0.0

    # ===== Setters + Getters =====

    def set_increment_amount(self, new_increment_amnt):
        self.increment_by_amount = new_increment_amnt


    
    def __activate_probe_runner_status(self):
        """When called, handles settings that need to be turned on for the probe runner main function."""
        probe_runner_active = True

    def __deactivate_probe_runner_status(self):
        """When called, handles settings that need to be turned off for the probe runner to stop effectively"""


    def __handle_probe_movement_result(self, motor_result):
        """Handle the result of moving the motor"""

        # if it reaches the end, handle it. 
        if motor_result["result"] == 1:
            # END REACHED
            print("Motor Reached End...")
            self.probe_runner_active = False
            

        # *MOTOR MOVED* - Handle Movement
        new_moved_pos = motor_result["new_pos"]

        self.curr_x_pos = new_moved_pos


    def __probe_runner(self, motor_ser):
        """Probe runner handles the running processes the entire system. Covering all parts of the probes scaning & movement behavior. Able to Track position and actions from current status."""

        print("PROBE RUNNING...")

        # EVERY ITERATION inside of PROBE RUNNER SHOULD REPRESENT AN INCHING MOVEMENT

        # BEFORE EVEN STARTING PROBE RUNNER, run a check to ensure the probes are out of the way
        self.probe_reading.wait_for_low_voltage(self.probe_reading.voltage_channel)

        while self.probe_runner_active:
            print("Probe runner active! Iterating...")
            
            # Wait for the Low Voltage to be zero
            self.probe_reading.wait_for_low_voltage(self.probe_reading.voltage_channel)

            motor_results = self.motor_movement_manager.move_by_inching(motor_ser, self.curr_x_pos, self.increment_by_amount)

            # Change Behaviors if the motor moved properly 
            self.__handle_probe_movement_result(motor_results)
            
            if self.probe_runner_active == False:
                break

            
            # ONCE HERE, A NEW WHILE LOOP IS NEEDED TO HANDLE WHILE WAITING FOR VOLTAGE INCREASE 
            # NOTHING HAPPENS UNTIL EITHER PROBE FORCIBLY STOPPED, OR VOLTAGE DETECTED
            
            self.probe_reading.start_and_take_safety_probe_reading(self.probe_reading.voltage_channel)





    


            


    def start_tracked_test(self):
        """Function called to start the entire process of incremental probing"""

        # Initalize the Probe Reader
        self.probe_reading.setup_charge_reading()

        # Initalize and prepare motor mover
        self.ser_probe_motor = self.motor_movement_manager.open_and_get_serial_connection()

        self.curr_x_pos = 0.0

        # Ensure the motor is at the start
        self.motor_movement_manager.stall_to_home(self.ser_probe_motor)

        # Call & start the runner
        self.__probe_runner()

    


