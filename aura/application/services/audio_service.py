import time

from aura.application.services.robot_state_store import RobotStateStore
from aura.config.settings import Settings
from aura.domain.ports.audio_recorder_port import AudioRecorderPort


class AudioService:
    def __init__(
        self,
        audio_recorder: AudioRecorderPort,
        state_store: RobotStateStore,
        settings: Settings,
    ):
        self._audio_recorder = audio_recorder
        self._state_store = state_store
        self._settings = settings

    def status(self) -> dict:
        state = self._state_store.snapshot()
        recorder_status = self._audio_recorder.status()
        return {
            "status": state.audio.get("status") if state.audio else "idle",
            "enabled": self._settings.audio_enabled,
            "provider": self._settings.audio_recorder_provider,
            "recorder": recorder_status,
            "last_recording": state.audio,
            "updated_at": time.time(),
        }

    def record(self, duration_seconds: int | None = None) -> dict:
        duration = self._resolve_duration(duration_seconds)
        if not self._settings.audio_enabled:
            result = self._result("disabled", duration, None, ["AUDIO_DISABLED"])
            self._state_store.set_audio(result)
            return result

        metadata = self._audio_recorder.record(duration)
        result = self._result(
            "recorded",
            duration,
            metadata.get("path"),
            metadata.get("response", []),
        )
        result["metadata"] = metadata
        self._state_store.set_audio(result)
        return result

    def _resolve_duration(self, duration_seconds: int | None) -> int:
        duration = duration_seconds or self._settings.audio_default_duration_seconds
        if type(duration) is not int:
            raise ValueError("duration_seconds must be an integer")
        if duration < 1:
            raise ValueError("duration_seconds must be at least 1")
        if duration > self._settings.audio_max_duration_seconds:
            raise ValueError(
                f"duration_seconds must be {self._settings.audio_max_duration_seconds} or less"
            )
        return duration

    def _result(
        self,
        status: str,
        duration_seconds: int,
        path: str | None,
        response: list[str],
    ) -> dict:
        return {
            "status": status,
            "enabled": self._settings.audio_enabled,
            "provider": self._settings.audio_recorder_provider,
            "duration_seconds": duration_seconds,
            "path": path,
            "response": response,
            "updated_at": time.time(),
        }
