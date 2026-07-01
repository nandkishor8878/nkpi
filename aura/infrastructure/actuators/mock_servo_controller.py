from aura.config.settings import Settings


class MockServoController:
    def __init__(self, settings: Settings):
        self._settings = settings
        self.angles: dict[int, int] = {}

    def set_angle(self, channel: int, angle: int) -> list[str]:
        self._validate_channel(channel)
        self._validate_angle(angle)
        self.angles[channel] = angle
        return ["OK"]

    def stop(self, channel: int) -> list[str]:
        self._validate_channel(channel)
        self.angles[channel] = None
        return ["OK"]

    def _validate_channel(self, channel: int) -> None:
        if channel < 0 or channel >= self._settings.pca9685_channels:
            raise ValueError(
                f"channel must be between 0 and {self._settings.pca9685_channels - 1}"
            )

    def _validate_angle(self, angle: int) -> None:
        if angle < self._settings.servo_min_angle or angle > self._settings.servo_max_angle:
            raise ValueError(
                f"angle must be between {self._settings.servo_min_angle} "
                f"and {self._settings.servo_max_angle}"
            )
