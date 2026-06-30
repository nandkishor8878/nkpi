import serial
import time

class SerialService:

    def __init__(self):
        self.ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
        time.sleep(2)

    def send(self, command):

        self.ser.write(f"{command}\n".encode())

        time.sleep(0.1)

        response = []

        while self.ser.in_waiting:
            response.append(
                self.ser.readline().decode().strip()
            )

        return response


serial_service = SerialService()
