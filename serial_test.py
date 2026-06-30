import serial
import time

ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)

time.sleep(2)

print("Connected!")

ser.write(b"PING\n")

time.sleep(0.5)

while ser.in_waiting:
    print(ser.readline().decode().strip())

ser.close()
