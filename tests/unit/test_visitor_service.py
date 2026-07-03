import time
import unittest

from aura.application.services.robot_state_store import RobotStateStore
from aura.application.services.speech_service import SpeechService
from aura.application.services.visitor_service import VisitorService
from aura.config.settings import Settings
from aura.infrastructure.audio.mock_speech_synthesizer import MockSpeechSynthesizer


class FakeFaceTrackingService:
    def __init__(self, results):
        self._results = list(results)

    def track_once(self):
        if len(self._results) == 1:
            return self._results[0]
        return self._results.pop(0)


def tracking_result(face_count):
    return {
        "status": "centered" if face_count else "no_face",
        "vision": {
            "status": "ok",
            "face_count": face_count,
            "qr_count": 0,
        },
    }


class VisitorServiceTests(unittest.TestCase):
    def test_first_detected_face_triggers_greeting(self):
        state_store = RobotStateStore()
        service = VisitorService(
            FakeFaceTrackingService([tracking_result(1)]),
            state_store,
            Settings(visitor_greeting_message="Welcome"),
        )

        visitor = service.check_visitor()

        self.assertEqual(visitor["state"], "greeting")
        self.assertEqual(visitor["greeting"], "Welcome")
        self.assertEqual(visitor["greeting_count"], 1)
        self.assertEqual(state_store.snapshot().visitor, "Greeting")

    def test_greeting_cooldown_prevents_repeat_greeting(self):
        state_store = RobotStateStore()
        service = VisitorService(
            FakeFaceTrackingService([tracking_result(1)]),
            state_store,
            Settings(visitor_greeting_cooldown_seconds=60),
        )

        service.check_visitor()
        visitor = service.check_visitor()

        self.assertEqual(visitor["state"], "waiting_for_response")
        self.assertIsNone(visitor["greeting"])
        self.assertEqual(visitor["greeting_count"], 1)

    def test_no_face_returns_no_visitor(self):
        state_store = RobotStateStore()
        service = VisitorService(
            FakeFaceTrackingService([tracking_result(0)]),
            state_store,
            Settings(),
        )

        visitor = service.check_visitor()

        self.assertEqual(visitor["state"], "no_visitor")
        self.assertEqual(visitor["display"], "No visitor")

    def test_status_transitions_greeting_to_waiting_after_display_window(self):
        state_store = RobotStateStore()
        service = VisitorService(
            FakeFaceTrackingService([tracking_result(1)]),
            state_store,
            Settings(visitor_greeting_display_seconds=0),
        )

        service.check_visitor()
        time.sleep(0.001)
        visitor = service.status()

        self.assertEqual(visitor["state"], "waiting_for_response")
        self.assertIsNone(visitor["greeting"])

    def test_greeting_speaks_when_speech_service_is_configured(self):
        settings = Settings(
            speech_provider="mock",
            visitor_greeting_message="Welcome",
        )
        state_store = RobotStateStore()
        synthesizer = MockSpeechSynthesizer(settings)
        speech_service = SpeechService(synthesizer, state_store, settings)
        service = VisitorService(
            FakeFaceTrackingService([tracking_result(1)]),
            state_store,
            settings,
            speech_service,
        )

        visitor = service.check_visitor()

        self.assertEqual(visitor["speech"]["status"], "spoken")
        self.assertEqual(synthesizer.spoken_texts, ["Welcome"])


if __name__ == "__main__":
    unittest.main()
