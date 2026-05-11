import serial
import time

# ========================= CONFIGURATION =========================
SERIAL_PORT = '/dev/ttyUSB0'   # Common on Raspberry Pi (check with ls /dev/ttyUSB*)
BAUD_RATE   = 115200
TRAVEL_MM   = 100.0            # How far to move (adjust to your stage length)
SPEED       = 2000             # Feed rate in mm/min (start low, e.g. 1000-3000)
REPEATS     = 1                # Number of back-and-forth cycles
# ================================================================

def wait_for_ok(ser):
    """Wait for GRBL 'ok' response"""
    while True:
        response = ser.readline().decode('utf-8').strip()
        print("GRBL:", response)
        if response == "ok" or "error" in response.lower():
            break

# Open serial connection
print("Connecting to Benbox/GRBL...")
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)                    # Wait for GRBL to boot
ser.flushInput()

# Wake up GRBL
ser.write(b"\r\n\r\n")
time.sleep(2)
ser.flushInput()

print("Homing (if limit switches are connected)...")
#ser.write(b"$H\n")               # Remove this line if no limit switches
#wait_for_ok(ser)

#print(f"Starting back-and-forth test: {TRAVEL_MM} mm @ {SPEED} mm/min")

for i in range(REPEATS):
  #  print(f"Cycle {i+1}/{REPEATS}: Moving to {TRAVEL_MM} mm")

    # DEV-Notes|UNIX-1778538875: MOVES DRIVE TO MAX POSITION AT GIVEN SPEED
    to_encode = "G1 X" + str(TRAVEL_MM) + " F" + str(SPEED) + "\n"
    
    ser.write(to_encode.encode('utf-8'))
    #ser.encode()
    wait_for_ok(ser)
    
    time.sleep(0.5)  # Brief pause at end
    iteration_increase = i + 1
    print("Cycle {}/{}: Returning to 0 mm".format(iteration_increase, REPEATS))
    
    # DEV-Notes|UNIX-1778538875: MOVE DRILL BACK TO START POSITION 0
    ser.write("G1 X0 F{}\n".format(SPEED).encode())
    wait_for_ok(ser)
    
    time.sleep(0.5)

print("Test completed! Shutting down motors...")
ser.write(b"M5\n")   # Optional: disable spindle (harmless here)
ser.write(b"G90\n")  # Back to absolute mode

ser.close()
print("Serial port closed. Ready for next test!")