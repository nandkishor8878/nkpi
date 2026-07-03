from aura.config.settings import Settings


class MockSpeechRecognizer:
    def __init__(self, settings: Settings):
        self._settings = settings
        self.audio_paths: list[str] = []

    def transcribe(self, audio_path: str) -> dict:
        self.audio_paths.append(audio_path)
        return {
            "transcript": self._settings.speech_recognition_mock_transcript,
            "confidence": 1.0,
            "response": ["OK:MOCK_TRANSCRIPT"],
        }
