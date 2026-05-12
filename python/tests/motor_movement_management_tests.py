import os
import sys

test_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(test_dir)

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from motor_movement.motor_movement_management import MotorMovementManagement


class MotorMovementManagementTests:

    motor_movement_manager = MotorMovementManagement()


    ser_motor = None # Uninitalized Serial Object for the motor

    def __TEST_initalize_and_start_motor(self):
        """Test motor initalization connection and motor start!"""
        print("Testing Initalize")

        # self.ser_motor = self.motor_movement_manager.open_and_get_serial_connection()

        # On Complete 
        self.__handle_testing_choice_actions()

    def __handle_testing_choice_actions(self):
        print("\n--------Test Options--------")

        print("1. __TEST_initalize_and_start_motor")

        print("\n")

        test_action_input = input("Select the Test your want to perform: ")

        print("----------------------")

        if test_action_input == "1":
            self.__TEST_initalize_and_start_motor()


    def start_main_testing_session(self):
        """Main Test Session Start Function. All Test Commands are to be able to be started & called from here."""

        print("Motor Movement Test Management Session Started..........")


        self.__handle_testing_choice_actions()

    





# Start the Testing Class

motor_testing_class = MotorMovementManagementTests()
motor_testing_class.start_main_testing_session()

