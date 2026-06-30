from typing import Protocol


class CommandTransportPort(Protocol):
    def send(self, command: str) -> list[str]:
        """Send a command and return response lines."""

    def close(self) -> None:
        """Release transport resources."""

