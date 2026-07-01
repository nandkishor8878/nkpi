from aura.application.services.camera_stream_service import CameraStreamService
from aura.application.services.robot_state_store import RobotStateStore


class VisionService:
    def __init__(
        self,
        camera_stream_service: CameraStreamService,
        state_store: RobotStateStore,
    ):
        self._camera_stream_service = camera_stream_service
        self._state_store = state_store

    def analyze_frame(self) -> dict:
        frame_bytes = self._camera_stream_service.get_jpeg_frame()
        result = self._analyze_jpeg(frame_bytes)
        self._state_store.set_vision(result)
        return result

    def _analyze_jpeg(self, frame_bytes: bytes) -> dict:
        import cv2
        import numpy as np

        encoded = np.frombuffer(frame_bytes, dtype=np.uint8)
        frame = cv2.imdecode(encoded, cv2.IMREAD_COLOR)
        if frame is None:
            return self._empty_result("frame_decode_failed")

        faces = self._detect_faces(cv2, frame)
        qr_codes = self._detect_qr_codes(cv2, frame)

        return {
            "status": "ok",
            "face_count": len(faces),
            "faces": faces,
            "qr_count": len(qr_codes),
            "qr_codes": qr_codes,
        }

    def _detect_faces(self, cv2, frame) -> list[dict]:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(cascade_path)
        if detector.empty():
            return []

        faces = detector.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(40, 40),
        )
        return [
            {
                "x": int(x),
                "y": int(y),
                "width": int(width),
                "height": int(height),
            }
            for x, y, width, height in faces
        ]

    def _detect_qr_codes(self, cv2, frame) -> list[dict]:
        detector = cv2.QRCodeDetector()
        ok, decoded_info, points, _ = detector.detectAndDecodeMulti(frame)
        if not ok or points is None:
            return []

        qr_codes = []
        for index, text in enumerate(decoded_info):
            if not text:
                continue
            point_set = points[index]
            qr_codes.append(
                {
                    "text": text,
                    "points": [
                        {"x": int(point[0]), "y": int(point[1])}
                        for point in point_set
                    ],
                }
            )
        return qr_codes

    def _empty_result(self, status: str) -> dict:
        return {
            "status": status,
            "face_count": 0,
            "faces": [],
            "qr_count": 0,
            "qr_codes": [],
        }
