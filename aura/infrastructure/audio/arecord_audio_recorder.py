import os
import shutil
import subprocess
import time

from aura.config.settings import Settings


class ArecordAudioRecorder:
    def __init__(self, settings: Settings):
        self._settings = settings

    def status(self) -> dict:
        return {
            "available": shutil.which(self._settings.audio_command) is not None,
            "provider": "arecord",
            "command": self._settings.audio_command,
            "device": self._settings.audio_device,
            "sample_rate": self._settings.audio_sample_rate,
            "channels": self._settings.audio_channels,
        }

    def record(self, duration_seconds: int) -> dict:
        command_path = shutil.which(self._settings.audio_command)
        if command_path is None:
            raise RuntimeError(
                f"Audio command not found: {self._settings.audio_command}. "
                "Install alsa-utils or set AURA_AUDIO_COMMAND."
            )

        os.makedirs(self._settings.audio_recordings_dir, exist_ok=True)
        audio_path = os.path.join(
            self._settings.audio_recordings_dir,
            f"visitor-{int(time.time() * 1000)}.wav",
        )
        command = [
            command_path,
            "-q",
            "-D",
            self._settings.audio_device,
            "-f",
            self._settings.audio_format,
            "-r",
            str(self._settings.audio_sample_rate),
            "-c",
            str(self._settings.audio_channels),
            "-d",
            str(duration_seconds),
            audio_path,
        ]
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=self._settings.audio_timeout_seconds,
        )
        if completed.returncode != 0:
            error = completed.stderr.strip() or completed.stdout.strip()
            raise RuntimeError(f"Audio recording failed: {error}")

        return {
            "path": audio_path,
            "duration_seconds": duration_seconds,
            "response": ["OK:RECORDED"],
        }
