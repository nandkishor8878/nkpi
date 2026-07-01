import unittest

from aura.application.services.robot_state_store import RobotStateStore
from aura.application.services.sensor_service import SensorService
from aura.infrastructure.communication.mock_transport import MockTransport
from aura.infrastructure.sensors.imu_sensor_client import ImuSensorClient
from aura.infrastructure.sensors.ultrasonic_sensor_client import UltrasonicSensorClient


class SensorServiceTests(unittest.TestCase):
    def test_distance_read_updates_robot_state(self):
        state_store = RobotStateStore()
        transport = MockTransport()
        ultrasonic_sensor = UltrasonicSensorClient(transport)
        imu_sensor = ImuSensorClient(transport)
        from aura.config.settings import Settings

        service = SensorService(ultrasonic_sensor, imu_sensor, state_store, Settings())

        distance_cm = service.read_distance_cm()

        self.assertEqual(distance_cm, 42.7)
        self.assertEqual(state_store.snapshot().distance_cm, 42.7)

    def test_imu_read_updates_robot_state(self):
        state_store = RobotStateStore()
        transport = MockTransport()
        ultrasonic_sensor = UltrasonicSensorClient(transport)
        imu_sensor = ImuSensorClient(transport)
        from aura.config.settings import Settings

        service = SensorService(ultrasonic_sensor, imu_sensor, state_store, Settings())

        imu = service.read_imu()

        self.assertEqual(imu["accel_z"], 1.0)
        self.assertEqual(state_store.snapshot().imu["gyro_z"], 0.3)

    def test_proximity_read_updates_robot_state(self):
        from aura.config.settings import Settings

        state_store = RobotStateStore()
        transport = MockTransport()
        ultrasonic_sensor = UltrasonicSensorClient(transport)
        imu_sensor = ImuSensorClient(transport)
        settings = Settings(proximity_threshold_cm=50)
        service = SensorService(ultrasonic_sensor, imu_sensor, state_store, settings)

        proximity = service.read_proximity()

        self.assertTrue(proximity["detected"])
        self.assertEqual(proximity["distance_cm"], 42.7)
        self.assertEqual(proximity["threshold_cm"], 50)
        self.assertTrue(state_store.snapshot().proximity_detected)


if __name__ == "__main__":
    unittest.main()
