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
        return ["UNKNOWN_COMMAND"]

    def close(self) -> None:
        return None
