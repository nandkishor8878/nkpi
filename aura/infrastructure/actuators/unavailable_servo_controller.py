import logging


logger = logging.getLogger(__name__)


class UnavailableServoController:
    def __init__(self, reason: str):
        self._reason = reason
        logger.error("Servo controller unavailable: %s", reason)

    def set_angle(self, channel: int, angle: int) -> list[str]:
        raise RuntimeError(f"Servo controller unavailable: {self._reason}")

    def stop(self, channel: int) -> list[str]:
        raise RuntimeError(f"Servo controller unavailable: {self._reason}")

    def stop(self, channel: int) -> list[str]:
        raise RuntimeError(f"Servo controller unavailable: {self._reason}")
