import unittest

from aura.application.services.robot_state_store import RobotStateStore
from aura.application.services.servo_service import ServoService
from aura.config.settings import Settings
from aura.infrastructure.actuators.mock_servo_controller import MockServoController


class ServoServiceTests(unittest.TestCase):
    def test_set_angle_updates_controller_and_state(self):
        settings = Settings(servo_smooth_step_delay_seconds=0)
        state_store = RobotStateStore()
        controller = MockServoController(settings)
        service = ServoService(controller, state_store, settings)

        result = service.set_angle(0, 90, smooth=False)

        self.assertEqual(result["channel"], 0)
        self.assertEqual(result["angle"], 90)
        self.assertEqual(controller.angles[0], 90)
        self.assertEqual(state_store.snapshot().servos[0], 90)

    def test_uses_default_channel_when_channel_is_missing(self):
        settings = Settings(servo_default_channel=2, servo_smooth_step_delay_seconds=0)
        state_store = RobotStateStore()
        controller = MockServoController(settings)
        service = ServoService(controller, state_store, settings)

        service.set_angle(None, 90, smooth=False)

        self.assertEqual(controller.angles[2], 90)

    def test_rejects_out_of_range_angle(self):
        settings = Settings()
        service = ServoService(MockServoController(settings), RobotStateStore(), settings)

        with self.assertRaises(ValueError):
            service.set_angle(0, 181)

    def test_stop_releases_servo_and_updates_state(self):
        settings = Settings()
        state_store = RobotStateStore()
        controller = MockServoController(settings)
        service = ServoService(controller, state_store, settings)

        result = service.stop(0)

        self.assertEqual(result["channel"], 0)
        self.assertEqual(result["state"], "stopped")
        self.assertIsNone(controller.angles[0])
        self.assertIsNone(state_store.snapshot().servos[0])

    def test_get_calibration_returns_safe_values(self):
        settings = Settings(
            servo_min_angle=30,
            servo_max_angle=150,
            servo_left_angle=60,
            servo_center_angle=90,
            servo_right_angle=120,
        )
        service = ServoService(MockServoController(settings), RobotStateStore(), settings)

        calibration = service.get_calibration()

        self.assertEqual(calibration["min_angle"], 30)
        self.assertEqual(calibration["max_angle"], 150)
        self.assertEqual(calibration["left_angle"], 60)
        self.assertEqual(calibration["center_angle"], 90)
        self.assertEqual(calibration["right_angle"], 120)

    def test_auto_release_releases_pwm_after_final_move(self):
        settings = Settings(
            servo_auto_release_after_move=True,
            servo_release_delay_seconds=0,
            servo_smooth_step_delay_seconds=0,
        )
        state_store = RobotStateStore()
        controller = MockServoController(settings)
        service = ServoService(controller, state_store, settings)

        result = service.set_angle(0, 90, smooth=False)

        self.assertIn("PWM_RELEASED_AFTER_MOVE", result["response"])
        self.assertIsNone(controller.angles[0])
        self.assertEqual(state_store.snapshot().servos[0], 90)


if __name__ == "__main__":
    unittest.main()
