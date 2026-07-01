import importlib.util
import unittest


FLASK_AVAILABLE = importlib.util.find_spec("flask") is not None


@unittest.skipUnless(FLASK_AVAILABLE, "Flask is not installed")
class FaceTrackingRouteTests(unittest.TestCase):
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

    def test_face_tracking_status_returns_idle_state(self):
        response = self.client.get("/api/v1/face-tracking/status")

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["face_tracking"]["status"], "idle")

    def test_face_tracking_track_returns_result(self):
        response = self.client.post("/api/v1/face-tracking/track")

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIn(payload["face_tracking"]["status"], {"no_face", "centered", "moved"})


if __name__ == "__main__":
    unittest.main()
