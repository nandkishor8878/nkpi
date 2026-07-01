from typing import Protocol


class ServoPort(Protocol):
    def set_angle(self, channel: int, angle: int) -> list[str]:
        """Move a servo channel to an angle."""

