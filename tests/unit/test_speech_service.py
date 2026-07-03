import unittest

from aura.application.services.robot_state_store import RobotStateStore
from aura.application.services.speech_service import SpeechService
from aura.config.settings import Settings
from aura.infrastructure.audio.mock_speech_synthesizer import MockSpeechSynthesizer


class SpeechServiceTests(unittest.TestCase):
    def test_speak_calls_synthesizer_and_updates_state(self):
        settings = Settings(speech_provider="mock")
        state_store = RobotStateStore()
        synthesizer = MockSpeechSynthesizer(settings)
        service = SpeechService(synthesizer, state_store, settings)

        result = service.speak("Hello")

        self.assertEqual(result["status"], "spoken")
        self.assertEqual(synthesizer.spoken_texts, ["Hello"])
        self.assertEqual(state_store.snapshot().speech["last_text"], "Hello")

    def test_disabled_speech_updates_state_without_speaking(self):
        settings = Settings(speech_provider="mock", speech_enabled=False)
        state_store = RobotStateStore()
        synthesizer = MockSpeechSynthesizer(settings)
        service = SpeechService(synthesizer, state_store, settings)

        result = service.speak("Hello")

        self.assertEqual(result["status"], "disabled")
        self.assertEqual(synthesizer.spoken_texts, [])

    def test_rejects_empty_text(self):
        settings = Settings()
        service = SpeechService(
            MockSpeechSynthesizer(settings),
            RobotStateStore(),
            settings,
        )

        with self.assertRaises(ValueError):
            service.speak(" ")

    def test_rejects_too_long_text(self):
        settings = Settings(speech_max_text_length=5)
        service = SpeechService(
            MockSpeechSynthesizer(settings),
            RobotStateStore(),
            settings,
        )

        with self.assertRaises(ValueError):
            service.speak("too long")


if __name__ == "__main__":
    unittest.main()
