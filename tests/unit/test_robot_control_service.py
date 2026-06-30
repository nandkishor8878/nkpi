import unittest

from aura.application.services.robot_control_service import RobotControlService
from aura.application.services.robot_state_store import RobotStateStore
from aura.config.settings import Settings
from aura.infrastructure.actuators.servo_controller import ServoController
from aura.infrastructure.communication.mock_transport import MockTransport


class RobotControlServiceTests(unittest.TestCase):
    def test_led_commands_are_sent_through_transport(self):
        transport = MockTransport()
        service = RobotControlService(transport)

        self.assertEqual(service.turn_led_on(), ["OK"])
        self.assertEqual(service.turn_led_off(), ["OK"])
        self.assertEqual(transport.commands, ["LED_ON", "LED_OFF"])

    def test_servo_angle_is_sent_through_servo_controller(self):
        transport = MockTransport()
        settings = Settings()
        servo_controller = ServoController(transport, settings)
        service = RobotControlService(transport, servo_controller)

        self.assertEqual(service.set_servo_angle(0, 90), ["OK"])
        self.assertEqual(transport.commands, ["SERVO:0:90"])

    def test_servo_angle_rejects_unsafe_angle(self):
        transport = MockTransport()
        settings = Settings()
        servo_controller = ServoController(transport, settings)
        service = RobotControlService(transport, servo_controller)

        with self.assertRaises(ValueError):
            service.set_servo_angle(0, 181)

        self.assertEqual(transport.commands, [])

    def test_successful_commands_update_robot_state(self):
        transport = MockTransport()
        settings = Settings()
        state_store = RobotStateStore()
        servo_controller = ServoController(transport, settings)
        service = RobotControlService(transport, servo_controller, state_store)

        service.turn_led_on()
        service.set_servo_angle(0, 90)

        state = state_store.snapshot()
        self.assertEqual(state.led, "on")
        self.assertEqual(state.servos[0], 90)


if __name__ == "__main__":
    unittest.main()
