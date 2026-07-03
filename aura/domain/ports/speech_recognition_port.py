from typing import Protocol


class SpeechRecognitionPort(Protocol):
    def transcribe(self, audio_path: str) -> dict:
        """Transcribe an audio file and return transcript metadata."""
