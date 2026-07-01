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
        service = SensorService(ultrasonic_sensor, imu_sensor, state_store)

        distance_cm = service.read_distance_cm()

        self.assertEqual(distance_cm, 42.7)
        self.assertEqual(state_store.snapshot().distance_cm, 42.7)

    def test_imu_read_updates_robot_state(self):
        state_store = RobotStateStore()
        transport = MockTransport()
        ultrasonic_sensor = UltrasonicSensorClient(transport)
        imu_sensor = ImuSensorClient(transport)
        service = SensorService(ultrasonic_sensor, imu_sensor, state_store)

        imu = service.read_imu()

        self.assertEqual(imu["accel_z"], 1.0)
        self.assertEqual(state_store.snapshot().imu["gyro_z"], 0.3)


if __name__ == "__main__":
    unittest.main()
