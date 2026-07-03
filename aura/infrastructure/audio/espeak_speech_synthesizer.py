import shutil
import subprocess

from aura.config.settings import Settings


class EspeakSpeechSynthesizer:
    def __init__(self, settings: Settings):
        self._settings = settings

    def speak(self, text: str) -> list[str]:
        command_path = shutil.which(self._settings.speech_command)
        if command_path is None and self._settings.speech_command == "espeak-ng":
            command_path = shutil.which("espeak")
        if command_path is None:
            raise RuntimeError(
                f"Speech command not found: {self._settings.speech_command}. "
                "Install espeak-ng or set AURA_SPEECH_COMMAND."
            )

        command = [
            command_path,
            "-s",
            str(self._settings.speech_speed_wpm),
            "-p",
            str(self._settings.speech_pitch),
            "-a",
            str(self._settings.speech_volume),
        ]
        if self._settings.speech_voice:
            command.extend(["-v", self._settings.speech_voice])
        command.append(text)

        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=self._settings.speech_timeout_seconds,
        )
        if completed.returncode != 0:
            error = completed.stderr.strip() or completed.stdout.strip()
            raise RuntimeError(f"Speech command failed: {error}")

        return ["OK:SPOKEN"]
