import os
import sys
import time
import re

test_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(test_dir)

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from motor_movement.motor_movement_management import MotorMovementManagement


class MotorMovementManagementTests:

    motor_movement_manager = MotorMovementManagement()


    DEFAULT_REPEATS = 5


    def __TEST_initalize_and_shutdown_motor(self):
        """Test motor initalization connection and motor start"""
        print("Testing Initalize & Shutdown Motor:")

        ser_test_motor = self.motor_movement_manager.open_and_get_serial_connection()
        
        test_sleep_time = 2
        print("Sleeping for:", test_sleep_time, "Seconds, Then Shutting Down.")
        time.sleep(2)                    # Wait for GRBL to boot

        self.motor_movement_manager.shut_down_motors(ser_test_motor)

        self.completed_test()


    def __TEST_dave_initaial_movement_test(self):
        MAX_POS_MM = 100.0


        """Preforms a modernized test of Daves first serial test"""
        print("Testing Modernized Dave First Serial Test")

        ser_test_motor = self.motor_movement_manager.open_and_get_serial_connection()

        repeats = input("How Many Repeats Should the Motor Do? ")

        # Input Handling
        try:
            repeats = int(repeats)
        except:
            print("Invalid Number Given, using 5")
            repeats = self.DEFAULT_REPEATS
        
        

        for i in range(repeats):
            print("Cycle {}/{}: Moving to Max Distance".format(i + 1, repeats))
            self.motor_movement_manager.move_motor_to_pos(ser_test_motor, MAX_POS_MM)

            print("Move Complete, Returning Home after delay...")

            print("Cycle {}/{}: Returning to 0 mm".format(i + 1, repeats))
            self.motor_movement_manager.return_motor_to_start(ser_test_motor)

        print("Test completed! Shutting down motors...")
        self.motor_movement_manager.shut_down_motors(ser_test_motor)

        self.completed_test()


    def __TEST_manual_position_input_testing(self):
        """A Test that allows for manual limited control over the motor. TO BE USED FOR TESTING ONLY!"""
        print("Starting Manual Postion Motor Movement Test....")

        ser_test_motor = self.motor_movement_manager.open_and_get_serial_connection()

        while True:
            print("\nMovement Commands: ")
            print("---------------------")

            print("- Type a number representing an x-coordinate in space")
            print("- home -> calls return to home command")
            print("- q -> Quit, Stop, Disconnect")
            print("")

            next_movement = input("Where do you want to move to? ")

            if next_movement == "q":
                print("Quit Manual Test")
                break
            elif next_movement == "home":
                print("Moving to Home")
                self.motor_movement_manager.return_motor_to_start(ser_test_motor)
            elif bool(re.search(r'\d', next_movement)):
                print("Moving to Position ", next_movement)

                self.motor_movement_manager.move_motor_to_pos(ser_test_motor, next_movement)
            else:
                print("Command Not Recognized")

            
        
                

        self.motor_movement_manager.return_motor_to_start(ser_test_motor)
        
        print("Test Complete! Shutting Down Motor...")
        self.motor_movement_manager.shut_down_motors(ser_test_motor)

        self.completed_test()




    def completed_test(self):
        print("\nTest Complete - Returning to Test Options\n")

        self.__handle_testing_choice_actions()


    def __handle_testing_choice_actions(self):
        print("\n--------Test Options--------")

        print("1. __TEST_initalize_and_start_motor")
        print("2. __TEST_dave_initaial_movement_test")
        print("3. __TEST_manual_position_input_testing")
        print("q. Quit Test")

        print("\n")

        test_action_input = input("Select the Test your want to perform: ")

        print("----------------------\n")

        if test_action_input == "1":
            self.__TEST_initalize_and_shutdown_motor()
        elif test_action_input == "2":
            self.__TEST_dave_initaial_movement_test()
        elif test_action_input == "3":
            self.__TEST_manual_position_input_testing()
        elif test_action_input == "q":
            print("Quitting Testing...")
            sys.exit()


    def start_main_testing_session(self):
        """Main Test Session Start Function. All Test Commands are to be able to be started & called from here."""

        print("Motor Movement Test Management Session Started..........")


        self.__handle_testing_choice_actions()

    





# Start the Testing Class

motor_testing_class = MotorMovementManagementTests()
motor_testing_class.start_main_testing_session()

