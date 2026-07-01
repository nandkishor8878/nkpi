import logging
import time

from aura.application.services.robot_state_store import RobotStateStore
from aura.config.settings import Settings
from aura.domain.ports.servo_port import ServoPort


logger = logging.getLogger(__name__)


class ServoService:
    def __init__(
        self,
        servo_controller: ServoPort,
        state_store: RobotStateStore,
        settings: Settings,
    ):
        self._servo_controller = servo_controller
        self._state_store = state_store
        self._settings = settings

    def set_angle(
        self,
        channel: int | None,
        angle: int,
        smooth: bool = True,
    ) -> dict:
        resolved_channel = self._settings.servo_default_channel if channel is None else channel
        self._validate_angle(angle)

        try:
            response = self._move(resolved_channel, angle, smooth)
        except Exception:
            self._state_store.record_error(
                f"Servo {resolved_channel} angle {angle} failed"
            )
            logger.exception(
                "Servo move failed for channel %s angle %s", resolved_channel, angle
            )
            raise

        self._state_store.set_servo_angle(resolved_channel, angle)
        return {
            "channel": resolved_channel,
            "angle": angle,
            "response": response,
        }

    def move_left(self, channel: int | None = None) -> dict:
        return self.set_angle(channel, self._settings.servo_left_angle)

    def move_center(self, channel: int | None = None) -> dict:
        return self.set_angle(channel, self._settings.servo_center_angle)

    def move_right(self, channel: int | None = None) -> dict:
        return self.set_angle(channel, self._settings.servo_right_angle)

    def get_calibration(self) -> dict:
        return {
            "default_channel": self._settings.servo_default_channel,
            "min_angle": self._settings.servo_min_angle,
            "max_angle": self._settings.servo_max_angle,
            "left_angle": self._settings.servo_left_angle,
            "center_angle": self._settings.servo_center_angle,
            "right_angle": self._settings.servo_right_angle,
            "smooth_step_degrees": self._settings.servo_smooth_step_degrees,
            "smooth_step_delay_seconds": self._settings.servo_smooth_step_delay_seconds,
            "auto_release_after_move": self._settings.servo_auto_release_after_move,
            "release_delay_seconds": self._settings.servo_release_delay_seconds,
            "driver": self._settings.servo_driver,
        }

    def stop(self, channel: int | None = None) -> dict:
        resolved_channel = self._settings.servo_default_channel if channel is None else channel

        try:
            response = self._servo_controller.stop(resolved_channel)
        except Exception:
            self._state_store.record_error(f"Servo {resolved_channel} stop failed")
            logger.exception("Servo stop failed for channel %s", resolved_channel)
            raise

        self._state_store.stop_servo(resolved_channel)
        return {
            "channel": resolved_channel,
            "state": "stopped",
            "response": response,
        }

    def _move(self, channel: int, target_angle: int, smooth: bool) -> list[str]:
        current_angle = self._state_store.snapshot().servos.get(channel)
        if not smooth or current_angle is None:
            response = self._servo_controller.set_angle(channel, target_angle)
            return self._release_after_move_if_enabled(channel, response)

        step_size = max(1, self._settings.servo_smooth_step_degrees)
        if target_angle < current_angle:
            step_size = -step_size

        last_response = ["OK"]
        for angle in range(current_angle + step_size, target_angle, step_size):
            last_response = self._servo_controller.set_angle(channel, angle)
            time.sleep(self._settings.servo_smooth_step_delay_seconds)

        last_response = self._servo_controller.set_angle(channel, target_angle)
        return self._release_after_move_if_enabled(channel, last_response)

    def _release_after_move_if_enabled(self, channel: int, response: list[str]) -> list[str]:
        if self._settings.servo_auto_release_after_move:
            time.sleep(self._settings.servo_release_delay_seconds)
            try:
                return [
                    *response,
                    *self._servo_controller.stop(channel),
                    "PWM_RELEASED_AFTER_MOVE",
                ]
            except RuntimeError:
                logger.warning(
                    "Servo auto-release is not supported by the configured driver"
                )
        return response

    def _validate_angle(self, angle: int) -> None:
        if angle < self._settings.servo_min_angle or angle > self._settings.servo_max_angle:
            raise ValueError(
                f"angle must be between {self._settings.servo_min_angle} "
                f"and {self._settings.servo_max_angle}"
            )
