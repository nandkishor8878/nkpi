from aura.application.services.robot_state_store import RobotStateStore
from aura.config.settings import Settings
from aura.infrastructure.sensors.imu_sensor_client import ImuSensorClient
from aura.infrastructure.sensors.ultrasonic_sensor_client import UltrasonicSensorClient


class SensorService:
    def __init__(
        self,
        ultrasonic_sensor: UltrasonicSensorClient,
        imu_sensor: ImuSensorClient,
        state_store: RobotStateStore,
        settings: Settings,
    ):
        self._ultrasonic_sensor = ultrasonic_sensor
        self._imu_sensor = imu_sensor
        self._state_store = state_store
        self._settings = settings

    def read_distance_cm(self) -> float:
        try:
            distance_cm = self._ultrasonic_sensor.read_distance_cm()
        except Exception as exc:
            self._state_store.record_error(f"Distance read failed: {exc}")
            raise
        self._state_store.set_distance_cm(distance_cm)
        return distance_cm

    def read_proximity(self) -> dict:
        distance_cm = self.read_distance_cm()
        detected = distance_cm <= self._settings.proximity_threshold_cm
        self._state_store.set_proximity(detected, distance_cm)
        return {
            "detected": detected,
            "distance_cm": distance_cm,
            "threshold_cm": self._settings.proximity_threshold_cm,
        }

    def read_imu(self) -> dict:
        try:
            imu = self._imu_sensor.read_imu()
        except Exception as exc:
            self._state_store.record_error(f"IMU read failed: {exc}")
            raise
        self._state_store.set_imu(imu)
        return imu

    def read_imu_status(self) -> dict:
        try:
            return self._imu_sensor.read_status()
        except Exception as exc:
            self._state_store.record_error(f"IMU status failed: {exc}")
            raise
