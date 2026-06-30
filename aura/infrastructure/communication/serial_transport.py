import time

from aura.config.settings import Settings


class SerialTransport:
    def __init__(self, settings: Settings):
        import serial

        self._serial = serial.Serial(
            settings.serial_port,
            settings.serial_baudrate,
            timeout=settings.serial_timeout_seconds,
        )
        time.sleep(settings.hardware_startup_delay_seconds)

    def send(self, command: str) -> list[str]:
        self._serial.write(f"{command}\n".encode("utf-8"))
        time.sleep(0.1)

        response = []
        while self._serial.in_waiting:
            response.append(self._serial.readline().decode("utf-8").strip())
        return response

    def close(self) -> None:
        if self._serial and self._serial.is_open:
            self._serial.close()

