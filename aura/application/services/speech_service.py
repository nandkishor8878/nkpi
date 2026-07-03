import logging
import time

from aura.application.services.robot_state_store import RobotStateStore
from aura.config.settings import Settings
from aura.domain.ports.speech_port import SpeechPort


logger = logging.getLogger(__name__)


class SpeechService:
    def __init__(
        self,
        speech_synthesizer: SpeechPort,
        state_store: RobotStateStore,
        settings: Settings,
    ):
        self._speech_synthesizer = speech_synthesizer
        self._state_store = state_store
        self._settings = settings

    def speak(self, text: str | None) -> dict:
        message = (text or "").strip()
        self._validate_text(message)

        if not self._settings.speech_enabled:
            result = self._result("disabled", message, ["SPEECH_DISABLED"])
            self._state_store.set_speech(result)
            return result

        try:
            response = self._speech_synthesizer.speak(message)
        except Exception:
            self._state_store.record_error("Speech output failed")
            logger.exception("Speech output failed")
            raise

        result = self._result("spoken", message, response)
        self._state_store.set_speech(result)
        return result

    def status(self) -> dict:
        state = self._state_store.snapshot()
        return state.speech or {
            "status": "idle",
            "enabled": self._settings.speech_enabled,
            "provider": self._settings.speech_provider,
            "last_text": None,
            "response": [],
            "updated_at": None,
        }

    def _validate_text(self, text: str) -> None:
        if not text:
            raise ValueError("text is required")
        if len(text) > self._settings.speech_max_text_length:
            raise ValueError(
                f"text must be {self._settings.speech_max_text_length} characters or fewer"
            )

    def _result(self, status: str, text: str, response: list[str]) -> dict:
        return {
            "status": status,
            "enabled": self._settings.speech_enabled,
            "provider": self._settings.speech_provider,
            "last_text": text,
            "response": response,
            "updated_at": time.time(),
        }
