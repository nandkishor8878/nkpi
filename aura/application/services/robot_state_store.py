from aura.domain.models.robot_state import RobotState


class RobotStateStore:
    def __init__(self):
        self._state = RobotState()

    def set_led(self, state: str) -> None:
        self._state.led = state

    def set_servo_angle(self, servo_id: int, angle: int) -> None:
        self._state.servos[servo_id] = angle

    def set_distance_cm(self, distance_cm: float) -> None:
        self._state.distance_cm = distance_cm

    def set_imu(self, imu: dict) -> None:
        self._state.imu = imu

    def snapshot(self) -> RobotState:
        return self._state
