from typing import Protocol


class CameraPort(Protocol):
    def get_frame(self) -> bytes:
        """Return a JPEG-encoded frame."""

    def close(self) -> None:
        """Release camera resources."""

