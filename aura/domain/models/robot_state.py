from dataclasses import dataclass, field
import time
from typing import Any


@dataclass
class RobotState:
    started_at: float = field(default_factory=time.monotonic)
    led: str = "unknown"
    servos: dict[int, int] = field(default_factory=dict)
    distance_cm: float | None = None
    imu: dict[str, Any] | None = None
    visitor: str | None = None
    mode: str = "reception"

    def uptime_seconds(self) -> int:
        return int(time.monotonic() - self.started_at)

