from aura.application.services.robot_state_store import RobotStateStore
from aura.infrastructure.sensors.ultrasonic_sensor_client import UltrasonicSensorClient


class SensorService:
    def __init__(
        self,
        ultrasonic_sensor: UltrasonicSensorClient,
        state_store: RobotStateStore,
    ):
        self._ultrasonic_sensor = ultrasonic_sensor
        self._state_store = state_store

    def read_distance_cm(self) -> float:
        distance_cm = self._ultrasonic_sensor.read_distance_cm()
        self._state_store.set_distance_cm(distance_cm)
        return distance_cm
