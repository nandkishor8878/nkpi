from aura.config.settings import Settings


class MockSpeechSynthesizer:
    def __init__(self, settings: Settings):
        self._settings = settings
        self.spoken_texts: list[str] = []

    def speak(self, text: str) -> list[str]:
        self.spoken_texts.append(text)
        return ["OK:MOCK_SPEECH"]
