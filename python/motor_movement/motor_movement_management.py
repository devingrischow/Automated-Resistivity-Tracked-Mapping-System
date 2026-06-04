import serial
import time

class MotorMovementManagement:

# ===================== CONFIGURATION CONSTANTS ==================

    DEFAULT_SERIAL_PORT = '/dev/ttyUSB0'
    BAUD_RATE   = 115200
    MAX_TRAVEL_DISTANCE_MM = 30            # Max Travel Distance the motor can move (Value from side of motor)
    SPEED       = 500             # Feed rate in mm/min (start low, e.g. 1000-3000)

# ================================================================

# ===================== CONFIGURATION VARIABLES ==================

    SERIAL_PORT = DEFAULT_SERIAL_PORT

# ================================================================

    

    def __wait_for_response(self, ser):
        """Wait for GRBL 'ok' or `error` response"""
        while True:
            response = ser.readline().decode('utf-8').strip()
            print("GRBL:", response)
            if response == "ok" or "error" in response.lower():
                break



    def __send_gcode_command(self, ser, command_to_send):
        """Main Function that Sends GCode Command to a given Serial"""
        ser.write(command_to_send.encode('utf-8'))

    def __send_gcode_command_wait_for_timed_response(self, ser, command_to_send, time_to_wait=2):
        """Sends GCode Command and waits for a timed response"""
        self.__send_gcode_command(ser, command_to_send)
        time.sleep(time_to_wait)

    def __send_gcode_command_wait_for_response(self, ser, command_to_send):
        """Sends GCode Command, and waits for response"""
        self.__send_gcode_command(ser, command_to_send)
        self.__wait_for_response(ser)




    def __set_serial_to_absolute_mode(self, ser):
        """Sends a command that sets the serial to GCode Absolute Mode"""
        print("Setting SER to Absolute Mode....")
        absolute_command = "G90\n"

        # Use the response from board to respond
        self.__send_gcode_command_wait_for_response(ser, absolute_command)

    def __set_serial_to_relative_mode(self, ser):
        """Sends command to sets the serial to Relative Mode"""
        print("Setting SER to Relative Mode....")
        rel_command = "G91\n"

        self.__send_gcode_command_wait_for_response(ser, rel_command)


    def __set_serial_home_zero_position(self, ser):
        """Sends a command to set the serial home zero position to the motors current position"""
        print("Setting New Ser Zero Position....")
        zero_command = "G92 X0\n"

        self.__send_gcode_command_wait_for_response(ser, zero_command)


    
    ### ---- Startup / Config ----

    def open_and_get_serial_connection(self):
        """Opens a Connection to a serial connection, and returns the new serial object"""

        print("Connecting to Benbox/GRBL...")
        ser = serial.Serial(self.SERIAL_PORT, self.BAUD_RATE, timeout=1)
        time.sleep(2)                    # Wait for GRBL to boot
        ser.flushInput()

        # Wake up GRBL
        flush_command = "\r\n\r\n"
        self.__send_gcode_command_wait_for_timed_response(ser, flush_command)
        ser.flushInput()

        self.__set_serial_to_absolute_mode(ser)


        return ser


    # def start_up_at_orgin_home(self):
    #     """Called When Started From the orgin spot on the motor, and the home location needs to be redeclared"""
    # ## Find Home Location

    def stall_to_home(self, ser):
        """Uses the Stall-Homing Method to find the zero home position on the motor setup, and sets the zero"""

        self.__set_serial_to_relative_mode(ser)

        print("Moving Backwards Along Length of Shaft until Stalled at End Point...")

        move_back_towards_start_command = "G1 X-{} F{}\n".format(self.MAX_TRAVEL_DISTANCE_MM, self.SPEED)
        self.__send_gcode_command_wait_for_response(ser, move_back_towards_start_command)

        wait_for_motor_arrive_at_home_duration = 5.0
        time.sleep(wait_for_motor_arrive_at_home_duration) # Long Pause to allow for motor to head towards Start

        print("Finished Moving Towards Start! Zeroing New Home Position...")

        # Return to absolute positioning and Zero Out the Position
        self.__set_serial_to_absolute_mode(ser)
        self.__set_serial_home_zero_position(ser)


    ### ---- Shutdown Handling ----

    def shut_down_motors(self, ser):
        print("Shut Down Motors Function Recieved...")

        optional_disable_spindle_command = "M5\n"
        self.__send_gcode_command_wait_for_response(ser, optional_disable_spindle_command)  # Optional: disable spindle (harmless here)

        self.__set_serial_to_absolute_mode(ser)  # Back to absolute mode (should already be in absolute mode, but for good measure)
        
        ser.close()                                         




    
    ### ---- Movement Controls ----

    def move_motor_to_pos(self, ser, move_to_pos):
        """When called takes a serial instance and an `x` Position to move to, and sends gcode to the serial to move to the given position."""
        str_move_pos = str(move_to_pos)

        print("Moving to X", str_move_pos, "....")

        move_to_position_cmd = "G1 X" + str_move_pos + " F" + str(self.SPEED) + "\n"

        self.__send_gcode_command_wait_for_response(ser, move_to_position_cmd)

        time.sleep(0.5)  # Brief pause at end of a wait for response code

    def move_by_inching(self, ser, curr_pos, inch_by):
        """Takes a `curr_pos` value and an `inch_by` value and increments the pos value by it, however refuses movement if inch will exceed safe amount. Returns a dictionary of operation results"""

        new_inched_pos = curr_pos + inch_by

        max_travel_leeway_amount = 5

        if new_inched_pos >= (self.MAX_TRAVEL_DISTANCE_MM - max_travel_leeway_amount):
            # Return Early, TO CLOSE TO END 
            reach_end_dict = {"result":0, "reason":"Reached End", "new_pos":curr_pos}
            return reach_end_dict

        move_by_inching_cmd = "G1 X{} F{}\N".format(new_inched_pos, self.SPEED)

        self.__send_gcode_command_wait_for_response(ser, move_by_inching_cmd)

        time.sleep(0.5)

        good_move_result = {"result":1, "new_pos":new_inched_pos}
        return good_move_result














    def return_motor_to_start(self, ser):
        """When called returns the motor back to the home position"""
        print("Return Motor to Start Function Recieved...")


        return_to_start_gcode_command = "G1 X0 F{}\n".format(self.SPEED)
        self.__send_gcode_command_wait_for_response(ser, return_to_start_gcode_command)
    