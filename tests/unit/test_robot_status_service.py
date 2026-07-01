import unittest

from aura.application.services.robot_state_store import RobotStateStore
from aura.application.services.robot_status_service import RobotStatusService


class FakeHealthService:
    def get_health(self):
        return {
            "components": {
                "api": {"status": "ok"},
                "esp32": {"status": "ok", "response": ["PONG"]},
            }
        }


class RobotStatusServiceTests(unittest.TestCase):
    def test_status_contains_operator_console_contract(self):
        state_store = RobotStateStore()
        state_store.set_led("on")
        state_store.set_servo_angle(0, 90)
        state_store.set_imu({"accel_x": 0.0, "accel_y": 0.0, "accel_z": 1.0})
        service = RobotStatusService(state_store, FakeHealthService())

        status = service.get_status()

        self.assertEqual(status["status"], "online")
        self.assertEqual(status["robot"]["name"], "Aura")
        self.assertEqual(status["components"]["esp32"], "ok")
        self.assertEqual(status["actuators"]["led"], "on")
        self.assertEqual(status["actuators"]["servos"]["0"]["angle"], 90)
        self.assertIsNone(status["sensors"]["distance_cm"])
        self.assertEqual(status["sensors"]["imu"]["accel_z"], 1.0)


if __name__ == "__main__":
    unittest.main()
