class MockCamera:
    _MINIMAL_JPEG = b"\xff\xd8\xff\xd9"

    def get_frame(self) -> bytes:
        return self._MINIMAL_JPEG

    def close(self) -> None:
        return None
