import serial
import time

class MotorMovementManagement:

# ===================== CONFIGURATION CONSTANTS ==================

    DEFAULT_SERIAL_PORT = '/dev/ttyUSB0'
    BAUD_RATE   = 115200
    MAX_TRAVEL_DISTANCE_MM = 100            # Max Travel Distance the motor can move (Value from side of motor)


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



    def __open_and_get_serial_connection(self):
        """Opens a Connection to a serial connection, and returns the serial"""

        print("Connecting to Benbox/GRBL...")
        ser = serial.Serial(self.SERIAL_PORT, self.BAUD_RATE, timeout=1)
        time.sleep(2)                    # Wait for GRBL to boot
        ser.flushInput()

        # Wake up GRBL
        flush_command = "\r\n\r\n"
        self.__send_gcode_command_wait_for_timed_response(ser, flush_command)
        
        ser.flushInput()

        return ser

