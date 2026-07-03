from typing import Protocol


class SpeechPort(Protocol):
    def speak(self, text: str) -> list[str]:
        """Speak text through the configured audio output."""
