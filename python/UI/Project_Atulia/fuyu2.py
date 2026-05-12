import serial
import time
import tkinter as tk
from tkinter import messagebox

# ========================= SETTINGS =========================
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE   = 115200
TRAVEL_MM   = 0.5    
SPEED       = 500    
REPEATS     = 5      
# ============================================================

class RailApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fuyu Rail Controller")
        self.root.geometry("450x500")
        self.ser = None
        self.stop_requested = False

        self.frame = tk.Frame(root)
        self.frame.pack(expand=True)


        self.btn_start = tk.Button(self.frame, text="START SCAN", command=self.execute_test, 
                                   bg="#2ecc71", font=("Arial", 12, "bold"), width=25, height=2)
        self.btn_start.pack(pady=10)

        self.btn_stop = tk.Button(self.frame, text="STOP AFTER STEP", command=self.request_stop, 
                                  bg="#f1c40f", font=("Arial", 11, "bold"), width=25, height=2)
        self.btn_stop.pack(pady=10)

        self.btn_kill = tk.Button(self.frame, text="EMERGENCY STOP", command=self.emergency_kill, 
                                  bg="#f1c40f", fg="#2ecc71", font=("Arial", 12, "bold"), width=25, height=2)
        self.btn_kill.pack(pady=10)

        self.init_serial()

    def init_serial(self): #opens connection
        try:
            self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            time.sleep(2) #2 sec pause
            self.ser.write(b"G90\n") 
        except Exception as e:
            messagebox.showerror("Error", f"Connection failed: {e}")

    def wait_for_ok(self, ser):
        while True:
            response = ser.readline().decode('utf-8').strip()
            if response == "ok" or "error" in response.lower():
                break

    def request_stop(self):
        self.stop_requested = Tru

    def execute_test(self):
        self.stop_requested = False
        self.btn_start.config(state="disabled", text="BUSY...")

        for i in range(REPEATS):
            if self.stop_requested:
                break
            
            iteration_increase = i + 1
            target_distance = iteration_increase * TRAVEL_MM
            
            to_encode = "G1 X" + str(target_distance) + " F" + str(SPEED) + "\n"
            
            print(f"Cycle {iteration_increase}/{REPEATS}: Moving to {target_distance} mm")
            
            self.ser.write(to_encode.encode('utf-8'))
            self.wait_for_ok(self.ser)
            
            time.sleep(2.0) 
            self.root.update() 

        # Return to 0 mm
        print("Returning to 0 mm...")
        self.ser.write("G1 X0 F1000\n".encode())
        self.wait_for_ok(self.ser)
        
        self.btn_start.config(state="normal", text="START SCAN")
        messagebox.showinfo("Status", "Scan complete. Rail reset.")

    def emergency_kill(self):
        if self.ser:
            self.ser.write(b"!\n") 
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = RailApp(root)
    root.mainloop()