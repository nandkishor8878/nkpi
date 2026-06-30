import unittest

from aura.infrastructure.sensors.ultrasonic_sensor_client import UltrasonicSensorClient


class FakeTransport:
    def __init__(self, response):
        self.response = response
        self.commands = []

    def send(self, command):
        self.commands.append(command)
        return self.response

    def close(self):
        return None


class UltrasonicSensorClientTests(unittest.TestCase):
    def test_parses_distance_response(self):
        transport = FakeTransport(["DISTANCE_CM:12.5"])
        sensor = UltrasonicSensorClient(transport)

        self.assertEqual(sensor.read_distance_cm(), 12.5)
        self.assertEqual(transport.commands, ["READ:DISTANCE"])

    def test_raises_error_response(self):
        sensor = UltrasonicSensorClient(FakeTransport(["ERROR:DISTANCE_TIMEOUT"]))

        with self.assertRaises(RuntimeError):
            sensor.read_distance_cm()


if __name__ == "__main__":
    unittest.main()

