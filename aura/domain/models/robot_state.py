from dataclasses import dataclass, field
import time
from typing import Any


@dataclass
class DiagnosticEvent:
    timestamp: float
    level: str
    message: str


@dataclass
class RobotState:
    started_at: float = field(default_factory=time.monotonic)
    led: str = "unknown"
    servos: dict[int, int] = field(default_factory=dict)
    distance_cm: float | None = None
    proximity_detected: bool | None = None
    imu: dict[str, Any] | None = None
    visitor: str | None = None
    mode: str = "reception"
    command_count: int = 0
    error_count: int = 0
    last_command: str | None = None
    last_error: str | None = None
    events: list[DiagnosticEvent] = field(default_factory=list)

    def uptime_seconds(self) -> int:
        return int(time.monotonic() - self.started_at)
