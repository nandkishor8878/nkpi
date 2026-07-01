import importlib.util
import unittest


FLASK_AVAILABLE = importlib.util.find_spec("flask") is not None


@unittest.skipUnless(FLASK_AVAILABLE, "Flask is not installed")
class ServoRouteTests(unittest.TestCase):
    def setUp(self):
        from aura.api.app_factory import create_app
        from aura.config.settings import Settings

        settings = Settings(
            camera_provider="mock",
            serial_transport="mock",
            testing=True,
        )
        self.app = create_app(settings)
        self.client = self.app.test_client()

    def test_set_servo_angle_sends_command(self):
        response = self.client.post("/api/v1/servos/0/angle", json={"angle": 90})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["response"], ["OK"])

        container = self.app.extensions["aura"]
        self.assertEqual(container.state_store.snapshot().servos[0], 90)

    def test_set_servo_endpoint_accepts_channel_and_angle(self):
        response = self.client.post(
            "/api/v1/servo",
            json={"channel": 0, "angle": 90, "smooth": False},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["channel"], 0)
        self.assertEqual(payload["angle"], 90)

        container = self.app.extensions["aura"]
        self.assertEqual(container.state_store.snapshot().servos[0], 90)

    def test_set_servo_angle_rejects_missing_angle(self):
        response = self.client.post("/api/v1/servos/0/angle", json={})

        self.assertEqual(response.status_code, 400)

    def test_set_servo_angle_rejects_out_of_range_angle(self):
        response = self.client.post("/api/v1/servos/0/angle", json={"angle": 181})

        self.assertEqual(response.status_code, 400)

    def test_set_servo_angle_rejects_boolean_angle(self):
        response = self.client.post("/api/v1/servos/0/angle", json={"angle": True})

        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
