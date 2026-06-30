import importlib.util
import unittest


FLASK_AVAILABLE = importlib.util.find_spec("flask") is not None


@unittest.skipUnless(FLASK_AVAILABLE, "Flask is not installed")
class LedRouteTests(unittest.TestCase):
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

    def test_led_on_uses_post_and_sends_command(self):
        response = self.client.post("/api/v1/led/on")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["response"], ["OK"])

        container = self.app.extensions["aura"]
        self.assertEqual(container.transport.commands, ["LED_ON"])

    def test_led_off_uses_post_and_sends_command(self):
        response = self.client.post("/api/v1/led/off")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["response"], ["OK"])

        container = self.app.extensions["aura"]
        self.assertEqual(container.transport.commands, ["LED_OFF"])

    def test_led_get_is_not_allowed(self):
        response = self.client.get("/api/v1/led/on")

        self.assertEqual(response.status_code, 405)


if __name__ == "__main__":
    unittest.main()
