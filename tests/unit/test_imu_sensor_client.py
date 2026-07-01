import unittest

from aura.infrastructure.sensors.imu_sensor_client import ImuSensorClient


class FakeTransport:
    def __init__(self, response):
        self.response = response
        self.commands = []

    def send(self, command):
        self.commands.append(command)
        return self.response

    def close(self):
        return None


class ImuSensorClientTests(unittest.TestCase):
    def test_parses_imu_response(self):
        transport = FakeTransport(
            ["IMU:AX:0.01:AY:0.02:AZ:1.00:GX:0.10:GY:0.20:GZ:0.30"]
        )
        sensor = ImuSensorClient(transport)

        imu = sensor.read_imu()

        self.assertEqual(transport.commands, ["READ:IMU"])
        self.assertEqual(imu["accel_x"], 0.01)
        self.assertEqual(imu["accel_z"], 1.0)
        self.assertEqual(imu["gyro_z"], 0.3)

    def test_raises_error_response(self):
        sensor = ImuSensorClient(FakeTransport(["ERROR:IMU_READ_FAILED"]))

        with self.assertRaises(RuntimeError):
            sensor.read_imu()


if __name__ == "__main__":
    unittest.main()
