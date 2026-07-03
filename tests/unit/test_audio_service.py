import unittest

from aura.application.services.audio_service import AudioService
from aura.application.services.robot_state_store import RobotStateStore
from aura.config.settings import Settings
from aura.infrastructure.audio.mock_audio_recorder import MockAudioRecorder


class AudioServiceTests(unittest.TestCase):
    def test_record_updates_state(self):
        settings = Settings(audio_recorder_provider="mock")
        state_store = RobotStateStore()
        recorder = MockAudioRecorder(settings)
        service = AudioService(recorder, state_store, settings)

        result = service.record(3)

        self.assertEqual(result["status"], "recorded")
        self.assertEqual(result["duration_seconds"], 3)
        self.assertEqual(result["path"], "mock://last-recording.wav")
        self.assertEqual(state_store.snapshot().audio["status"], "recorded")

    def test_disabled_audio_does_not_record(self):
        settings = Settings(audio_recorder_provider="mock", audio_enabled=False)
        state_store = RobotStateStore()
        recorder = MockAudioRecorder(settings)
        service = AudioService(recorder, state_store, settings)

        result = service.record(3)

        self.assertEqual(result["status"], "disabled")
        self.assertEqual(recorder.recordings, [])

    def test_rejects_invalid_duration(self):
        settings = Settings(audio_max_duration_seconds=5)
        service = AudioService(
            MockAudioRecorder(settings),
            RobotStateStore(),
            settings,
        )

        with self.assertRaises(ValueError):
            service.record(6)


if __name__ == "__main__":
    unittest.main()
