from aura.config.settings import Settings


class PiCamera:
    def __init__(self, settings: Settings):
        import cv2
        from picamera2 import Picamera2

        self._cv2 = cv2
        self._picam2 = Picamera2()
        config = self._picam2.create_video_configuration(
            main={"size": (settings.camera_width, settings.camera_height)}
        )
        self._picam2.configure(config)
        self._picam2.start()

    def get_frame(self) -> bytes:
        frame = self._picam2.capture_array()
        _, buffer = self._cv2.imencode(".jpg", frame)
        return buffer.tobytes()

    def close(self) -> None:
        self._picam2.stop()

