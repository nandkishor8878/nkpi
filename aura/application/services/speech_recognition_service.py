import time

from aura.application.services.audio_service import AudioService
from aura.application.services.robot_state_store import RobotStateStore
from aura.config.settings import Settings
from aura.domain.ports.speech_recognition_port import SpeechRecognitionPort


class SpeechRecognitionService:
    def __init__(
        self,
        audio_service: AudioService,
        speech_recognizer: SpeechRecognitionPort,
        state_store: RobotStateStore,
        settings: Settings,
    ):
        self._audio_service = audio_service
        self._speech_recognizer = speech_recognizer
        self._state_store = state_store
        self._settings = settings

    def status(self) -> dict:
        state = self._state_store.snapshot()
        return state.speech_recognition or {
            "status": "idle",
            "enabled": self._settings.speech_recognition_enabled,
            "provider": self._settings.speech_recognition_provider,
            "transcript": None,
            "audio": None,
            "updated_at": None,
        }

    def listen(self, duration_seconds: int | None = None) -> dict:
        audio = self._audio_service.record(duration_seconds)

        if not self._settings.speech_recognition_enabled:
            recognition = self._result(
                "disabled",
                None,
                audio,
                ["SPEECH_RECOGNITION_DISABLED"],
            )
            self._state_store.set_speech_recognition(recognition)
            return recognition

        if audio.get("status") != "recorded" or not audio.get("path"):
            recognition = self._result("no_audio", None, audio, ["NO_AUDIO_RECORDED"])
            self._state_store.set_speech_recognition(recognition)
            return recognition

        transcription = self._speech_recognizer.transcribe(audio["path"])
        transcript = transcription.get("transcript")
        recognition = self._result(
            "transcribed",
            transcript,
            audio,
            transcription.get("response", []),
        )
        recognition["metadata"] = transcription
        self._state_store.set_speech_recognition(recognition)
        self._state_store.set_visitor_transcript(transcript or "", recognition)
        return recognition

    def _result(
        self,
        status: str,
        transcript: str | None,
        audio: dict,
        response: list[str],
    ) -> dict:
        return {
            "status": status,
            "enabled": self._settings.speech_recognition_enabled,
            "provider": self._settings.speech_recognition_provider,
            "transcript": transcript,
            "audio": audio,
            "response": response,
            "updated_at": time.time(),
        }
