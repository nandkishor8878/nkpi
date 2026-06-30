import unittest

from aura.application.services.robot_state_store import RobotStateStore
from aura.application.services.sensor_service import SensorService
from aura.infrastructure.communication.mock_transport import MockTransport
from aura.infrastructure.sensors.ultrasonic_sensor_client import UltrasonicSensorClient


class SensorServiceTests(unittest.TestCase):
    def test_distance_read_updates_robot_state(self):
        state_store = RobotStateStore()
        sensor = UltrasonicSensorClient(MockTransport())
        service = SensorService(sensor, state_store)

        distance_cm = service.read_distance_cm()

        self.assertEqual(distance_cm, 42.7)
        self.assertEqual(state_store.snapshot().distance_cm, 42.7)


if __name__ == "__main__":
    unittest.main()

