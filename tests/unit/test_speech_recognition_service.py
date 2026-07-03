import unittest

from aura.application.services.audio_service import AudioService
from aura.application.services.robot_state_store import RobotStateStore
from aura.application.services.speech_recognition_service import SpeechRecognitionService
from aura.config.settings import Settings
from aura.infrastructure.audio.mock_audio_recorder import MockAudioRecorder
from aura.infrastructure.audio.mock_speech_recognizer import MockSpeechRecognizer


class SpeechRecognitionServiceTests(unittest.TestCase):
    def test_listen_records_transcribes_and_updates_visitor_state(self):
        settings = Settings(
            audio_recorder_provider="mock",
            speech_recognition_provider="mock",
            speech_recognition_mock_transcript="I am here for a meeting.",
        )
        state_store = RobotStateStore()
        audio_service = AudioService(MockAudioRecorder(settings), state_store, settings)
        recognizer = MockSpeechRecognizer(settings)
        service = SpeechRecognitionService(
            audio_service,
            recognizer,
            state_store,
            settings,
        )

        result = service.listen(3)

        self.assertEqual(result["status"], "transcribed")
        self.assertEqual(result["transcript"], "I am here for a meeting.")
        self.assertEqual(
            state_store.snapshot().visitor_state["latest_transcript"],
            "I am here for a meeting.",
        )

    def test_disabled_recognition_records_audio_without_transcribing(self):
        settings = Settings(
            audio_recorder_provider="mock",
            speech_recognition_enabled=False,
        )
        state_store = RobotStateStore()
        audio_service = AudioService(MockAudioRecorder(settings), state_store, settings)
        service = SpeechRecognitionService(
            audio_service,
            MockSpeechRecognizer(settings),
            state_store,
            settings,
        )

        result = service.listen(3)

        self.assertEqual(result["status"], "disabled")
        self.assertIsNone(result["transcript"])


if __name__ == "__main__":
    unittest.main()
