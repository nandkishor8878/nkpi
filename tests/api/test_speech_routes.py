import importlib.util
import unittest


FLASK_AVAILABLE = importlib.util.find_spec("flask") is not None


@unittest.skipUnless(FLASK_AVAILABLE, "Flask is not installed")
class SpeechRouteTests(unittest.TestCase):
    def setUp(self):
        from aura.api.app_factory import create_app
        from aura.config.settings import Settings

        settings = Settings(
            camera_provider="mock",
            serial_transport="mock",
            servo_driver="mock",
            speech_provider="mock",
            testing=True,
        )
        self.client = create_app(settings).test_client()

    def test_speech_status_returns_idle_state(self):
        response = self.client.get("/api/v1/speech/status")

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["speech"]["status"], "idle")

    def test_speech_say_speaks_text(self):
        response = self.client.post("/api/v1/speech/say", json={"text": "Hello"})

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["speech"]["status"], "spoken")
        self.assertEqual(payload["speech"]["last_text"], "Hello")

    def test_speech_say_rejects_empty_text(self):
        response = self.client.post("/api/v1/speech/say", json={"text": " "})

        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
