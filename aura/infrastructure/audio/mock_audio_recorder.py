from aura.config.settings import Settings


class MockAudioRecorder:
    def __init__(self, settings: Settings):
        self._settings = settings
        self.recordings: list[dict] = []

    def status(self) -> dict:
        return {
            "available": True,
            "provider": "mock",
            "device": self._settings.audio_device,
        }

    def record(self, duration_seconds: int) -> dict:
        recording = {
            "path": "mock://last-recording.wav",
            "duration_seconds": duration_seconds,
            "response": ["OK:MOCK_AUDIO"],
        }
        self.recordings.append(recording)
        return recording
