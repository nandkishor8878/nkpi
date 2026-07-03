import importlib.util
import unittest


FLASK_AVAILABLE = importlib.util.find_spec("flask") is not None


@unittest.skipUnless(FLASK_AVAILABLE, "Flask is not installed")
class VisitorRouteTests(unittest.TestCase):
    def setUp(self):
        from aura.api.app_factory import create_app
        from aura.config.settings import Settings

        settings = Settings(
            camera_provider="mock",
            serial_transport="mock",
            servo_driver="mock",
            testing=True,
        )
        self.client = create_app(settings).test_client()

    def test_visitor_status_returns_state(self):
        response = self.client.get("/api/v1/visitor/status")

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["visitor"]["state"], "no_visitor")

    def test_visitor_check_validates_track_type(self):
        response = self.client.post("/api/v1/visitor/check", json={"track": "yes"})

        self.assertEqual(response.status_code, 400)

    def test_visitor_reset_returns_no_visitor(self):
        response = self.client.post("/api/v1/visitor/reset")

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["visitor"]["state"], "no_visitor")


if __name__ == "__main__":
    unittest.main()
