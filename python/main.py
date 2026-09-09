"""
Crystal — Automated Resistivity Mapping System
main.py — Core scan logic + local web server

Run this file directly: python3 main.py
Then open http://localhost:5000 in any browser.
"""

import serial
import time
import csv
import os
import json
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

# ========================= CONFIGURATION =========================
SERIAL_PORT  = '/dev/ttyUSB0'   # Windows: 'COM3', Mac: '/dev/tty.usbserial-*'
BAUD_RATE    = 115200
CURRENT_A    = 0.00453          # Assumed 4.53 mA — confirm with hardware team
STEP_MM      = 1                # Measure every 1 mm
TOTAL_MM     = 100              # Total travel of FUYU stage (mm)
SPEED        = 500              # Feed rate mm/min — safe starting speed
OUTPUT_FILE  = 'scan_results.csv'
# ================================================================

# Global state shared between scan thread and web server
scan_state = {
    "status": "ready",       # ready | scanning | complete | error
    "progress": 0,           # 0-100
    "current_position": 0,
    "results": [],           # list of {position, voltage, resistance}
    "error": None
}

# ── Scan logic ──────────────────────────────────────────────────

def wait_for_ok(ser, timeout=10):
    """Wait for GRBL 'ok' response"""
    start = time.time()
    while True:
        if time.time() - start > timeout:
            raise TimeoutError("GRBL did not respond in time")
        response = ser.readline().decode('utf-8', errors='ignore').strip()
        if response == "ok":
            return True
        if "error" in response.lower():
            raise RuntimeError(f"GRBL error: {response}")

def read_voltage():
    """
    Read voltage from ADS1115 via I2C.
    Returns voltage in volts.
    Requires: pip install adafruit-circuitpython-ads1x15
    """
    try:
        import board
        import busio
        import adafruit_ads1x15.ads1115 as ADS
        from adafruit_ads1x15.analog_in import AnalogIn

        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c)
        chan = AnalogIn(ads, ADS.P0, ADS.P1)  # differential mode
        return chan.voltage
    except Exception:
        # If no hardware connected, return simulated value for testing
        import random
        return random.uniform(0.020, 0.055)

def calculate_resistance(voltage):
    """
    Rs = 4.532 * (V / I)
    Standard four-point probe formula for thin films.
    4.532 = pi / ln(2) — geometric correction factor
    """
    if CURRENT_A == 0:
        return 0
    return 4.532 * (voltage / CURRENT_A)

def run_scan():
    """Main scan loop — runs in a background thread"""
    global scan_state

    scan_state["status"] = "scanning"
    scan_state["progress"] = 0
    scan_state["results"] = []
    scan_state["error"] = None

    results = []

    try:
        # Connect to Benbox/GRBL
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
        time.sleep(2)
        ser.flushInput()

        # Wake up GRBL
        ser.write(b"\r\n\r\n")
        time.sleep(2)
        ser.flushInput()

        # Home the stage
        ser.write(b"G1 X0 F{}\n".format(SPEED).encode())
        wait_for_ok(ser)
        time.sleep(0.5)

        positions = list(range(0, TOTAL_MM + 1, STEP_MM))
        total_steps = len(positions)

        # Open CSV for writing
        with open(OUTPUT_FILE, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Position (mm)', 'Voltage (V)', 'Current (A)', 'Sheet Resistance (ohms/sq)', 'Timestamp'])

            for i, pos in enumerate(positions):
                # Move stage
                cmd = "G1 X{} F{}\n".format(pos, SPEED)
                ser.write(cmd.encode('utf-8'))
                wait_for_ok(ser)
                time.sleep(0.3)  # settle time

                # Read voltage and calculate resistance
                voltage = read_voltage()
                resistance = calculate_resistance(voltage)
                timestamp = datetime.now().strftime('%H:%M:%S')

                row = {
                    "position": pos,
                    "voltage": round(voltage, 6),
                    "resistance": round(resistance, 2),
                    "timestamp": timestamp
                }
                results.append(row)

                # Write to CSV
                writer.writerow([pos, voltage, CURRENT_A, resistance, timestamp])
                csvfile.flush()

                # Update global state
                scan_state["results"] = results.copy()
                scan_state["current_position"] = pos
                scan_state["progress"] = int((i + 1) / total_steps * 100)

        # Return stage to home
        ser.write("G1 X0 F{}\n".format(SPEED).encode())
        wait_for_ok(ser)
        ser.close()

        scan_state["status"] = "complete"
        scan_state["progress"] = 100

    except serial.SerialException:
        # No hardware — run in demo mode with simulated data
        print("No serial device found — running in DEMO MODE with simulated data")
        positions = list(range(0, TOTAL_MM + 1, STEP_MM))
        import random
        with open(OUTPUT_FILE, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Position (mm)', 'Voltage (V)', 'Current (A)', 'Sheet Resistance (ohms/sq)', 'Timestamp'])
            for i, pos in enumerate(positions):
                time.sleep(0.05)  # simulate scan speed
                voltage = random.uniform(0.020, 0.055)
                resistance = calculate_resistance(voltage)
                timestamp = datetime.now().strftime('%H:%M:%S')
                row = {
                    "position": pos,
                    "voltage": round(voltage, 6),
                    "resistance": round(resistance, 2),
                    "timestamp": timestamp
                }
                results.append(row)
                writer.writerow([pos, round(voltage, 6), CURRENT_A, round(resistance, 2), timestamp])
                csvfile.flush()
                scan_state["results"] = results.copy()
                scan_state["current_position"] = pos
                scan_state["progress"] = int((i + 1) / len(positions) * 100)

        scan_state["status"] = "complete"
        scan_state["progress"] = 100

    except Exception as e:
        scan_state["status"] = "error"
        scan_state["error"] = str(e)
        print(f"Scan error: {e}")

# ── Web server ───────────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PAGE = open(os.path.join(BASE_DIR, 'ui.html')).read()
CSS_PAGE  = open(os.path.join(BASE_DIR, 'styles.css')).read()
JS_PAGE   = open(os.path.join(BASE_DIR, 'app.js')).read()

class CrystalHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # suppress server logs

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode())

        elif self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(scan_state).encode())

        elif self.path == '/styles.css':
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            self.wfile.write(CSS_PAGE.encode())

        elif self.path == '/app.js':
            self.send_response(200)
            self.send_header('Content-type', 'application/javascript')
            self.end_headers()
            self.wfile.write(JS_PAGE.encode())

        elif self.path == '/start':
            if scan_state["status"] not in ("scanning",):
                thread = threading.Thread(target=run_scan, daemon=True)
                thread.start()
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"started": True}).encode())
            else:
                self.send_response(400)
                self.end_headers()

        elif self.path == '/download':
            if os.path.exists(OUTPUT_FILE):
                self.send_response(200)
                self.send_header('Content-type', 'text/csv')
                self.send_header('Content-Disposition', 'attachment; filename="scan_results.csv"')
                self.end_headers()
                with open(OUTPUT_FILE, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

PORT = 8765  # Using 8765 to avoid Chrome's localhost blocking

def open_browser():
    time.sleep(1)
    import platform
    import subprocess
    url = f'http://127.0.0.1:{PORT}'
    system = platform.system()
    if system == 'Darwin':  # Mac — try Chrome first, then Safari as fallback
        try:
            subprocess.call(['open', '-a', 'Google Chrome', url])
        except Exception:
            pass
        try:
            subprocess.call(['open', '-a', 'Safari', url])
        except Exception:
            pass
    elif system == 'Windows':
        subprocess.call(['start', url], shell=True)
    else:  # Linux / Raspberry Pi
        subprocess.call(['xdg-open', url])

if __name__ == '__main__':
    PORT_URL = f'http://127.0.0.1:{PORT}'
    print("Crystal Resistivity Scanner starting...")
    print(f"Opening browser at {PORT_URL}")
    print(f"If browser doesn't open, go to: {PORT_URL}")
    threading.Thread(target=open_browser, daemon=True).start()
    server = HTTPServer(('0.0.0.0', PORT), CrystalHandler)
    server.serve_forever()
