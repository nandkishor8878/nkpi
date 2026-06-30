import importlib.util
import unittest


FLASK_AVAILABLE = importlib.util.find_spec("flask") is not None


@unittest.skipUnless(FLASK_AVAILABLE, "Flask is not installed")
class SensorRouteTests(unittest.TestCase):
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

    def test_distance_endpoint_returns_reading_and_updates_status(self):
        response = self.client.get("/api/v1/sensors/distance")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["distance_cm"], 42.7)

        status = self.client.get("/api/v1/status").get_json()
        self.assertEqual(status["sensors"]["distance_cm"], 42.7)


if __name__ == "__main__":
    unittest.main()

