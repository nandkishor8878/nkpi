from typing import Protocol


class ServoPort(Protocol):
    def set_angle(self, channel: int, angle: int) -> list[str]:
        """Move a servo channel to an angle."""

    def stop(self, channel: int) -> list[str]:
        """Release or stop a servo channel when supported."""

