import serial
import time

class MotorMovementManagement:

# ===================== CONFIGURATION CONSTANTS ==================

    DEFAULT_SERIAL_PORT = '/dev/ttyUSB0'
    BAUD_RATE   = 115200
    MAX_TRAVEL_DISTANCE_MM = 100            # Max Travel Distance the motor can move (Value from side of motor)
    SPEED       = 2000             # Feed rate in mm/min (start low, e.g. 1000-3000)

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
        absolute_command = "G90\n"

        # Use the response from board to respond
        self.__send_gcode_command_wait_for_response(ser, absolute_command)


    def open_and_get_serial_connection(self):
        """Opens a Connection to a serial connection, and returns the serial object"""

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

    def shut_down_motors(self, ser):
        optional_disable_spindle_command = "M5\n"

        self.__send_gcode_command_wait_for_response(ser, optional_disable_spindle_command)  # Optional: disable spindle (harmless here)
        self.__set_serial_to_absolute_mode(ser)                                             # Back to absolute mode



    def return_motor_to_start(self, ser):
        """When called returns the motor back to the home position"""

        return_to_start_gcode_command = "G1 X0 F{}\n".format(self.SPEED)

        self.__send_gcode_command_wait_for_response(ser, return_to_start_gcode_command)