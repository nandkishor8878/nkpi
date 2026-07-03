import importlib.util
import unittest


FLASK_AVAILABLE = importlib.util.find_spec("flask") is not None


@unittest.skipUnless(FLASK_AVAILABLE, "Flask is not installed")
class AudioRouteTests(unittest.TestCase):
    def setUp(self):
        from aura.api.app_factory import create_app
        from aura.config.settings import Settings

        settings = Settings(
            camera_provider="mock",
            serial_transport="mock",
            servo_driver="mock",
            audio_recorder_provider="mock",
            speech_provider="mock",
            speech_recognition_provider="mock",
            testing=True,
        )
        self.client = create_app(settings).test_client()

    def test_audio_status_returns_recorder_status(self):
        response = self.client.get("/api/v1/audio/status")

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["audio"]["recorder"]["provider"], "mock")

    def test_audio_record_returns_recording(self):
        response = self.client.post("/api/v1/audio/record", json={"duration_seconds": 3})

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["audio"]["status"], "recorded")

    def test_audio_record_validates_duration(self):
        response = self.client.post("/api/v1/audio/record", json={"duration_seconds": 100})

        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
