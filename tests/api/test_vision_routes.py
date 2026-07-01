import importlib.util
import unittest


FLASK_AVAILABLE = importlib.util.find_spec("flask") is not None


@unittest.skipUnless(FLASK_AVAILABLE, "Flask is not installed")
class VisionRouteTests(unittest.TestCase):
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

    def test_vision_analyze_returns_result(self):
        response = self.client.get("/api/v1/vision/analyze")

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["vision"]["face_count"], 0)
        self.assertEqual(payload["vision"]["qr_count"], 0)


if __name__ == "__main__":
    unittest.main()
