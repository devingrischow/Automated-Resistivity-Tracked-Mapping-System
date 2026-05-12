import serial 
import time

SERIAL_PROT = '/dev/ttyUSB0'
BAUD_RATE   = 115200 # talking speed b/w pi and fuyu
TRAVEL_MM   = 100.0
SPEED       = 0.5
REPEATS     = 1

def wait_for_ok(ser):
    while True:
        response = ser.readline().decode('utf-8').strip()
        print("GRBL:", response)
        if response == "ok" or "error" in response.lower():
            break

# Open serial connection
print("Connecting to the Benbon/GRBL...")
ser = serial.Serial(SERIAL_PROT, BAUD_RATE, timeout=1)
time.sleep(2)
ser.flushInput()

# Wake up GRBL
ser.write(b"\r\n\r\n")
time.sleep(2)
ser.flushInput()

for i in range(REPEATS):
    to_encode = "G1 X" + str(TRAVEL_MM) + "F " + str(SPEED) + "\n"
    ser.write(to_encode.encode('utf-8'))
    wait_for_ok(ser)

    time.sleep(0.5)
    iteration_increase = i + 1
    print("Cycle {}/{}: Returning to 0mm".format(iteration_increase, REPEATS))

    ser.write("G1 X0 F{}\n".format(SPEED.encode())) 
    wait_for_ok(ser)

    time.sleep(0.5)


print("Test completed! Shutting down motors...")
ser.write(b"M5\n")
ser.write(b"G90\n")

ser.close()
print("Serial Port closed. Ready for next test!")