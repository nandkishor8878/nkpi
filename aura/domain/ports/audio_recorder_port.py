from typing import Protocol


class AudioRecorderPort(Protocol):
    def status(self) -> dict:
        """Return recorder availability and configuration."""

    def record(self, duration_seconds: int) -> dict:
        """Record audio and return metadata including the recorded path."""
