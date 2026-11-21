"""Select and persist Pikachu using the custom firmware's SPEC command."""
import argparse
import time

import serial

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--port", required=True)
args = parser.parse_args()
connection = serial.Serial(port=None, baudrate=115200, timeout=0.25, write_timeout=5)
connection.dtr = True
connection.rts = False
connection.port = args.port

def command(text):
    connection.write((text + "\n").encode())
    connection.flush()
    deadline = time.monotonic() + 10
    lines = []
    while time.monotonic() < deadline:
        line = connection.readline().decode(errors="replace").strip()
        if line:
            print(line)
            lines.append(line)
            if line == "DONE":
                return lines
    raise RuntimeError("No complete response to " + text)

connection.open()
try:
    time.sleep(1)
    connection.reset_input_buffer()
    command("SPEC 25")
    stats = command("STATS")
    health = command("HEALTH")
    if not any(line.startswith("spec=25 ") for line in stats):
        raise SystemExit("Pikachu selection was not confirmed")
    if not any("mon=1" in line for line in health):
        raise SystemExit("Pikachu selected, but sprite loading was not confirmed")
    print("Pikachu selected and saved; sprite loaded")
finally:
    connection.close()
