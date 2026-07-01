from aura.infrastructure.communication.protocol import Esp32Protocol


class MockTransport:
    def __init__(self):
        self.commands: list[str] = []

    def send(self, command: str) -> list[str]:
        self.commands.append(command)
        if command == Esp32Protocol.PING:
            return ["PONG"]
        if command in {Esp32Protocol.LED_ON, Esp32Protocol.LED_OFF}:
            return ["OK"]
        if command.startswith("SERVO:"):
            return ["OK"]
        if command == Esp32Protocol.READ_DISTANCE:
            return ["DISTANCE_CM:42.7"]
        if command == Esp32Protocol.READ_IMU:
            return ["IMU:AX:0.01:AY:0.02:AZ:1.00:GX:0.10:GY:0.20:GZ:0.30"]
        if command == Esp32Protocol.READ_IMU_STATUS:
            return ["IMU_STATUS:CONNECTED:1:ADDRESS:0x68:ERROR:NONE"]
        return ["UNKNOWN_COMMAND"]

    def close(self) -> None:
        return None
