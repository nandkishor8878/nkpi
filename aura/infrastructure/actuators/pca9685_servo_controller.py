import logging

from aura.config.settings import Settings


logger = logging.getLogger(__name__)


class Pca9685ServoController:
    def __init__(self, settings: Settings):
        from adafruit_servokit import ServoKit

        self._settings = settings
        self._kit = ServoKit(
            channels=settings.pca9685_channels,
            address=settings.pca9685_i2c_address,
        )
        logger.info(
            "Initialized PCA9685 ServoKit at address 0x%02x with %s channels",
            settings.pca9685_i2c_address,
            settings.pca9685_channels,
        )

    def set_angle(self, channel: int, angle: int) -> list[str]:
        self._validate_channel(channel)
        self._validate_angle(angle)

        try:
            self._kit.servo[channel].angle = angle
        except Exception:
            logger.exception("Failed to set servo channel %s to angle %s", channel, angle)
            raise

        logger.info("Set servo channel %s to %s degrees", channel, angle)
        return ["OK"]

    def stop(self, channel: int) -> list[str]:
        self._validate_channel(channel)

        try:
            self._kit.servo[channel].angle = None
        except Exception:
            logger.exception("Failed to stop servo channel %s", channel)
            raise

        logger.info("Released servo channel %s PWM signal", channel)
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

