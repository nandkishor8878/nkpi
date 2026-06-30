import importlib.util
import unittest


FLASK_AVAILABLE = importlib.util.find_spec("flask") is not None


@unittest.skipUnless(FLASK_AVAILABLE, "Flask is not installed")
class StatusRouteTests(unittest.TestCase):
    def setUp(self):
        from aura.api.app_factory import create_app
        from aura.config.settings import Settings

        settings = Settings(
            camera_provider="mock",
            serial_transport="mock",
            testing=True,
        )
        self.client = create_app(settings).test_client()

    def test_status_endpoint_returns_robot_state(self):
        response = self.client.get("/api/v1/status")

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["status"], "online")
        self.assertEqual(payload["robot"]["name"], "Aura")
        self.assertEqual(payload["components"]["api"], "ok")


if __name__ == "__main__":
    unittest.main()
