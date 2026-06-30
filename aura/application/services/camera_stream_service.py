from aura.domain.ports.camera_port import CameraPort


class CameraStreamService:
    def __init__(self, camera: CameraPort):
        self._camera = camera

    def get_jpeg_frame(self) -> bytes:
        return self._camera.get_frame()

    def mjpeg_frames(self):
        while True:
            frame = self.get_jpeg_frame()
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + frame
                + b"\r\n"
            )

