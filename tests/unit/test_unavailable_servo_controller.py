import unittest

from aura.infrastructure.actuators.unavailable_servo_controller import (
    UnavailableServoController,
)


class UnavailableServoControllerTests(unittest.TestCase):
    def test_set_angle_raises_clear_error(self):
        controller = UnavailableServoController("missing dependency")

        with self.assertRaisesRegex(RuntimeError, "missing dependency"):
            controller.set_angle(0, 90)


if __name__ == "__main__":
    unittest.main()
